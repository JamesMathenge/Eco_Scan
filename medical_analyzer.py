import os
import requests
import json
import logging
import re
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

class MedicalAnalyzer:
    """
    LLM-driven medical symptom analyzer using gpt-oss models via Ollama
    Lets the AI do the actual medical reasoning instead of rule-based classification
    """
    
    def __init__(self):
        self.ollama_url = os.getenv('OLLAMA_URL', 'http://localhost:11434')
        self.model_name = os.getenv('MODEL_NAME', 'gpt-oss:20b')
        self.temperature = float(os.getenv('MODEL_TEMPERATURE', '0.3'))
        self.max_tokens = int(os.getenv('MODEL_MAX_TOKENS', '2000'))
        
        # Supported languages
        self.supported_languages = {
            'en': 'English', 'es': 'Español', 'fr': 'Français', 'pt': 'Português',
            'ar': 'العربية', 'hi': 'हिन्दी', 'zh': '中文', 'ru': 'Русский', 'sw': 'Kiswahili'
        }
        
        # Only the most obvious life-threatening emergencies (minimal rule-based filtering)
        self.absolute_emergencies = [
            'not breathing', 'no pulse', 'unconscious', 'unresponsive',
            'major bleeding', 'severe burns over large area', 'overdose confirmed',
            'active seizure', 'choking right now', 'severe allergic reaction with throat closing'
        ]
        
        self.disclaimer = """
        🏥 IMPORTANT: This AI provides health information to help you understand symptoms.
        It is not a medical diagnosis. For health concerns, consult qualified healthcare providers.
        In emergencies, contact your local emergency services immediately.
        """
    
    def check_model_status(self) -> Dict[str, Any]:
        """Check if Ollama and gpt-oss model are available"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get('models', [])
                model_available = any(
                    self.model_name in model.get('name', '') 
                    for model in models
                )
                return {
                    'status': 'ready' if model_available else 'model_not_found',
                    'model_available': model_available,
                    'available_models': [m.get('name') for m in models if 'gpt-oss' in m.get('name', '')]
                }
            return {'status': 'ollama_not_running', 'model_available': False}
        except:
            return {'status': 'connection_error', 'model_available': False}
    
    def check_absolute_emergency(self, symptoms: str) -> bool:
        """Only check for absolutely obvious life-threatening situations"""
        symptoms_lower = symptoms.lower()
        return any(emergency in symptoms_lower for emergency in self.absolute_emergencies)
    
    def create_comprehensive_prompt(self, symptoms: str, age: str, gender: str, language: str) -> str:
        """Create a comprehensive prompt that lets the LLM do the medical reasoning"""
        
        prompt = f"""You are an experienced medical AI assistant with expertise in symptom analysis and triage. You will analyze the following patient presentation and provide comprehensive medical guidance.

PATIENT PRESENTATION:
Age: {age if age else 'Not specified'}
Gender: {gender if gender else 'Not specified'}
Chief Complaint and Symptoms: {symptoms}

Please analyze this case thoroughly and provide your assessment in the following structured format:

## CLINICAL ASSESSMENT

### SYMPTOM ANALYSIS
Provide your clinical interpretation of the presented symptoms, including:
- Primary symptoms and their characteristics
- Associated symptoms and their significance
- Symptom pattern analysis (onset, duration, progression, triggers)
- Review of systems implications

### DIFFERENTIAL DIAGNOSIS
List your top 4-5 differential diagnoses in order of likelihood:
1. **[Most Likely Condition]** - Brief rationale
2. **[Second Most Likely]** - Brief rationale  
3. **[Third Possibility]** - Brief rationale
4. **[Fourth Possibility]** - Brief rationale
5. **[Less Likely but Important]** - Brief rationale

### URGENCY ASSESSMENT
Based on your medical knowledge, classify this case:
- **EMERGENCY** (Life-threatening, needs immediate care within minutes)
- **URGENT** (Serious condition, needs care within hours)
- **SEMI-URGENT** (Concerning symptoms, needs care within days)
- **ROUTINE** (Mild symptoms, can schedule regular appointment)

