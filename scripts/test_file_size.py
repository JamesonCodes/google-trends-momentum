#!/usr/bin/env python3
"""
Test script for file size optimization
"""

import sys
import os
import json
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from build_data import TrendsDataPipeline
import numpy as np

def create_large_test_topic(term, category, score):
    """Create a test topic with a large sparkline."""
    # Create a 52-week sparkline (maximum size)
    sparkline = [int(np.random.normal(50, 20)) for _ in range(52)]
    sparkline = [max(0, val) for val in sparkline]  # Ensure non-negative
    
    return {
        'term': term,
        'category': category,
        'score': score,
        'percentChange': np.random.normal(20, 30),
        'sparkline': sparkline,
        'firstSeen': '2024-01-01T00:00:00',
        'lastSeen': '2024-01-15T00:00:00',
        'volume': int(np.median(sparkline[-8:])),
        'relatedQueries': ['related1', 'related2', 'related3'],
        'debug': {
            'slope': np.random.normal(0, 5),
            'volatility': np.std(sparkline),
            'medianVolume': int(np.median(sparkline[-8:]))
        }
    }

def test_file_size_optimization():
    """Test file size optimization with large datasets."""
    print("Testing file size optimization...")
    
    # Create a large dataset with 52-week sparklines
    large_topics = []
    categories = ['ai-tools', 'ecommerce', 'fitness', 'crypto', 'design-tools', 'home-office', 'sustainability']
    
    for i in range(200):  # 200 topics with large sparklines
        category = categories[i % len(categories)]
        score = np.random.normal(5.0, 2.0)
        
        large_topics.append(create_large_test_topic(
            f"large_topic_{i}", 
            category, 
            score
        ))
    
    print(f"Created {len(large_topics)} topics with 52-week sparklines")
    
    # Test without optimization
    print("\n--- Without optimization ---")
    unoptimized_data = {
        'generatedAt': '2024-01-15T00:00:00',
        'totalTopics': len(large_topics),
        'topics': large_topics
    }
    
    with open('test_unoptimized.json', 'w') as f:
        json.dump(unoptimized_data, f, indent=2)
    
    unoptimized_size = os.path.getsize('test_unoptimized.json')
    print(f"Unoptimized file size: {unoptimized_size / 1024:.1f}KB")
    
    # Test with optimization
    print("\n--- With optimization ---")
    pipeline = TrendsDataPipeline()
    
    # Apply optimization
    optimized_topics = pipeline._optimize_sparklines(large_topics)
    cleaned_topics = pipeline._clean_debug_info(optimized_topics)
    
    optimized_data = {
        'generatedAt': '2024-01-15T00:00:00',
        'totalTopics': len(cleaned_topics),
        'topics': cleaned_topics
    }
    
    with open('test_optimized.json', 'w') as f:
        json.dump(optimized_data, f, indent=2)
    
    optimized_size = os.path.getsize('test_optimized.json')
    print(f"Optimized file size: {optimized_size / 1024:.1f}KB")
    
    # Calculate savings
    savings = (unoptimized_size - optimized_size) / unoptimized_size * 100
    print(f"Size reduction: {savings:.1f}%")
    
    # Check if under 400KB target
    if optimized_size / 1024 < 400:
        print("✅ File size under 400KB target")
    else:
        print("❌ File size exceeds 400KB target")
    
    # Verify sparkline lengths
    original_lengths = [len(t['sparkline']) for t in large_topics]
    optimized_lengths = [len(t['sparkline']) for t in optimized_topics]
    
    print(f"\nSparkline length statistics:")
    print(f"  Original: {min(original_lengths)} to {max(original_lengths)} points (avg: {np.mean(original_lengths):.1f})")
    print(f"  Optimized: {min(optimized_lengths)} to {max(optimized_lengths)} points (avg: {np.mean(optimized_lengths):.1f})")
    
    # Clean up test files
    os.remove('test_unoptimized.json')
    os.remove('test_optimized.json')

if __name__ == "__main__":
    test_file_size_optimization()
