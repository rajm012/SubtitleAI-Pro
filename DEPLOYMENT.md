# SubtitleAI Pro - Railway Deployment Guide

This guide will help you deploy your SubtitleAI Pro application to Railway.

## 🚀 Quick Deploy to Railway

1. **Push your code to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit for Railway deployment"
   git branch -M main
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Deploy to Railway:**
   - Go to [Railway.app](https://railway.app)
   - Sign in with your GitHub account
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your SubtitleAI Pro repository
   - Railway will automatically detect and deploy your app!

## 🔧 Configuration Files Included

Your app is now production-ready with these files:

- **`server.py`** - Cross-platform production server (Waitress for Windows, Gunicorn for Linux)
- **`wsgi.py`** - WSGI entry point for traditional deployments
- **`Procfile`** - Railway/Heroku process definition
- **`railway.json`** - Railway-specific configuration
- **`runtime.txt`** - Python version specification
- **`requirements.txt`** - Updated with production dependencies
- **`.gitignore`** - Excludes unnecessary files from deployment

## 🔒 Environment Variables

Set these environment variables in Railway:

1. **`SECRET_KEY`** (Required):
   ```
   Generate a secure secret key for production
   ```

2. **`PORT`** (Automatic):
   ```
   Railway automatically sets this
   ```

3. **`WEB_CONCURRENCY`** (Optional):
   ```
   Number of worker processes (default: 1)
   ```

## 📝 Database Considerations

**Current Setup:**
- Uses SQLite database (`subtitleai.db`)
- Works for small to medium applications
- Database file is stored locally

**For High Traffic:**
Consider upgrading to PostgreSQL:
1. Add Railway PostgreSQL plugin
2. Update database connection in `app.py`
3. Use environment variables for database URL

## 🧪 Local Testing

Test your production setup locally:

**Windows:**
```cmd
start.bat
```

**Unix/Linux:**
```bash
python server.py
```

Your app will run on http://localhost:8000

## 📊 Performance Features

- **Waitress** for Windows development
- **Gunicorn** for Linux production
- Auto-scaling based on CPU usage
- Request timeout: 120 seconds
- Worker restart after 1000 requests
- Proper error logging

## 🔍 Monitoring

Check your app status:
- Railway Dashboard: Real-time logs and metrics
- Health Check: Available at your app URL
- Error Tracking: All errors logged to Railway console

## 🚨 Important Notes

1. **File Uploads:** 500MB max size limit
2. **Processing Time:** Long audio files may take time to process
3. **Memory Usage:** Monitor RAM usage for large files
4. **Storage:** Uploaded files are stored temporarily

## 🐛 Troubleshooting

**Common Issues:**

1. **Build Fails:**
   - Check `requirements.txt` formatting
   - Ensure all dependencies are compatible

2. **App Won't Start:**
   - Check Railway logs for errors
   - Verify environment variables

3. **Database Issues:**
   - Ensure SQLite file permissions
   - Check database initialization

## 📞 Support

If you encounter issues:
1. Check Railway logs
2. Review this deployment guide
3. Test locally first

Happy deploying! 🎉
