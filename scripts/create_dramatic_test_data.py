#!/usr/bin/env python3
"""
Create dramatic test data to show refresh is working
"""

import json
import os
from datetime import datetime

def create_dramatic_test_data():
    """Create test data with very different content."""
    
    # Create data with different topics and scores
    test_data = {
        "generatedAt": datetime.now().isoformat(),
        "totalTopics": 6,
        "topics": [
            {
                "term": "🚀 EXPLOSIVE_TOPIC_1",
                "category": "ai-tools",
                "score": 9.5,
                "percentChange": 150.0,
                "sparkline": [10, 25, 45, 70, 95, 100, 85, 90],
                "firstSeen": "2024-01-01T00:00:00",
                "lastSeen": datetime.now().isoformat(),
                "volume": 1000,
                "relatedQueries": ["AI revolution", "Machine learning boom"]
            },
            {
                "term": "🔥 TRENDING_NOW_2",
                "category": "tech",
                "score": 8.2,
                "percentChange": 200.0,
                "sparkline": [5, 15, 30, 60, 80, 95, 100, 85],
                "firstSeen": "2024-01-01T00:00:00",
                "lastSeen": datetime.now().isoformat(),
                "volume": 850,
                "relatedQueries": ["Tech innovation", "Future tech"]
            },
            {
                "term": "⚡ VIRAL_CONCEPT_3",
                "category": "business",
                "score": 7.8,
                "percentChange": 75.0,
                "sparkline": [20, 35, 50, 65, 80, 70, 85, 90],
                "firstSeen": "2024-01-01T00:00:00",
                "lastSeen": datetime.now().isoformat(),
                "volume": 650,
                "relatedQueries": ["Business growth", "Market trends"]
            },
            {
                "term": "🌟 BREAKTHROUGH_4",
                "category": "science",
                "score": 6.9,
                "percentChange": 120.0,
                "sparkline": [15, 25, 40, 55, 70, 85, 90, 95],
                "firstSeen": "2024-01-01T00:00:00",
                "lastSeen": datetime.now().isoformat(),
                "volume": 500,
                "relatedQueries": ["Scientific discovery", "Research breakthrough"]
            },
            {
                "term": "💡 INNOVATION_5",
                "category": "ai-tools",
                "score": 5.5,
                "percentChange": 80.0,
                "sparkline": [30, 40, 50, 60, 70, 75, 80, 85],
                "firstSeen": "2024-01-01T00:00:00",
                "lastSeen": datetime.now().isoformat(),
                "volume": 400,
                "relatedQueries": ["Creative solutions", "Problem solving"]
            },
            {
                "term": "🎯 FOCUS_AREA_6",
                "category": "tech",
                "score": 4.2,
                "percentChange": 45.0,
                "sparkline": [40, 45, 50, 55, 60, 65, 70, 75],
                "firstSeen": "2024-01-01T00:00:00",
                "lastSeen": datetime.now().isoformat(),
                "volume": 300,
                "relatedQueries": ["Targeted approach", "Strategic focus"]
            }
        ]
    }
    
    # Write to latest.json
    output_file = "public/data/latest.json"
    with open(output_file, 'w') as f:
        json.dump(test_data, f, indent=2)
    
    print(f"Created dramatic Rising Topics test data with {len(test_data['topics'])} topics")
    print(f"Generated at: {test_data['generatedAt']}")
    print("Topics include emojis and different categories to make changes obvious!")

if __name__ == "__main__":
    create_dramatic_test_data()
