# 🎬 SubtitleAI Pro - Web Application

A powerful AI-powered web application that generates English subtitles from YouTube videos and uploaded video files using advanced speech recognition technology.

![SubtitleAI Pro Banner](https://img.shields.io/badge/SubtitleAI-Pro-blue?style=for-the-badge&logo=youtube&logoColor=white)

## ✨ Features

### 🚀 **Dual Input Methods**
- **YouTube URL Processing**: Paste any YouTube URL and get instant subtitle generation
- **Video File Upload**: Upload video files directly from your device (MP4, AVI, MOV, MKV, WMV)

### 🤖 **AI-Powered Transcription**
- **Multiple Quality Levels**: Choose from Tiny, Base, Small, or Medium models
- **Multi-language Support**: Automatically converts any language to English subtitles
- **High Accuracy**: Uses OpenAI's Whisper model for professional-grade transcription

### 👥 **User Management**
- **Secure Authentication**: User registration and login system
- **Personal Dashboard**: Track all your subtitle generation jobs
- **Job History**: View and download previously generated subtitles

### ⚡ **Asynchronous Processing**
- **Background Processing**: Long videos don't block the interface
- **Real-time Status**: Live job progress tracking
- **Queue Management**: Handle multiple videos simultaneously

### 📁 **File Management**
- **SRT Format**: Industry-standard subtitle format
- **Easy Download**: One-click download of completed subtitles
- **Secure Storage**: Files processed securely with automatic cleanup

## 🛠️ Technology Stack

### Backend
- **Flask 3.1.1** - Web framework
- **SQLite** - Database for user and job management
- **faster-whisper 1.1.1** - AI transcription engine
- **pytubefix 9.4.1** - YouTube video processing

### Frontend
- **HTML5/CSS3** - Modern responsive design
- **JavaScript ES6** - Interactive user interface
- **Beautiful UI** - Gradient themes and smooth animations

### AI/ML
- **OpenAI Whisper** - Speech-to-text conversion
- **ctranslate2** - Optimized inference engine
- **ONNX Runtime** - High-performance AI model execution

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip package manager
- 500MB+ available storage for model downloads

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/rajm012/subtitleai-pro.git
   cd subtitleai-pro
   ```

2. **Create virtual environment**
   ```bash
   python -m venv subtitle_env
   # Windows
   subtitle_env\Scripts\activate
   # macOS/Linux
   source subtitle_env/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize database**
   ```bash
   python app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:3000`

## 📁 Project Structure

```
webapp/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── subtitleai.db         # SQLite database
├── templates/            # HTML templates
│   ├── base.html        # Base template
│   ├── index.html       # Landing page
│   ├── login.html       # User login
│   ├── register.html    # User registration
│   └── dashboard.html   # Main dashboard
├── static/              # Static assets
│   ├── css/            # Stylesheets
│   └── js/             # JavaScript files
├── uploads/            # Temporary file storage
└── downloads/          # Generated subtitle files
```

## 🎯 Usage

### For YouTube Videos
1. **Register/Login** to your account
2. **Navigate** to the dashboard
3. **Select** "YouTube URL" tab
4. **Paste** your YouTube video URL
5. **Choose** AI model quality (Tiny for speed, Medium for accuracy)
6. **Click** "Generate Subtitles"
7. **Monitor** progress in real-time
8. **Download** your SRT file when complete

### For Uploaded Videos
1. **Login** to your account
2. **Switch** to "Upload Video" tab
3. **Drag & drop** or select your video file
4. **Choose** AI model quality
5. **Upload** and wait for processing
6. **Download** your generated subtitles

## ⚙️ Configuration

### Model Quality Options

| Model | Speed | Accuracy | Best For |
|-------|-------|----------|----------|
| **Tiny** | ⚡ Fastest (~30s) | Good | Quick previews, short clips |
| **Base** | 🔵 Balanced (~1-2min) | Better | Most videos, balanced quality |
| **Small** | 🔸 Slower (~2-3min) | High | Important content |
| **Medium** | 🔴 Slowest (~3-5min) | Highest | Professional transcription |

### Supported File Formats
- **Video**: MP4, AVI, MOV, MKV, WMV, FLV, WebM, M4V, 3GP
- **Max Size**: 500MB per upload
- **Output**: SRT (SubRip Subtitle) format

## 🔧 Environment Variables

For production deployment, set these environment variables:

```bash
FLASK_SECRET_KEY=your-super-secret-key-here
FLASK_ENV=production  
MAX_CONTENT_LENGTH=524288000  # 500MB in bytes
```

## 🚀 Deployment

### Recommended Platforms

1. **Railway** (Recommended)
   - Easy Python deployment
   - Built-in SQLite support
   - Automatic HTTPS

2. **Render**
   - Free tier available
   - Git-based deployment
   - Automatic builds

3. **Heroku**
   - Popular platform
   - Add-on ecosystem
   - Easy scaling

### Deployment Steps (Railway)

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Connect to Railway**
   - Go to [railway.app](https://railway.app)
   - Connect your GitHub repository
   - Select the webapp directory as root

3. **Environment Setup**
   - Set `FLASK_SECRET_KEY` in Railway dashboard
   - Configure start command: `python app.py`

4. **Deploy**
   - Railway will automatically install requirements.txt
   - Your app will be live at `yourapp.railway.app`

## 🎨 Features in Detail

### 🔐 Security
- Password hashing with secure algorithms
- Session management
- File upload validation
- SQL injection protection

### 🚄 Performance
- Asynchronous job processing
- Thread-safe database operations
- Efficient file handling
- Model caching for faster inference

### 📱 User Experience
- Responsive design for all devices
- Drag-and-drop file uploads
- Real-time progress tracking
- Beautiful gradient UI

## 🐛 Troubleshooting

### Common Issues

**"Database is locked" error**
- The app uses thread-safe database operations
- Restart the application if issues persist

**Upload fails**
- Check file size (max 500MB)
- Ensure supported video format
- Verify stable internet connection

**Slow processing**
- Try Tiny or Base model for faster results
- Shorter videos process quicker
- Close other resource-intensive applications

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 Support

For support, email rajmahimaurya@gmail.com or create an issue on GitHub.

## 🙏 Acknowledgments

- OpenAI for the Whisper model
- Flask community for the excellent framework
- All contributors and users

---

**Made with ❤️ by Rajm012**

[![GitHub stars](https://img.shields.io/github/stars/rajm012/subtitleai-pro.svg)](https://github.com/rajm012/subtitleai-pro/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/rajm012/subtitleai-pro.svg)](https://github.com/rajm012/subtitleai-pro/issues)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
