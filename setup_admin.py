#!/usr/bin/env python3
"""
Admin Setup Script
Creates admin users for accessing the analytics dashboard
"""
import sqlite3
from analytics_functions import add_admin_user

def setup_admin_users():
    """Setup initial admin users"""
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    
    # Check if any users exist
    cursor.execute("SELECT userId, first_name, last_name, email FROM User LIMIT 10")
    users = cursor.fetchall()
    
    if not users:
        print("No users found in the database. Please create some users first.")
        return
    
    print("Available users:")
    print("-" * 50)
    for user in users:
        print(f"ID: {user[0]}, Name: {user[1]} {user[2]}, Email: {user[3]}")
    
    print("\n" + "="*60)
    print("ADMIN SETUP - Grant Analytics Dashboard Access")
    print("="*60)
    
    try:
        user_id = input("\nEnter the User ID to make admin (or press Enter to make user ID 1 admin): ").strip()
        
        if not user_id:
            user_id = 1
        else:
            user_id = int(user_id)
        
        # Verify user exists
        cursor.execute("SELECT first_name, last_name, email FROM User WHERE userId = ?", (user_id,))
        user_info = cursor.fetchone()
        
        if not user_info:
            print(f"User with ID {user_id} not found!")
            return
        
        print(f"\nMaking user '{user_info[0]} {user_info[1]}' ({user_info[2]}) an admin...")
        
        # Add admin privileges
        add_admin_user(user_id, admin_level=2, granted_by=user_id)  # Level 2 = super admin
        
        print(f"✅ Successfully granted admin access to user ID {user_id}")
        print(f"   Name: {user_info[0]} {user_info[1]}")
        print(f"   Email: {user_info[2]}")
        print(f"\nThey can now access the analytics dashboard at: /analytics")
        
    except ValueError:
        print("Invalid user ID. Please enter a number.")
    except Exception as e:
        print(f"Error setting up admin: {e}")
    finally:
        conn.close()

def list_current_admins():
    """List current admin users"""
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT u.userId, u.first_name, u.last_name, u.email, a.admin_level, a.granted_date
        FROM User u
        JOIN AdminUsers a ON u.userId = a.user_id
        ORDER BY a.admin_level DESC, a.granted_date ASC
    """)
    
    admins = cursor.fetchall()
    
    if admins:
        print("\nCurrent Admin Users:")
        print("-" * 80)
        print(f"{'ID':<4} {'Name':<25} {'Email':<30} {'Level':<6} {'Since':<20}")
        print("-" * 80)
        for admin in admins:
            level_text = "Super" if admin[4] == 2 else "Basic"
            print(f"{admin[0]:<4} {admin[1]} {admin[2]:<25} {admin[3]:<30} {level_text:<6} {admin[5]:<20}")
    else:
        print("No admin users found.")
    
    conn.close()

if __name__ == "__main__":
    print("🔧 Analytics Dashboard Admin Setup")
    print("=" * 40)
    
    while True:
        print("\nOptions:")
        print("1. Setup new admin user")
        print("2. List current admin users")
        print("3. Exit")
        
        choice = input("\nSelect option (1-3): ").strip()
        
        if choice == "1":
            setup_admin_users()
        elif choice == "2":
            list_current_admins()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please select 1, 2, or 3.")