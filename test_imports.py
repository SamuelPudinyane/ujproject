#!/usr/bin/env python3

# Test if we can run the actual application imports without errors
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Testing imports...")

try:
    print("1. Testing Flask import...")
    from flask import Flask, request, session
    print("✓ Flask imported")
    
    print("2. Testing user module import...")
    from user import selectAllfromUser_with_Id
    print("✓ User module imported")
    
    print("3. Testing application import...")
    import app
    print("✓ Application imported")
    
    print("4. Testing app configuration...")
    app = app.app
    print(f"✓ App secret key exists: {bool(app.secret_key)}")
    print(f"✓ App template folder: {app.template_folder}")
    
    print("5. Testing user data retrieval...")
    user_data = selectAllfromUser_with_Id(2)
    print(f"✓ User data retrieved: {user_data['first_name']} {user_data['last_name']}")
    
    print("6. Testing route registration...")
    routes = [rule.rule for rule in app.url_map.iter_rules()]
    selectedUserProfile_routes = [r for r in routes if 'selectedUserProfile' in r]
    print(f"✓ selectedUserProfile routes found: {selectedUserProfile_routes}")
    
    print("\n✅ All imports successful! The issue might be runtime-specific.")
    
except Exception as e:
    print(f"❌ Import error: {e}")
    import traceback
    traceback.print_exc()