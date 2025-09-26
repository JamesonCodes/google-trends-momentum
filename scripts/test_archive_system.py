#!/usr/bin/env python3
"""
Test script for the archive system functionality
"""

import sys
import os
import json
import shutil
from datetime import datetime, timedelta
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from build_data import TrendsDataPipeline
import numpy as np

def create_test_topic(term, category, score):
    """Create a test topic with mock data."""
    sparkline = [int(np.random.normal(50, 20)) for _ in range(12)]
    sparkline = [max(0, val) for val in sparkline]
    
    return {
        'term': term,
        'category': category,
        'score': score,
        'percentChange': np.random.normal(20, 30),
        'sparkline': sparkline,
        'firstSeen': '2024-01-01T00:00:00',
        'lastSeen': '2024-01-15T00:00:00',
        'volume': int(np.median(sparkline[-8:])),
        'relatedQueries': ['related1', 'related2']
    }

def create_test_archive_data(date_str, topic_count=10):
    """Create test archive data for a specific date."""
    topics = []
    for i in range(topic_count):
        topics.append(create_test_topic(f"topic_{i}_{date_str}", "ai-tools", 5.0 + i))
    
    return {
        'generatedAt': f"{date_str}T12:00:00",
        'totalTopics': len(topics),
        'topics': topics
    }

def test_archive_creation():
    """Test archive creation and validation."""
    print("Testing archive creation...")
    
    # Create a temporary pipeline instance
    pipeline = TrendsDataPipeline()
    
    # Create test data
    test_topics = [create_test_topic(f"test_topic_{i}", "ai-tools", 5.0 + i) for i in range(5)]
    
    # Test saving data (this should create an archive)
    pipeline._save_data(test_topics)
    
    # Check if latest.json was created
    if os.path.exists(pipeline.latest_file):
        print("✅ latest.json created successfully")
    else:
        print("❌ latest.json not created")
        return False
    
    # Check if archive was created
    today = datetime.now().strftime('%Y-%m-%d')
    archive_path = os.path.join(pipeline.archive_dir, f"{today}.json")
    
    if os.path.exists(archive_path):
        print("✅ Archive created successfully")
        
        # Validate the archive
        if pipeline._validate_archive(archive_path):
            print("✅ Archive validation passed")
        else:
            print("❌ Archive validation failed")
            return False
    else:
        print("❌ Archive not created")
        return False
    
    return True

def test_archive_cleanup():
    """Test archive cleanup functionality."""
    print("\nTesting archive cleanup...")
    
    # Create a temporary pipeline instance
    pipeline = TrendsDataPipeline()
    
    # Create test archives for different dates
    test_dates = []
    for i in range(10):  # Create archives for 10 days
        date = datetime.now() - timedelta(days=i)
        date_str = date.strftime('%Y-%m-%d')
        test_dates.append(date_str)
        
        # Create archive file
        archive_path = os.path.join(pipeline.archive_dir, f"{date_str}.json")
        archive_data = create_test_archive_data(date_str, 5)
        
        with open(archive_path, 'w') as f:
            json.dump(archive_data, f, indent=2)
    
    print(f"Created {len(test_dates)} test archives")
    
    # Get initial statistics
    initial_stats = pipeline._get_archive_statistics()
    print(f"Initial archives: {initial_stats['total_archives']}")
    
    # Run cleanup
    pipeline._cleanup_archives()
    
    # Get final statistics
    final_stats = pipeline._get_archive_statistics()
    print(f"Final archives: {final_stats['total_archives']}")
    
    # Should have 7 or fewer archives (7-day limit)
    if final_stats['total_archives'] <= 7:
        print("✅ Archive cleanup working correctly")
        return True
    else:
        print(f"❌ Too many archives remaining: {final_stats['total_archives']}")
        return False

