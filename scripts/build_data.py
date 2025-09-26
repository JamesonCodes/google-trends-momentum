#!/usr/bin/env python3
"""
Rising Topics Data Pipeline
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

# Configure comprehensive logging
def setup_logging():
    """Set up comprehensive logging with multiple handlers and levels."""
    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
    )
    simple_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Create handlers
    handlers = []
    
    # File handler for detailed logs
    file_handler = logging.FileHandler('data_pipeline.log')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(detailed_formatter)
    handlers.append(file_handler)
    
    # Console handler for important messages
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(simple_formatter)
    handlers.append(console_handler)
    
    # Error file handler for critical errors
    error_handler = logging.FileHandler('data_pipeline_errors.log')
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(detailed_formatter)
    handlers.append(error_handler)
    
    # Configure root logger
    logging.basicConfig(
        level=logging.DEBUG,
        handlers=handlers
    )
    
    # Set specific logger levels
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('requests').setLevel(logging.WARNING)
    
    return logging.getLogger(__name__)

# Set up logging
logger = setup_logging()

# Error tracking and metrics
class ErrorTracker:
    """Track errors and performance metrics."""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.metrics = {
            'api_calls': 0,
            'api_errors': 0,
            'processing_errors': 0,
            'validation_errors': 0,
            'start_time': None,
            'end_time': None
        }
    
    def log_error(self, error_type: str, message: str, context: dict = None):
        """Log an error with context."""
        error_entry = {
            'timestamp': datetime.now().isoformat(),
            'type': error_type,
            'message': message,
            'context': context or {}
        }
        self.errors.append(error_entry)
        logger.error(f"[{error_type}] {message}", extra={'context': context})
    
    def log_warning(self, warning_type: str, message: str, context: dict = None):
        """Log a warning with context."""
        warning_entry = {
            'timestamp': datetime.now().isoformat(),
            'type': warning_type,
            'message': message,
            'context': context or {}
        }
        self.warnings.append(warning_entry)
        logger.warning(f"[{warning_type}] {message}", extra={'context': context})
    
    def increment_metric(self, metric_name: str, value: int = 1):
        """Increment a metric counter."""
        if metric_name in self.metrics:
            self.metrics[metric_name] += value
        else:
            self.metrics[metric_name] = value
    
    def get_summary(self) -> dict:
        """Get error and performance summary."""
        return {
            'total_errors': len(self.errors),
            'total_warnings': len(self.warnings),
            'metrics': self.metrics.copy(),
            'error_types': list(set(e['type'] for e in self.errors)),
            'warning_types': list(set(w['type'] for w in self.warnings))
        }

class TrendsDataPipeline:
    def __init__(self, seeds_file: str = "data/seeds.json"):
        """Initialize the data pipeline with seeds configuration."""
        self.seeds_file = seeds_file
        self.output_dir = "public/data"
        self.archive_dir = os.path.join(self.output_dir, "archive")
        self.latest_file = os.path.join(self.output_dir, "latest.json")
        
        # Initialize error tracking
        self.error_tracker = ErrorTracker()
        self.error_tracker.metrics['start_time'] = datetime.now().isoformat()
        
        try:
            # Ensure directories exist
            os.makedirs(self.output_dir, exist_ok=True)
            os.makedirs(self.archive_dir, exist_ok=True)
            logger.debug("Output directories created successfully")
            
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
            logger.debug("Pytrends initialized successfully")
            
            # Rate limiting settings
            self.min_delay = 12  # Minimum seconds between requests
            self.max_delay = 15  # Maximum seconds between requests
            self.last_request_time = 0
            
        except Exception as e:
            self.error_tracker.log_error(
                'INITIALIZATION_ERROR',
                f"Failed to initialize pipeline: {str(e)}",
                {'seeds_file': seeds_file, 'error': str(e)}
            )
            raise
        
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
            self.error_tracker.increment_metric('api_calls')
            
            self.pytrends.build_payload([term], timeframe=timeframe, geo='', gprop='')
            interest_data = self.pytrends.interest_over_time()
            
            if interest_data.empty or term not in interest_data.columns:
                self.error_tracker.log_warning(
                    'NO_DATA',
                    f"No interest data for term: {term}",
                    {'term': term, 'timeframe': timeframe}
                )
                return None
            
            # Get the last 52 weeks of data (weekly)
            values = interest_data[term].tolist()
            if len(values) < 8:  # Need at least 8 weeks for meaningful analysis
                self.error_tracker.log_warning(
                    'INSUFFICIENT_DATA',
                    f"Insufficient data for term: {term} (only {len(values)} weeks)",
                    {'term': term, 'data_points': len(values), 'min_required': 8}
                )
                return None
                
            logger.debug(f"Successfully retrieved {len(values)} data points for {term}")
            return values[-52:] if len(values) > 52 else values  # Cap at 52 weeks
            
        except (ResponseError, TooManyRequestsError) as e:
            self.error_tracker.increment_metric('api_errors')
            self.error_tracker.log_error(
                'API_ERROR',
                f"API error for term {term}: {str(e)}",
                {'term': term, 'error_type': type(e).__name__, 'error': str(e)}
            )
            return None
        except Exception as e:
            self.error_tracker.increment_metric('api_errors')
            self.error_tracker.log_error(
                'UNEXPECTED_ERROR',
                f"Unexpected error for term {term}: {str(e)}",
                {'term': term, 'error_type': type(e).__name__, 'error': str(e)}
            )
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
    
    def _passes_quality_filters(self, term: str, sparkline: List[int], slope: float, percent_change: float, volatility: float) -> bool:
        """Apply comprehensive quality filters to determine if a topic should be included."""
        
        # 1. Volume threshold check (last 8 weeks median)
        median_volume = np.median(sparkline[-8:])
        min_volume = self.seeds_data['globalSettings']['minVolumeThreshold']
        
        if median_volume < min_volume:
            logger.debug(f"Skipping {term}: volume too low ({median_volume:.1f} < {min_volume})")
            return False
        
        # 2. Data completeness check (need sufficient data points)
        if len(sparkline) < 8:
            logger.debug(f"Skipping {term}: insufficient data ({len(sparkline)} weeks)")
            return False
        
        # 3. Trend stability check (avoid extremely volatile data)
        max_volatility = 50.0  # Maximum allowed volatility
        if volatility > max_volatility:
            logger.debug(f"Skipping {term}: too volatile ({volatility:.1f} > {max_volatility})")
            return False
        
        # 4. Recent activity check (ensure recent data isn't all zeros)
        recent_weeks = sparkline[-4:]  # Last 4 weeks
        if all(val == 0 for val in recent_weeks):
            logger.debug(f"Skipping {term}: no recent activity")
            return False
        
        # 5. Data consistency check (avoid data with too many zeros)
        zero_ratio = sum(1 for val in sparkline if val == 0) / len(sparkline)
        max_zero_ratio = 0.7  # Maximum 70% zeros allowed
        if zero_ratio > max_zero_ratio:
            logger.debug(f"Skipping {term}: too many zeros ({zero_ratio:.1%} > {max_zero_ratio:.1%})")
            return False
        
        # 6. Minimum trend strength check (avoid completely flat trends)
        if abs(slope) < 0.1 and abs(percent_change) < 5.0:
            logger.debug(f"Skipping {term}: trend too weak (slope: {slope:.2f}, change: {percent_change:.1f}%)")
            return False
        
        # 7. Outlier detection (check for suspicious spikes)
        if len(sparkline) > 4:
            recent_avg = np.mean(sparkline[-4:])
            historical_avg = np.mean(sparkline[:-4])
            if recent_avg > historical_avg * 10:  # 10x spike might be suspicious
                logger.debug(f"Skipping {term}: suspicious spike detected")
                return False
        
        logger.debug(f"✅ {term} passed all quality filters (volume: {median_volume:.1f}, volatility: {volatility:.1f})")
        return True
    
    def _apply_final_filtering_and_capping(self, topics: List[Dict]) -> List[Dict]:
        """Apply final filtering and intelligent capping to topics."""
        if not topics:
            return topics
        
        original_count = len(topics)
        logger.info(f"Applying final filtering and capping to {original_count} topics")
        
        # 1. Remove topics with negative scores (not trending)
        positive_score_topics = [t for t in topics if t['score'] > 0]
        removed_negative = len(topics) - len(positive_score_topics)
        if removed_negative > 0:
            logger.info(f"Removed {removed_negative} topics with negative scores")
        
        # 2. Apply score-based quality threshold
        if positive_score_topics:
            scores = [t['score'] for t in positive_score_topics]
            score_threshold = np.percentile(scores, 10)  # Keep top 90% by score
            quality_topics = [t for t in positive_score_topics if t['score'] >= score_threshold]
            removed_low_quality = len(positive_score_topics) - len(quality_topics)
            if removed_low_quality > 0:
                logger.info(f"Removed {removed_low_quality} low-quality topics (score < {score_threshold:.2f})")
        else:
            quality_topics = positive_score_topics
        
        # 3. Apply hard cap of 150 topics
        max_topics = 150
        if len(quality_topics) > max_topics:
            capped_topics = quality_topics[:max_topics]
            removed_by_cap = len(quality_topics) - len(capped_topics)
            logger.info(f"Capped to {max_topics} topics (removed {removed_by_cap} lowest scoring)")
        else:
            capped_topics = quality_topics
        
        # 4. Ensure category diversity (optional - keep at least 1 topic per category if possible)
        category_counts = {}
        for topic in capped_topics:
            category = topic['category']
            category_counts[category] = category_counts.get(category, 0) + 1
        
        logger.info(f"Final topic distribution by category:")
        for category, count in sorted(category_counts.items()):
            logger.info(f"  {category}: {count} topics")
        
        # 5. Calculate final statistics
        final_count = len(capped_topics)
        total_removed = original_count - final_count
        
        if final_count > 0:
            avg_score = np.mean([t['score'] for t in capped_topics])
            min_score = min(t['score'] for t in capped_topics)
            max_score = max(t['score'] for t in capped_topics)
            
            logger.info(f"Final filtering complete:")
            logger.info(f"  Original: {original_count} topics")
            logger.info(f"  Final: {final_count} topics")
            logger.info(f"  Removed: {total_removed} topics")
            logger.info(f"  Score range: {min_score:.2f} to {max_score:.2f} (avg: {avg_score:.2f})")
        else:
            logger.warning("No topics passed final filtering!")
        
        return capped_topics
    
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
            
            # Enhanced volume and quality filtering
            if not self._passes_quality_filters(term, sparkline, slope, percent_change, volatility):
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
        """Keep only the last 7 days of archives with date-based cleanup."""
        try:
            if not os.path.exists(self.archive_dir):
                return
            
            archive_files = []
            current_date = datetime.now().date()
            
            # Collect all archive files with their dates
            for filename in os.listdir(self.archive_dir):
                if filename.endswith('.json') and filename != 'latest.json':
                    filepath = os.path.join(self.archive_dir, filename)
                    
                    # Try to parse date from filename (YYYY-MM-DD.json)
                    try:
                        date_str = filename.replace('.json', '')
                        file_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                        
                        # Calculate days difference
                        days_old = (current_date - file_date).days
                        
                        archive_files.append((filepath, file_date, days_old))
                    except ValueError:
                        # If filename doesn't match expected format, use file modification time
                        mtime = os.path.getmtime(filepath)
                        file_date = datetime.fromtimestamp(mtime).date()
                        days_old = (current_date - file_date).days
                        archive_files.append((filepath, file_date, days_old))
            
            # Sort by date (newest first)
            archive_files.sort(key=lambda x: x[1], reverse=True)
            
            # Remove files older than 7 days
            removed_count = 0
            for filepath, file_date, days_old in archive_files:
                if days_old > 7:
                    try:
                        os.remove(filepath)
                        logger.info(f"Removed old archive: {os.path.basename(filepath)} ({days_old} days old)")
                        removed_count += 1
                    except OSError as e:
                        logger.warning(f"Could not remove archive {filepath}: {e}")
            
            # Log archive statistics
            remaining_count = len(archive_files) - removed_count
            logger.info(f"Archive cleanup complete: {removed_count} removed, {remaining_count} remaining")
            
            # List remaining archives
            if remaining_count > 0:
                logger.debug("Remaining archives:")
                for filepath, file_date, days_old in archive_files[:remaining_count]:
                    logger.debug(f"  {os.path.basename(filepath)} ({days_old} days old)")
                
        except Exception as e:
            logger.error(f"Error cleaning up archives: {e}")
    
    def _validate_archive(self, filepath: str) -> bool:
        """Validate that an archive file is properly formatted."""
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            # Check required fields
            required_fields = ['generatedAt', 'totalTopics', 'topics']
            if not all(field in data for field in required_fields):
                logger.warning(f"Archive {filepath} missing required fields")
                return False
            
            # Check topics structure
            if not isinstance(data['topics'], list):
                logger.warning(f"Archive {filepath} has invalid topics structure")
                return False
            
            # Check topic structure (at least one topic should have required fields)
            if data['topics']:
                topic = data['topics'][0]
                topic_required_fields = ['term', 'category', 'score', 'sparkline']
                if not all(field in topic for field in topic_required_fields):
                    logger.warning(f"Archive {filepath} has invalid topic structure")
                    return False
            
            return True
            
        except (json.JSONDecodeError, IOError) as e:
            logger.warning(f"Archive {filepath} is corrupted: {e}")
            return False
    
    def _get_archive_statistics(self) -> Dict:
        """Get statistics about the archive system."""
        try:
            if not os.path.exists(self.archive_dir):
                return {'total_archives': 0, 'total_size_kb': 0, 'oldest_date': None, 'newest_date': None}
            
            archive_files = []
            total_size = 0
            
            for filename in os.listdir(self.archive_dir):
                if filename.endswith('.json') and filename != 'latest.json':
                    filepath = os.path.join(self.archive_dir, filename)
                    file_size = os.path.getsize(filepath)
                    total_size += file_size
                    
                    try:
                        date_str = filename.replace('.json', '')
                        file_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                        archive_files.append((filepath, file_date, file_size))
                    except ValueError:
                        # Use modification time if filename doesn't match format
                        mtime = os.path.getmtime(filepath)
                        file_date = datetime.fromtimestamp(mtime).date()
                        archive_files.append((filepath, file_date, file_size))
            
            if not archive_files:
                return {'total_archives': 0, 'total_size_kb': 0, 'oldest_date': None, 'newest_date': None}
            
            # Sort by date
            archive_files.sort(key=lambda x: x[1])
            
            return {
                'total_archives': len(archive_files),
                'total_size_kb': round(total_size / 1024, 1),
                'oldest_date': archive_files[0][1].isoformat(),
                'newest_date': archive_files[-1][1].isoformat(),
                'files': [os.path.basename(f[0]) for f in archive_files]
            }
            
        except Exception as e:
            logger.error(f"Error getting archive statistics: {e}")
            return {'error': str(e)}
    
    def _clean_debug_info(self, topics: List[Dict]) -> List[Dict]:
        """Remove debug information from topics before saving."""
        cleaned_topics = []
        for topic in topics:
            cleaned_topic = {k: v for k, v in topic.items() if k != 'debug'}
            cleaned_topics.append(cleaned_topic)
        return cleaned_topics
    
    def _optimize_sparklines(self, topics: List[Dict]) -> List[Dict]:
        """Optimize sparkline data for performance and file size."""
        for topic in topics:
            sparkline = topic['sparkline']
            
            # If sparkline is too long, keep only the last 24 points for performance
            if len(sparkline) > 24:
                topic['sparkline'] = sparkline[-24:]
                logger.debug(f"Trimmed sparkline for {topic['term']} from {len(sparkline)} to 24 points")
        
        return topics

    def _save_data(self, topics: List[Dict]):
        """Save topics to latest.json and create archive."""
        try:
            # Optimize sparklines for performance
            optimized_topics = self._optimize_sparklines(topics)
            
            # Clean debug information
            cleaned_topics = self._clean_debug_info(optimized_topics)
            
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
            
            # Create archive with validation
            archive_filename = f"{datetime.now().strftime('%Y-%m-%d')}.json"
            archive_path = os.path.join(self.archive_dir, archive_filename)
            
            # Check if archive already exists for today
            if os.path.exists(archive_path):
                logger.warning(f"Archive for today already exists: {archive_filename}")
                # Create backup with timestamp
                timestamp = datetime.now().strftime('%H%M%S')
                backup_filename = f"{datetime.now().strftime('%Y-%m-%d')}_{timestamp}.json"
                backup_path = os.path.join(self.archive_dir, backup_filename)
                archive_path = backup_path
                archive_filename = backup_filename
            
            with open(archive_path, 'w') as f:
                json.dump(output_data, f, indent=2)
            
            # Validate the created archive
            if self._validate_archive(archive_path):
                logger.info(f"Created and validated archive: {archive_filename}")
            else:
                logger.error(f"Archive validation failed: {archive_filename}")
                # Remove invalid archive
                try:
                    os.remove(archive_path)
                    logger.info(f"Removed invalid archive: {archive_filename}")
                except OSError:
                    pass
            
            # Check file size and log warning if too large
            file_size = os.path.getsize(self.latest_file)
            file_size_kb = file_size / 1024
            
            if file_size_kb > 400:
                logger.warning(f"Output file is large: {file_size_kb:.1f}KB (target: <400KB)")
                if file_size_kb > 500:
                    logger.error(f"File size exceeds 500KB! Consider reducing topic count or sparkline length.")
            else:
                logger.info(f"Output file size: {file_size_kb:.1f}KB")
            
            # Clean up old archives
            self._cleanup_archives()
            
            # Log archive statistics
            archive_stats = self._get_archive_statistics()
            if 'error' not in archive_stats:
                logger.info(f"Archive system status: {archive_stats['total_archives']} files, "
                          f"{archive_stats['total_size_kb']}KB total, "
                          f"range: {archive_stats['oldest_date']} to {archive_stats['newest_date']}")
            
        except Exception as e:
            logger.error(f"Error saving data: {e}")
            raise
    
    def run(self):
        """Run the complete data pipeline with comprehensive error handling."""
        logger.info("Starting Rising Topics data pipeline")
        start_time = time.time()
        self.error_tracker.metrics['start_time'] = datetime.now().isoformat()
        
        try:
            all_topics = []
            categories_processed = 0
            total_terms_processed = 0
            
            # Process each category
            for category, config in self.seeds_data['categories'].items():
                try:
                    terms = config['terms']
                    logger.info(f"Processing category: {category} with {len(terms)} terms")
                    
                    category_topics = self._process_category(category, terms)
                    all_topics.extend(category_topics)
                    
                    categories_processed += 1
                    total_terms_processed += len(terms)
                    
                    logger.info(f"Category {category} completed: {len(category_topics)} topics collected")
                    
                except Exception as e:
                    self.error_tracker.log_error(
                        'CATEGORY_PROCESSING_ERROR',
                        f"Failed to process category {category}: {str(e)}",
                        {'category': category, 'terms_count': len(config['terms']), 'error': str(e)}
                    )
                    # Continue with other categories
                    continue
            
            logger.info(f"Collected {len(all_topics)} topics before deduplication")
            self.error_tracker.metrics['topics_before_dedup'] = len(all_topics)
            
            # Deduplicate topics
            try:
                all_topics = self._deduplicate_topics(all_topics)
                logger.info(f"After deduplication: {len(all_topics)} topics")
                self.error_tracker.metrics['topics_after_dedup'] = len(all_topics)
            except Exception as e:
                self.error_tracker.log_error(
                    'DEDUPLICATION_ERROR',
                    f"Failed to deduplicate topics: {str(e)}",
                    {'topics_count': len(all_topics), 'error': str(e)}
                )
                # Continue with original topics
                pass
            
            # Calculate final scores
            try:
                all_topics = self._calculate_final_scores(all_topics)
                logger.info("Final scores calculated successfully")
            except Exception as e:
                self.error_tracker.log_error(
                    'SCORING_ERROR',
                    f"Failed to calculate final scores: {str(e)}",
                    {'topics_count': len(all_topics), 'error': str(e)}
                )
                # Continue with unscored topics
                pass
            
            # Sort by score (highest first)
            all_topics.sort(key=lambda x: x.get('score', 0), reverse=True)
            
            # Apply intelligent capping and filtering
            try:
                all_topics = self._apply_final_filtering_and_capping(all_topics)
                logger.info("Final filtering and capping completed")
                self.error_tracker.metrics['topics_final'] = len(all_topics)
            except Exception as e:
                self.error_tracker.log_error(
                    'FILTERING_ERROR',
                    f"Failed to apply final filtering: {str(e)}",
                    {'topics_count': len(all_topics), 'error': str(e)}
                )
                # Continue with unfiltered topics
                pass
            
            # Save data
            try:
                self._save_data(all_topics)
                logger.info("Data saved successfully")
            except Exception as e:
                self.error_tracker.log_error(
                    'SAVE_ERROR',
                    f"Failed to save data: {str(e)}",
                    {'topics_count': len(all_topics), 'error': str(e)}
                )
                raise  # Re-raise as this is critical
            
            # Calculate final metrics
            runtime = time.time() - start_time
            self.error_tracker.metrics['end_time'] = datetime.now().isoformat()
            self.error_tracker.metrics['runtime_seconds'] = runtime
            self.error_tracker.metrics['categories_processed'] = categories_processed
            self.error_tracker.metrics['terms_processed'] = total_terms_processed
            
            # Log comprehensive summary
            self._log_pipeline_summary(runtime, all_topics)
            
            return True
            
        except Exception as e:
            self.error_tracker.log_error(
                'PIPELINE_CRITICAL_ERROR',
                f"Pipeline failed with critical error: {str(e)}",
                {'error': str(e), 'traceback': str(e.__traceback__)}
            )
            logger.error(f"Pipeline failed: {e}")
            return False
    
    def _log_pipeline_summary(self, runtime: float, final_topics: List[Dict]):
        """Log comprehensive pipeline summary."""
        summary = self.error_tracker.get_summary()
        
        logger.info("=" * 60)
        logger.info("RISING TOPICS PIPELINE EXECUTION SUMMARY")
        logger.info("=" * 60)
        logger.info(f"Runtime: {runtime:.1f} seconds")
        logger.info(f"Final topics: {len(final_topics)}")
        logger.info(f"Categories processed: {summary['metrics'].get('categories_processed', 0)}")
        logger.info(f"Terms processed: {summary['metrics'].get('terms_processed', 0)}")
        logger.info(f"API calls made: {summary['metrics'].get('api_calls', 0)}")
        logger.info(f"API errors: {summary['metrics'].get('api_errors', 0)}")
        logger.info(f"Total errors: {summary['total_errors']}")
        logger.info(f"Total warnings: {summary['total_warnings']}")
        
        if summary['error_types']:
            logger.info(f"Error types: {', '.join(summary['error_types'])}")
        
        if summary['warning_types']:
            logger.info(f"Warning types: {', '.join(summary['warning_types'])}")
        
        # Log success/failure status
        if summary['total_errors'] == 0:
            logger.info("STATUS: SUCCESS - No errors encountered")
        elif summary['total_errors'] < 5:
            logger.info("STATUS: SUCCESS WITH WARNINGS - Minor errors encountered")
        else:
            logger.warning("STATUS: PARTIAL SUCCESS - Multiple errors encountered")
        
        logger.info("=" * 60)

def main():
    """Main entry point."""
    pipeline = TrendsDataPipeline()
    success = pipeline.run()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
