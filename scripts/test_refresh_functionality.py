#!/usr/bin/env python3
"""
Test script to verify refresh functionality works
"""

import json
import time
import os
from datetime import datetime

def create_test_data(version):
    """Create test data with a specific version number."""
    return {
        "generatedAt": datetime.now().isoformat(),
        "totalTopics": version,
        "topics": [
            {
                "term": f"test_topic_v{version}_{i}",
                "category": "ai-tools",
                "score": 5.0 + i,
                "percentChange": 10.0 + (i * 5),
                "sparkline": [10 + i, 20 + i, 30 + i, 40 + i, 50 + i],
                "firstSeen": "2024-01-01T00:00:00",
                "lastSeen": datetime.now().isoformat(),
                "volume": 50 + (i * 10),
                "relatedQueries": [f"related{i}_1", f"related{i}_2"]
            }
            for i in range(version)
        ]
    }

def test_refresh_functionality():
    """Test the refresh functionality by updating data multiple times."""
    
    print("Testing refresh functionality...")
    print("This will update the data file multiple times to test if the UI refreshes.")
    
    # Initial data
    data = create_test_data(2)
    with open("public/data/latest.json", 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Created initial data with {data['totalTopics']} topics")
    
    # Wait for user to test
    input("Press Enter after you've loaded the page and seen the initial data...")
    
    # Update data multiple times
    for version in [3, 4, 5, 6]:
        print(f"\nUpdating data to version {version}...")
        data = create_test_data(version)
        with open("public/data/latest.json", 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Updated data with {data['totalTopics']} topics")
        print("Now click the refresh button in the UI to see if it updates...")
        
        if version < 6:  # Don't wait on last iteration
            input("Press Enter to continue to next version...")
    
    print("\nTest complete! Check if the UI updated with each refresh.")

if __name__ == "__main__":
    test_refresh_functionality()
