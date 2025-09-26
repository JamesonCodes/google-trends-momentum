#!/usr/bin/env python3
"""
Archive Management Utility
Provides commands to manage and inspect the archive system
"""

import sys
import os
import json
import argparse
from datetime import datetime, timedelta
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from build_data import TrendsDataPipeline

def list_archives():
    """List all archives with details."""
    pipeline = TrendsDataPipeline()
    stats = pipeline._get_archive_statistics()
    
    if 'error' in stats:
        print(f"Error getting archive statistics: {stats['error']}")
        return
    
    print(f"Archive System Status:")
    print(f"  Total archives: {stats['total_archives']}")
    print(f"  Total size: {stats['total_size_kb']}KB")
    print(f"  Date range: {stats['oldest_date']} to {stats['newest_date']}")
    print()
    
    if stats.get('files'):
        print("Archive files:")
        for filename in sorted(stats['files']):
            filepath = os.path.join(pipeline.archive_dir, filename)
            if os.path.exists(filepath):
                file_size = os.path.getsize(filepath)
                file_date = os.path.getmtime(filepath)
                date_str = datetime.fromtimestamp(file_date).strftime('%Y-%m-%d %H:%M:%S')
                print(f"  {filename:<25} {file_size:>8} bytes  {date_str}")
    else:
        print("No archives found.")

def validate_archives():
    """Validate all archives for integrity."""
    pipeline = TrendsDataPipeline()
    
    if not os.path.exists(pipeline.archive_dir):
        print("No archive directory found.")
        return
    
    valid_count = 0
    invalid_count = 0
    
    for filename in os.listdir(pipeline.archive_dir):
        if filename.endswith('.json') and filename != 'latest.json':
            filepath = os.path.join(pipeline.archive_dir, filename)
            
            if pipeline._validate_archive(filepath):
                print(f"✅ {filename}")
                valid_count += 1
            else:
                print(f"❌ {filename}")
                invalid_count += 1
    
    print(f"\nValidation complete: {valid_count} valid, {invalid_count} invalid")

def cleanup_archives():
    """Manually trigger archive cleanup."""
    pipeline = TrendsDataPipeline()
    
    print("Running archive cleanup...")
    pipeline._cleanup_archives()
    
    stats = pipeline._get_archive_statistics()
    if 'error' not in stats:
        print(f"Cleanup complete: {stats['total_archives']} archives remaining")

def show_archive_details(filename):
    """Show detailed information about a specific archive."""
    pipeline = TrendsDataPipeline()
    filepath = os.path.join(pipeline.archive_dir, filename)
    
    if not os.path.exists(filepath):
        print(f"Archive file not found: {filename}")
        return
    
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        print(f"Archive Details: {filename}")
        print(f"  Generated: {data.get('generatedAt', 'Unknown')}")
        print(f"  Total topics: {data.get('totalTopics', 0)}")
        
        if 'topics' in data and data['topics']:
            topics = data['topics']
            print(f"  Sample topics:")
            for i, topic in enumerate(topics[:5]):  # Show first 5 topics
                print(f"    {i+1}. {topic.get('term', 'Unknown')} (score: {topic.get('score', 0):.2f})")
            
            if len(topics) > 5:
                print(f"    ... and {len(topics) - 5} more")
        
        # File size
        file_size = os.path.getsize(filepath)
        print(f"  File size: {file_size} bytes ({file_size / 1024:.1f}KB)")
        
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error reading archive: {e}")

def main():
    """Main command line interface."""
    parser = argparse.ArgumentParser(description='Archive Management Utility')
    parser.add_argument('command', choices=['list', 'validate', 'cleanup', 'show'],
                       help='Command to execute')
    parser.add_argument('--file', help='Archive filename for show command')
    
    args = parser.parse_args()
    
    if args.command == 'list':
        list_archives()
    elif args.command == 'validate':
        validate_archives()
    elif args.command == 'cleanup':
        cleanup_archives()
    elif args.command == 'show':
        if not args.file:
            print("Error: --file required for show command")
            sys.exit(1)
        show_archive_details(args.file)

if __name__ == "__main__":
    main()
