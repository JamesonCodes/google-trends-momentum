#!/usr/bin/env python3
"""
Log Monitoring Utility
Provides commands to analyze and monitor pipeline logs
"""

import sys
import os
import json
import re
from datetime import datetime, timedelta
from collections import Counter, defaultdict
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def parse_log_file(log_file: str) -> list:
    """Parse log file and return structured log entries."""
    entries = []
    
    if not os.path.exists(log_file):
        return entries
    
    # Log format: timestamp - logger - level - function:line - message
    log_pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) - ([^-]+) - (\w+) - ([^:]+:\d+) - (.+)'
    
    with open(log_file, 'r') as f:
        for line in f:
            match = re.match(log_pattern, line.strip())
            if match:
                timestamp, logger, level, location, message = match.groups()
                entries.append({
                    'timestamp': timestamp,
                    'logger': logger,
                    'level': level,
                    'location': location,
                    'message': message
                })
    
    return entries

def analyze_errors(log_entries: list) -> dict:
    """Analyze error patterns in log entries."""
    errors = [entry for entry in log_entries if entry['level'] == 'ERROR']
    warnings = [entry for entry in log_entries if entry['level'] == 'WARNING']
    
    # Count error types
    error_types = Counter()
    warning_types = Counter()
    
    for error in errors:
        # Extract error type from message [TYPE] pattern
        match = re.search(r'\[([^\]]+)\]', error['message'])
        if match:
            error_types[match.group(1)] += 1
    
    for warning in warnings:
        match = re.search(r'\[([^\]]+)\]', warning['message'])
        if match:
            warning_types[match.group(1)] += 1
    
    return {
        'total_errors': len(errors),
        'total_warnings': len(warnings),
        'error_types': dict(error_types.most_common()),
        'warning_types': dict(warning_types.most_common()),
        'recent_errors': errors[-10:] if errors else [],
        'recent_warnings': warnings[-10:] if warnings else []
    }

def analyze_performance(log_entries: list) -> dict:
    """Analyze performance metrics from log entries."""
    # Look for pipeline summary entries
    summaries = [entry for entry in log_entries if 'PIPELINE EXECUTION SUMMARY' in entry['message']]
    
    # Extract metrics from log messages
    metrics = {
        'runtime': [],
        'topics_final': [],
        'api_calls': [],
        'api_errors': []
    }
    
    for entry in log_entries:
        message = entry['message']
        
        # Extract runtime
        runtime_match = re.search(r'Runtime: ([\d.]+) seconds', message)
        if runtime_match:
            metrics['runtime'].append(float(runtime_match.group(1)))
        
        # Extract final topics count
        topics_match = re.search(r'Final topics: (\d+)', message)
        if topics_match:
            metrics['topics_final'].append(int(topics_match.group(1)))
        
        # Extract API calls
        api_calls_match = re.search(r'API calls made: (\d+)', message)
        if api_calls_match:
            metrics['api_calls'].append(int(api_calls_match.group(1)))
        
        # Extract API errors
        api_errors_match = re.search(r'API errors: (\d+)', message)
        if api_errors_match:
            metrics['api_errors'].append(int(api_errors_match.group(1)))
    
    # Calculate statistics
    stats = {}
    for metric, values in metrics.items():
        if values:
            stats[metric] = {
                'count': len(values),
                'min': min(values),
                'max': max(values),
                'avg': sum(values) / len(values),
                'latest': values[-1]
            }
    
    return stats

def show_recent_activity(log_entries: list, hours: int = 24):
    """Show recent activity from the last N hours."""
    cutoff_time = datetime.now() - timedelta(hours=hours)
    
    recent_entries = []
    for entry in log_entries:
        try:
            entry_time = datetime.strptime(entry['timestamp'], '%Y-%m-%d %H:%M:%S,%f')
            if entry_time >= cutoff_time:
                recent_entries.append(entry)
        except ValueError:
            continue
    
    return recent_entries

def generate_report(log_file: str):
    """Generate a comprehensive log analysis report."""
    print(f"Log Analysis Report: {log_file}")
    print("=" * 60)
    
    # Parse log entries
    entries = parse_log_file(log_file)
    
    if not entries:
        print("No log entries found.")
        return
    
    print(f"Total log entries: {len(entries)}")
    
    # Analyze errors
    error_analysis = analyze_errors(entries)
    print(f"\nError Analysis:")
    print(f"  Total errors: {error_analysis['total_errors']}")
    print(f"  Total warnings: {error_analysis['total_warnings']}")
    
    if error_analysis['error_types']:
        print(f"  Error types:")
        for error_type, count in error_analysis['error_types'].items():
            print(f"    {error_type}: {count}")
    
    if error_analysis['warning_types']:
        print(f"  Warning types:")
        for warning_type, count in error_analysis['warning_types'].items():
            print(f"    {warning_type}: {count}")
    
    # Analyze performance
    perf_analysis = analyze_performance(entries)
    if perf_analysis:
        print(f"\nPerformance Analysis:")
        for metric, stats in perf_analysis.items():
            print(f"  {metric}:")
            print(f"    Count: {stats['count']}")
            print(f"    Latest: {stats['latest']}")
            print(f"    Average: {stats['avg']:.2f}")
            print(f"    Range: {stats['min']} - {stats['max']}")
    
    # Show recent activity
    recent = show_recent_activity(entries, 24)
    print(f"\nRecent Activity (last 24 hours): {len(recent)} entries")
    
    if recent:
        print("  Recent errors:")
        for error in recent[-5:]:
            if error['level'] == 'ERROR':
                print(f"    {error['timestamp']}: {error['message'][:100]}...")

def main():
    """Main command line interface."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Log Monitoring Utility')
    parser.add_argument('command', choices=['analyze', 'errors', 'performance', 'recent'],
                       help='Command to execute')
    parser.add_argument('--file', default='data_pipeline.log',
                       help='Log file to analyze')
    parser.add_argument('--hours', type=int, default=24,
                       help='Hours to look back for recent activity')
    
    args = parser.parse_args()
    
    if args.command == 'analyze':
        generate_report(args.file)
    elif args.command == 'errors':
        entries = parse_log_file(args.file)
        error_analysis = analyze_errors(entries)
        print("Error Summary:")
        for error_type, count in error_analysis['error_types'].items():
            print(f"  {error_type}: {count}")
    elif args.command == 'performance':
        entries = parse_log_file(args.file)
        perf_analysis = analyze_performance(entries)
        print("Performance Summary:")
        for metric, stats in perf_analysis.items():
            print(f"  {metric}: {stats['latest']} (avg: {stats['avg']:.2f})")
    elif args.command == 'recent':
        entries = parse_log_file(args.file)
        recent = show_recent_activity(entries, args.hours)
        print(f"Recent Activity (last {args.hours} hours):")
        for entry in recent[-10:]:
            print(f"  {entry['timestamp']} [{entry['level']}] {entry['message'][:80]}...")

if __name__ == "__main__":
    main()
