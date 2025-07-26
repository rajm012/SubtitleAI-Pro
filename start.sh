#!/bin/bash

echo "🚀 Starting SubtitleAI Pro with Gunicorn..."
echo "📡 Server will run on http://localhost:8000"
echo "🎬 Ready to process subtitle requests!"
echo "-" * 50

gunicorn --config gunicorn.conf.py wsgi:application
