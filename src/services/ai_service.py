"""AI service for generating responses using Ollama."""
import logging
from typing import Optional
from ollama import Client

logger = logging.getLogger(__name__)


class AIService:
    """Service for AI response generation."""
    
    def __init__(self, model_name: str = "llama3:latest"):
        self.model_name = model_name
        self.client = Client()
    
    def generate_response(self, user_input: str, context: Optional[str] = None) -> str:
        """Generate AI response for user input."""
        try:
            # Create context-aware prompt
            if context:
                prompt = f"Previous conversation:\n{context}\n\nNew message: {user_input}\n\nRespond as a helpful AI assistant:"
            else:
                prompt = f"User: {user_input}\n\nRespond as a helpful AI assistant:"
            
            # Generate response using Ollama
            response = self.client.generate(
                model=self.model_name,
                prompt=prompt,
                stream=False
            )
            
            return response['response']
            
        except Exception as e:
            logger.error(f"AI generation failed: {e}")
            return "Sorry, I'm having trouble generating a response. Please try again."
