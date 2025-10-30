#!/usr/bin/env python3
"""
Script to remove {"success": True, "data": ...} wrappers from API responses
Keeps {"success": True, "message": ...} intact
"""

import re
import sys

def remove_success_data_wrappers(content):
    """Remove success/data wrappers from return statements"""
    
    # Pattern 1: return {"success": True, "data": [...]}
    # Replace with: return [...]
    pattern1 = r'return\s*\{\s*"success":\s*True,\s*"data":\s*(\[[\s\S]*?\])\s*\}'
    content = re.sub(pattern1, r'return \1', content)
    
    # Pattern 2: return {"success": True, "data": {...}}
    # Replace with: return {...}
    pattern2 = r'return\s*\{\s*"success":\s*True,\s*"data":\s*(\{[^}]*\})\s*\}'
    content = re.sub(pattern2, r'return \1', content)
    
    return content

if __name__ == "__main__":
    files = [
        "backend/app/routes/admin.py",
        "backend/app/routes/menu.py",
        "backend/app/routes/locations.py"
    ]
    
    for filepath in files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            new_content = remove_success_data_wrappers(content)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"✓ Processed {filepath}")
        except FileNotFoundError:
            print(f"✗ File not found: {filepath}")
        except Exception as e:
            print(f"✗ Error processing {filepath}: {e}")
