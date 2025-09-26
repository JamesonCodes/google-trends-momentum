#!/usr/bin/env python3
"""
Test script for the scoring algorithm
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from build_data import TrendsDataPipeline
import numpy as np

def test_scoring_algorithm():
    """Test the scoring algorithm with sample data."""
    print("Testing scoring algorithm...")
    
    # Create pipeline instance
    pipeline = TrendsDataPipeline()
    
    # Test data: different trend patterns
    test_cases = [
        {
            'name': 'Rising trend',
            'sparkline': [10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65],
            'expected_slope': 'positive'
        },
        {
            'name': 'Falling trend', 
            'sparkline': [60, 55, 50, 45, 40, 35, 30, 25, 20, 15, 10, 5],
            'expected_slope': 'negative'
        },
        {
            'name': 'Stable trend',
            'sparkline': [30, 32, 28, 31, 29, 33, 30, 32, 29, 31, 30, 32],
            'expected_slope': 'near zero'
        },
        {
            'name': 'High volatility',
            'sparkline': [10, 80, 5, 90, 2, 85, 8, 88, 3, 87, 6, 89],
            'expected_volatility': 'high'
        }
    ]
    
    for case in test_cases:
        print(f"\n--- {case['name']} ---")
        sparkline = case['sparkline']
        
        # Calculate components
        slope, percent_change, volatility = pipeline._calculate_score(sparkline)
        
        print(f"Sparkline: {sparkline}")
        print(f"Slope: {slope:.2f}")
        print(f"Percent Change: {percent_change:.2f}%")
        print(f"Volatility: {volatility:.2f}")
        
        # Verify expectations
        if 'expected_slope' in case:
            if case['expected_slope'] == 'positive' and slope > 0:
                print("✅ Slope is positive as expected")
            elif case['expected_slope'] == 'negative' and slope < 0:
                print("✅ Slope is negative as expected")
            elif case['expected_slope'] == 'near zero' and abs(slope) < 1:
                print("✅ Slope is near zero as expected")
            else:
                print(f"❌ Slope expectation not met: expected {case['expected_slope']}, got {slope}")
        
        if 'expected_volatility' in case:
            if case['expected_volatility'] == 'high' and volatility > 30:
                print("✅ High volatility detected as expected")
            else:
                print(f"❌ Volatility expectation not met: expected {case['expected_volatility']}, got {volatility}")

def test_normalization():
    """Test the normalization function."""
    print("\n--- Testing Normalization ---")
    
    pipeline = TrendsDataPipeline()
    
    # Test data
    test_values = [1, 2, 3, 4, 5, 10, 15, 20]
    normalized = pipeline._normalize_score(test_values)
    
    print(f"Original values: {test_values}")
    print(f"Normalized values: {[f'{x:.2f}' for x in normalized]}")
    
    # Check that mean is ~0 and std is ~1
    mean_norm = np.mean(normalized)
    std_norm = np.std(normalized)
    
    print(f"Normalized mean: {mean_norm:.3f} (should be ~0)")
    print(f"Normalized std: {std_norm:.3f} (should be ~1)")
    
    if abs(mean_norm) < 0.01 and abs(std_norm - 1.0) < 0.01:
        print("✅ Normalization working correctly")
    else:
        print("❌ Normalization not working correctly")

if __name__ == "__main__":
    test_scoring_algorithm()
    test_normalization()
