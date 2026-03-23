#!/usr/bin/env python3
"""
Fallout Vision CLI - Fast TUI for screen capture + vision analysis
Quick terminal-based interface, callable from bash
"""

import sys
import io
import base64
import argparse
import time
from datetime import datetime

try:
    from PyQt6.QtWidgets import QApplication
    from PyQt6.QtGui import QImage
    from PyQt6.QtCore import Qt
    PyQt6_AVAILABLE = True
except ImportError:
    PyQt6_AVAILABLE = False
    print("[ERROR] PyQt6 not installed. Install with: pip install PyQt6")
    sys.exit(1)

try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False
    print("[ERROR] ollama not installed. Install with: pip install ollama")
    sys.exit(1)

# === Configuration ===
CONFIG = {
    "game_window": "Fallout 4",
    "capture_region": "window",
    "model_name": "qwen3.5:2b",
    "vision_prompt": "Analyze this Fallout 4 screenshot. Be concise - key threats, items, location in 2-3 sentences max."
}

class FastCapture:
    """Simplified KDE screen capture - no threading, direct call"""
    
    @staticmethod
    def capture(target_window=None):
        """Capture screen or window, return bytes"""
        app = QApplication.instance() or QApplication([])
        screens = app.screens()
        
        if not screens:
            print("[CAPTURE] No screens found")
            return None
        
        primary = app.primaryScreen()
        image = primary.grabWindow(0)
        
        # Convert to bytes
        buffer = io.BytesIO()
        image.save(buffer, format='PNG')
        buffer.seek(0)
        return buffer.getvalue()

def analyze_vision(image_bytes, prompt=None):
    """Send image to Ollama vision model"""
    image_b64 = base64.b64encode(image_bytes).decode('utf-8')
    image_path = f"data:image/png;base64,{image_b64}"
    
    message = {
        "role": "user",
        "content": prompt or CONFIG["vision_prompt"],
        "images": [image_path]
    }
    
    try:
        response = ollama.chat(model=CONFIG["model_name"], messages=[message])
        return response["message"]["content"]
    except Exception as e:
        print(f"[OLLAMA] Error: {e}")
        return None

def main_tui():
    """Terminal UI - interactive mode"""
    print("--- Fallout Vision CLI TUI ---")
    print("Commands: [c]apture [q]uit  |  Model:", CONFIG["model_name"])
    
    capture = FastCapture()
    
    while True:
        try:
            cmd = input(">>> ").strip().lower()
            
            if cmd in ["q", "quit"]:
                break
            
            if cmd in ["c", "capture"]:
                image_data = capture.capture()
                if image_data:
                    print(f"[+] Capture: {len(image_data)} bytes")
                    analysis = analyze_vision(image_data)
                    if analysis:
                        print(analysis)
        except KeyboardInterrupt:
            break

def main_snapshot():
    """Single snapshot mode - fast exit for bash scripting"""
    capture = FastCapture()
    image_data = capture.capture()
    
    if not image_data:
        sys.exit(1)
    
    analysis = analyze_vision(image_data)
    if analysis:
        print(analysis)

def main():
    parser = argparse.ArgumentParser(description="Fallout Vision CLI")
    parser.add_argument("-t", "--tui", action="store_true", help="TUI mode")
    parser.add_argument("-m", "--model", default="qwen3.5:2b")
    
    args = parser.parse_args()
    CONFIG["model_name"] = args.model
    
    if args.tui:
        main_tui()
    else:
        main_snapshot()

if __name__ == "__main__":
    main()
