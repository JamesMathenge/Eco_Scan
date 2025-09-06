/**
 * MedHelp - Privacy-Focused Medical Symptom Checker
 * Client-side JavaScript for enhanced accessibility and user experience
 */

class MedHelpApp {
    constructor() {
        this.recognition = null;
        this.isListening = false;
        this.currentLanguage = 'en';
        
        this.init();
    }

    init() {
        this.setupVoiceRecognition();
        this.setupFormHandlers();
        this.setupAccessibilityFeatures();
        this.setupOfflineDetection();
        
        console.log('MedHelp app initialized');
    }

    /**
     * Set up Web Speech API for voice input
     */
    setupVoiceRecognition() {
        // Check for Web Speech API support
        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            console.warn('Web Speech API not supported');
            this.hideVoiceButton();
            return;
        }

        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        this.recognition = new SpeechRecognition();
        
        // Configure speech recognition
        this.recognition.continuous = true;
        this.recognition.interimResults = true;
        this.recognition.maxAlternatives = 1;
        
        // Set language based on user selection
        const languageSelect = document.getElementById('language');
        if (languageSelect) {
            this.currentLanguage = languageSelect.value === 'auto' ? 'en' : languageSelect.value;
            this.recognition.lang = this.getLanguageCode(this.currentLanguage);
            
            languageSelect.addEventListener('change', (e) => {
                this.currentLanguage = e.target.value === 'auto' ? 'en' : e.target.value;
                this.recognition.lang = this.getLanguageCode(this.currentLanguage);
            });
        }

        // Speech recognition event handlers
        this.recognition.onstart = () => {
            this.isListening = true;
            this.updateVoiceUI('listening');
            this.showVoiceStatus('🎤 Listening... Speak clearly about your symptoms', 'listening');
        };

        this.recognition.onresult = (event) => {
            let finalTranscript = '';
            let interimTranscript = '';

            for (let i = event.resultIndex; i < event.results.length; i++) {
                const transcript = event.results[i][0].transcript;
                if (event.results[i].isFinal) {
                    finalTranscript += transcript + ' ';
                } else {
                    interimTranscript += transcript;
                }
            }

            // Update the symptoms textarea
            const symptomsTextarea = document.getElementById('symptoms');
            if (symptomsTextarea) {
                symptomsTextarea.value = (symptomsTextarea.value + finalTranscript).trim();
                
                // Show interim results in status
                if (interimTranscript) {
                    this.showVoiceStatus(`🎤 "${interimTranscript}" (continue speaking...)`, 'listening');
                }
            }
        };

        this.recognition.onerror = (event) => {
            console.error('Speech recognition error:', event.error);
            this.isListening = false;
            this.updateVoiceUI('error');
            
            let errorMessage = 'Voice input error: ';
            switch (event.error) {
                case 'no-speech':
                    errorMessage += 'No speech detected. Please try again.';
                    break;
                case 'audio-capture':
                    errorMessage += 'Microphone not accessible. Please check permissions.';
                    break;
                case 'not-allowed':
                    errorMessage += 'Microphone permission denied. Please enable microphone access.';
                    break;
                case 'network':
                    errorMessage += 'Network error. Voice recognition works offline in most browsers.';
                    break;
                default:
                    errorMessage += event.error;
            }
            
            this.showVoiceStatus(errorMessage, 'error');
        };

        this.recognition.onend = () => {
            this.isListening = false;
            this.updateVoiceUI('stopped');
            this.showVoiceStatus('✅ Voice input complete. Review your text and submit when ready.', 'success');
        };

