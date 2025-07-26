from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash, send_file
from flask_cors import CORS
import sqlite3
import hashlib
import uuid
import threading
import os
import time
import sys
from datetime import datetime
import io
import zipfile
from werkzeug.utils import secure_filename

# DEBUG: Added enhanced error logging for upload debugging
# Database connection lock to prevent concurrent access issues
db_lock = threading.Lock()

# Add parent directory to Python path to import gen.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import your existing functions
from gen import download_audio, transcribe_audio, clean_youtube_url
from pytubefix import YouTube

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-this-in-production')
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
CORS(app)

# Allowed video extensions
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv', 'wmv', 'flv', 'webm', 'm4v', '3gp'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Create upload directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Database setup
def init_db():
    conn = sqlite3.connect('subtitleai.db')
    c = conn.cursor()
    
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE NOT NULL,
                  email TEXT UNIQUE NOT NULL,
                  password_hash TEXT NOT NULL,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    # Jobs table
    c.execute('''CREATE TABLE IF NOT EXISTS jobs
                 (id TEXT PRIMARY KEY,
                  user_id INTEGER NOT NULL,
                  url TEXT,
                  video_title TEXT,
                  model_size TEXT DEFAULT 'base',
                  status TEXT DEFAULT 'pending',
                  progress TEXT,
                  subtitle_content TEXT,
                  error_message TEXT,
                  job_type TEXT DEFAULT 'youtube',
                  file_path TEXT,
                  file_size INTEGER,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  completed_at TIMESTAMP,
                  FOREIGN KEY (user_id) REFERENCES users (id))''')
    
    conn.commit()
    conn.close()

