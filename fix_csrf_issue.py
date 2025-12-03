#!/usr/bin/env python3
"""
Fix CSRF token issues in templates since CSRF protection is disabled
"""
import os
import re

def fix_csrf_tokens():
    """Remove CSRF token references from templates since CSRF is disabled"""
    
    templates_dir = "templates"
    templates_to_fix = []
    
    # Find all HTML files with csrf_token references
    for filename in os.listdir(templates_dir):
        if filename.endswith('.html'):
            filepath = os.path.join(templates_dir, filename)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
            if 'csrf_token()' in content:
                templates_to_fix.append(filename)
                print(f"Found CSRF token in: {filename}")
    
    print(f"\nTotal templates with CSRF tokens: {len(templates_to_fix)}")
    
    # Show what we would fix
    print("\n=== CSRF TOKEN ISSUE ANALYSIS ===")
    print("CSRF protection is disabled in application.py:")
    print("# csrf = CSRFProtect(app)")
    print("\nBut templates are still trying to use csrf_token():")
    for template in templates_to_fix:
        print(f"  - {template}")
    
    print("\n=== RECOMMENDED SOLUTION ===")
    print("1. Remove csrf_token() references from all templates")
    print("2. Or enable CSRF protection if needed")
    print("3. For now, removing from editPost.html should fix the immediate error")

if __name__ == "__main__":
    fix_csrf_tokens()