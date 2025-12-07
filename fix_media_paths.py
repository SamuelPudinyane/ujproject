#!/usr/bin/env python3

import sqlite3
import os

def update_media_paths():
    # Check what files actually exist
    uploads_dir = "static/uploads"
    actual_files = []
    
    if os.path.exists(uploads_dir):
        actual_files = os.listdir(uploads_dir)
        print(f"Files in uploads directory: {actual_files}")
    
    # Connect to database
    try:
        conn = sqlite3.connect('blog.db')
        cursor = conn.cursor()
        
        # Get all posts with media
        cursor.execute("SELECT postId, media FROM \"Post\" WHERE media IS NOT NULL AND media != ''")
        posts = cursor.fetchall()
        
        print(f"Found {len(posts)} posts with media")
        
        for post_id, media_string in posts:
            print(f"Post {post_id}: {media_string}")
            
            # Check if it's the problematic video file
            if "NAO robot drives autonomously it's own car.mp4" in media_string:
                # Replace with the actual filename
                new_media_string = media_string.replace(
                    "NAO robot drives autonomously it's own car.mp4",
                    "Energy Harvesting from Electromagnetic Signals - Rectenna.mp4"
                )
                
                # Update the database
                cursor.execute("UPDATE \"Post\" SET media = ? WHERE postId = ?", (new_media_string, post_id))
                print(f"Updated post {post_id} media to: {new_media_string}")
        
        conn.commit()
        print("Database updated successfully!")
        
    except Exception as e:
        print(f"Error updating database: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    update_media_paths()