# Helper functions
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def get_user_by_username(username):
    conn = sqlite3.connect('subtitleai.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = c.fetchone()
    conn.close()
    return user

def create_user(username, email, password):
    conn = sqlite3.connect('subtitleai.db')
    c = conn.cursor()
    try:
        password_hash = hash_password(password)
        c.execute('INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
                  (username, email, password_hash))
        conn.commit()
        user_id = c.lastrowid
        conn.close()
        return user_id
    except sqlite3.IntegrityError:
        conn.close()
        return None

def get_user_jobs(user_id):
    with db_lock:  # Use thread lock to prevent database locking
        conn = sqlite3.connect('subtitleai.db', timeout=10.0)  # Add timeout
        c = conn.cursor()
        c.execute('''SELECT id, user_id, url, video_title, model_size, status, progress,
                            subtitle_content, error_message, job_type, file_path, file_size,
                            created_at, completed_at FROM jobs 
                     WHERE user_id = ? ORDER BY created_at DESC''', (user_id,))
        jobs = c.fetchall()
        conn.close()
        return jobs

def create_job(user_id, url=None, model_size='base', job_type='youtube', file_path=None, file_size=None, video_title=None):
    job_id = str(uuid.uuid4())
    
    with db_lock:  # Use thread lock to prevent database locking
        conn = sqlite3.connect('subtitleai.db', timeout=10.0)  # Add timeout
        c = conn.cursor()
        
        try:
            if job_type == 'upload':
                c.execute('''INSERT INTO jobs (id, user_id, url, model_size, status, progress, job_type, file_path, file_size, video_title) 
                             VALUES (?, ?, ?, ?, 'pending', 'Queued for processing', ?, ?, ?, ?)''',
                          (job_id, user_id, url, model_size, job_type, file_path, file_size, video_title))
            else:
                c.execute('''INSERT INTO jobs (id, user_id, url, model_size, status, progress, job_type) 
                             VALUES (?, ?, ?, ?, 'pending', 'Queued for processing', ?)''',
                          (job_id, user_id, url, model_size, job_type))
            
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    return job_id

def update_job_status(job_id, status, progress=None, video_title=None, subtitle_content=None, error_message=None):
    with db_lock:  # Use thread lock to prevent database locking
        conn = sqlite3.connect('subtitleai.db', timeout=10.0)  # Add timeout
        c = conn.cursor()
        
        try:
            if status == 'completed':
                print(f"DEBUG: Completing job {job_id}, subtitle_content length: {len(subtitle_content) if subtitle_content else 0}")
                c.execute('''UPDATE jobs SET status = ?, progress = ?, video_title = ?, 
                                          subtitle_content = ?, completed_at = CURRENT_TIMESTAMP 
                             WHERE id = ?''',
                          (status, progress, video_title, subtitle_content, job_id))
            elif status == 'failed':
                c.execute('''UPDATE jobs SET status = ?, progress = ?, error_message = ?, 
                                          completed_at = CURRENT_TIMESTAMP 
                             WHERE id = ?''',
                          (status, progress, error_message, job_id))
            else:
                c.execute('UPDATE jobs SET status = ?, progress = ? WHERE id = ?',
                          (status, progress, job_id))
            
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

def get_job(job_id):
    conn = sqlite3.connect('subtitleai.db')
    c = conn.cursor()
    c.execute('SELECT * FROM jobs WHERE id = ?', (job_id,))
    job = c.fetchone()
    conn.close()
    return job

# Background job processing
def process_subtitle_job(job_id, url=None, model_size='base', job_type='youtube', file_path=None):
    try:
        print(f"🎬 Processing {job_type} job {job_id}")
        
        if job_type == 'upload':
            print(f"🎬 Processing uploaded video: {file_path}")
            update_job_status(job_id, 'processing', 'Processing uploaded video...')
            
            # Get video title from filename
            video_title = os.path.splitext(os.path.basename(file_path))[0]
            video_title = "".join(c for c in video_title if c.isalnum() or c in (' ', '-', '_')).rstrip()
            
            update_job_status(job_id, 'processing', 'Generating subtitles with AI...', video_title)
            
            # Transcribe the uploaded video directly
            subtitles = transcribe_audio(file_path, model_size)
            
            if not subtitles:
                update_job_status(job_id, 'failed', 'Failed to generate subtitles', error_message='No subtitles generated')
                return
            
            # Generate SRT content
            srt_content = ""
            for i, sub in enumerate(subtitles, 1):
                start_time = seconds_to_srt_time(sub["start"])
                end_time = seconds_to_srt_time(sub["end"])
                srt_content += f"{i}\n{start_time} --> {end_time}\n{sub['text']}\n\n"
            
            # Clean up uploaded file after processing
            try:
                os.remove(file_path)
                print(f"🗑️ Cleaned up uploaded file: {file_path}")
            except Exception as e:
                print(f"Warning: Could not remove uploaded file: {e}")
            
            update_job_status(job_id, 'completed', f'✅ Generated {len(subtitles)} subtitle segments', 
                             video_title, srt_content)
            
            print(f"✅ Upload job {job_id} completed successfully!")
            
        else:
            # Original YouTube processing logic
            print(f"🎬 Processing YouTube job {job_id}: {url}")
            update_job_status(job_id, 'processing', 'Getting video information...')
            
            # Get video title
            try:
                yt = YouTube(clean_youtube_url(url))
                video_title = yt.title
                video_title = "".join(c for c in video_title if c.isalnum() or c in (' ', '-', '_')).rstrip()
            except Exception as e:
                video_title = "YouTube Video"
                print(f"Warning: Could not get video title: {e}")
            
            update_job_status(job_id, 'processing', 'Downloading audio...', video_title)
            
            # Download audio
            audio_path = download_audio(url)
            print(f"✅ Audio downloaded: {audio_path}")
            
            update_job_status(job_id, 'processing', 'Generating subtitles with AI...')
            
            # Generate subtitles
            subtitles = transcribe_audio(audio_path, model_size)
            
            if not subtitles:
                update_job_status(job_id, 'failed', 'Failed to generate subtitles', error_message='No subtitles generated')
                return
            
            # Generate SRT content
            srt_content = ""
            for i, sub in enumerate(subtitles, 1):
                start_time = seconds_to_srt_time(sub["start"])
                end_time = seconds_to_srt_time(sub["end"])
                srt_content += f"{i}\n{start_time} --> {end_time}\n{sub['text']}\n\n"
            
            # Clean up audio file
            try:
                os.remove(audio_path)
                print(f"🗑️ Cleaned up: {audio_path}")
            except Exception as e:
                print(f"Warning: Could not remove temp file: {e}")
            
            update_job_status(job_id, 'completed', f'✅ Generated {len(subtitles)} subtitle segments', 
                             video_title, srt_content)
            
            print(f"✅ YouTube job {job_id} completed successfully!")
        
    except Exception as e:
        print(f"❌ Job {job_id} failed: {str(e)}")
        update_job_status(job_id, 'failed', f'❌ Error: {str(e)}', error_message=str(e))

def seconds_to_srt_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{milliseconds:03}"

# Routes
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        email = request.form['email'].strip()
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if not username or not email or not password:
            flash('All fields are required!', 'error')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long!', 'error')
            return render_template('register.html')
        
        user_id = create_user(username, email, password)
        if user_id:
            session['user_id'] = user_id
            session['username'] = username
            flash('Account created successfully!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Username or email already exists!', 'error')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        
        user = get_user_by_username(username)
        if user and user[3] == hash_password(password):  # user[3] is password_hash
            session['user_id'] = user[0]  # user[0] is id
            session['username'] = user[1]  # user[1] is username
            flash('Logged in successfully!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password!', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    jobs = get_user_jobs(session['user_id'])
    return render_template('dashboard.html', jobs=jobs, username=session['username'])

@app.route('/submit-job', methods=['POST'])
def submit_job():
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not authenticated'}), 401
    
    data = request.get_json()
    url = data.get('url', '').strip()
    model_size = data.get('model_size', 'base')
    
    if not url:
        return jsonify({'success': False, 'error': 'URL is required'}), 400
    
    if 'youtube.com' not in url and 'youtu.be' not in url:
        return jsonify({'success': False, 'error': 'Please provide a valid YouTube URL'}), 400
    
    # Create job
    job_id = create_job(session['user_id'], url, model_size, 'youtube')
    
    # Start background processing
    thread = threading.Thread(target=process_subtitle_job, args=(job_id, url, model_size, 'youtube'))
    thread.daemon = True
    thread.start()
    
    return jsonify({'success': True, 'job_id': job_id})

@app.route('/submit-upload', methods=['POST'])
def submit_upload():
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not authenticated'}), 401
    
    if 'video_file' not in request.files:
        return jsonify({'success': False, 'error': 'No file uploaded'}), 400
    
    file = request.files['video_file']
    model_size = request.form.get('model_size', 'base')
    
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'success': False, 'error': 'Invalid file type. Please upload a video file (mp4, avi, mov, etc.)'}), 400
    
    try:
        # Secure the filename and save
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        
        # Ensure upload folder exists
        upload_folder = app.config['UPLOAD_FOLDER']
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder, exist_ok=True)
        
        file.save(file_path)
        file_size = os.path.getsize(file_path)
        
        # Get video title from filename
        video_title = os.path.splitext(filename)[0]
        
        # Create job
        job_id = create_job(session['user_id'], None, model_size, 'upload', 
                           file_path, file_size, video_title)
        
        # Start background processing
        thread = threading.Thread(target=process_subtitle_job, 
                                args=(job_id, None, model_size, 'upload', file_path))
        thread.daemon = True
        thread.start()
        
        return jsonify({'success': True, 'job_id': job_id, 'filename': filename})
        
    except Exception as e:
        return jsonify({'success': False, 'error': f'Upload failed: {str(e)}'}), 500