def test_archive_validation():
    """Test archive validation functionality."""
    print("\nTesting archive validation...")
    
    pipeline = TrendsDataPipeline()
    
    # Test valid archive
    valid_data = create_test_archive_data("2024-01-15", 5)
    valid_path = os.path.join(pipeline.archive_dir, "valid_test.json")
    
    with open(valid_path, 'w') as f:
        json.dump(valid_data, f, indent=2)
    
    if pipeline._validate_archive(valid_path):
        print("✅ Valid archive validation passed")
    else:
        print("❌ Valid archive validation failed")
    
    # Test invalid archive (missing fields)
    invalid_data = {"generatedAt": "2024-01-15T12:00:00"}  # Missing topics
    invalid_path = os.path.join(pipeline.archive_dir, "invalid_test.json")
    
    with open(invalid_path, 'w') as f:
        json.dump(invalid_data, f, indent=2)
    
    if not pipeline._validate_archive(invalid_path):
        print("✅ Invalid archive correctly rejected")
    else:
        print("❌ Invalid archive incorrectly accepted")
    
    # Test corrupted archive
    corrupted_path = os.path.join(pipeline.archive_dir, "corrupted_test.json")
    with open(corrupted_path, 'w') as f:
        f.write("invalid json content")
    
    if not pipeline._validate_archive(corrupted_path):
        print("✅ Corrupted archive correctly rejected")
    else:
        print("❌ Corrupted archive incorrectly accepted")
    
    # Clean up test files
    for path in [valid_path, invalid_path, corrupted_path]:
        if os.path.exists(path):
            os.remove(path)
    
    return True

def test_archive_statistics():
    """Test archive statistics functionality."""
    print("\nTesting archive statistics...")
    
    pipeline = TrendsDataPipeline()
    
    # Create some test archives
    test_dates = ["2024-01-10", "2024-01-11", "2024-01-12"]
    for date_str in test_dates:
        archive_path = os.path.join(pipeline.archive_dir, f"{date_str}.json")
        archive_data = create_test_archive_data(date_str, 3)
        
        with open(archive_path, 'w') as f:
            json.dump(archive_data, f, indent=2)
    
    # Get statistics
    stats = pipeline._get_archive_statistics()
    
    print(f"Archive statistics:")
    print(f"  Total archives: {stats['total_archives']}")
    print(f"  Total size: {stats['total_size_kb']}KB")
    print(f"  Oldest date: {stats['oldest_date']}")
    print(f"  Newest date: {stats['newest_date']}")
    print(f"  Files: {stats['files']}")
    
    if stats['total_archives'] == 3:
        print("✅ Archive statistics correct")
        return True
    else:
        print(f"❌ Incorrect archive count: {stats['total_archives']}")
        return False

def test_duplicate_archive_handling():
    """Test handling of duplicate archives for the same date."""
    print("\nTesting duplicate archive handling...")
    
    pipeline = TrendsDataPipeline()
    
    # Create first archive for today
    today = datetime.now().strftime('%Y-%m-%d')
    archive_path = os.path.join(pipeline.archive_dir, f"{today}.json")
    archive_data = create_test_archive_data(today, 5)
    
    with open(archive_path, 'w') as f:
        json.dump(archive_data, f, indent=2)
    
    print(f"Created first archive: {today}.json")
    
    # Try to create another archive for the same date
    test_topics = [create_test_topic(f"duplicate_topic_{i}", "ai-tools", 3.0 + i) for i in range(3)]
    
    # This should create a timestamped backup
    pipeline._save_data(test_topics)
    
    # Check if timestamped backup was created
    archive_files = [f for f in os.listdir(pipeline.archive_dir) if f.startswith(today) and f.endswith('.json')]
    
    if len(archive_files) >= 2:
        print(f"✅ Duplicate handling working: {len(archive_files)} files for {today}")
        print(f"  Files: {archive_files}")
        return True
    else:
        print(f"❌ Duplicate handling failed: {len(archive_files)} files for {today}")
        return False

def cleanup_test_archives():
    """Clean up all test archives."""
    pipeline = TrendsDataPipeline()
    
    if os.path.exists(pipeline.archive_dir):
        for filename in os.listdir(pipeline.archive_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(pipeline.archive_dir, filename)
                os.remove(filepath)
        print("Cleaned up test archives")

if __name__ == "__main__":
    try:
        # Run all tests
        test_archive_creation()
        test_archive_cleanup()
        test_archive_validation()
        test_archive_statistics()
        test_duplicate_archive_handling()
        
        print("\n🎉 All archive system tests completed!")
        
    finally:
        # Clean up test files
        cleanup_test_archives()
