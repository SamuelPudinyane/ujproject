#!/usr/bin/env python3
"""
Quick admin setup script
"""
from analytics_functions import add_admin_user

# Make user ID 1 an admin (super admin level 2)
add_admin_user(user_id=1, admin_level=2, granted_by=1)
print("✅ User ID 1 is now a super admin!")

# Make user ID 2 an admin as backup
add_admin_user(user_id=2, admin_level=2, granted_by=1)
print("✅ User ID 2 is now a super admin!")

print("\nBoth users can now access the analytics dashboard at /analytics")