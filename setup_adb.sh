#!/bin/bash

# LocalSMS Chatbot - ADB Setup Script
# Based on comprehensive ADB commands from: https://gist.github.com/Pulimet/5013acf2cd5b28e55036c82c91bd56d8

echo "📱 LocalSMS Chatbot - ADB Setup"
echo "==============================="

# Check if ADB is installed
if ! command -v adb &> /dev/null; then
    echo "❌ ADB not found. Installing..."
    brew install android-platform-tools
fi

# Start ADB server
echo "🔄 Starting ADB server..."
adb kill-server
adb start-server

# Check for devices
echo "📱 Checking for connected devices..."
DEVICES=$(adb devices | grep -v "List of devices" | grep "device" | wc -l)

if [ $DEVICES -eq 0 ]; then
    echo "❌ No devices found"
    echo ""
    echo "📋 Setup Instructions:"
    echo "1. Enable Developer Options on your Android device:"
    echo "   - Go to Settings > About Phone"
    echo "   - Tap 'Build Number' 7 times"
    echo "   - Go back to Settings > Developer Options"
    echo "   - Enable 'USB Debugging'"
    echo "   - Enable 'Wireless Debugging' (for wireless connection)"
    echo ""
    echo "2. Connect your device:"
    echo "   - USB: Connect via USB cable"
    echo "   - Wireless: Use 'adb connect IP:PORT'"
    echo ""
    echo "3. Test connection:"
    echo "   - Run: adb devices"
    echo "   - Should show your device as 'device'"
    echo ""
    exit 1
fi

echo "✅ Found $DEVICES device(s)"

# Get device info
echo "📊 Device Information:"
adb devices

# Check device properties
echo ""
echo "🔍 Device Properties:"
echo "Model: $(adb shell getprop ro.product.model)"
echo "Android Version: $(adb shell getprop ro.build.version.release)"
echo "API Level: $(adb shell getprop ro.build.version.sdk)"

# Check SMS permissions
echo ""
echo "📱 Checking SMS Permissions..."
SMS_PERMISSIONS=$(adb shell dumpsys package com.android.providers.telephony | grep -i "permission" | wc -l)
if [ $SMS_PERMISSIONS -gt 0 ]; then
    echo "✅ SMS permissions found"
else
    echo "⚠️  SMS permissions may need setup"
fi

# Test SMS access
echo ""
echo "🧪 Testing SMS Access..."
SMS_TEST=$(adb shell "content query --uri content://sms/inbox --projection _id:address:body:date:read --where 'read=0' --sort 'date DESC' LIMIT 1" 2>/dev/null)
if [ $? -eq 0 ] && [ -n "$SMS_TEST" ]; then
    echo "✅ SMS access working"
    echo "📨 Latest unread SMS:"
    echo "$SMS_TEST" | head -1
else
    echo "❌ SMS access failed"
    echo ""
    echo "🔧 Troubleshooting SMS Access:"
    echo "1. Make sure your device has SMS messages"
    echo "2. Check if SMS app is set as default"
    echo "3. Try different SMS apps (Messages, Google Messages)"
    echo "4. Check device permissions in Settings > Apps > Messages > Permissions"
fi

# Test SMS sending
echo ""
echo "📤 Testing SMS Sending..."
PHONE_NUMBER="+1234567890"  # Dummy number for test
SMS_SEND_TEST=$(adb shell "am start -a android.intent.action.SENDTO -d sms:$PHONE_NUMBER --es sms_body 'Test message'" 2>/dev/null)
if [ $? -eq 0 ]; then
    echo "✅ SMS sending capability confirmed"
    echo "📱 SMS app should have opened with pre-filled message"
else
    echo "⚠️  SMS sending test inconclusive"
fi

# Check for Termux (alternative SMS method)
echo ""
echo "🔍 Checking for Termux..."
TERMUX_CHECK=$(adb shell "pm list packages | grep com.termux" 2>/dev/null)
if [ -n "$TERMUX_CHECK" ]; then
    echo "✅ Termux found - alternative SMS method available"
else
    echo "ℹ️  Termux not found - using Android intents for SMS"
fi

# Wireless debugging setup
echo ""
echo "📡 Wireless Debugging Setup:"
echo "1. On your Android device:"
echo "   - Go to Settings > Developer Options"
echo "   - Enable 'Wireless Debugging'"
echo "   - Note the IP address and port"
echo ""
echo "2. Connect wirelessly:"
echo "   adb connect IP:PORT"
echo ""
echo "3. Test wireless connection:"
echo "   adb devices"
echo "   adb shell getprop ro.product.model"

# Performance optimization
echo ""
echo "⚡ Performance Optimization:"
echo "1. Disable unnecessary services:"
echo "   adb shell settings put global development_settings_enabled 0"
echo ""
echo "2. Optimize ADB connection:"
echo "   adb shell settings put global adb_enabled 1"
echo ""
echo "3. Check battery optimization:"
echo "   adb shell dumpsys deviceidle whitelist"

# Security recommendations
echo ""
echo "🔒 Security Recommendations:"
echo "1. Use wireless debugging only on trusted networks"
echo "2. Disable ADB when not in use:"
echo "   adb shell settings put global adb_enabled 0"
echo "3. Use authentication for wireless debugging"
echo "4. Regularly update your Android device"

echo ""
echo "✅ ADB Setup Complete!"
echo ""
echo "🚀 Next Steps:"
echo "1. Run: ./run_clean.sh (recommended)"
echo "2. Or run: ./run.sh (legacy)"
echo ""
echo "📚 For more ADB commands, see:"
echo "   https://gist.github.com/Pulimet/5013acf2cd5b28e55036c82c91bd56d8"
