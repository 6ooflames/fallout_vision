# Fallout Vision 🎮👁️

AI-powered game assistant for Fallout 4 that analyzes gameplay in real-time using screen capture and LLM vision capabilities.

## 🚀 Features

- **KDE Native Screen Capture** - Zero filesystem dependency, direct memory capture
- **Window Targeting** - Automatically finds and captures Fallout 4 window
- **AI Vision Analysis** - Get insights from your gameplay using Ollama/local LLMs
- **Auto & Interactive Modes** - Scheduled captures or manual triggering
- **Privacy First** - All processing happens locally, no cloud dependencies

## 📋 Requirements

### System Requirements
- Linux (KDE Plasma recommended)
- Qt5/PyQt5 installed
- Python 3.8+

### Python Dependencies
```bash
pip install -r requirements.txt
```

## 🔧 Installation

1. **Clone/Download the project:**
```bash
cd /home/david/Code/projects/fallout_vision
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Ensure Ollama is running:**
```bash
ollama serve
ollama pull llama3.2-vision
```

## ▶️ Usage

### Auto Mode (Continuous Monitoring)
```bash
python vision_analyze_v2.py auto
```
- Captures screen every 30 seconds
- Automatically analyzes and provides insights

### Interactive Mode (Manual Trigger)
```bash
python vision_analyze_v2.py interactive
```
- Type `capture` to take a screenshot
- Type `quit` to exit
- Full control over when to analyze

### Direct Screen Capture Testing
```bash
python screen_capture_kde.py
```
- Test screen capture functionality independently
- Outputs captured images to `/tmp/fallout_vision/`

## 🛠️ Technical Details

### Screen Capture Architecture
- **Qt QScreen API** - Native KDE/Qt integration
- **In-Memory Processing** - No filesystem writes during operation
- **Thread-Safe** - Non-blocking capture via QThread
- **Window Targeting** - Searches for "Fallout 4" window by title

### AI Analysis Pipeline
1. Capture screen via Qt
2. Convert to base64/bytes
3. Send to Ollama vision endpoint
4. Receive and display analysis

## 📁 Project Structure

```
fallout_vision/
├── screen_capture_kde.py      # KDE native screen capture module
├── vision_analyze.py          # Original analysis script (FS-based)
├── vision_analyze_v2.py       # Integrated version (no FS)
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## 🎮 Gameplay Examples

### Typical Analysis Outputs

**Combat Detection:**
> "Detected enemy encounter at coordinates. Recommend taking cover behind the wall at 3 o'clock. Your weapon is currently depleted."

**Resource Identification:**
> "Workbench detected. Available materials: steel x12, glass x5. Can craft: Combat Knife, Stimpaks."

**Quest Progress:**
> "NPC conversation in progress. Dialogue option highlighted: Ask about the Institute. This appears to be a critical quest decision point."

## 🔒 Privacy & Security

- **Local Processing** - All screen captures and AI processing stay on your machine
- **No Cloud Uploads** - Ollama runs locally by default
- **Temporary Storage** - Images are held in memory, not saved to disk

## 🐛 Troubleshooting

### Screen Capture Not Working
```bash
# Check if Qt5 is installed
qmake --version

# Check window detection
python screen_capture_kde.py test
```

### Ollama Not Responding
```bash
# Ensure Ollama server is running
ollama serve

# Check if vision model is available
ollama list
```

### Permission Issues
```bash
# Add X11 permissions if needed
xhost +local:root
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📝 License

MIT License - Feel free to use and modify for your own projects.

## 🔗 Related Projects

- [Ollama](https://ollama.ai/) - Local LLM inference
- [KDE Plasma](https://kde.org/) - Desktop environment
- [Fallout 4](https://fallout.4game.com/) - The game

---

**Created by:** David's Code Projects  
**Last Updated:** 2024  
**Status:** Active Development 🚀
