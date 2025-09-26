#!/usr/bin/env python3
"""
Exploding Topics Data Pipeline
Fetches trending topics from Google Trends and generates latest.json
"""

import json
import os
import sys
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import time
import random

# Third-party imports
try:
    from pytrends.request import TrendReq
    from pytrends.exceptions import ResponseError, TooManyRequestsError
    from rapidfuzz import fuzz, process
    import numpy as np
    import pandas as pd
except ImportError as e:
    print(f"Missing required package: {e}")
    print("Please install requirements: pip install -r requirements.txt")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data_pipeline.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class TrendsDataPipeline:
    def __init__(self, seeds_file: str = "data/seeds.json"):
        """Initialize the data pipeline with seeds configuration."""
        self.seeds_file = seeds_file
        self.output_dir = "public/data"
        self.archive_dir = os.path.join(self.output_dir, "archive")
        self.latest_file = os.path.join(self.output_dir, "latest.json")
        
        # Ensure directories exist
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.archive_dir, exist_ok=True)
        
        # Load seeds data
        self.seeds_data = self._load_seeds()
        
        # Initialize pytrends with rate limiting
        self.pytrends = TrendReq(
            hl='en-US',
            tz=360,
            timeout=(10, 25),
            retries=2,
            backoff_factor=0.1,
            requests_args={'verify': False}
        )
        
        # Rate limiting settings
        self.min_delay = 12  # Minimum seconds between requests
        self.max_delay = 15  # Maximum seconds between requests
        self.last_request_time = 0
        
    def _load_seeds(self) -> Dict:
        """Load seeds configuration from JSON file."""
        try:
            with open(self.seeds_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"Seeds file not found: {self.seeds_file}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in seeds file: {e}")
            sys.exit(1)
    
    def _rate_limit(self):
        """Implement rate limiting between requests."""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.min_delay:
            sleep_time = self.min_delay - time_since_last + random.uniform(0, 3)
            logger.info(f"Rate limiting: sleeping for {sleep_time:.1f} seconds")
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    def _get_interest_over_time(self, term: str, timeframe: str = "today 12-m") -> Optional[List[int]]:
        """Get interest over time data for a single term."""
        try:
            self._rate_limit()
            
            self.pytrends.build_payload([term], timeframe=timeframe, geo='', gprop='')
            interest_data = self.pytrends.interest_over_time()
            
            if interest_data.empty or term not in interest_data.columns:
                logger.warning(f"No interest data for term: {term}")
                return None
            
            # Get the last 52 weeks of data (weekly)
            values = interest_data[term].tolist()
            if len(values) < 8:  # Need at least 8 weeks for meaningful analysis
                logger.warning(f"Insufficient data for term: {term} (only {len(values)} weeks)")
                return None
                
            return values[-52:] if len(values) > 52 else values  # Cap at 52 weeks
            
        except (ResponseError, TooManyRequestsError) as e:
            logger.error(f"API error for term {term}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error for term {term}: {e}")
            return None
    
    def _get_related_queries(self, term: str) -> List[str]:
        """Get related queries (top + rising) for a term."""
        try:
            self._rate_limit()
            
            self.pytrends.build_payload([term], timeframe="today 12-m", geo='', gprop='')
            related_data = self.pytrends.related_queries()
            
            if term not in related_data or related_data[term] is None:
                return []
            
            related_queries = []
            
            # Get top queries
            if 'top' in related_data[term] and related_data[term]['top'] is not None:
                top_queries = related_data[term]['top']['query'].tolist()[:5]  # Top 5
                related_queries.extend(top_queries)
            
            # Get rising queries
            if 'rising' in related_data[term] and related_data[term]['rising'] is not None:
                rising_queries = related_data[term]['rising']['query'].tolist()[:5]  # Top 5
                related_queries.extend(rising_queries)
            
            return related_queries
            
        except (ResponseError, TooManyRequestsError) as e:
            logger.error(f"Related queries error for term {term}: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error getting related queries for {term}: {e}")
            return []
    
    def _calculate_score(self, sparkline: List[int]) -> Tuple[float, float, float]:
        """Calculate score components: slope, percent change, and volatility."""
        if len(sparkline) < 8:
            return 0.0, 0.0, 0.0
        
        all_weeks = sparkline
        
        # Calculate slope (trend over last 8 weeks)
        last_8_weeks = sparkline[-8:]
        x = np.arange(len(last_8_weeks))
        y = np.array(last_8_weeks)
        slope = np.polyfit(x, y, 1)[0] if len(last_8_weeks) > 1 else 0
        
        # Calculate percent change (last 4 weeks vs previous 4 weeks)
        if len(all_weeks) >= 8:
            recent_4 = np.mean(all_weeks[-4:])
            previous_4 = np.mean(all_weeks[-8:-4])
            percent_change = ((recent_4 - previous_4) / previous_4 * 100) if previous_4 > 0 else 0
        else:
            percent_change = 0
        
        # Calculate volatility (standard deviation of all data)
        volatility = np.std(all_weeks) if len(all_weeks) > 1 else 0
        
        return slope, percent_change, volatility
    
    def _normalize_score(self, values: List[float]) -> List[float]:
        """Normalize scores using z-score normalization."""
        if not values or len(values) < 2:
            return [0.0] * len(values)
        
        mean_val = np.mean(values)
        std_val = np.std(values)
        
        if std_val == 0:
            return [0.0] * len(values)
        
        return [(val - mean_val) / std_val for val in values]
    
    def _normalize_term_for_dedup(self, term: str) -> str:
        """Normalize term for better deduplication matching."""
        # Convert to lowercase and strip whitespace
        normalized = term.lower().strip()
        
        # Remove common punctuation and special characters, but keep spaces
        # This helps with abbreviations like "A.I." -> "ai" and "Chat-GPT" -> "chatgpt"
        normalized = normalized.replace('-', '').replace('_', '').replace('.', '')
        
        # Remove extra spaces
        normalized = ' '.join(normalized.split())
        
        return normalized

    def _calculate_similarity_threshold(self, term1: str, term2: str) -> int:
        """Calculate dynamic similarity threshold based on term characteristics."""
        # Base threshold
        base_threshold = 85
        
        # Lower threshold for shorter terms (more likely to be abbreviations)
        if len(term1) <= 3 or len(term2) <= 3:
            return 75
        
        # Lower threshold for terms with numbers
        if any(char.isdigit() for char in term1 + term2):
            return 80
        
        # Higher threshold for very long terms (more specific)
        if len(term1) > 20 or len(term2) > 20:
            return 90
        
        return base_threshold

    def _deduplicate_topics(self, topics: List[Dict]) -> List[Dict]:
        """Remove duplicate topics using fuzzy matching with multiple algorithms."""
        if not topics:
            return topics
        
        logger.info(f"Starting deduplication of {len(topics)} topics")
        
        # Sort topics by score (highest first) to keep best versions
        topics_sorted = sorted(topics, key=lambda x: x['score'], reverse=True)
        
        unique_topics = []
        seen_terms = set()
        duplicates_found = 0
        
        for topic in topics_sorted:
            term = topic['term']
            normalized_term = self._normalize_term_for_dedup(term)
            
            # Skip if exact duplicate already processed
            if normalized_term in seen_terms:
                duplicates_found += 1
                continue
            
            # Check for fuzzy duplicates using multiple algorithms
            is_duplicate = False
            best_match = None
            best_similarity = 0
            
            for existing in unique_topics:
                existing_term = existing['term']
                existing_normalized = self._normalize_term_for_dedup(existing_term)
                
                # Use multiple fuzzy matching algorithms for better accuracy
                ratio_similarity = fuzz.ratio(normalized_term, existing_normalized)
                partial_similarity = fuzz.partial_ratio(normalized_term, existing_normalized)
                token_sort_similarity = fuzz.token_sort_ratio(normalized_term, existing_normalized)
                token_set_similarity = fuzz.token_set_ratio(normalized_term, existing_normalized)
                
                # Take the maximum similarity across all algorithms
                max_similarity = max(ratio_similarity, partial_similarity, token_sort_similarity, token_set_similarity)
                
                # Use dynamic threshold based on term characteristics
                threshold = self._calculate_similarity_threshold(normalized_term, existing_normalized)
                
                # Consider it a duplicate if similarity exceeds threshold
                if max_similarity > threshold:
                    if max_similarity > best_similarity:
                        best_match = existing
                        best_similarity = max_similarity
                    is_duplicate = True
            
            if is_duplicate and best_match:
                # Keep the one with higher score (topics_sorted is already sorted by score)
                if topic['score'] > best_match['score']:
                    # Replace the existing topic with the better one
                    unique_topics.remove(best_match)
                    unique_topics.append(topic)
                    logger.debug(f"Replaced '{best_match['term']}' with '{topic['term']}' (similarity: {best_similarity:.1f}%)")
                else:
                    logger.debug(f"Kept '{best_match['term']}' over '{topic['term']}' (similarity: {best_similarity:.1f}%)")
                duplicates_found += 1
            else:
                # No duplicate found, add to unique topics
                unique_topics.append(topic)
                seen_terms.add(normalized_term)
        
        logger.info(f"Deduplication complete: {duplicates_found} duplicates removed, {len(unique_topics)} unique topics remaining")
        return unique_topics
    
    def _process_category(self, category: str, terms: List[str]) -> List[Dict]:
        """Process all terms in a category and return scored topics."""
        logger.info(f"Processing category: {category} with {len(terms)} terms")
        topics = []
        
        for term in terms:
            logger.info(f"Processing term: {term}")
            
            # Get interest over time data
            sparkline = self._get_interest_over_time(term)
            if not sparkline:
                continue
            
            # Calculate score components
            slope, percent_change, volatility = self._calculate_score(sparkline)
            
            # Check volume threshold
            median_volume = np.median(sparkline[-8:])  # Last 8 weeks median
            if median_volume < self.seeds_data['globalSettings']['minVolumeThreshold']:
                logger.info(f"Skipping {term}: volume too low ({median_volume})")
                continue
            
            # Get related queries
            related_queries = self._get_related_queries(term)
            
            # Create topic entry
            topic = {
                'term': term,
                'category': category,
                'score': 0.0,  # Will be calculated after normalization
                'percentChange': percent_change,
                'sparkline': sparkline,
                'firstSeen': (datetime.now() - timedelta(weeks=len(sparkline))).isoformat(),
                'lastSeen': datetime.now().isoformat(),
                'volume': int(median_volume),
                'relatedQueries': related_queries[:3],  # Keep top 3 related queries
                # Debug info (will be removed in production)
                'debug': {
                    'slope': slope,
                    'volatility': volatility,
                    'medianVolume': median_volume
                }
            }
            
            topics.append(topic)
        
        return topics
    
    def _calculate_final_scores(self, all_topics: List[Dict]) -> List[Dict]:
        """Calculate final scores using normalized components."""
        if not all_topics:
            return all_topics
        
        # Extract components for normalization
        slopes = []
        percent_changes = []
        volatilities = []
        
        for topic in all_topics:
            sparkline = topic['sparkline']
            if len(sparkline) >= 8:
                # Calculate actual slope from last 8 weeks
                last_8_weeks = sparkline[-8:]
                x = np.arange(len(last_8_weeks))
                y = np.array(last_8_weeks)
                slope = np.polyfit(x, y, 1)[0] if len(last_8_weeks) > 1 else 0
                slopes.append(slope)
            else:
                slopes.append(0.0)
            
            percent_changes.append(topic['percentChange'])
            volatilities.append(np.std(sparkline) if len(sparkline) > 1 else 0)
        
        # Normalize components
        norm_slopes = self._normalize_score(slopes)
        norm_percent_changes = self._normalize_score(percent_changes)
        norm_volatilities = self._normalize_score(volatilities)
        
        # Calculate final scores: z(slope) + 0.7·z(%Δ) - 0.3·z(volatility)
        for i, topic in enumerate(all_topics):
            topic['score'] = (
                norm_slopes[i] + 
                0.7 * norm_percent_changes[i] - 
                0.3 * norm_volatilities[i]
            )
        
        return all_topics
    
    def _cleanup_archives(self):
        """Keep only the last 7 days of archives."""
        try:
            archive_files = []
            for filename in os.listdir(self.archive_dir):
                if filename.endswith('.json'):
                    filepath = os.path.join(self.archive_dir, filename)
                    archive_files.append((filepath, os.path.getmtime(filepath)))
            
            # Sort by modification time (newest first)
            archive_files.sort(key=lambda x: x[1], reverse=True)
            
            # Keep only the 7 most recent files
            for filepath, _ in archive_files[7:]:
                os.remove(filepath)
                logger.info(f"Removed old archive: {filepath}")
                
        except Exception as e:
            logger.error(f"Error cleaning up archives: {e}")
    
    def _clean_debug_info(self, topics: List[Dict]) -> List[Dict]:
        """Remove debug information from topics before saving."""
        cleaned_topics = []
        for topic in topics:
            cleaned_topic = {k: v for k, v in topic.items() if k != 'debug'}
            cleaned_topics.append(cleaned_topic)
        return cleaned_topics

    def _save_data(self, topics: List[Dict]):
        """Save topics to latest.json and create archive."""
        try:
            # Clean debug information
            cleaned_topics = self._clean_debug_info(topics)
            
            # Create output data structure
            output_data = {
                'generatedAt': datetime.now().isoformat(),
                'totalTopics': len(cleaned_topics),
                'topics': cleaned_topics
            }
            
            # Save latest.json
            with open(self.latest_file, 'w') as f:
                json.dump(output_data, f, indent=2)
            
            logger.info(f"Saved {len(topics)} topics to {self.latest_file}")
            
            # Create archive
            archive_filename = f"{datetime.now().strftime('%Y-%m-%d')}.json"
            archive_path = os.path.join(self.archive_dir, archive_filename)
            
            with open(archive_path, 'w') as f:
                json.dump(output_data, f, indent=2)
            
            logger.info(f"Created archive: {archive_path}")
            
            # Clean up old archives
            self._cleanup_archives()
            
        except Exception as e:
            logger.error(f"Error saving data: {e}")
            raise
    
    def run(self):
        """Run the complete data pipeline."""
        logger.info("Starting Exploding Topics data pipeline")
        start_time = time.time()
        
        try:
            all_topics = []
            
            # Process each category
            for category, config in self.seeds_data['categories'].items():
                terms = config['terms']
                category_topics = self._process_category(category, terms)
                all_topics.extend(category_topics)
            
            logger.info(f"Collected {len(all_topics)} topics before deduplication")
            
            # Deduplicate topics
            all_topics = self._deduplicate_topics(all_topics)
            logger.info(f"After deduplication: {len(all_topics)} topics")
            
            # Calculate final scores
            all_topics = self._calculate_final_scores(all_topics)
            
            # Sort by score (highest first)
            all_topics.sort(key=lambda x: x['score'], reverse=True)
            
            # Cap at 150 topics
            if len(all_topics) > 150:
                all_topics = all_topics[:150]
                logger.info(f"Capped topics to 150 (was {len(all_topics)})")
            
            # Save data
            self._save_data(all_topics)
            
            # Log summary
            runtime = time.time() - start_time
            logger.info(f"Pipeline completed successfully in {runtime:.1f} seconds")
            logger.info(f"Final topics: {len(all_topics)}")
            
            return True
            
        except Exception as e:
            logger.error(f"Pipeline failed: {e}")
            return False

def main():
    """Main entry point."""
    pipeline = TrendsDataPipeline()
    success = pipeline.run()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
