#!/usr/bin/env python3
import sqlite3

def check_comments():
    """Check comments in the database"""
    try:
        conn = sqlite3.connect('blog.db')
        cursor = conn.cursor()
        
        # Get all comments
        cursor.execute('SELECT * FROM Comment ORDER BY comment_id DESC LIMIT 10')
        comments = cursor.fetchall()
        
        print("=== CURRENT COMMENTS IN DATABASE ===")
        if comments:
            for comment in comments:
                print(f"ID: {comment[0]}, Post: {comment[1]}, User: {comment[2]}, Text: '{comment[3]}', Date: {comment[4]}, Time: {comment[5]}")
        else:
            print("No comments found in database")
        
        # Check comment count for post 4
        cursor.execute('SELECT comment FROM Post WHERE post_id = 4')
        result = cursor.fetchone()
        if result:
            print(f"\n=== COMMENT COUNT FOR POST 4 ===")
            print(f"Current comment count: {result[0]}")
        
        # Count actual comments for post 4
        cursor.execute('SELECT COUNT(*) FROM Comment WHERE post_id = 4')
        actual_count = cursor.fetchone()[0]
        print(f"Actual comments in DB for post 4: {actual_count}")
        
        conn.close()
        
    except Exception as e:
        print(f"Error checking comments: {e}")

if __name__ == "__main__":
    check_comments()