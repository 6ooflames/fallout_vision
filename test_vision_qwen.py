#!/usr/bin/env python3
"""
Quick Vision Test with qwen3.5:2b and KDE Screen Capture
"""

import sys
import io
import base64
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QImage, QScreen
import ollama

def capture_screen():
    """Capture full screen using Qt"""
    app = QApplication.instance() or QApplication([])
    primary_screen = app.primaryScreen()
    
    if not primary_screen:
        print("❌ No screen found")
        return None
    
    # Grab the whole screen (window id 0 = root window)
    image = primary_screen.grabWindow(0)
    
    if image.isNull():
        print("❌ Failed to capture")
        return None
    
    # Convert to bytes
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    buffer.seek(0)
    
    return buffer.getvalue()

def analyze_with_vision(image_bytes, prompt):
    """Send image to qwen3.5:2b for vision analysis"""
    # Convert to base64
    image_b64 = base64.b64encode(image_bytes).decode('utf-8')
    
    print(f"📸 Captured: {len(image_bytes)} bytes")
    
    try:
        response = ollama.chat(
            model='qwen3.5:2b',
            messages=[{
                'role': 'user',
                'content': prompt,
                'images': [image_b64]
            }]
        )
        return response['message']['content']
    except Exception as e:
        return f"Error: {e}"

def main():
    print("🎮 Fallout 4 Vision Test with qwen3.5:2b")
    print("=" * 50)
    
    # Capture screen
    print("📷 Capturing screen...")
    image_bytes = capture_screen()
    
    if not image_bytes:
        print("❌ Failed to capture screen")
        return
    
    print(f"✅ Screen captured: {len(image_bytes)} bytes")
    
    # Vision prompt for Fallout 4
    prompt = """Analyze this Fallout 4 screenshot. Tell me:
1. What location/area is this?
2. Any visible NPCs or enemies?
3. What items or objects can you see?
4. Current quest objective or situation?

Keep it brief but informative."""
    
    print("\n🧠 Analyzing with qwen3.5:2b...")
    result = analyze_with_vision(image_bytes, prompt)
    
    print("\n" + "=" * 50)
    print("📋 Analysis Result:")
    print("=" * 50)
    print(result)
    print()

if __name__ == "__main__":
    main()
