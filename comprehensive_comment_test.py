#!/usr/bin/env python3
import sqlite3
import requests
import time

def comprehensive_comment_test():
    """Test comment insertion and count update"""
    
    print("=== COMPREHENSIVE COMMENT TEST ===")
    
    # Step 1: Check initial state
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    
    # Get current comment count from Post table
    cursor.execute('SELECT comments FROM Post WHERE postId = 4')
    initial_post_count = cursor.fetchone()[0]
    
    # Get current comments from Comment table
    cursor.execute('SELECT COUNT(*) FROM Comment WHERE post_id = 4')
    initial_comment_count = cursor.fetchone()[0]
    
    print(f"Initial state:")
    print(f"  Post table comment count: {initial_post_count}")
    print(f"  Actual comments in Comment table: {initial_comment_count}")
    
    conn.close()
    
    # Step 2: Test direct database insertion (to verify function works)
    print(f"\nTesting direct insertion...")
    from user import insert_comment
    
    try:
        test_comment_text = f"Direct test comment {int(time.time())}"
        print(f"Inserting comment: '{test_comment_text}'")
        insert_comment(4, 1, test_comment_text)  # post_id=4, user_id=1, comment=test_text
        print("Direct insertion successful!")
        
        # Check new state
        conn = sqlite3.connect('blog.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT comments FROM Post WHERE postId = 4')
        new_post_count = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM Comment WHERE post_id = 4')
        new_comment_count = cursor.fetchone()[0]
        
        print(f"After direct insertion:")
        print(f"  Post table comment count: {new_post_count}")
        print(f"  Actual comments in Comment table: {new_comment_count}")
        
        if new_post_count == initial_post_count + 1:
            print("✓ Comment count updated correctly!")
        else:
            print("✗ Comment count NOT updated correctly!")
        
        # Get the latest comment
        cursor.execute('SELECT text FROM Comment WHERE post_id = 4 ORDER BY commentId DESC LIMIT 1')
        latest = cursor.fetchone()
        if latest and latest[0] == test_comment_text:
            print("✓ Comment inserted correctly!")
        else:
            print("✗ Comment NOT inserted correctly!")
        
        conn.close()
        
    except Exception as e:
        print(f"Error during direct insertion: {e}")

if __name__ == "__main__":
    comprehensive_comment_test()