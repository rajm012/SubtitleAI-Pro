"""
WSGI entry point for Render deployment
"""
import os
from app import app, init_db

# Initialize the database on startup
init_db()

# Configure for production
app.config['DEBUG'] = False
app.config['TESTING'] = False

# This is the WSGI callable that Gunicorn will use
application = app

if __name__ == "__main__":
    # For local testing
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
