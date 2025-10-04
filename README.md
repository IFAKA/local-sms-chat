# 🤖 LocalSMS Chatbot

A **100% local, SMS-based AI chatbot** that enables users on any feature phone to interact with an AI assistant via SMS, using natural language processing powered by a locally hosted large language model (Ollama).

## 🏗️ Project Structure

```
local-sms-chat/
├── 📦 Scripts
│   ├── install.sh          # Complete installation
│   ├── run.sh              # Run chatbot
│   ├── setup_adb.sh        # ADB setup & testing
│   └── uninstall.sh        # Complete removal
├── 🏗️ Clean Architecture
│   └── src/
│       ├── core/           # Business logic
│       │   └── chatbot.py  # Main orchestration
│       ├── services/       # Service layer
│       │   ├── sms_service.py      # SMS operations
│       │   ├── ai_service.py       # AI generation
│       │   └── database_service.py # Database operations
│       ├── models/         # Data models
│       │   └── sms.py      # SMS & conversation models
│       └── utils/          # Utilities
│           └── device_manager.py  # ADB management
├── 📚 Documentation
│   └── README.md           # This file
├── 🚀 Entry Points
│   ├── main.py             # Clean architecture entry
│   └── chatbot_sms.py      # Legacy monolithic version
```

## 🚀 Quick Start

### **1. Install Everything**
```bash
./install.sh
```

### **2. Run Chatbot**
```bash
./run.sh
```

### **3. Uninstall Everything**
```bash
./uninstall.sh
```

> **Smart Uninstall**: The uninstall script only removes software that was installed by this project, preserving any pre-existing installations.

## 🏗️ Architecture

### **Clean Architecture (Recommended)**
- **Modular Design**: 8 focused files vs 1 monolithic file
- **Separation of Concerns**: Each layer has specific responsibilities
- **Testability**: Easy to unit test individual components
- **Maintainability**: Changes to one layer don't affect others
- **Scalability**: Easy to add new features

### **Legacy Architecture**
- Single monolithic file (`chatbot_sms.py`)
- All functionality in one place
- Harder to maintain and test

## 📱 Setup Requirements

### **Hardware**
- **Laptop**: 8GB+ RAM, macOS/Linux/Windows
- **Smartphone**: Android with SIM card
- **Feature Phone**: Any phone with SMS capability

### **Software**
- **Python 3.13.5** (via pyenv)
- **Ollama** (local LLM)
- **ADB** (Android Debug Bridge)
- **spaCy** (offline NLP)

## 🔧 ADB Commands Integration

This project uses comprehensive ADB commands for SMS operations. For a complete reference, see:

**[📚 Complete ADB Commands Gist](https://gist.github.com/Pulimet/5013acf2cd5b28e55036c82c91bd56d8)**

### **Key ADB Commands Used**

#### **SMS Reading**
```bash
# Read unread SMS
adb shell "content query --uri content://sms/inbox --projection _id:address:body:date:read --where 'read=0' --sort 'date DESC'"
```

#### **SMS Sending**
```bash
# Send SMS via Android intent
adb shell "am start -a android.intent.action.SENDTO -d sms:PHONE_NUMBER --es sms_body 'MESSAGE'"

# Alternative: Termux SMS
adb shell "termux-sms-send -n PHONE_NUMBER 'MESSAGE'"
```

#### **Mark SMS as Read**
```bash
# Method 1: Content provider
adb shell "content update --uri content://sms/inbox --bind read:i:1 --where '_id=SMS_ID'"

# Method 2: SQLite direct
adb shell "sqlite3 /data/data/com.android.providers.telephony/databases/telephony.db 'UPDATE sms SET read=1 WHERE _id=SMS_ID'"
```

#### **Device Management**
```bash
# List devices
adb devices

# Connect wirelessly
adb connect IP:PORT

# Enable wireless debugging
adb tcpip 5555
```

## 🔄 Data Flow

```
Feature Phone → Android Phone → Laptop → AI Response
    (SMS)    →   (ADB)     → (Ollama) →   (SMS)
```

1. **User sends**: `"CHAT: Tell me a joke"` from feature phone
2. **Android receives**: SMS via SIM card
3. **Laptop reads**: SMS via ADB content provider
4. **AI processes**: With Ollama (LLaMA 3) + conversation context
5. **Laptop sends**: AI response back via ADB
6. **User receives**: `"Why did the scarecrow win an award? Because he was outstanding in his field!"`

## 🎯 Features

### **Core Features**
- ✅ **100% Local**: No external APIs or internet required
- ✅ **SMS Gateway**: Uses Android phone as SMS gateway
- ✅ **AI Responses**: Powered by Ollama (LLaMA 3)
- ✅ **Conversation Memory**: Remembers context per phone number
- ✅ **Feature Phone Compatible**: Works with any SMS-capable phone
- ✅ **Toll-Free for User**: User pays no SMS costs

### **Technical Features**
- ✅ **Clean Architecture**: Modular, testable, maintainable
- ✅ **ADB Integration**: Comprehensive Android debugging
- ✅ **Database Management**: SQLite for conversation context
- ✅ **Error Handling**: Robust error recovery
- ✅ **Logging**: Comprehensive logging system

## 📊 Architecture Comparison

| Aspect | Legacy | Clean Architecture |
|--------|--------|-------------------|
| **Files** | 1 monolithic file | 8 modular files |
| **Lines** | ~500 lines | ~200 lines total |
| **Testability** | Hard to test | Easy to unit test |
| **Maintainability** | Complex | Simple |
| **Scalability** | Limited | Highly scalable |
| **Readability** | Mixed concerns | Clear separation |

## 🛠️ Development

### **Adding New Features**

1. **New Service**: Add to `src/services/`
2. **New Model**: Add to `src/models/`
3. **New Utility**: Add to `src/utils/`
4. **Core Logic**: Modify `src/core/chatbot.py`

### **Testing**
```bash
# Test ADB connection
./setup_adb.sh

# Test SMS reading
adb shell "content query --uri content://sms/inbox --projection _id:address:body:date:read --where 'read=0' --sort 'date DESC' LIMIT 1"

# Test Ollama
ollama run llama3 "Tell me a joke"
```

## 🆘 Troubleshooting

### **Common Issues**

1. **ADB Device Not Found**
   ```bash
   adb kill-server
   adb start-server
   adb devices
   ```

2. **SMS Not Being Read**
   - Check Android permissions
   - Verify SMS app is default
   - Try different ADB methods

3. **Ollama Model Not Found**
   ```bash
   ollama pull llama3:latest
   ```

4. **Database Errors**
   - Check file permissions
   - Verify SQLite installation
   - Try recreating database

### **Debug Commands**

```bash
# Check ADB connection
adb devices

# Check SMS permissions
adb shell dumpsys package com.android.providers.telephony

# Check Ollama status
ollama list

# Check database
sqlite3 sessions.db ".tables"
```

## 🔗 References

- **[ADB Commands Gist](https://gist.github.com/Pulimet/5013acf2cd5b28e55036c82c91bd56d8)** - Comprehensive ADB command reference
- **[Ollama Documentation](https://ollama.ai/)** - Local LLM framework
- **[Android Content Providers](https://developer.android.com/guide/topics/providers/content-providers)** - SMS access
- **[spaCy Documentation](https://spacy.io/)** - Offline NLP

## 📝 License

MIT License - Feel free to use and modify for your projects.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

**Built with ❤️ for bridging the digital divide**