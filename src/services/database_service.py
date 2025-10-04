"""Database service for conversation management."""
import sqlite3
import logging
from typing import Optional
from datetime import datetime
from ..models.sms import ConversationContext

logger = logging.getLogger(__name__)


class DatabaseService:
    """Service for database operations."""
    
    def __init__(self, db_path: str = "sessions.db"):
        self.db_path = db_path
        self.db = None
        self._init_database()
    
    def _init_database(self):
        """Initialize SQLite database."""
        try:
            self.db = sqlite3.connect(self.db_path, timeout=30.0)
            self.db.execute('PRAGMA journal_mode=WAL')
            self.db.execute('''
                CREATE TABLE IF NOT EXISTS sessions (
                    phone TEXT PRIMARY KEY,
                    last_input TEXT,
                    context TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            self.db.commit()
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            self.db = None
    
    def get_conversation_context(self, phone_number: str) -> Optional[str]:
        """Get conversation context for a phone number."""
        if not self.db:
            return None
            
        try:
            cursor = self.db.execute(
                'SELECT context FROM sessions WHERE phone = ?',
                (phone_number,)
            )
            result = cursor.fetchone()
            return result[0] if result else None
        except Exception as e:
            logger.error(f"Failed to get context: {e}")
            return None
    
    def update_conversation_context(self, phone_number: str, input_text: str, response: str) -> bool:
        """Update conversation context."""
        if not self.db:
            return False
            
        try:
            # Get existing context
            existing_context = self.get_conversation_context(phone_number) or ""
            
            # Add new interaction to context
            new_context = f"{existing_context}\nUser: {input_text}\nAssistant: {response}".strip()
            
            # Update or insert
            self.db.execute('''
                INSERT OR REPLACE INTO sessions (phone, last_input, context, updated_at)
                VALUES (?, ?, ?, ?)
            ''', (phone_number, input_text, new_context, datetime.now()))
            
            self.db.commit()
            return True
        except Exception as e:
            logger.error(f"Failed to update context: {e}")
            return False
    
    def close(self):
        """Close database connection."""
        if self.db:
            self.db.close()
