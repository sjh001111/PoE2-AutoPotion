# PoE2 AutoPotion

A real-time health management system for Path of Exile 2 that uses memory reading and automated input injection to maintain optimal HP/MP/ES levels during gameplay.

## ✨ Features

- 🩸 **HP Auto-heal**: Automatically uses health potions when HP drops below 60%
- 🔮 **MP Management**: Triggers mana potions when MP falls below 70%
- 🛡️ **Energy Shield Support**: ES monitoring with Eternal Youth passive compatibility
- 🚨 **Emergency Safety**: Auto-escape (ESC key) when ES drops critically low (25%)
- ⚡ **Real-time Monitoring**: 200ms polling rate for responsive healing
- 🎯 **Non-intrusive**: Uses memory reading instead of screen capture

## 🛠️ Tech Stack

- **Python 3.11+** - Core programming language
- **pymem** - Process memory manipulation and reading
- **win32api/win32gui** - Windows API for input injection and window handling
- **asyncio** - Asynchronous programming for concurrent monitoring routines
- **Memory forensics** - Multi-level pointer chain resolution

## 🔧 How it Works

### Memory Architecture
```python
Base Address: PathOfExileSteam.exe + 0x3B8FEE8
Pointer Chain: [0x70, 0x0, 0x80, 0x2A8, offset]
├── HP: Current (0x1E0), Max (0x1DC)
├── MP: Current (0x230), Max (0x22C)  
└── ES: Current (0x268), Max (0x264)
```

### Multi-threaded Monitoring
- **HP Routine**: Monitors health percentage, triggers '1' key for healing
- **MP Routine**: Watches mana levels, activates '2' key for mana potions
- **ES Routine**: Energy shield management with '1' key (Eternal Youth builds)
- **ES Limit**: Emergency escape mechanism with 120-second cooldown

### Input Injection
Uses `PostMessage` API for clean, undetectable key simulation without interfering with normal gameplay.

## 🚀 Usage

1. **Launch Path of Exile 2** (Steam version)
2. **Run the script**:
   ```bash
   python main.py
   ```
3. **Configure thresholds** (optional):
   ```python
   hp_threshold = 60    # HP heal trigger (%)
   mp_threshold = 70    # MP restore trigger (%)
   es_threshold = 75    # ES management trigger (%)
   es_limit_threshold = 25  # Emergency escape trigger (%)
   ```

## 📋 Requirements

- **Windows OS** (Win32 API dependency)
- **Python 3.11+**
- **Path of Exile 2** (Steam version)
- **Administrator privileges** (for memory access)

### Dependencies
```bash
pip install pymem pywin32
```

## ⚠️ Important Notes

- **Game Updates**: Memory offsets may require updates after patches
- **Terms of Service**: Use at your own risk - may violate game ToS
- **Builds Supported**: Optimized for Eternal Youth ES builds, but works with any character
- **Detection Risk**: While designed to be undetectable, use responsibly

## 🏗️ Architecture

### Core Components
- **Memory Scanner**: Resolves multi-level pointer chains to access game state
- **Health Monitor**: Asynchronous routines for each resource type
- **Input Controller**: Windows API integration for seamless key injection
- **Safety System**: Emergency mechanisms to prevent character death

### Performance
- **CPU Usage**: <1% on modern systems
- **Response Time**: <200ms from threshold trigger to potion use
- **Memory Footprint**: ~10MB

## 🎮 Game Compatibility

- ✅ **Path of Exile 2** (Steam)
- ✅ **Windows 10/11**
- ⚠️ **Eternal Youth Builds** (Enhanced ES support)
- ❌ **Non-Steam versions** (Different process names)

## 📝 License

MIT License

## ⚠️ Disclaimer

This tool is for educational purposes. Users are responsible for compliance with game terms of service and applicable laws.
