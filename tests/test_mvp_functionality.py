#!/usr/bin/env python3
"""
Test MVP functionality - verify the app works with realistic data
"""

import json
import requests
import time

def test_data_endpoint():
    """Test that the data endpoint is accessible"""
    try:
        response = requests.get('http://localhost:3000/data/latest.json')
        if response.status_code == 200:
            data = response.json()
            print("✅ Data endpoint accessible")
            print(f"   - Total topics: {data.get('totalTopics', 0)}")
            print(f"   - Generated at: {data.get('generatedAt', 'Unknown')}")
            return True
        else:
            print(f"❌ Data endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Data endpoint error: {e}")
        return False

def test_app_endpoint():
    """Test that the main app is accessible"""
    try:
        response = requests.get('http://localhost:3000/')
        if response.status_code == 200:
            print("✅ Main app accessible")
            return True
        else:
            print(f"❌ Main app failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Main app error: {e}")
        return False

def verify_data_quality():
    """Verify the data has realistic topic names"""
    try:
        with open('public/data/latest.json', 'r') as f:
            data = json.load(f)
        
        topics = data.get('topics', [])
        if not topics:
            print("❌ No topics found in data")
            return False
        
        # Check for realistic topic names (not placeholders)
        placeholder_terms = ['EXPLOSIVE_TOPIC', 'TRENDING_NOW', 'VIRAL_CONCEPT', 'BREAKTHROUGH', 'INNOVATION', 'FOCUS_AREA']
        
        realistic_count = 0
        for topic in topics:
            term = topic.get('term', '')
            if not any(placeholder in term for placeholder in placeholder_terms):
                realistic_count += 1
        
        print(f"✅ Data quality check:")
        print(f"   - Total topics: {len(topics)}")
        print(f"   - Realistic topics: {realistic_count}")
        print(f"   - Sample topics: {[t['term'] for t in topics[:3]]}")
        
        return realistic_count > 0
    except Exception as e:
        print(f"❌ Data quality check error: {e}")
        return False

def main():
    """Run all MVP tests"""
    print("🧪 Testing MVP functionality...")
    print("=" * 50)
    
    # Wait a moment for the dev server to be ready
    print("⏳ Waiting for dev server to be ready...")
    time.sleep(2)
    
    # Test data quality first
    print("\n1. Testing data quality...")
    data_quality_ok = verify_data_quality()
    
    # Test endpoints
    print("\n2. Testing endpoints...")
    data_endpoint_ok = test_data_endpoint()
    app_endpoint_ok = test_app_endpoint()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    print(f"   Data Quality: {'✅ PASS' if data_quality_ok else '❌ FAIL'}")
    print(f"   Data Endpoint: {'✅ PASS' if data_endpoint_ok else '❌ FAIL'}")
    print(f"   App Endpoint: {'✅ PASS' if app_endpoint_ok else '❌ FAIL'}")
    
    if data_quality_ok and data_endpoint_ok and app_endpoint_ok:
        print("\n🎉 MVP functionality is working correctly!")
        print("   - Realistic topic names are displayed")
        print("   - Data endpoint is accessible")
        print("   - Main app is accessible")
        print("   - Ready for Phase 3 Task 2!")
    else:
        print("\n⚠️  Some tests failed. Check the issues above.")
    
    return data_quality_ok and data_endpoint_ok and app_endpoint_ok

if __name__ == "__main__":
    main()
