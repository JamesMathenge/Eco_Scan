import os
import logging
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from medical_analyzer import MedicalAnalyzer
from language_support import LanguageSupport
import json

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "medical-privacy-key-2025")

# Initialize components
medical_analyzer = MedicalAnalyzer()
language_support = LanguageSupport()

@app.route('/')
def index():
    """Main page with symptom input form"""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_symptoms():
    """Analyze symptoms using gpt-oss model"""
    try:
        # Get form data
        symptoms = request.form.get('symptoms', '').strip()
        age = request.form.get('age', '')
        gender = request.form.get('gender', '')
        language = request.form.get('language', 'en')
        
        # Validate input
        if not symptoms:
            flash('Please describe your symptoms', 'error')
            return redirect(url_for('index'))
        
        if len(symptoms) < 10:
            flash('Please provide more detailed symptom description', 'error')
            return redirect(url_for('index'))
        
        # Detect language if auto-detect is selected
        if language == 'auto':
            language = language_support.detect_language(symptoms)
        
        # Analyze symptoms
        logger.info(f"Analyzing symptoms in {language}")
        analysis_result = medical_analyzer.analyze_symptoms(
            symptoms=symptoms,
            age=age,
            gender=gender,
            language=language
        )
        
        # Check for emergency indicators
        if analysis_result.get('emergency_level', 'low') == 'high':
            return render_template('emergency.html', 
                                 analysis=analysis_result,
                                 language=language)
        
        return render_template('results.html', 
                             analysis=analysis_result,
                             original_symptoms=symptoms,
                             language=language)
        
    except Exception as e:
        logger.error(f"Error analyzing symptoms: {str(e)}")
        flash(f'Error analyzing symptoms: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/emergency')
def emergency():
    """Emergency guidance page"""
    return render_template('emergency.html')

@app.route('/api/voice-input', methods=['POST'])
def voice_input():
    """Handle voice input transcription"""
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        # Detect language
        language = language_support.detect_language(text)
        
        return jsonify({
            'text': text,
            'language': language,
            'success': True
        })
        
    except Exception as e:
        logger.error(f"Error processing voice input: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/translate', methods=['POST'])
def translate_text():
    """Translate text for multi-language support"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        target_language = data.get('target_language', 'en')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        translated = language_support.translate_text(text, target_language)
        
        return jsonify({
            'translated_text': translated,
            'target_language': target_language,
            'success': True
        })
        
    except Exception as e:
        logger.error(f"Error translating text: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    try:
        # Check if Ollama is running and model is available
        status = medical_analyzer.check_model_status()
        return jsonify(status)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    return render_template('index.html'), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {str(error)}")
    flash('An internal error occurred. Please try again.', 'error')
    return render_template('index.html'), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
