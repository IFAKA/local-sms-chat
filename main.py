#!/usr/bin/env python3
"""Main entry point for LocalSMS Chatbot with clean architecture."""
import sys
import logging
from src.core.chatbot import LocalSMSChatbot
from src.utils.device_manager import DeviceManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('chatbot.log'),
        logging.StreamHandler()
    ]
)

def main():
    """Main function."""
    print("🤖 LocalSMS Chatbot - Clean Architecture")
    print("=" * 50)
    
    # Check ADB connection
    if not DeviceManager.check_adb_connection():
        print("❌ No ADB device connected")
        print("   Please connect your Android device and enable USB debugging")
        sys.exit(1)
    
    # Get device ID
    device_id = DeviceManager.get_main_device_id()
    if not device_id:
        print("❌ No main device found")
        print("   Please disconnect pairing connections")
        sys.exit(1)
    
    print(f"✅ Connected to device: {device_id}")
    
    # Initialize chatbot
    chatbot = LocalSMSChatbot(
        device_id=device_id,
        model_name="llama3:latest",
        db_path="sessions.db"
    )
    
    # Run chatbot
    try:
        chatbot.run(poll_interval=2)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
