# 🎬 SubtitleAI Pro

An AI-powered web application that automatically generates English subtitles from YouTube videos using OpenAI's Whisper model.

## ⚠️ **Important: Deployment Challenges & YouTube Bot Detection**

### 🚫 **Why This App Is Not Deployed**

This application faces significant challenges when deployed to cloud platforms due to **YouTube's aggressive bot detection system**. When hosted on popular platforms, YouTube blocks video access, making the app non-functional for online deployment.

### 🛡️ **YouTube Bot Detection Issues**

When deployed on cloud platforms, you'll encounter:
- ❌ **"Video unavailable"** errors
- ❌ **"This content is not available"** messages  
- ❌ **HTTP 403 Forbidden** responses
- ❌ **Age restriction** blocks even for public videos
- ❌ **Geo-blocking** for all regions

**Root Cause**: YouTube actively blocks known cloud platform IP ranges and data center addresses to prevent automated content extraction.

## � **Potential Solutions (Advanced Users)**

### **1. 🌐 Use Alternative Hosting Providers**
Instead of commonly blocked platforms, try:
- **Netlify** - Static site hosting with serverless functions
- **Railway** - Container hosting with rotating IPs  
- **Vercel** - Edge functions with global distribution
- **Render** - Docker deployments with better IP reputation
- **DigitalOcean** - VPS with custom IP configuration
- **Linode** - Cloud instances with dedicated IPs
- **Vultr** - High-frequency compute with clean IP ranges

### **2. 🔒 Proxy & VPN Solutions**
- **Residential Proxies** (Paid):
  - Bright Data
  - Oxylabs  
  - Smartproxy
  - ProxyMesh
- **Rotating IP Services**:
  - ProxyRotator
  - Storm Proxies
  - MyPrivateProxy
- **VPN Integration**:
  - NordVPN API
  - ExpressVPN
  - Surfshark

### **3. 🏗️ Infrastructure Solutions**
- **Custom VPS Setup**: Deploy on personal VPS with clean IP
- **Residential Internet**: Host on home server with residential IP
- **CDN Integration**: Use Cloudflare or AWS CloudFront
- **Load Balancers**: Distribute requests across multiple IPs
- **IP Rotation**: Implement automatic IP switching

### **4. 🔄 Alternative Approaches**
- **Client-Side Processing**: Download on user's machine
- **Third-Party APIs**: Use external YouTube download services
- **Hybrid Model**: Combine local download + cloud processing
- **Browser Extensions**: Process videos in user's browser

## � **Recommended Usage: Run Locally**

### **Why Local Deployment Works Best:**
✅ **No IP Blocking**: Your home IP is trusted by YouTube  
✅ **Full Functionality**: All features work without restrictions  
✅ **Better Performance**: Direct access without proxy overhead  
✅ **Cost Effective**: No hosting or proxy fees  
✅ **Privacy**: Videos processed locally, not on cloud servers  

## 🚀 **Quick Start (Local Setup)**

### **Prerequisites**
- Python 3.8 or higher
- 4GB+ RAM (for Whisper AI model)
- Internet connection

### **Installation**

1. **Clone the repository**
   ```bash
   git clone https://github.com/rajm012/SubtitleAI-Pro.git
   cd SubtitleAI-Pro
   ```

2. **Create virtual environment**
   ```bash
   python -m venv sub
   # Windows
   sub\Scripts\activate
   # Linux/Mac
   source sub/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the app**
   ```
   Open: http://localhost:3000
   ```

## 🎯 **Features**

- 🎬 **YouTube Video Processing**: Extract audio from YouTube videos
- 🤖 **AI Transcription**: Uses OpenAI Whisper for accurate speech-to-text
- 📝 **SRT Generation**: Creates industry-standard subtitle files
- 👤 **User Management**: Registration and login system
- 📊 **Job Tracking**: Monitor processing status and history
- ⚡ **Multiple Models**: Choose from Tiny, Base, Small, Medium quality
- 📁 **File Upload**: Support for video/audio file uploads
- 💾 **Download**: Get completed subtitles as .srt files

## 🛠️ **Technology Stack**

- **Backend**: Flask (Python)
- **AI Model**: OpenAI Whisper (faster-whisper)
- **Database**: SQLite
- **Frontend**: HTML, CSS, JavaScript
- **Video Processing**: yt-dlp, pytubefix
- **Audio Processing**: av (PyAV)

## 📋 **System Requirements**

### **Minimum**
- Python 3.8+
- 4GB RAM
- 2GB free disk space
- Internet connection

### **Recommended**
- Python 3.10+
- 8GB+ RAM
- SSD storage
- Stable broadband connection

## 🔧 **Configuration**

### **Model Selection**
- **Tiny**: Fastest, lower accuracy (~30 seconds)
- **Base**: Balanced speed/quality (~1-2 minutes) 
- **Small**: Better accuracy (~2-3 minutes)
- **Medium**: Highest quality (~3-5 minutes)

### **Supported Formats**
- **Video**: MP4, AVI, MOV, MKV, WMV, FLV, WebM
- **Audio**: MP3, WAV, AAC, M4A, OGG, FLAC

## 🐛 **Troubleshooting**

### **Common Issues**

1. **"Video unavailable" on deployment**
   - **Solution**: Run locally instead of cloud deployment

2. **Slow processing**
   - **Solution**: Use smaller Whisper model (Tiny/Base)

3. **Out of memory errors**
   - **Solution**: Close other applications, use Tiny model

4. **Installation issues**
   - **Solution**: Update pip, use virtual environment

## 📄 **License**

This project is for educational purposes. Respect YouTube's Terms of Service and copyright laws.

## 🤝 **Contributing**

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch  
5. Create Pull Request

## 📞 **Support**

For issues and questions:
- Open GitHub Issues
- Check troubleshooting section
- Ensure you're running locally

---

**⭐ Star this repo if it helped you generate subtitles!**

**Note**: This application works best when run locally due to YouTube's bot detection systems. Cloud deployment is possible with advanced networking solutions but requires additional setup and costs.

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
