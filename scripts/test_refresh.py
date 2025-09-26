#!/usr/bin/env python3
"""
Test the refresh functionality by updating data and checking the response
"""

import json
import requests
import time
from datetime import datetime

def test_refresh():
    """Test the refresh functionality"""
    print("🔄 Testing refresh functionality...")
    
    # Update the timestamp first
    with open('public/data/latest.json', 'r') as f:
        data = json.load(f)
    
    old_timestamp = data['generatedAt']
    data['generatedAt'] = datetime.now().isoformat()
    
    with open('public/data/latest.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    new_timestamp = data['generatedAt']
    print(f"📝 Updated timestamp from {old_timestamp} to {new_timestamp}")
    
    # Test the API endpoint
    try:
        response = requests.get('http://localhost:3000/data/latest.json')
        if response.status_code == 200:
            api_data = response.json()
            print(f"🌐 API returned timestamp: {api_data['generatedAt']}")
            
            if api_data['generatedAt'] == new_timestamp:
                print("✅ Refresh test PASSED - API returns updated timestamp")
                return True
            else:
                print("❌ Refresh test FAILED - API returns old timestamp")
                return False
        else:
            print(f"❌ API request failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API request error: {e}")
        return False

if __name__ == "__main__":
    test_refresh()
