#!/usr/bin/env python3
import sqlite3

def check_comments_and_counts():
    """Check comments and post counts properly"""
    try:
        conn = sqlite3.connect('blog.db')
        cursor = conn.cursor()
        
        # Get all comments for post 4
        cursor.execute('SELECT * FROM Comment WHERE post_id = 4 ORDER BY commentId DESC')
        comments = cursor.fetchall()
        
        print("=== COMMENTS FOR POST 4 ===")
        if comments:
            for comment in comments:
                print(f"ID: {comment[0]}, User: {comment[1]}, Post: {comment[2]}, Text: '{comment[3]}', Date: {comment[4]}, Time: {comment[5]}")
        else:
            print("No comments found for post 4")
        
        actual_count = len(comments)
        print(f"Actual number of comments for post 4: {actual_count}")
        
        # Check comment count in Post table (using correct column name)
        cursor.execute('SELECT comments FROM Post WHERE postId = 4')
        result = cursor.fetchone()
        if result:
            stored_count = result[0]
            print(f"Stored comment count in Post table: {stored_count}")
            
            if actual_count != stored_count:
                print(f"MISMATCH: Actual comments ({actual_count}) != Stored count ({stored_count})")
            else:
                print("Comment counts match!")
        
        conn.close()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_comments_and_counts()