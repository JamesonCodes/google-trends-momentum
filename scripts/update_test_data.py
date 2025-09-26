#!/usr/bin/env python3
"""
Simple script to update the test data for refresh testing
"""

import json
import os
from datetime import datetime

def update_test_data():
    """Update the latest.json file with new test data."""
    
    # Create new test data with current timestamp
    new_data = {
        "generatedAt": datetime.now().isoformat(),
        "totalTopics": 4,
        "topics": [
            {
                "term": f"updated_topic_{i}",
                "category": "ai-tools",
                "score": 5.0 + i,
                "percentChange": 10.0 + (i * 5),
                "sparkline": [10 + i, 20 + i, 30 + i, 40 + i, 50 + i],
                "firstSeen": "2024-01-01T00:00:00",
                "lastSeen": datetime.now().isoformat(),
                "volume": 50 + (i * 10),
                "relatedQueries": [f"related{i}_1", f"related{i}_2"]
            }
            for i in range(4)
        ]
    }
    
    # Write to latest.json
    output_file = "public/data/latest.json"
    with open(output_file, 'w') as f:
        json.dump(new_data, f, indent=2)
    
    print(f"Updated {output_file} with {len(new_data['topics'])} topics")
    print(f"Generated at: {new_data['generatedAt']}")

if __name__ == "__main__":
    update_test_data()
