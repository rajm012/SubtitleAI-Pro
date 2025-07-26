"""
WSGI entry point for production deployment
"""
import os
from app import app, init_db

# Initialize the database on startup
init_db()

# This is the WSGI callable that Gunicorn will use
application = app

if __name__ == "__main__":
    # For local testing with Gunicorn
    application.run()
