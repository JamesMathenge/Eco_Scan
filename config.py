import os
from typing import Dict, Any

class Config:
    """Configuration settings for the MedHelp application"""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SESSION_SECRET', 'medical-privacy-key-2025')
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    # Ollama settings
    OLLAMA_URL = os.environ.get('OLLAMA_URL', 'http://localhost:11434')
    MODEL_NAME = os.environ.get('MODEL_NAME', 'gpt-oss-20b')  # Default to 20b for better performance
    MODEL_TIMEOUT = int(os.environ.get('MODEL_TIMEOUT', '60'))
    
    # Application settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max request size
    LANGUAGES_SUPPORTED = [
        'en', 'es', 'fr', 'pt', 'ar', 'hi', 'zh', 'ru', 'sw'
    ]
    
    # Medical settings
    MIN_SYMPTOM_LENGTH = int(os.environ.get('MIN_SYMPTOM_LENGTH', '10'))
    MAX_SYMPTOM_LENGTH = int(os.environ.get('MAX_SYMPTOM_LENGTH', '2000'))
    
    # Emergency keywords for high-priority detection
    EMERGENCY_KEYWORDS = [
        'chest pain', 'heart attack', 'stroke', 'difficulty breathing',
        'severe bleeding', 'unconscious', 'seizure', 'severe headache',
        'suicidal thoughts', 'overdose', 'severe burns', 'broken bone',
        'severe allergic reaction', 'anaphylaxis', 'poisoning',
        'cannot breathe', 'choking', 'severe injury', 'loss of consciousness'
    ]
    
    # Rate limiting (if needed in production)
    RATELIMIT_STORAGE_URL = os.environ.get('RATELIMIT_STORAGE_URL', 'memory://')
    RATELIMIT_DEFAULT = os.environ.get('RATELIMIT_DEFAULT', '100 per hour')
    
    @staticmethod
    def get_model_config() -> Dict[str, Any]:
        """Get model configuration for gpt-oss"""
        return {
            'model': Config.MODEL_NAME,
            'temperature': float(os.environ.get('MODEL_TEMPERATURE', '0.3')),
            'top_p': float(os.environ.get('MODEL_TOP_P', '0.9')),
            'max_tokens': int(os.environ.get('MODEL_MAX_TOKENS', '1500')),
            'timeout': Config.MODEL_TIMEOUT
        }
    
    @staticmethod
    def get_emergency_contacts() -> Dict[str, Dict[str, str]]:
        """Get emergency contact information by country/region"""
        return {
            'US': {
                'emergency': '911',
                'poison': '1-800-222-1222',
                'crisis': '988',
                'name': 'United States'
            },
            'EU': {
                'emergency': '112',
                'poison': '112',
                'crisis': '116 123',
                'name': 'European Union'
            },
            'UK': {
                'emergency': '999',
                'poison': '111',
                'crisis': '116 123',
                'name': 'United Kingdom'
            },
            'AU': {
                'emergency': '000',
                'poison': '13 11 26',
                'crisis': '13 11 14',
                'name': 'Australia'
            },
            'CA': {
                'emergency': '911',
                'poison': '1-844-764-7669',
                'crisis': '1-833-456-4566',
                'name': 'Canada'
            }
        }
    
    @staticmethod
    def validate_environment():
        """Validate that required environment variables are set"""
        required_vars = []
        missing_vars = [var for var in required_vars if not os.environ.get(var)]
        
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
        
        return True

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    
    # Enhanced security for production
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False

# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config(config_name=None):
    """Get configuration based on environment"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')
    
    return config.get(config_name, DevelopmentConfig)
