import logging
from typing import Dict, List
import re

logger = logging.getLogger(__name__)

class LanguageSupport:
    """Multi-language support for the medical symptom checker"""
    
    def __init__(self):
        # Supported languages with their codes and names
        self.supported_languages = {
            'en': 'English',
            'es': 'Español',
            'fr': 'Français',
            'pt': 'Português',
            'ar': 'العربية',
            'hi': 'हिन्दी',
            'zh': '中文',
            'ru': 'Русский',
            'sw': 'Kiswahili'
        }
        
        # Common medical terms for language detection
        self.language_patterns = {
            'en': ['pain', 'headache', 'fever', 'nausea', 'dizzy', 'tired', 'hurt', 'ache'],
            'es': ['dolor', 'cabeza', 'fiebre', 'náusea', 'mareado', 'cansado', 'duele'],
            'fr': ['douleur', 'tête', 'fièvre', 'nausée', 'étourdi', 'fatigué', 'mal'],
            'pt': ['dor', 'cabeça', 'febre', 'náusea', 'tonto', 'cansado', 'doer'],
            'ar': ['ألم', 'صداع', 'حمى', 'غثيان', 'دوخة', 'تعب', 'وجع'],
            'hi': ['दर्द', 'सिरदर्द', 'बुखार', 'जी मिचलाना', 'चक्कर', 'थकान'],
            'zh': ['疼痛', '头痛', '发烧', '恶心', '头晕', '疲劳', '痛'],
            'ru': ['боль', 'головная', 'лихорадка', 'тошнота', 'головокружение', 'усталость'],
            'sw': ['maumivu', 'kichwa', 'homa', 'kichefuchefu', 'kizunguzungu', 'uchovu']
        }
        
        # Emergency contact information by language
        self.emergency_contacts = {
            'en': {
                'emergency_number': '911 (US), 112 (EU), or your local emergency number',
                'poison_control': 'Poison Control: 1-800-222-1222 (US)',
                'crisis_line': 'Crisis Line: 988 (US) or your local crisis helpline'
            },
            'es': {
                'emergency_number': '911 (EE.UU.), 112 (UE), o su número de emergencia local',
                'poison_control': 'Control de Envenenamiento: 1-800-222-1222 (EE.UU.)',
                'crisis_line': 'Línea de Crisis: 988 (EE.UU.) o su línea de crisis local'
            },
            'fr': {
                'emergency_number': '15 (France), 112 (UE), ou votre numéro d\'urgence local',
                'poison_control': 'Centre Antipoison: 15 (France)',
                'crisis_line': 'Ligne de Crise: 3114 (France) ou votre ligne de crise locale'
            },
            'pt': {
                'emergency_number': '192 (Brasil), 112 (UE), ou seu número de emergência local',
                'poison_control': 'Centro de Informação Toxicológica: 0800-722-6001 (Brasil)',
                'crisis_line': 'Linha de Crise: 188 (Brasil) ou sua linha de crise local'
            }
        }
        
        # Default to English for unsupported languages
        for lang in self.supported_languages.keys():
            if lang not in self.emergency_contacts:
                self.emergency_contacts[lang] = self.emergency_contacts['en']
    
    def detect_language(self, text: str) -> str:
        """Detect language based on medical terms and patterns"""
        try:
            text_lower = text.lower()
            language_scores = {}
            
            # Score based on medical term matches
            for lang_code, terms in self.language_patterns.items():
                score = 0
                for term in terms:
                    if term.lower() in text_lower:
                        score += 1
                language_scores[lang_code] = score
            
            # Return language with highest score, default to English
            if language_scores:
                detected_lang = max(language_scores.keys(), key=lambda k: language_scores[k])
                if language_scores[detected_lang] > 0:
                    logger.info(f"Detected language: {detected_lang} (score: {language_scores[detected_lang]})")
                    return detected_lang
            
            # Fallback: simple character-based detection
            if self._contains_arabic(text):
                return 'ar'
            elif self._contains_chinese(text):
                return 'zh'
            elif self._contains_hindi(text):
                return 'hi'
            elif self._contains_cyrillic(text):
                return 'ru'
            
            # Default to English
            logger.info("Language detection defaulted to English")
            return 'en'
            
        except Exception as e:
            logger.error(f"Error in language detection: {str(e)}")
            return 'en'
    
    def _contains_arabic(self, text: str) -> bool:
        """Check if text contains Arabic characters"""
        arabic_pattern = re.compile(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]')
        return bool(arabic_pattern.search(text))
    
    def _contains_chinese(self, text: str) -> bool:
        """Check if text contains Chinese characters"""
        chinese_pattern = re.compile(r'[\u4e00-\u9fff\u3400-\u4dbf\u20000-\u2a6df\u2a700-\u2b73f\u2b740-\u2b81f\u2b820-\u2ceaf\uf900-\ufaff\u2f800-\u2fa1f]')
        return bool(chinese_pattern.search(text))
    
    def _contains_hindi(self, text: str) -> bool:
        """Check if text contains Hindi/Devanagari characters"""
        hindi_pattern = re.compile(r'[\u0900-\u097F]')
        return bool(hindi_pattern.search(text))
    
    def _contains_cyrillic(self, text: str) -> bool:
        """Check if text contains Cyrillic characters"""
        cyrillic_pattern = re.compile(r'[\u0400-\u04FF\u0500-\u052F\u2DE0-\u2DFF\uA640-\uA69F]')
        return bool(cyrillic_pattern.search(text))
    
    def get_emergency_contacts(self, language: str) -> Dict[str, str]:
        """Get emergency contact information for a specific language"""
        return self.emergency_contacts.get(language, self.emergency_contacts['en'])
    
    def translate_text(self, text: str, target_language: str) -> str:
        """Basic translation helper (would use local translation in production)"""
        # Note: In a real implementation, this would use a local translation model
        # For now, we'll return the original text with a note
        if target_language == 'en' or target_language not in self.supported_languages:
            return text
        
        return f"[Translation to {self.supported_languages[target_language]} would be provided by local translation model] {text}"
    
    def get_interface_text(self, language: str) -> Dict[str, str]:
        """Get interface text translations"""
        translations = {
            'en': {
                'title': 'Privacy-Focused Medical Symptom Checker',
                'subtitle': 'Accessible Healthcare Guidance for Everyone',
                'describe_symptoms': 'Describe your symptoms',
                'age_label': 'Age (optional)',
                'gender_label': 'Gender (optional)',
                'language_label': 'Language',
                'analyze_button': 'Analyze Symptoms',
                'voice_input': 'Use Voice Input',
                'emergency_warning': 'If this is a medical emergency, call emergency services immediately',
                'disclaimer_short': 'This tool provides general information only. Always consult healthcare professionals.',
                'privacy_note': 'All analysis performed locally - your data never leaves this device'
            },
            'es': {
                'title': 'Verificador de Síntomas Médicos Centrado en la Privacidad',
                'subtitle': 'Orientación Sanitaria Accesible para Todos',
                'describe_symptoms': 'Describe tus síntomas',
                'age_label': 'Edad (opcional)',
                'gender_label': 'Género (opcional)',
                'language_label': 'Idioma',
                'analyze_button': 'Analizar Síntomas',
                'voice_input': 'Usar Entrada de Voz',
                'emergency_warning': 'Si esto es una emergencia médica, llame a los servicios de emergencia inmediatamente',
                'disclaimer_short': 'Esta herramienta proporciona información general solamente. Siempre consulte a profesionales de la salud.',
                'privacy_note': 'Todo el análisis se realiza localmente - sus datos nunca salen de este dispositivo'
            },
            'fr': {
                'title': 'Vérificateur de Symptômes Médicaux Axé sur la Confidentialité',
                'subtitle': 'Conseils de Santé Accessibles pour Tous',
                'describe_symptoms': 'Décrivez vos symptômes',
                'age_label': 'Âge (optionnel)',
                'gender_label': 'Genre (optionnel)',
                'language_label': 'Langue',
                'analyze_button': 'Analyser les Symptômes',
                'voice_input': 'Utiliser l\'Entrée Vocale',
                'emergency_warning': 'Si c\'est une urgence médicale, appelez immédiatement les services d\'urgence',
                'disclaimer_short': 'Cet outil fournit des informations générales seulement. Consultez toujours des professionnels de la santé.',
                'privacy_note': 'Toute l\'analyse est effectuée localement - vos données ne quittent jamais cet appareil'
            }
        }
        
        return translations.get(language, translations['en'])