        // Set up voice button click handler
        const voiceButton = document.getElementById('voice-btn');
        if (voiceButton) {
            voiceButton.addEventListener('click', () => {
                this.toggleVoiceRecognition();
            });
        }
    }

    /**
     * Toggle voice recognition on/off
     */
    toggleVoiceRecognition() {
        if (!this.recognition) {
            this.showVoiceStatus('❌ Voice input not supported in this browser', 'error');
            return;
        }

        if (this.isListening) {
            this.recognition.stop();
        } else {
            try {
                this.recognition.start();
            } catch (error) {
                console.error('Error starting speech recognition:', error);
                this.showVoiceStatus('❌ Could not start voice input. Please try again.', 'error');
            }
        }
    }

    /**
     * Update voice button UI based on state
     */
    updateVoiceUI(state) {
        const voiceButton = document.getElementById('voice-btn');
        if (!voiceButton) return;

        const icon = voiceButton.querySelector('i');
        
        switch (state) {
            case 'listening':
                voiceButton.classList.add('listening');
                voiceButton.setAttribute('aria-label', 'Stop voice input');
                voiceButton.title = 'Click to stop voice input';
                if (icon) icon.className = 'fas fa-stop';
                break;
            case 'stopped':
            case 'error':
                voiceButton.classList.remove('listening');
                voiceButton.setAttribute('aria-label', 'Start voice input');
                voiceButton.title = 'Click to use voice input';
                if (icon) icon.className = 'fas fa-microphone';
                break;
        }
    }

    /**
     * Show voice recognition status
     */
    showVoiceStatus(message, type) {
        const statusElement = document.getElementById('voice-status');
        if (!statusElement) return;

        statusElement.textContent = message;
        statusElement.className = `voice-status active ${type}`;
        
        // Auto-hide success messages after 3 seconds
        if (type === 'success') {
            setTimeout(() => {
                statusElement.classList.remove('active');
            }, 3000);
        }
    }

    /**
     * Hide voice button if not supported
     */
    hideVoiceButton() {
        const voiceButton = document.getElementById('voice-btn');
        if (voiceButton) {
            voiceButton.style.display = 'none';
        }
    }

    /**
     * Get proper language code for speech recognition
     */
    getLanguageCode(lang) {
        const languageCodes = {
            'en': 'en-US',
            'es': 'es-ES',
            'fr': 'fr-FR',
            'pt': 'pt-BR',
            'ar': 'ar-SA',
            'hi': 'hi-IN',
            'zh': 'zh-CN',
            'ru': 'ru-RU',
            'sw': 'sw-KE'
        };
        
        return languageCodes[lang] || 'en-US';
    }

    /**
     * Set up form handlers and validation
     */
    setupFormHandlers() {
        const form = document.querySelector('.symptom-form');
        const symptomsTextarea = document.getElementById('symptoms');
        const analyzeButton = document.getElementById('analyze-btn');

        if (form && symptomsTextarea) {
            // Real-time character count and validation
            symptomsTextarea.addEventListener('input', () => {
                const length = symptomsTextarea.value.length;
                const isValid = length >= 10 && length <= 2000;
                
                // Update button state
                if (analyzeButton) {
                    analyzeButton.disabled = !isValid;
                }
                
                // Add visual feedback
                if (length > 0 && length < 10) {
                    symptomsTextarea.style.borderColor = '#ffc107';
                } else if (length >= 10) {
                    symptomsTextarea.style.borderColor = '#28a745';
                } else {
                    symptomsTextarea.style.borderColor = '#dee2e6';
                }
            });

            // Form submission handler
            form.addEventListener('submit', (e) => {
                const symptoms = symptomsTextarea.value.trim();
                
                if (symptoms.length < 10) {
                    e.preventDefault();
                    alert('Please provide a more detailed description of your symptoms (at least 10 characters).');
                    symptomsTextarea.focus();
                    return;
                }

                // Show loading state
                if (analyzeButton) {
                    analyzeButton.disabled = true;
                    analyzeButton.innerHTML = '<i class="fas fa-spinner fa-spin" aria-hidden="true"></i> Analyzing...';
                }
            });
        }
    }

    /**
     * Set up accessibility features
     */
    setupAccessibilityFeatures() {
        // Add skip link
        this.addSkipLink();
        
        // Enhance keyboard navigation
        this.enhanceKeyboardNavigation();
        
        // Set up focus management
        this.setupFocusManagement();
        
        // Add ARIA live regions for dynamic content
        this.setupLiveRegions();
    }

    /**
     * Add skip navigation link
     */
    addSkipLink() {
        if (document.querySelector('.skip-link')) return; // Already exists
        
        const skipLink = document.createElement('a');
        skipLink.href = '#main';
        skipLink.className = 'skip-link';
        skipLink.textContent = 'Skip to main content';
        
        document.body.insertBefore(skipLink, document.body.firstChild);
        
        // Ensure main content has proper ID
        const main = document.querySelector('main');
        if (main && !main.id) {
            main.id = 'main';
        }
    }

    /**
     * Enhance keyboard navigation
     */
    enhanceKeyboardNavigation() {
        // Add keyboard support for voice button
        const voiceButton = document.getElementById('voice-btn');
        if (voiceButton) {
            voiceButton.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    this.toggleVoiceRecognition();
                }
            });
        }
        
        // Escape key to stop voice recognition
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.isListening) {
                this.recognition.stop();
            }
        });
    }

    /**
     * Set up focus management
     */
    setupFocusManagement() {
        // Focus management for form submission
        const form = document.querySelector('.symptom-form');
        if (form) {
            form.addEventListener('submit', () => {
                // Focus will be managed by server response
                setTimeout(() => {
                    const errorMessage = document.querySelector('.flash-message');
                    const resultsSection = document.querySelector('.results-section');
                    
                    if (errorMessage) {
                        errorMessage.focus();
                    } else if (resultsSection) {
                        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
                    }
                }, 100);
            });
        }
    }

    /**
     * Set up ARIA live regions for dynamic content
     */
    setupLiveRegions() {
        // Voice status is already set up as aria-live
        // Add any additional live regions as needed
    }

    /**
     * Set up offline detection and notification
     */
    setupOfflineDetection() {
        // Check if app works offline (when Ollama is local)
        window.addEventListener('online', () => {
            console.log('Connection restored');
        });

        window.addEventListener('offline', () => {
            console.log('Connection lost - app continues to work offline');
            this.showOfflineNotification();
        });
    }

    /**
     * Show offline notification
     */
    showOfflineNotification() {
        // Only show if not already shown
        if (document.querySelector('.offline-notification')) return;
        
        const notification = document.createElement('div');
        notification.className = 'flash-message flash-info offline-notification';
        notification.innerHTML = `
            <i class="fas fa-wifi-slash" aria-hidden="true"></i>
            You're offline, but MedHelp continues to work using your local AI model.
        `;
        
        const main = document.querySelector('main');
        if (main) {
            main.insertBefore(notification, main.firstChild);
            
            // Auto-remove after 5 seconds
            setTimeout(() => {
                notification.remove();
            }, 5000);
        }
    }

    /**
     * Character limit display for accessibility
     */
    setupCharacterCount() {
        const symptomsTextarea = document.getElementById('symptoms');
        if (!symptomsTextarea) return;
        
        const counter = document.createElement('div');
        counter.id = 'char-counter';
        counter.className = 'help-text';
        counter.setAttribute('aria-live', 'polite');
        
        symptomsTextarea.parentNode.insertBefore(counter, symptomsTextarea.nextSibling);
        
        const updateCounter = () => {
            const length = symptomsTextarea.value.length;
            const remaining = 2000 - length;
            counter.textContent = `${length}/2000 characters (minimum 10 required)`;
            
            if (remaining < 100) {
                counter.style.color = '#dc3545';
            } else if (length < 10) {
                counter.style.color = '#ffc107';
            } else {
                counter.style.color = '#28a745';
            }
        };
        
        symptomsTextarea.addEventListener('input', updateCounter);
        updateCounter(); // Initial update
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const app = new MedHelpApp();
    
    // Expose app instance globally for debugging
    window.MedHelpApp = app;
    
    // Set up character counter
    app.setupCharacterCount();
});

