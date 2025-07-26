#!/usr/bin/env python3
"""
Test script to verify database fixes
"""

import sqlite3
import sys
import os

# Add the webapp directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_database_fixes():
    print("Testing database fixes...")
    
    # Test 1: Check if URL can be NULL
    try:
        conn = sqlite3.connect('subtitleai.db')
        cursor = conn.cursor()
        
        # Test inserting with NULL URL
        test_id = "test-null-url"
        cursor.execute('''
            INSERT OR REPLACE INTO jobs (id, user_id, url, model_size, job_type, video_title)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (test_id, 1, None, 'base', 'upload', 'Test Upload'))
        
        conn.commit()
        print("✅ NULL URL constraint test passed")
        
        # Clean up
        cursor.execute('DELETE FROM jobs WHERE id = ?', (test_id,))
        conn.commit()
        conn.close()
        
    except Exception as e:
        print(f"❌ NULL URL constraint test failed: {e}")
        return False
    
    # Test 2: Test the create_job function
    try:
        from app import create_job
        
        # Test creating upload job
        job_id = create_job(
            user_id=1,
            url=None,  # NULL URL for upload
            model_size='base',
            job_type='upload',
            file_path='/path/to/test.mp4',
            file_size=12345,
            video_title='Test Video'
        )
        
        print(f"✅ create_job function test passed, job ID: {job_id}")
        
        # Clean up
        conn = sqlite3.connect('subtitleai.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM jobs WHERE id = ?', (job_id,))
        conn.commit()
        conn.close()
        
    except Exception as e:
        print(f"❌ create_job function test failed: {e}")
        return False
    
    print("🎉 All database fixes verified successfully!")
    return True

if __name__ == "__main__":
    test_database_fixes()
