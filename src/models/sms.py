"""SMS data models and types."""
from dataclasses import dataclass
from typing import Optional, Dict, Any
from datetime import datetime


@dataclass
class SMSMessage:
    """SMS message data structure."""
    id: str
    phone_number: str
    body: str
    date: int
    read: bool = False
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SMSMessage':
        """Create SMSMessage from dictionary."""
        return cls(
            id=data.get('id', ''),
            phone_number=data.get('number', ''),
            body=data.get('body', ''),
            date=int(data.get('date', '0')),
            read=data.get('read', '0') == '1'
        )


@dataclass
class ConversationContext:
    """Conversation context for a phone number."""
    phone_number: str
    last_input: str
    context: str
    created_at: datetime
    updated_at: datetime