Explain your urgency classification with medical reasoning.

### IMMEDIATE RECOMMENDATIONS
What should the patient do right now based on your assessment?

### RED FLAGS TO WATCH FOR
What warning signs should prompt immediate medical attention?

### SELF-CARE MEASURES
What safe measures can help manage symptoms? (Only if appropriate for the condition)

### FOLLOW-UP GUIDANCE
When and how should the patient seek professional medical care?

## IMPORTANT NOTES
- Base your assessment on established medical knowledge and clinical reasoning
- Consider patient demographics (age/gender) in your differential diagnosis
- Be thorough but practical in your recommendations
- If you identify any emergency conditions, clearly state this upfront
- Acknowledge diagnostic limitations without direct examination

Please provide your complete medical assessment now."""

        return prompt
    
    def query_llm_for_analysis(self, prompt: str) -> str:
        """Let the LLM do the actual medical reasoning"""
        try:
            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": self.temperature,
                    "top_p": 0.9,
                    "max_tokens": self.max_tokens,
                    "repeat_penalty": 1.1,
                    "stop": ["## IMPORTANT NOTES", "---", "***"]
                }
            }
            
            logger.info(f"Sending comprehensive analysis request to {self.model_name}")
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json=payload,
                timeout=600  # Longer timeout for comprehensive analysis
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', 'Unable to generate medical analysis')
            else:
                logger.error(f"LLM API error: {response.status_code}")
                return f"Error connecting to medical AI: HTTP {response.status_code}"
                
        except requests.exceptions.Timeout:
            logger.error("Timeout during LLM analysis")
            return "Medical analysis timed out. Please try again with a shorter description."
        except Exception as e:
            logger.error(f"Error during LLM analysis: {str(e)}")
            return f"Error during medical analysis: {str(e)}"
    
    def parse_llm_analysis(self, llm_response: str) -> Dict[str, Any]:
        """Parse the LLM's comprehensive medical analysis"""
        try:
            analysis = {
                'symptom_analysis': '',
                'differential_diagnosis': [],
                'urgency_assessment': '',
                'urgency_level': 'routine',
                'immediate_recommendations': '',
                'red_flags': '',
                'self_care': '',
                'follow_up': '',
                'full_llm_response': llm_response,
                'ai_generated': True
            }
            
            # Extract sections using flexible parsing
            sections = {
                'symptom_analysis': r'### SYMPTOM ANALYSIS\s*(.*?)(?=###|$)',
                'differential_diagnosis': r'### DIFFERENTIAL DIAGNOSIS\s*(.*?)(?=###|$)',
                'urgency_assessment': r'### URGENCY ASSESSMENT\s*(.*?)(?=###|$)',
                'immediate_recommendations': r'### IMMEDIATE RECOMMENDATIONS\s*(.*?)(?=###|$)',
                'red_flags': r'### RED FLAGS TO WATCH FOR\s*(.*?)(?=###|$)',
                'self_care': r'### SELF-CARE MEASURES\s*(.*?)(?=###|$)',
                'follow_up': r'### FOLLOW-UP GUIDANCE\s*(.*?)(?=###|$)'
            }
            
            for key, pattern in sections.items():
                match = re.search(pattern, llm_response, re.IGNORECASE | re.DOTALL)
                if match:
                    content = match.group(1).strip()
                    
                    if key == 'differential_diagnosis':
                        # Parse numbered differential diagnosis list
                        diagnoses = re.findall(r'\d+\.\s*\*\*(.*?)\*\*\s*-\s*(.*?)(?=\d+\.|$)', content, re.DOTALL)
                        analysis[key] = [{'condition': d[0].strip(), 'rationale': d[1].strip()} for d in diagnoses]
                        if not analysis[key]:  # Fallback parsing
                            lines = [line.strip() for line in content.split('\n') if line.strip() and ('**' in line or line[0].isdigit())]
                            analysis[key] = [{'condition': line, 'rationale': ''} for line in lines[:5]]
                    else:
                        analysis[key] = content
            
            # Extract urgency level from urgency assessment
            urgency_text = analysis['urgency_assessment'].lower()
            if 'emergency' in urgency_text:
                analysis['urgency_level'] = 'emergency'
            elif 'urgent' in urgency_text and 'semi' not in urgency_text:
                analysis['urgency_level'] = 'urgent'
            elif 'semi-urgent' in urgency_text:
                analysis['urgency_level'] = 'semi-urgent'
            else:
                analysis['urgency_level'] = 'routine'
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error parsing LLM analysis: {str(e)}")
            return {
                'error': 'Failed to parse AI medical analysis',
                'full_llm_response': llm_response,
                'urgency_level': 'urgent',  # Default to urgent if parsing fails
                'ai_generated': True
            }
    
    def create_emergency_override(self, symptoms: str) -> Dict[str, Any]:
        """Only for absolute medical emergencies - bypass normal analysis"""
        return {
            'emergency_override': True,
            'urgency_level': 'emergency',
            'symptom_analysis': f'MEDICAL EMERGENCY DETECTED: {symptoms}',
            'differential_diagnosis': [
                {'condition': 'Life-threatening emergency', 'rationale': 'Immediate intervention required'}
            ],
            'immediate_recommendations': '🚨 CALL EMERGENCY SERVICES IMMEDIATELY (911/112/999). Do not delay.',
            'red_flags': 'You are experiencing a medical emergency.',
            'self_care': 'Do not attempt self-treatment. Call emergency services now.',
            'follow_up': 'Emergency medical care required immediately.',
            'urgency_assessment': 'EMERGENCY - Life-threatening condition requiring immediate medical intervention',
            'ai_generated': False
        }
    
    def analyze_symptoms(self, symptoms: str, age: str = '', gender: str = '', language: str = 'en') -> Dict[str, Any]:
        """Main analysis method - lets LLM do the medical thinking"""
        try:
            # Validate inputs
            if not symptoms.strip():
                return {'error': 'Please describe your symptoms to receive medical guidance.'}
            
            if language not in self.supported_languages:
                language = 'en'
            
            # Only check for absolute obvious emergencies
            if self.check_absolute_emergency(symptoms):
                logger.warning("Absolute emergency detected - bypassing normal analysis")
                analysis = self.create_emergency_override(symptoms)
            else:
                # Check if LLM is available
                model_status = self.check_model_status()
                
                if model_status['status'] != 'ready':
                    return {
                        'error': f"Medical AI service unavailable ({model_status['status']}). Please consult a healthcare provider.",
                        'available_models': model_status.get('available_models', []),
                        'urgency_level': 'urgent',
                        'immediate_recommendations': 'Since AI analysis is unavailable, please consult with a healthcare provider about your symptoms.'
                    }
                
                # Let the LLM do comprehensive medical analysis
                prompt = self.create_comprehensive_prompt(symptoms, age, gender, language)
                llm_response = self.query_llm_for_analysis(prompt)
                
                if 'Error' in llm_response or 'timed out' in llm_response:
                    return {
                        'error': 'Unable to complete medical analysis',
                        'technical_details': llm_response,
                        'urgency_level': 'urgent',
                        'immediate_recommendations': 'Please consult with a healthcare provider about your symptoms.'
                    }
                
                # Parse the LLM's medical analysis
                analysis = self.parse_llm_analysis(llm_response)
            
            # Add metadata
            analysis.update({
                'timestamp': self._get_timestamp(),
                'language': language,
                'model_used': self.model_name,
                'disclaimer': self.disclaimer,
                'privacy_note': 'Complete privacy - all analysis performed locally on your device',
                'input_symptoms': symptoms,
                'patient_age': age,
                'patient_gender': gender
            })
            
            return analysis
            
        except Exception as e:
            logger.error(f"Critical error in symptom analysis: {str(e)}")
            return {
                'error': 'Medical analysis system error',
                'urgency_level': 'urgent',
                'immediate_recommendations': 'Due to system error, please consult with a healthcare provider about your symptoms.',
                'technical_error': str(e)
            }
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


