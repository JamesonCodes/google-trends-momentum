#!/usr/bin/env python3
"""
Test runner for Rising Topics
Runs all tests in the tests directory
"""

import os
import sys
import subprocess
import glob
from pathlib import Path

def run_python_tests():
    """Run all Python test files"""
    test_dir = Path(__file__).parent
    test_files = list(test_dir.glob("test_*.py"))
    
    if not test_files:
        print("❌ No test files found")
        return False
    
    print(f"🧪 Running {len(test_files)} test files...")
    print("=" * 50)
    
    all_passed = True
    
    for test_file in sorted(test_files):
        print(f"\n📋 Running {test_file.name}...")
        try:
            result = subprocess.run([sys.executable, str(test_file)], 
                                  capture_output=True, text=True, cwd=test_dir.parent)
            
            if result.returncode == 0:
                print(f"✅ {test_file.name} - PASSED")
                if result.stdout.strip():
                    print(f"   {result.stdout.strip()}")
            else:
                print(f"❌ {test_file.name} - FAILED")
                if result.stderr.strip():
                    print(f"   Error: {result.stderr.strip()}")
                if result.stdout.strip():
                    print(f"   Output: {result.stdout.strip()}")
                all_passed = False
                
        except Exception as e:
            print(f"❌ {test_file.name} - ERROR: {e}")
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All tests passed!")
    else:
        print("⚠️  Some tests failed")
    
    return all_passed

def main():
    """Main test runner"""
    print("🚀 Rising Topics Test Suite")
    print("=" * 50)
    
    # Change to project root
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    # Run tests
    success = run_python_tests()
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
