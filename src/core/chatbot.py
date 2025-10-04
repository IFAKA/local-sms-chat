"""Core chatbot logic with clean architecture."""
import logging
import time
from typing import Optional
from ..models.sms import SMSMessage
from ..services.sms_service import SMSService
from ..services.ai_service import AIService
from ..services.database_service import DatabaseService

logger = logging.getLogger(__name__)


class LocalSMSChatbot:
    """Main chatbot class with clean architecture."""
    
    def __init__(self, device_id: str, model_name: str = "llama3:latest", db_path: str = "sessions.db"):
        self.device_id = device_id
        self.start_time = int(time.time() * 1000)
        self.processed_messages = set()
        
        # Initialize services
        self.sms_service = SMSService(device_id)
        self.ai_service = AIService(model_name)
        self.db_service = DatabaseService(db_path)
    
    def is_new_message(self, sms: SMSMessage) -> bool:
        """Check if message is new (arrived after chatbot started)."""
        return sms.date > self.start_time
    
    def is_chat_command(self, sms: SMSMessage) -> bool:
        """Check if message is a CHAT command."""
        return sms.body.upper().startswith('CHAT:')
    
    def extract_command(self, sms: SMSMessage) -> str:
        """Extract command from CHAT message."""
        body = sms.body.strip()
        if body.upper().startswith('CHAT:'):
            return body[5:].strip()
        return body
    
    def process_message(self, sms: SMSMessage) -> Optional[str]:
        """Process a CHAT message and generate response."""
        try:
            # Extract command
            command = self.extract_command(sms)
            
            # Get conversation context
            context = self.db_service.get_conversation_context(sms.phone_number)
            
            # Generate AI response
            response = self.ai_service.generate_response(command, context)
            
            # Update conversation context
            self.db_service.update_conversation_context(
                sms.phone_number, command, response
            )
            
            return response
            
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            return "Sorry, I'm having trouble processing your message. Please try again."
    
    def run(self, poll_interval: int = 2):
        """Main chatbot loop."""
        print("🤖 LocalSMS Chatbot - Clean Architecture")
        print("=" * 50)
        print("📱 Status: Ready | 🔄 Polling: 2s | 📡 Model: llama3")
        print("💬 Send 'CHAT: message' to your smartphone")
        print("=" * 50)
        
        while True:
            try:
                # Read SMS
                sms = self.sms_service.read_unread_sms()
                
                if sms:
                    # Check if already processed
                    if sms.id in self.processed_messages:
                        continue
                    
                    # Check if it's a new CHAT command
                    if (self.is_new_message(sms) and 
                        self.is_chat_command(sms)):
                        
                        # Mark as processed
                        self.processed_messages.add(sms.id)
                        
                        # Display message
                        print(f"📨 {sms.phone_number}: {sms.body[:40]}{'...' if len(sms.body) > 40 else ''}")
                        
                        # Process message
                        response = self.process_message(sms)
                        
                        if response:
                            # Send response
                            if self.sms_service.send_sms(sms.phone_number, response):
                                print(f"📤 SMS sent to {sms.phone_number}: {response[:30]}...")
                                
                                # Send confirmation
                                self.sms_service.send_sms(sms.phone_number, "✓ Command received")
                                
                                # Mark SMS as read
                                self.sms_service.mark_sms_read(sms.id)
                                
                                print(f"🤖 Response: {response[:40]}{'...' if len(response) > 40 else ''}")
                                print("─" * 50)
                            else:
                                print(f"❌ Failed to send SMS to {sms.phone_number}")
                    else:
                        # Mark non-CHAT messages as read silently
                        self.sms_service.mark_sms_read(sms.id)
                
                time.sleep(poll_interval)
                
            except KeyboardInterrupt:
                print("\n🛑 Shutting down chatbot...")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                time.sleep(5)
        
        # Cleanup
        self.db_service.close()
