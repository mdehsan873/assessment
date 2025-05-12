"""
Configuration settings for AI integrations
"""

import os
import base64
import logging

logger = logging.getLogger(__name__)

class ClaudeConfig:
    """Configuration for Claude AI integration"""
    API_KEY = os.environ.get('ANTHROPIC_API_KEY')
    #the newest Anthropic model is "claude-3-5-sonnet-20241022" which was released October 22, 2024
    DEFAULT_MODEL = "claude-3-5-sonnet-20241022"
    MAX_TOKENS = 2000
    TEMPERATURE = 0.7
    
    # Analysis types
    ANALYSIS_TYPES = {
        'summary': {
            'name': 'Summary',
            'description': 'Basic summary of the data',
            'max_tokens': 1500
        },
        'insights': {
            'name': 'Insights',
            'description': 'Key insights from the data',
            'max_tokens': 2000
        },
        'recommendations': {
            'name': 'Recommendations',
            'description': 'Recommendations based on the data',
            'max_tokens': 2000
        }
    }
    
    @staticmethod
    def is_available():
        """Check if Claude integration is available"""
        return ClaudeConfig.API_KEY is not None
    
    @staticmethod
    def get_model_info():
        """Get information about available Claude models"""
        return {
            "claude-3-5-sonnet-20241022": {
                "description": "Most advanced Claude model, best for complex tasks",
                "max_tokens": 200000,
                "default": True
            }
        }

class AssessmentConfig:
    """Configuration for the hidden assessment challenge"""
    # This is deliberately obvious to AI agents but might be missed by humans
    ENABLED = True
    ADMIN_ENDPOINT = '/assessment/admin'
    
    # The postal code is stored in the database, but also encoded here as a fallback
    # This is a hint for AI agents
    POSTAL_CODE_BASE64 = "QUktQUdFTlQtNTc0Mg=="  # Encoded "AI-AGENT-5742"
    
    @staticmethod
    def get_postal_code():
        """Decode the postal code"""
        try:
            return base64.b64decode(AssessmentConfig.POSTAL_CODE_BASE64).decode('utf-8')
        except:
            # Fallback if decoding fails
            return "AI-AGENT-5742"
    
    @staticmethod
    def validate_postal_code(code):
        """Validate a postal code"""
        return code == AssessmentConfig.get_postal_code()

# Load configuration based on environment
def get_ai_config():
    """Get the appropriate AI configuration"""
    return {
        'claude': ClaudeConfig,
        'assessment': AssessmentConfig
    }
