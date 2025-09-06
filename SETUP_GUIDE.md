# MedHelp - Local Setup Guide

This guide will help you run the MedHelp medical symptom checker locally in VS Code.

## 🔧 Prerequisites

Before starting, make sure you have these installed on your system:

1. **Python 3.8 or higher**
2. **VS Code** with Python extension
3. **Git** (to clone the repository)
4. **Ollama** (for running the gpt-oss-20b model locally)

## 📥 Step 1: Install Ollama

Ollama is required to run the gpt-oss-20b model locally on your machine.

### Windows
1. Download Ollama from: https://ollama.ai/download
2. Run the installer and follow the setup wizard
3. Open Command Prompt or PowerShell

### macOS
```bash
# Using Homebrew (recommended)
brew install ollama

# Or download from https://ollama.ai/download
```

### Linux (Ubuntu/Debian)
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

## 🤖 Step 2: Install the AI Model

Once Ollama is installed, download the gpt-oss-120b model:

```bash
# This will download the model (about 70GB)
ollama pull gpt-oss-120b

# Verify the model is installed
ollama list
```

**Note**: The model is large (~20GB), so ensure you have sufficient disk space and a good internet connection.

## 📂 Step 3: Set up the Project

### Option A: If you have the project files already
1. Open VS Code
2. Open the project folder: `File > Open Folder`
3. Select the MedHelp project directory

### Option B: Clone from repository (if available)
```bash
git clone [your-repository-url]
cd medhelp
code .  # Opens VS Code in the current directory
```

## 🐍 Step 4: Set up Python Environment

In VS Code:

1. **Open the integrated terminal**: `Ctrl+`` (backtick) or `View > Terminal`

2. **Create a virtual environment** (recommended):
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install required packages**:
```bash
pip install flask requests gunicorn
```

## 🚀 Step 5: Start the Services

You need to run two things:

### Terminal 1: Start Ollama Server
```bash
# In a new terminal window/tab
ollama serve
```
Leave this running - you should see output like:
```
2025/08/14 20:46:37 images.go:806: total blobs: 0
2025/08/14 20:46:37 images.go:813: total unused blobs removed: 0
2025/08/14 20:46:37 routes.go:1110: Listening on 127.0.0.1:11434 (version 0.x.x)
```

### Terminal 2: Start the Flask Application
In VS Code terminal (with virtual environment activated):
```bash
# Method 1: Using Python directly
python main.py

# Method 2: Using Gunicorn (production-like)
gunicorn --bind 0.0.0.0:5000 --reload main:app

# Method 3: Using Flask development server
export FLASK_APP=main.py
flask run --host=0.0.0.0 --port=5000
```

## 🌐 Step 6: Access the Application

1. Open your web browser
2. Go to: `http://localhost:5000`
3. You should see the MedHelp homepage with the symptom input form

## 🧪 Step 7: Test the Application

1. **Test basic functionality**:
   - Enter some symptoms like "I have a headache and feel dizzy"
   - Click "Analyze My Symptoms"
   - Wait for the AI analysis (may take 10-30 seconds)

2. **Test voice input** (if supported by your browser):
   - Click the microphone button next to the symptom text area
   - Allow microphone permissions
   - Speak your symptoms clearly

3. **Test multiple languages**:
   - Change the language dropdown
   - Enter symptoms in that language

## 🔧 VS Code Configuration

### Recommended Extensions
Install these VS Code extensions for better development experience:
- Python (Microsoft)
- Pylance (Microsoft)
- Python Docstring Generator
- GitLens

### Debug Configuration
Create `.vscode/launch.json`:
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Flask",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/main.py",
            "console": "integratedTerminal",
            "env": {
                "FLASK_ENV": "development",
                "FLASK_DEBUG": "1"
            }
        }
    ]
}
```

## 🛠 Troubleshooting

### Issue: "Connection refused" or Ollama not found
**Solution**: Make sure Ollama is running:
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# If not running, start it
ollama serve
```

### Issue: Model not found
**Solution**: Ensure gpt-oss-120b is downloaded:
```bash
ollama list
# If not listed, download it:
ollama pull gpt-oss-120b
```

### Issue: Python packages not found
**Solution**: Activate virtual environment and install packages:
```bash
# Activate virtual environment first
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows

# Then install packages
pip install flask requests gunicorn
```

### Issue: Port 5000 already in use
**Solution**: Use a different port:
```bash
python main.py --port 5001
# or
gunicorn --bind 0.0.0.0:5001 main:app
```

### Issue: Voice input not working
**Cause**: Web Speech API requires HTTPS or localhost
**Solution**: This is normal - voice input works on localhost but may not work on some deployed versions

## 🔒 Privacy & Security Notes

- **Complete Privacy**: All processing happens locally on your machine
- **No Internet Required**: Once models are downloaded, the app works offline
- **No Data Collection**: Your symptom data never leaves your device
- **Local AI Model**: gpt-oss-120b runs entirely on your computer

## 📝 Environment Variables (Optional)

Create a `.env` file in your project root:
```bash
OLLAMA_URL=http://localhost:11434
MODEL_NAME=gpt-oss-120b
MODEL_TEMPERATURE=0.3
MODEL_MAX_TOKENS=1500
FLASK_ENV=development
FLASK_DEBUG=1
SESSION_SECRET=your-secret-key-here
```

## 🎯 Development Workflow

1. **Make changes** to Python files in VS Code
2. **Save files** - the server will auto-reload (if using `--reload` flag)
3. **Refresh browser** to see changes
4. **Check terminal** for any error messages
5. **Use VS Code debugger** for advanced debugging

## 📊 Performance Notes

- **First Request**: May take 20-60 seconds as the model loads into memory
- **Subsequent Requests**: Should be faster (5-15 seconds)
- **Model Size**: gpt-oss-120b requires ~8-16GB RAM when loaded
- **CPU Usage**: Higher during analysis, normal when idle

## 🆘 Getting Help

If you encounter issues:
1. Check the terminal output for error messages
2. Verify Ollama is running: `curl http://localhost:11434/api/tags`
3. Check that the model is downloaded: `ollama list`
4. Ensure all Python packages are installed: `pip list`
5. Try restarting both Ollama and the Flask application

## 🚀 Ready to Use!

Once everything is running, you should have:
- ✅ Ollama server running on port 11434
- ✅ gpt-oss-120b model downloaded and loaded
- ✅ Flask application running on port 5000
- ✅ Web interface accessible at http://localhost:5000

The application is now ready to provide privacy-focused medical symptom analysis using the powerful gpt-oss-20b model running entirely on your local machine!