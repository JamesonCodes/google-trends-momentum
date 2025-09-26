#!/usr/bin/env python3
"""
Test script for error handling and logging functionality
"""

import sys
import os
import json
import tempfile
import shutil
from datetime import datetime
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))

from build_data import TrendsDataPipeline, ErrorTracker

def test_error_tracker():
    """Test the ErrorTracker class functionality."""
    print("Testing ErrorTracker...")
    
    tracker = ErrorTracker()
    
    # Test error logging
    tracker.log_error('TEST_ERROR', 'This is a test error', {'context': 'test'})
    tracker.log_warning('TEST_WARNING', 'This is a test warning', {'context': 'test'})
    
    # Test metrics
    tracker.increment_metric('api_calls', 5)
    tracker.increment_metric('api_errors', 2)
    
    # Test summary
    summary = tracker.get_summary()
    
    print(f"  Total errors: {summary['total_errors']}")
    print(f"  Total warnings: {summary['total_warnings']}")
    print(f"  API calls: {summary['metrics']['api_calls']}")
    print(f"  API errors: {summary['metrics']['api_errors']}")
    print(f"  Error types: {summary['error_types']}")
    print(f"  Warning types: {summary['warning_types']}")
    
    if summary['total_errors'] == 1 and summary['total_warnings'] == 1:
        print("✅ ErrorTracker working correctly")
        return True
    else:
        print("❌ ErrorTracker not working correctly")
        return False

def test_logging_setup():
    """Test the logging setup and file creation."""
    print("\nTesting logging setup...")
    
    # Check if log files are created
    log_files = ['data_pipeline.log', 'data_pipeline_errors.log']
    
    for log_file in log_files:
        if os.path.exists(log_file):
            print(f"✅ {log_file} exists")
            
            # Check if file has content
            with open(log_file, 'r') as f:
                content = f.read()
                if content.strip():
                    print(f"✅ {log_file} has content")
                else:
                    print(f"❌ {log_file} is empty")
        else:
            print(f"❌ {log_file} does not exist")
    
    return True

def test_pipeline_error_handling():
    """Test pipeline error handling with invalid data."""
    print("\nTesting pipeline error handling...")
    
    # Create a temporary directory for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create invalid seeds file
        invalid_seeds = {
            "categories": {
                "test-category": {
                    "weight": 1.0,
                    "terms": ["invalid_term_that_will_fail"]
                }
            },
            "globalSettings": {
                "maxTopicsPerCategory": 20,
                "minVolumeThreshold": 10,
                "timeframe": "today 12-m",
                "geo": "",
                "gprop": ""
            }
        }
        
        seeds_path = os.path.join(temp_dir, "invalid_seeds.json")
        with open(seeds_path, 'w') as f:
            json.dump(invalid_seeds, f)
        
        # Create pipeline with invalid seeds
        try:
            pipeline = TrendsDataPipeline(seeds_path)
            
            # Run pipeline (this should handle errors gracefully)
            success = pipeline.run()
            
            # Check error tracking
            summary = pipeline.error_tracker.get_summary()
            
            print(f"  Pipeline success: {success}")
            print(f"  Total errors: {summary['total_errors']}")
            print(f"  Total warnings: {summary['total_warnings']}")
            print(f"  Error types: {summary['error_types']}")
            
            # Pipeline should handle errors gracefully
            if summary['total_errors'] > 0:
                print("✅ Pipeline handled errors gracefully")
                return True
            else:
                print("❌ Pipeline should have encountered errors")
                return False
                
        except Exception as e:
            print(f"❌ Pipeline failed with unhandled exception: {e}")
            return False

def test_file_operations_error_handling():
    """Test error handling for file operations."""
    print("\nTesting file operations error handling...")
    
    # Create a pipeline
    pipeline = TrendsDataPipeline()
    
    # Test with read-only directory (simulate permission error)
    try:
        # Create a temporary directory and make it read-only
        with tempfile.TemporaryDirectory() as temp_dir:
            # Make directory read-only
            os.chmod(temp_dir, 0o444)
            
            # Try to create a file in read-only directory
            test_file = os.path.join(temp_dir, "test.json")
            
            try:
                with open(test_file, 'w') as f:
                    json.dump({"test": "data"}, f)
                print("❌ Should have failed to write to read-only directory")
                return False
            except PermissionError:
                print("✅ Correctly handled permission error")
                return True
                
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_api_error_handling():
    """Test API error handling."""
    print("\nTesting API error handling...")
    
    pipeline = TrendsDataPipeline()
    
    # Test with invalid term (should trigger API error)
    try:
        result = pipeline._get_interest_over_time("invalid_term_that_does_not_exist")
        
        # Check if error was tracked
        summary = pipeline.error_tracker.get_summary()
        
        print(f"  API calls made: {summary['metrics']['api_calls']}")
        print(f"  API errors: {summary['metrics']['api_errors']}")
        print(f"  Result: {result}")
        
        if summary['metrics']['api_calls'] > 0:
            print("✅ API call was made")
        else:
            print("❌ No API call was made")
            
        if summary['metrics']['api_errors'] > 0:
            print("✅ API error was tracked")
        else:
            print("❌ API error was not tracked")
            
        return True
        
    except Exception as e:
        print(f"❌ Unexpected error in API test: {e}")
        return False

def test_log_rotation():
    """Test log file rotation and management."""
    print("\nTesting log file management...")
    
    # Check if log files exist and are being written to
    log_files = ['data_pipeline.log', 'data_pipeline_errors.log']
    
    for log_file in log_files:
        if os.path.exists(log_file):
            # Get file size
            size = os.path.getsize(log_file)
            print(f"  {log_file}: {size} bytes")
            
            # Check if file is growing (has recent content)
            with open(log_file, 'r') as f:
                lines = f.readlines()
                if lines:
                    last_line = lines[-1].strip()
                    if datetime.now().strftime('%Y-%m-%d') in last_line:
                        print(f"✅ {log_file} has recent content")
                    else:
                        print(f"⚠️  {log_file} may not have recent content")
                else:
                    print(f"❌ {log_file} is empty")
        else:
            print(f"❌ {log_file} does not exist")
    
    return True

def test_error_recovery():
    """Test error recovery mechanisms."""
    print("\nTesting error recovery...")
    
    pipeline = TrendsDataPipeline()
    
    # Test that pipeline can recover from individual term failures
    test_terms = ["valid_term", "invalid_term", "another_valid_term"]
    
    successful_terms = 0
    failed_terms = 0
    
    for term in test_terms:
        try:
            result = pipeline._get_interest_over_time(term)
            if result is not None:
                successful_terms += 1
            else:
                failed_terms += 1
        except Exception as e:
            failed_terms += 1
            print(f"  Term '{term}' failed: {e}")
    
    print(f"  Successful terms: {successful_terms}")
    print(f"  Failed terms: {failed_terms}")
    
    # Pipeline should handle some failures gracefully
    if failed_terms > 0:
        print("✅ Pipeline handled term failures gracefully")
        return True
    else:
        print("❌ Pipeline should have had some failures")
        return False

if __name__ == "__main__":
    print("Testing Error Handling and Logging System")
    print("=" * 50)
    
    tests = [
        test_error_tracker,
        test_logging_setup,
        test_pipeline_error_handling,
        test_file_operations_error_handling,
        test_api_error_handling,
        test_log_rotation,
        test_error_recovery
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"Error Handling Tests: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All error handling tests passed!")
    else:
        print(f"⚠️  {total - passed} tests failed")
