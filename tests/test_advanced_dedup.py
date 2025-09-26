#!/usr/bin/env python3
"""
Test script for advanced deduplication features
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))

from build_data import TrendsDataPipeline

def create_test_topic(term, category, score):
    """Create a test topic with mock data."""
    return {
        'term': term,
        'category': category,
        'score': score,
        'percentChange': 0,
        'sparkline': [10, 20, 30, 40, 50, 60, 70, 80],
        'firstSeen': '2024-01-01T00:00:00',
        'lastSeen': '2024-01-15T00:00:00',
        'volume': 1000,
        'relatedQueries': ['related1', 'related2'],
        'debug': {'slope': 10.0, 'volatility': 25.0, 'medianVolume': 1000}
    }

def test_normalization():
    """Test the term normalization functionality."""
    print("Testing term normalization...")
    
    pipeline = TrendsDataPipeline()
    
    test_cases = [
        ("ChatGPT", "chatgpt"),
        ("Chat-GPT", "chatgpt"),
        ("Chat_GPT", "chatgpt"),
        ("Chat.GPT", "chatgpt"),
        ("  ChatGPT  ", "chatgpt"),
        ("Machine Learning", "machine learning"),
        ("machine-learning", "machinelearning"),
        ("Machine_Learning", "machinelearning"),
    ]
    
    for input_term, expected in test_cases:
        result = pipeline._normalize_term_for_dedup(input_term)
        if result == expected:
            print(f"✅ '{input_term}' -> '{result}'")
        else:
            print(f"❌ '{input_term}' -> '{result}' (expected '{expected}')")

def test_dynamic_thresholds():
    """Test the dynamic similarity threshold calculation."""
    print("\nTesting dynamic similarity thresholds...")
    
    pipeline = TrendsDataPipeline()
    
    test_cases = [
        ("AI", "A.I.", 75),  # Short terms
        ("ML", "Machine Learning", 75),  # Short vs long
        ("Python3", "Python 3", 80),  # Terms with numbers
        ("JavaScript", "JS", 75),  # Short abbreviation
        ("Artificial Intelligence", "AI", 75),  # Long vs short
        ("Machine Learning", "Deep Learning", 85),  # Normal terms
        ("Very Long Term Name Here", "Another Very Long Term Name", 90),  # Very long terms
    ]
    
    for term1, term2, expected in test_cases:
        result = pipeline._calculate_similarity_threshold(term1, term2)
        if result == expected:
            print(f"✅ '{term1}' vs '{term2}' -> {result}% threshold")
        else:
            print(f"❌ '{term1}' vs '{term2}' -> {result}% threshold (expected {expected}%)")

def test_advanced_deduplication():
    """Test advanced deduplication scenarios."""
    print("\nTesting advanced deduplication scenarios...")
    
    pipeline = TrendsDataPipeline()
    
    # Test cases with various normalization scenarios
    test_cases = [
        {
            'name': 'Punctuation variations',
            'topics': [
                create_test_topic('ChatGPT', 'ai-tools', 8.5),
                create_test_topic('Chat-GPT', 'ai-tools', 7.0),
                create_test_topic('Chat_GPT', 'ai-tools', 6.5),
                create_test_topic('Chat.GPT', 'ai-tools', 6.0),
            ],
            'expected_unique': 1
        },
        {
            'name': 'Abbreviation handling',
            'topics': [
                create_test_topic('Machine Learning', 'ai-tools', 8.0),
                create_test_topic('ML', 'ai-tools', 7.5),
                create_test_topic('A.I.', 'ai-tools', 7.0),
                create_test_topic('AI', 'ai-tools', 6.5),
            ],
            'expected_unique': 3  # Machine Learning + ML + AI variants
        },
        {
            'name': 'Number variations',
            'topics': [
                create_test_topic('Python3', 'programming', 8.0),
                create_test_topic('Python 3', 'programming', 7.5),
                create_test_topic('Python-3', 'programming', 7.0),
                create_test_topic('JavaScript', 'programming', 6.5),
            ],
            'expected_unique': 2  # Python3 variants + JavaScript
        },
        {
            'name': 'Case sensitivity',
            'topics': [
                create_test_topic('React', 'programming', 8.0),
                create_test_topic('react', 'programming', 7.5),
                create_test_topic('REACT', 'programming', 7.0),
                create_test_topic('Vue', 'programming', 6.5),
            ],
            'expected_unique': 2  # React variants + Vue
        }
    ]
    
    for case in test_cases:
        print(f"\n--- {case['name']} ---")
        
        unique_topics = pipeline._deduplicate_topics(case['topics'])
        
        print(f"Input: {len(case['topics'])} topics")
        print(f"Output: {len(unique_topics)} unique topics")
        print(f"Expected: {case['expected_unique']} unique topics")
        
        if len(unique_topics) == case['expected_unique']:
            print("✅ Correct number of unique topics")
        else:
            print(f"❌ Expected {case['expected_unique']}, got {len(unique_topics)}")
        
        print("Unique topics:")
        for topic in unique_topics:
            print(f"  - '{topic['term']}' (score: {topic['score']})")

if __name__ == "__main__":
    test_normalization()
    test_dynamic_thresholds()
    test_advanced_deduplication()
