# MedHelp - Privacy-Focused Medical Symptom Checker

## Overview

MedHelp is a privacy-first, offline medical symptom checker built for the OpenAI Open Model Hackathon's "For Humanity" category. The application provides accessible healthcare guidance to underserved communities using gpt-oss-20b, OpenAI's open-weight reasoning model. The system operates entirely offline once the model is loaded, ensuring complete privacy by processing all medical information locally on the user's device without any external data transmission.

The application features comprehensive accessibility support including voice input, multi-language support (9 languages), screen reader compatibility, and keyboard navigation. It provides intelligent symptom analysis with emergency detection, risk assessment, and actionable medical guidance while maintaining strict privacy standards.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Flask with Jinja2 templating engine
- **Client-Side**: Vanilla JavaScript with Web Speech API integration for voice input
- **Styling**: CSS with comprehensive accessibility features including high contrast mode, reduced motion support, and WCAG compliance
- **Responsive Design**: Mobile-first approach supporting phones, tablets, and desktop computers
- **Accessibility**: Full keyboard navigation, screen reader compatibility, and voice input capabilities

### Backend Architecture
- **Web Framework**: Flask application with modular design
- **AI Integration**: Direct integration with Ollama running gpt-oss-20b model locally
- **Medical Analysis**: Custom MedicalAnalyzer class that processes symptoms using structured prompts and provides emergency detection
- **Language Support**: Multi-language processing with automatic language detection and localized emergency contact information
- **Privacy Design**: No database storage, no external API calls, all processing happens in-memory

### Core Components
- **app.py**: Main Flask application with routing and request handling
- **medical_analyzer.py**: AI-powered symptom analysis using gpt-oss-20b via Ollama
- **language_support.py**: Multi-language support with 9 languages and emergency contact localization
- **config.py**: Centralized configuration management with environment variable support
- **Static Assets**: CSS for accessibility, JavaScript for voice input and offline detection

### Data Processing Flow
1. User inputs symptoms via text or voice (Web Speech API)
2. Language detection if auto-detect is selected
3. Local AI analysis using gpt-oss-120b through Ollama
4. Emergency keyword detection for high-priority symptoms
5. Structured medical assessment with risk categorization
6. Results presentation with actionable guidance and emergency contacts

## External Dependencies

### AI Model Infrastructure
- **Ollama**: Local AI model server for running gpt-oss-20b
- **gpt-oss-20b**: OpenAI's open-weight reasoning model for medical analysis
- **Model Requirements**: Local installation required, no internet connectivity needed once installed

### Browser APIs
- **Web Speech API**: For voice input functionality (webkitSpeechRecognition/SpeechRecognition)
- **Navigator API**: For offline detection and network status monitoring

### Development Dependencies
- **Flask**: Python web framework for backend application
- **Requests**: HTTP library for communicating with local Ollama server
- **Font Awesome**: Icon library for user interface elements

### Runtime Environment
- **Python 3.8+**: Required for Flask application
- **Local Ollama Server**: Must be running on localhost:11434 with gpt-oss-20b model loaded
- **Modern Web Browser**: Required for Web Speech API and accessibility features

### Configuration Management
- Environment variables for Ollama URL, model settings, and application configuration
- No external configuration services or remote dependencies
- All settings configurable via environment variables with sensible defaults