@app.route('/job-status/<job_id>')
def job_status(job_id):
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not authenticated'}), 401
    
    job = get_job(job_id)
    if not job or job[1] != session['user_id']:  # job[1] is user_id
        return jsonify({'success': False, 'error': 'Job not found'}), 404
    
    return jsonify({
        'success': True,
        'status': job[5],  # status
        'progress': job[6],  # progress
        'video_title': job[3],  # video_title
        'created_at': job[9],  # created_at
        'completed_at': job[10]  # completed_at
    })

@app.route('/download/<job_id>')
def download_subtitle(job_id):
    if 'user_id' not in session:
        flash('Please log in to download subtitles.', 'error')
        return redirect(url_for('login'))
    
    job = get_job(job_id)
    if not job or job[1] != session['user_id']:  # job[1] is user_id
        flash('Subtitle file not found.', 'error')
        return redirect(url_for('dashboard'))
    
    print(f"DEBUG: Job details - Status: {job[5]}, Content length: {len(job[7]) if job[7] else 0}")
    print(f"DEBUG: Job fields - ID: {job[0]}, User: {job[1]}, Title: {job[3]}")
    
    if job[5] != 'completed':  # job[5] is status
        flash('Subtitle is not ready for download yet. Please wait for processing to complete.', 'error')
        return redirect(url_for('dashboard'))
    
    if not job[7]:  # job[7] is subtitle_content
        flash('Subtitle content is empty. Please try regenerating the subtitles.', 'error')
        return redirect(url_for('dashboard'))
    
    # Create file-like object
    subtitle_bytes = io.BytesIO(job[7].encode('utf-8'))
    subtitle_bytes.seek(0)
    
    filename = f"{job[3] or 'youtube_video'}_subtitles.srt"  # job[3] is video_title
    filename = "".join(c for c in filename if c.isalnum() or c in (' ', '-', '_', '.')).rstrip()
    
    print(f"DEBUG: Serving file: {filename}, Size: {len(job[7])} chars")
    
    return send_file(subtitle_bytes, 
                     as_attachment=True, 
                     download_name=filename,
                     mimetype='text/plain')

# Debug route to test database access
@app.route('/debug-job/<job_id>')
def debug_job(job_id):
    if 'user_id' not in session:
        return "Not logged in"
    
    job = get_job(job_id)
    if not job:
        return f"Job {job_id} not found"
    
    return f"""
    <h2>Job Debug Info</h2>
    <p><strong>Job ID:</strong> {job[0]}</p>
    <p><strong>User ID:</strong> {job[1]} (Session: {session['user_id']})</p>
    <p><strong>URL:</strong> {job[2]}</p>
    <p><strong>Video Title:</strong> {job[3]}</p>
    <p><strong>Model Size:</strong> {job[4]}</p>
    <p><strong>Status:</strong> {job[5]}</p>
    <p><strong>Progress:</strong> {job[6]}</p>
    <p><strong>Content Length:</strong> {len(job[7]) if job[7] else 0} chars</p>
    <p><strong>Content Preview:</strong></p>
    <pre>{job[7][:500] if job[7] else 'No content'}...</pre>
    """


init_db()

if __name__ == '__main__':
    init_db()
    print("🚀 Starting SubtitleAI Pro Web Application...")
    print("📡 Server will run on http://localhost:3000")
    print("🎬 Ready to process subtitle requests!")
    print("-" * 50)
    
    # Get port from environment variable for Railway deployment
    port = int(os.environ.get('PORT', 3000))
    
    app.run(host='0.0.0.0', port=port, debug=False)
