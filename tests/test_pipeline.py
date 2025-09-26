#!/usr/bin/env python3
"""
Test script for the data pipeline - runs with limited data for testing
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scripts'))

from build_data import TrendsDataPipeline
import json

def test_pipeline():
    """Test the pipeline with a small subset of data."""
    print("Testing data pipeline with limited data...")
    
    # Create a test seeds file with just one category and 2 terms
    test_seeds = {
        "categories": {
            "ai-tools": {
                "weight": 1.0,
                "terms": ["chatgpt", "claude"]
            }
        },
        "globalSettings": {
            "maxTopicsPerCategory": 20,
            "minVolumeThreshold": 5,  # Lower threshold for testing
            "timeframe": "today 12-m",
            "geo": "",
            "gprop": ""
        }
    }
    
    # Save test seeds
    with open("data/test_seeds.json", "w") as f:
        json.dump(test_seeds, f, indent=2)
    
    # Run pipeline with test data
    pipeline = TrendsDataPipeline("data/test_seeds.json")
    success = pipeline.run()
    
    if success:
        print("✅ Pipeline test completed successfully!")
        
        # Check if output files were created
        if os.path.exists("public/data/latest.json"):
            with open("public/data/latest.json", "r") as f:
                data = json.load(f)
            print(f"📊 Generated {data['totalTopics']} topics")
            print(f"🕐 Generated at: {data['generatedAt']}")
        else:
            print("❌ No output file created")
    else:
        print("❌ Pipeline test failed")
    
    # Clean up test file
    if os.path.exists("data/test_seeds.json"):
        os.remove("data/test_seeds.json")

if __name__ == "__main__":
    test_pipeline()
