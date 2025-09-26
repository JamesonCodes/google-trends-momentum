#!/usr/bin/env python3
"""
Test script for filtering and capping functionality
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))

from build_data import TrendsDataPipeline
import numpy as np

def create_test_topic(term, category, score, sparkline, percent_change=0):
    """Create a test topic with specified data."""
    return {
        'term': term,
        'category': category,
        'score': score,
        'percentChange': percent_change,
        'sparkline': sparkline,
        'firstSeen': '2024-01-01T00:00:00',
        'lastSeen': '2024-01-15T00:00:00',
        'volume': int(np.median(sparkline[-8:])),
        'relatedQueries': ['related1', 'related2'],
        'debug': {
            'slope': 10.0,
            'volatility': np.std(sparkline),
            'medianVolume': int(np.median(sparkline[-8:]))
        }
    }

def test_quality_filters():
    """Test the quality filtering functionality."""
    print("Testing quality filters...")
    
    pipeline = TrendsDataPipeline()
    
    # Test cases for quality filtering
    test_cases = [
        {
            'name': 'Good data - should pass',
            'sparkline': [10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65],
            'slope': 5.0,
            'percent_change': 30.0,
            'volatility': 20.0,
            'expected': True
        },
        {
            'name': 'Low volume - should fail',
            'sparkline': [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2],
            'slope': 0.1,
            'percent_change': 5.0,
            'volatility': 0.5,
            'expected': False
        },
        {
            'name': 'Too volatile - should fail',
            'sparkline': [10, 80, 5, 90, 2, 85, 8, 88, 3, 87, 6, 89],
            'slope': 2.0,
            'percent_change': 10.0,
            'volatility': 60.0,  # Very high volatility
            'expected': False
        },
        {
            'name': 'No recent activity - should fail',
            'sparkline': [10, 20, 30, 40, 50, 60, 70, 80, 0, 0, 0, 0],
            'slope': -5.0,
            'percent_change': -50.0,
            'volatility': 30.0,
            'expected': False
        },
        {
            'name': 'Too many zeros - should fail',
            'sparkline': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            'slope': 0.0,
            'percent_change': 0.0,
            'volatility': 0.0,
            'expected': False
        },
        {
            'name': 'Weak trend - should fail',
            'sparkline': [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
            'slope': 0.05,  # Very small slope
            'percent_change': 2.0,  # Very small change
            'volatility': 0.1,
            'expected': False
        },
        {
            'name': 'Suspicious spike - should fail',
            'sparkline': [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 1000],
            'slope': 50.0,
            'percent_change': 9000.0,
            'volatility': 300.0,
            'expected': False
        }
    ]
    
    for case in test_cases:
        print(f"\n--- {case['name']} ---")
        result = pipeline._passes_quality_filters(
            "test_term", 
            case['sparkline'], 
            case['slope'], 
            case['percent_change'], 
            case['volatility']
        )
        
        if result == case['expected']:
            print(f"✅ Correctly {'passed' if result else 'failed'} quality filters")
        else:
            print(f"❌ Expected {case['expected']}, got {result}")

def test_final_filtering_and_capping():
    """Test the final filtering and capping functionality."""
    print("\nTesting final filtering and capping...")
    
    pipeline = TrendsDataPipeline()
    
    # Create test topics with various scores
    test_topics = []
    
    # High quality topics (should be kept)
    for i in range(5):
        test_topics.append(create_test_topic(
            f"high_quality_{i}", 
            "ai-tools", 
            8.0 + i, 
            [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120]
        ))
    
    # Medium quality topics (some should be kept)
    for i in range(10):
        test_topics.append(create_test_topic(
            f"medium_quality_{i}", 
            "ecommerce", 
            3.0 + i * 0.5, 
            [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]
        ))
    
    # Low quality topics (should be filtered out)
    for i in range(5):
        test_topics.append(create_test_topic(
            f"low_quality_{i}", 
            "fitness", 
            -2.0 + i * 0.1,  # Negative scores
            [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2]
        ))
    
    # Very low quality topics (should be filtered out)
    for i in range(5):
        test_topics.append(create_test_topic(
            f"very_low_quality_{i}", 
            "crypto", 
            0.1 + i * 0.05,  # Very low positive scores
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ))
    
    print(f"Created {len(test_topics)} test topics")
    
    # Test filtering and capping
    filtered_topics = pipeline._apply_final_filtering_and_capping(test_topics)
    
    print(f"After filtering: {len(filtered_topics)} topics")
    
    # Verify results
    if len(filtered_topics) <= 150:
        print("✅ Capped at 150 topics or less")
    else:
        print(f"❌ Not properly capped: {len(filtered_topics)} topics")
    
    # Check that no negative scores remain
    negative_scores = [t for t in filtered_topics if t['score'] <= 0]
    if len(negative_scores) == 0:
        print("✅ No negative scores in final topics")
    else:
        print(f"❌ Found {len(negative_scores)} topics with negative scores")
    
    # Check score distribution
    if filtered_topics:
        scores = [t['score'] for t in filtered_topics]
        print(f"Score range: {min(scores):.2f} to {max(scores):.2f}")
        print(f"Average score: {np.mean(scores):.2f}")
        
        # Show top 5 topics
        print("Top 5 topics:")
        for i, topic in enumerate(sorted(filtered_topics, key=lambda x: x['score'], reverse=True)[:5]):
            print(f"  {i+1}. {topic['term']} (score: {topic['score']:.2f}, category: {topic['category']})")

def test_performance_with_large_dataset():
    """Test filtering performance with a large dataset."""
    print("\nTesting performance with large dataset...")
    
    pipeline = TrendsDataPipeline()
    
    # Create a large dataset
    large_dataset = []
    categories = ['ai-tools', 'ecommerce', 'fitness', 'crypto', 'design-tools']
    
    for i in range(500):  # 500 topics
        category = categories[i % len(categories)]
        score = np.random.normal(5.0, 3.0)  # Normal distribution around 5
        sparkline = [max(0, int(np.random.normal(50, 20))) for _ in range(12)]
        
        large_dataset.append(create_test_topic(
            f"topic_{i}", 
            category, 
            score, 
            sparkline
        ))
    
    print(f"Created {len(large_dataset)} topics for performance test")
    
    # Time the filtering
    import time
    start_time = time.time()
    filtered_topics = pipeline._apply_final_filtering_and_capping(large_dataset)
    end_time = time.time()
    
    print(f"Filtering took {end_time - start_time:.3f} seconds")
    print(f"Reduced from {len(large_dataset)} to {len(filtered_topics)} topics")
    print(f"Removal rate: {(len(large_dataset) - len(filtered_topics)) / len(large_dataset) * 100:.1f}%")

if __name__ == "__main__":
    test_quality_filters()
    test_final_filtering_and_capping()
    test_performance_with_large_dataset()
