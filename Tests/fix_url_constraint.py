#!/usr/bin/env python3
"""
Database migration script to fix URL constraint for upload functionality
"""

import sqlite3
import os

def fix_url_constraint():
    db_path = 'subtitleai.db'
    
    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        print("Fixing URL constraint to allow NULL values for upload jobs...")
        
        # Get current table structure
        cursor.execute("PRAGMA table_info(jobs)")
        columns = cursor.fetchall()
        print("\nCurrent table structure:")
        for col in columns:
            print(f"  {col}")
        
        # SQLite doesn't support modifying column constraints directly
        # We need to recreate the table
        
        # Step 1: Create new table with correct constraints
        cursor.execute('''
            CREATE TABLE jobs_new (
                id TEXT PRIMARY KEY,
                user_id INTEGER NOT NULL,
                url TEXT,  -- Allow NULL for upload jobs
                video_title TEXT,
                model_size TEXT DEFAULT 'base',
                status TEXT DEFAULT 'pending',
                progress TEXT,
                subtitle_content TEXT,
                error_message TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP,
                job_type TEXT DEFAULT 'youtube',
                file_path TEXT,
                file_size INTEGER,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Step 2: Copy data from old table to new table
        cursor.execute('''
            INSERT INTO jobs_new (id, user_id, url, video_title, model_size, status, 
                                 progress, subtitle_content, error_message, created_at, 
                                 completed_at, job_type, file_path, file_size)
            SELECT id, user_id, url, video_title, model_size, status, 
                   progress, subtitle_content, error_message, created_at, 
                   completed_at, job_type, file_path, file_size
            FROM jobs
        ''')
        
        # Step 3: Drop old table
        cursor.execute('DROP TABLE jobs')
        
        # Step 4: Rename new table
        cursor.execute('ALTER TABLE jobs_new RENAME TO jobs')
        
        conn.commit()
        print("\n✅ URL constraint fixed successfully!")
        
        # Show updated structure
        cursor.execute("PRAGMA table_info(jobs)")
        columns = cursor.fetchall()
        print("\nUpdated table structure:")
        for col in columns:
            print(f"  {col}")
            
        # Test insert with NULL URL
        test_id = "test-upload-job"
        cursor.execute('''
            INSERT OR REPLACE INTO jobs (id, user_id, url, model_size, job_type, video_title)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (test_id, 1, None, 'base', 'upload', 'Test Upload'))
        
        print(f"\n✅ Test insert with NULL URL successful!")
        
        # Clean up test record
        cursor.execute('DELETE FROM jobs WHERE id = ?', (test_id,))
        conn.commit()
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    fix_url_constraint()
