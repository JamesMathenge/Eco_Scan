# MedHelp - Privacy-Focused Medical Symptom Checker

A privacy-first, offline medical symptom checker built for the OpenAI Open Model Hackathon's "For Humanity" category. This application uses gpt-oss-20b to provide accessible healthcare guidance for underserved communities while ensuring complete privacy and offline functionality.

## 🏆 Hackathon Entry: For Humanity Category

**Built with gpt-oss-20b for the OpenAI Open Model Hackathon**

This project demonstrates how open-weight AI models can provide essential healthcare guidance to underserved communities while maintaining complete privacy and working entirely offline.

## 🌟 Key Features

### Privacy-First Design
- **Complete Privacy**: All processing happens locally on your device
- **No Data Transmission**: Your medical information never leaves your device
- **Offline Functionality**: Works without internet connection once the model is loaded
- **No Registration Required**: Anonymous usage without any personal data collection

### Accessibility & Inclusion
- **Voice Input**: Speech-to-text for users with limited mobility
- **Multi-Language Support**: 9 languages including English, Spanish, French, Portuguese, Arabic, Hindi, Chinese, Russian, and Swahili
- **Screen Reader Compatible**: Full WCAG compliance for visually impaired users
- **High Contrast Mode**: Supports system-level accessibility preferences
- **Keyboard Navigation**: Complete keyboard accessibility
- **Responsive Design**: Works on phones, tablets, and computers

### Advanced AI Analysis
- **gpt-oss-120b Integration**: Uses OpenAI's open-weight reasoning model
- **Intelligent Symptom Analysis**: Structured medical assessment with multiple perspectives
- **Emergency Detection**: Automatic identification of symptoms requiring immediate care
- **Risk Assessment**: Clear severity classification (Low, Moderate, High)
- **Actionable Guidance**: Specific next steps and self-care recommendations

### Medical Features
- **Symptom Summary**: AI-powered summary of reported symptoms
- **Condition Analysis**: Evidence-based assessment of possible conditions
- **Treatment Guidance**: Safe self-care suggestions and medical referral guidance
- **Warning Signs**: Clear indicators for when to seek emergency care
- **Emergency Contacts**: Location-appropriate emergency service information

## 🚀 Quick Start

### Prerequisites

1. **Python 3.8+** installed on your system
2. **Ollama** installed and running locally
3. **gpt-oss-120b model** downloaded via Ollama

### Installation

1. **Install Ollama** (if not already installed):
   ```bash
   # macOS
   brew install ollama
   
   # Linux
   curl -fsSL https://ollama.ai/install.sh | sh
   
   # Windows - Download from https://ollama.ai/download
   ```

2. **Download a gpt-oss model** (choose one):
   ```bash
   # Recommended: Faster and smaller (22B parameters)
   ollama pull gpt-oss-20b
   
   # Alternative: Larger and more detailed (120B parameters)
   ollama pull gpt-oss-120b
   ```

3. **Clone and set up the application**:
   ```bash
   git clone <your-repo-url>
   cd medhelp
   
   # Install Python dependencies (will be handled separately)
   pip install flask requests langdetect
   ```

4. **Start Ollama** (if not running):
   ```bash
   ollama serve
   ```

5. **Run the application**:
   ```bash
   python main.py
   ```

6. **Access the application**:
   Open your browser and go to `http://localhost:5000`

## 🔧 Configuration

### Environment Variables

```bash
# Optional configuration
export OLLAMA_URL="http://localhost:11434"
export MODEL_NAME="gpt-oss-20b"
export MODEL_TEMPERATURE="0.3"
export MODEL_MAX_TOKENS="1500"
export SESSION_SECRET="your-secret-key"
