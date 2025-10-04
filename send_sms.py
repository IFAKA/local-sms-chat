#!/usr/bin/env python3
"""Simple script to send SMS using the project's SMS service."""
import sys
import argparse
from src.services.sms_service import SMSService
from src.utils.device_manager import DeviceManager

def main():
    parser = argparse.ArgumentParser(description='Send SMS message')
    parser.add_argument('phone_number', help='Phone number to send SMS to')
    parser.add_argument('message', help='Message to send')
    
    args = parser.parse_args()
    
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
    
    # Initialize SMS service
    sms_service = SMSService(device_id)
    
    # Send SMS
    print(f"📤 Sending SMS to {args.phone_number}...")
    success = sms_service.send_sms(args.phone_number, args.message)
    
    if success:
        print(f"✅ SMS sent successfully to {args.phone_number}")
    else:
        print(f"❌ Failed to send SMS to {args.phone_number}")
        sys.exit(1)

if __name__ == "__main__":
    main()
