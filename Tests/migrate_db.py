#!/usr/bin/env python3
"""
Database migration script to add new columns for video upload functionality
"""

import sqlite3
import os

def migrate_database():
    db_path = 'subtitleai.db'
    
    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check current table structure
        cursor.execute("PRAGMA table_info(jobs)")
        columns = cursor.fetchall()
        print("Current jobs table structure:")
        for col in columns:
            print(f"  {col}")
        
        # Check if new columns already exist
        column_names = [col[1] for col in columns]
        
        # Add missing columns
        if 'job_type' not in column_names:
            print("\nAdding job_type column...")
            cursor.execute("ALTER TABLE jobs ADD COLUMN job_type TEXT DEFAULT 'youtube'")
            
        if 'file_path' not in column_names:
            print("Adding file_path column...")
            cursor.execute("ALTER TABLE jobs ADD COLUMN file_path TEXT")
            
        if 'file_size' not in column_names:
            print("Adding file_size column...")
            cursor.execute("ALTER TABLE jobs ADD COLUMN file_size INTEGER")
        
        # Update existing records to have job_type = 'youtube'
        cursor.execute("UPDATE jobs SET job_type = 'youtube' WHERE job_type IS NULL")
        
        conn.commit()
        print("\n✅ Database migration completed successfully!")
        
        # Show updated structure
        cursor.execute("PRAGMA table_info(jobs)")
        columns = cursor.fetchall()
        print("\nUpdated jobs table structure:")
        for col in columns:
            print(f"  {col}")
            
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_database()
