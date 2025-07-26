#!/usr/bin/env python3
"""
Quick test to verify database schema is working
"""

import sqlite3

def test_database():
    try:
        conn = sqlite3.connect('subtitleai.db')
        cursor = conn.cursor()
        
        # Test the updated query
        cursor.execute('''SELECT id, user_id, url, video_title, model_size, status, progress,
                         subtitle_content, error_message, created_at, completed_at, job_type, file_path, file_size
                         FROM jobs LIMIT 5''')
        
        results = cursor.fetchall()
        print("✅ Database query successful!")
        print(f"Found {len(results)} jobs in database")
        
        if results:
            print("\nSample job structure:")
            for i, job in enumerate(results[:2]):  # Show first 2 jobs
                print(f"Job {i+1}: {len(job)} fields")
                field_names = ['id', 'user_id', 'url', 'video_title', 'model_size', 'status', 'progress',
                              'subtitle_content', 'error_message', 'created_at', 'completed_at', 'job_type', 'file_path', 'file_size']
                for j, field in enumerate(field_names):
                    print(f"  {j}: {field} = {job[j]}")
                print()
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

if __name__ == "__main__":
    test_database()
