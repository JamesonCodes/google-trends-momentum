#!/usr/bin/env python3
"""
Test script for the deduplication functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from build_data import TrendsDataPipeline
import json

def create_test_topic(term, category, score, percent_change=0):
    """Create a test topic with mock data."""
    return {
        'term': term,
        'category': category,
        'score': score,
        'percentChange': percent_change,
        'sparkline': [10, 20, 30, 40, 50, 60, 70, 80],
        'firstSeen': '2024-01-01T00:00:00',
        'lastSeen': '2024-01-15T00:00:00',
        'volume': 1000,
        'relatedQueries': ['related1', 'related2'],
        'debug': {
            'slope': 10.0,
            'volatility': 25.0,
            'medianVolume': 1000
        }
    }

def test_deduplication():
    """Test the deduplication functionality with various scenarios."""
    print("Testing deduplication functionality...")
    
    # Create pipeline instance
    pipeline = TrendsDataPipeline()
    
    # Test cases for deduplication
    test_cases = [
        {
            'name': 'Exact duplicates',
            'topics': [
                create_test_topic('ChatGPT', 'ai-tools', 8.5),
                create_test_topic('chatgpt', 'ai-tools', 7.2),  # Exact duplicate (different case)
                create_test_topic('ChatGPT', 'ai-tools', 6.8),  # Exact duplicate
            ],
            'expected_unique': 1,
            'expected_kept': 'ChatGPT'  # Should keep the first one (highest score)
        },
        {
            'name': 'Fuzzy duplicates - similar terms',
            'topics': [
                create_test_topic('ChatGPT', 'ai-tools', 8.5),
                create_test_topic('Chat GPT', 'ai-tools', 7.2),  # Space difference
                create_test_topic('chat-gpt', 'ai-tools', 6.8),  # Hyphen difference
                create_test_topic('OpenAI', 'ai-tools', 9.0),    # Different term
            ],
            'expected_unique': 2,  # ChatGPT variants + OpenAI
            'expected_kept': 'OpenAI'  # Should keep OpenAI (highest score)
        },
        {
            'name': 'Fuzzy duplicates - word order',
            'topics': [
                create_test_topic('Machine Learning', 'ai-tools', 8.0),
                create_test_topic('Learning Machine', 'ai-tools', 7.5),  # Word order
                create_test_topic('ML', 'ai-tools', 6.0),  # Abbreviation
            ],
            'expected_unique': 2,  # ML variants + ML abbreviation
            'expected_kept': 'Machine Learning'  # Should keep the first one
        },
        {
            'name': 'Fuzzy duplicates - partial matches',
            'topics': [
                create_test_topic('Artificial Intelligence', 'ai-tools', 8.0),
                create_test_topic('AI', 'ai-tools', 7.5),  # Abbreviation
                create_test_topic('Artificial', 'ai-tools', 6.0),  # Partial match
                create_test_topic('Blockchain', 'crypto', 9.0),  # Different category
            ],
            'expected_unique': 2,  # AI variants + Blockchain
            'expected_kept': 'Blockchain'  # Should keep Blockchain (highest score)
        },
        {
            'name': 'No duplicates',
            'topics': [
                create_test_topic('Python', 'programming', 8.0),
                create_test_topic('JavaScript', 'programming', 7.5),
                create_test_topic('React', 'programming', 6.0),
            ],
            'expected_unique': 3,
            'expected_kept': 'Python'  # Should keep all (no duplicates)
        }
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n--- Test Case {i}: {case['name']} ---")
        
        # Run deduplication
        unique_topics = pipeline._deduplicate_topics(case['topics'])
        
        print(f"Input topics: {len(case['topics'])}")
        print(f"Unique topics: {len(unique_topics)}")
        print(f"Expected unique: {case['expected_unique']}")
        
        # Check if we got the expected number of unique topics
        if len(unique_topics) == case['expected_unique']:
            print("✅ Correct number of unique topics")
        else:
            print(f"❌ Expected {case['expected_unique']} unique topics, got {len(unique_topics)}")
        
        # Check if the highest scoring topic was kept
        if unique_topics:
            highest_score_topic = max(unique_topics, key=lambda x: x['score'])
            print(f"Highest scoring topic kept: '{highest_score_topic['term']}' (score: {highest_score_topic['score']})")
            
            if case['expected_kept'] in [t['term'] for t in unique_topics]:
                print(f"✅ Expected topic '{case['expected_kept']}' was kept")
            else:
                print(f"❌ Expected topic '{case['expected_kept']}' was not kept")
        
        # Show all unique topics
        print("Unique topics:")
        for topic in unique_topics:
            print(f"  - '{topic['term']}' (score: {topic['score']}, category: {topic['category']})")

def test_deduplication_performance():
    """Test deduplication performance with larger datasets."""
    print("\n--- Performance Test ---")
    
    pipeline = TrendsDataPipeline()
    
    # Create a larger dataset with some duplicates
    topics = []
    
    # Add some unique topics
    unique_terms = ['Python', 'JavaScript', 'React', 'Vue', 'Angular', 'Node.js', 'Express', 'MongoDB', 'PostgreSQL', 'Redis']
    for i, term in enumerate(unique_terms):
        topics.append(create_test_topic(term, 'programming', 8.0 - i * 0.1))
    
    # Add some duplicates with variations
    duplicate_variations = [
        ('Python', 'python', 7.5),
        ('Python', 'Python Programming', 7.0),
        ('JavaScript', 'JS', 6.5),
        ('JavaScript', 'javascript', 6.0),
        ('React', 'React.js', 5.5),
        ('React', 'ReactJS', 5.0),
    ]
    
    for original, variation, score in duplicate_variations:
        topics.append(create_test_topic(variation, 'programming', score))
    
    print(f"Created {len(topics)} topics for performance test")
    
    # Run deduplication
    import time
    start_time = time.time()
    unique_topics = pipeline._deduplicate_topics(topics)
    end_time = time.time()
    
    print(f"Deduplication took {end_time - start_time:.3f} seconds")
    print(f"Reduced from {len(topics)} to {len(unique_topics)} topics")
    print(f"Removed {len(topics) - len(unique_topics)} duplicates")

if __name__ == "__main__":
    test_deduplication()
    test_deduplication_performance()