// Service worker registration for offline capability (if needed)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        // Skip service worker for now as we're running locally
        console.log('Service worker capability available but not implemented');
    });
}

// Emergency contact helper
function callEmergency(number) {
    if (confirm(`Call ${number} for emergency services?`)) {
        window.location.href = `tel:${number}`;
    }
}

// Print functionality enhancement
function printResults() {
    // Hide non-essential elements before printing
    const elementsToHide = [
        '.action-buttons',
        '.voice-button',
        '.footer'
    ];
    
    elementsToHide.forEach(selector => {
        const elements = document.querySelectorAll(selector);
        elements.forEach(el => el.style.display = 'none');
    });
    
    window.print();
    
    // Restore elements after printing
    setTimeout(() => {
        elementsToHide.forEach(selector => {
            const elements = document.querySelectorAll(selector);
            elements.forEach(el => el.style.display = '');
        });
    }, 1000);
}

// Utility function to copy results to clipboard
function copyToClipboard() {
    const resultsContent = document.querySelector('main').innerText;
    
    if (navigator.clipboard) {
        navigator.clipboard.writeText(resultsContent).then(() => {
            alert('Results copied to clipboard');
        }).catch(err => {
            console.error('Could not copy text: ', err);
            fallbackCopyTextToClipboard(resultsContent);
        });
    } else {
        fallbackCopyTextToClipboard(resultsContent);
    }
}

function fallbackCopyTextToClipboard(text) {
    const textArea = document.createElement('textarea');
    textArea.value = text;
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    
    try {
        document.execCommand('copy');
        alert('Results copied to clipboard');
    } catch (err) {
        console.error('Fallback copy failed', err);
        alert('Could not copy to clipboard');
    }
    
    document.body.removeChild(textArea);
}
