"""
Production server startup script
Works on both Windows (waitress) and Linux (gunicorn)
"""
import os
import sys
import platform
from app import app, init_db

def start_production_server():
    """Start the production server based on the platform"""
    
    # Initialize database
    init_db()
    
    # Get port from environment
    port = int(os.environ.get('PORT', 8000))
    host = '0.0.0.0'
    
    # Check if we're on Windows or Linux
    if platform.system() == 'Windows':
        # Use waitress for Windows
        print("🚀 Starting SubtitleAI Pro with Waitress (Windows)...")
        print(f"📡 Server will run on http://{host}:{port}")
        print("🎬 Ready to process subtitle requests!")
        print("-" * 50)
        
        from waitress import serve
        serve(app, host=host, port=port, threads=4)
    else:
        # Use gunicorn for Linux (Railway)
        print("🚀 Starting SubtitleAI Pro with Gunicorn (Linux)...")
        print(f"📡 Server will run on http://{host}:{port}")
        print("🎬 Ready to process subtitle requests!")
        print("-" * 50)
        
        # Import and start gunicorn programmatically
        from gunicorn.app.base import BaseApplication
        
        class StandaloneApplication(BaseApplication):
            def __init__(self, app, options=None):
                self.options = options or {}
                self.application = app
                super().__init__()
            
            def load_config(self):
                config = {key: value for key, value in self.options.items()
                         if key in self.cfg.settings and value is not None}
                for key, value in config.items():
                    self.cfg.set(key.lower(), value)
            
            def load(self):
                return self.application
        
        options = {
            'bind': f'{host}:{port}',
            'workers': int(os.environ.get('WEB_CONCURRENCY', 1)),
            'worker_class': 'sync',
            'timeout': 120,
            'max_requests': 1000,
            'max_requests_jitter': 100,
            'accesslog': '-',
            'errorlog': '-',
            'loglevel': 'info',
            'preload_app': True
        }
        
        StandaloneApplication(app, options).run()

if __name__ == '__main__':
    start_production_server()
