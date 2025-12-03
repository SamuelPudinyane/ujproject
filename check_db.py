#!/usr/bin/env python3

import sqlite3

conn = sqlite3.connect('blog.db')
cursor = conn.cursor()

# Get table names
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("Tables in database:", [table[0] for table in tables])

# Check the post table (might have a different name)
for table_name in [table[0] for table in tables]:
    if 'post' in table_name.lower():
        print(f"\nChecking table: {table_name}")
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        print("Columns:", [col[1] for col in columns])
        
        # Check for media data
        try:
            cursor.execute(f"SELECT * FROM {table_name} WHERE media IS NOT NULL LIMIT 3")
            rows = cursor.fetchall()
            if rows:
                print("Sample rows:", rows)
        except:
            pass

conn.close()