#!/usr/bin/env python3
"""
Update the timestamp in latest.json to test refresh functionality
"""

import json
from datetime import datetime, timezone

def update_timestamp():
    """Update the generatedAt timestamp in latest.json"""
    try:
        # Read current data
        with open('public/data/latest.json', 'r') as f:
            data = json.load(f)
        
        # Update timestamp (use UTC to avoid timezone issues)
        data['generatedAt'] = datetime.now(timezone.utc).isoformat()
        
        # Write back to file
        with open('public/data/latest.json', 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"✅ Updated timestamp to: {data['generatedAt']}")
        return True
        
    except Exception as e:
        print(f"❌ Error updating timestamp: {e}")
        return False

if __name__ == "__main__":
    update_timestamp()
