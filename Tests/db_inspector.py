import sqlite3
import sys

def inspect_database():
    try:
        conn = sqlite3.connect('subtitleai.db')
        c = conn.cursor()
        
        print("=== SUBTITLEAI DATABASE INSPECTION ===\n")
        
        # Check users
        c.execute('SELECT COUNT(*) FROM users')
        user_count = c.fetchone()[0]
        print(f"👥 Total Users: {user_count}")
        
        if user_count > 0:
            c.execute('SELECT username, email, created_at FROM users')
            users = c.fetchall()
            for user in users:
                print(f"   - {user[0]} ({user[1]}) - {user[2]}")
        
        print()
        
        # Check jobs
        c.execute('SELECT COUNT(*) FROM jobs')
        job_count = c.fetchone()[0]
        print(f"📋 Total Jobs: {job_count}")
        
        if job_count > 0:
            c.execute('''SELECT id, url, video_title, status, 
                                LENGTH(subtitle_content) as content_length,
                                created_at, completed_at 
                         FROM jobs ORDER BY created_at DESC''')
            jobs = c.fetchall()
            
            for job in jobs:
                job_id, url, title, status, content_len, created, completed = job
                print(f"\n🎬 Job: {job_id[:8]}...")
                print(f"   URL: {url}")
                print(f"   Title: {title or 'No title'}")
                print(f"   Status: {status}")
                print(f"   Content Length: {content_len or 0} characters")
                print(f"   Created: {created}")
                print(f"   Completed: {completed or 'Not completed'}")
                
                if status == 'completed' and content_len and content_len > 0:
                    # Show first few lines of subtitle content
                    c2 = conn.cursor()
                    c2.execute('SELECT subtitle_content FROM jobs WHERE id = ?', (job_id,))
                    content = c2.fetchone()[0]
                    if content:
                        lines = content.split('\n')[:6]  # First 6 lines
                        print(f"   Preview:")
                        for line in lines:
                            print(f"      {line}")
                        if len(content.split('\n')) > 6:
                            print(f"      ... ({len(content.split('\n'))} total lines)")
        
        conn.close()
        
    except Exception as e:
        print(f"Error inspecting database: {e}")

if __name__ == "__main__":
    inspect_database()
