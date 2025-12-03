#!/usr/bin/env python3
import sqlite3

def check_db_structure():
    """Check database structure and comments"""
    try:
        conn = sqlite3.connect('blog.db')
        cursor = conn.cursor()
        
        # Get Comment table structure
        cursor.execute("PRAGMA table_info(Comment)")
        columns = cursor.fetchall()
        print("=== COMMENT TABLE STRUCTURE ===")
        for col in columns:
            print(f"Column: {col[1]}, Type: {col[2]}, NotNull: {col[3]}, Default: {col[4]}, PK: {col[5]}")
        
        # Get all comments using correct column names
        cursor.execute('SELECT * FROM Comment ORDER BY rowid DESC LIMIT 10')
        comments = cursor.fetchall()
        
        print("\n=== CURRENT COMMENTS IN DATABASE ===")
        if comments:
            for comment in comments:
                print(f"Comment: {comment}")
        else:
            print("No comments found in database")
        
        # Check Post table structure for comment count
        cursor.execute("PRAGMA table_info(Post)")
        post_columns = cursor.fetchall()
        print("\n=== POST TABLE STRUCTURE ===")
        for col in post_columns:
            print(f"Column: {col[1]}, Type: {col[2]}, NotNull: {col[3]}, Default: {col[4]}, PK: {col[5]}")
        
        # Check comment count for post 4
        cursor.execute('SELECT * FROM Post WHERE post_id = 4')
        result = cursor.fetchone()
        if result:
            print(f"\n=== POST 4 DATA ===")
            print(f"Post data: {result}")
        
        conn.close()
        
    except Exception as e:
        print(f"Error checking database: {e}")

if __name__ == "__main__":
    check_db_structure()