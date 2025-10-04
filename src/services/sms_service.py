"""SMS service for reading and sending SMS messages."""
import subprocess
import logging
import time
from typing import Optional, List
from ..models.sms import SMSMessage

logger = logging.getLogger(__name__)


class SMSService:
    """Service for SMS operations via ADB."""
    
    def __init__(self, device_id: str):
        self.device_id = device_id
    
    def read_unread_sms(self) -> Optional[SMSMessage]:
        """Read the latest unread SMS message."""
        try:
            result = subprocess.run(
                ['adb', '-s', self.device_id, 'shell', 
                 'content query --uri content://sms/inbox --projection _id:address:body:date:read --where "read=0" --sort "date DESC"'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode != 0:
                logger.error(f"ADB command failed: {result.stderr}")
                return None
            
            if not result.stdout.strip():
                return None
            
            # Parse the first (most recent) unread message
            lines = result.stdout.strip().split('\n')
            if not lines or not lines[0].startswith('Row:'):
                return None
            
            latest_line = lines[0]
            parts = latest_line.split(', ')
            sms_data = {}
            
            for part in parts:
                if '=' in part:
                    key, value = part.split('=', 1)
                    if '_id=' in part:
                        sms_data['id'] = value
                    elif key == 'address':
                        sms_data['number'] = value
                    elif key == 'body':
                        sms_data['body'] = value
                    elif key == 'date':
                        sms_data['date'] = value
                    elif key == 'read':
                        sms_data['read'] = value
            
            return SMSMessage.from_dict(sms_data)
            
        except subprocess.TimeoutExpired:
            logger.error("ADB command timed out")
            return None
        except Exception as e:
            logger.error(f"Error reading SMS: {e}")
            return None
    
    def send_sms(self, phone_number: str, message: str) -> bool:
        """Send SMS message using proper Android methods."""
        try:
            # Truncate message to SMS limit
            if len(message) > 160:
                message = message[:157] + "..."
            
            # Escape quotes and special characters
            escaped_message = message.replace("'", "\\'").replace('"', '\\"')
            
            # Method 1: Use Termux SMS API via broadcast (most reliable)
            result = subprocess.run(
                ['adb', '-s', self.device_id, 'shell', 
                 f'am broadcast -a com.termux.api.SEND_SMS -e number {phone_number} -e text "{escaped_message}"'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                logger.info(f"SMS sent successfully via Termux broadcast")
                return True
            
            # Method 1b: Use Termux app directly with command
            result = subprocess.run(
                ['adb', '-s', self.device_id, 'shell', 
                 f'am start -n com.termux/.HomeActivity -e command "termux-sms-send -n {phone_number} \\"{escaped_message}\\""'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                logger.info(f"SMS sent successfully via Termux app")
                return True
            
            # Method 2: Use Android SMS Manager via shell command
            # Create a temporary script to send SMS using Android's SmsManager
            script_content = f'''
import android
droid = android.Android()
droid.smsSend("{phone_number}", "{escaped_message}")
'''
            
            # Write script to device
            subprocess.run(
                ['adb', '-s', self.device_id, 'shell', 'echo', f'"{script_content}"', '>', '/data/local/tmp/send_sms.py'],
                capture_output=True,
                timeout=5
            )
            
            # Execute script
            result = subprocess.run(
                ['adb', '-s', self.device_id, 'shell', 'python', '/data/local/tmp/send_sms.py'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                logger.info(f"SMS sent successfully via Android SMS Manager")
                return True
            
            # Method 3: Use content insert to add SMS to outbox (corrected syntax)
            result = subprocess.run(
                ['adb', '-s', self.device_id, 'shell', 
                 f'content insert --uri content://sms/outbox --bind address:s:"{phone_number}" --bind body:s:"{escaped_message}" --bind type:i:2 --bind date:l:{int(time.time() * 1000)}'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                logger.info(f"SMS added to outbox")
                return True
            
            # Method 4: Fallback to intent (opens SMS app)
            result = subprocess.run(
                ['adb', '-s', self.device_id, 'shell', 
                 f'am start -a android.intent.action.SENDTO -d sms:{phone_number} --es sms_body "{escaped_message}"'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                logger.warning(f"SMS app opened with message (manual send required)")
                return True
            
            logger.error(f"All SMS sending methods failed")
            return False
            
        except Exception as e:
            logger.error(f"Error sending SMS: {e}")
            return False
    
    def mark_sms_read(self, sms_id: str) -> bool:
        """Mark SMS as read using multiple ADB methods."""
        if not sms_id:
            return False
            
        try:
            # Method 1: Direct content update (most reliable)
            result = subprocess.run(
                ['adb', '-s', self.device_id, 'shell', 
                 f'content update --uri content://sms/inbox --bind read:i:1 --where "_id={sms_id}"'],
                capture_output=True,
                timeout=2
            )
            if result.returncode == 0:
                return True
            
            # Method 2: Alternative syntax
            result = subprocess.run(
                ['adb', '-s', self.device_id, 'shell', 
                 f'content update --uri content://sms/inbox --bind read:i:1 --where "_id=\'{sms_id}\'"'],
                capture_output=True,
                timeout=2
            )
            if result.returncode == 0:
                return True
            
            # Method 3: Using SQLite directly (if available)
            result = subprocess.run(
                ['adb', '-s', self.device_id, 'shell', 
                 f'sqlite3 /data/data/com.android.providers.telephony/databases/telephony.db "UPDATE sms SET read=1 WHERE _id={sms_id}"'],
                capture_output=True,
                timeout=2
            )
            if result.returncode == 0:
                return True
                
            return False
            
        except Exception as e:
            logger.error(f"Failed to mark SMS as read: {e}")
            return False
