#!/usr/bin/env python3
"""
Fallout Vision - KDE Native Screen Capture Integration
v2 - Integrated with native Qt screen capture (no FS dependency)
"""

import ollama
import io
import base64
import sys

# Import local module
sys.path.insert(0, '/home/david/Code/projects/fallout_vision')
from screen_capture_kde import KDEScreenCapture, CONFIG

# === Updated Config ===
VISION_CONFIG = {
    "game": "Fallout 4",
    "appid": "377160",
    "screenshot_dir": None,  # No longer needed - memory-based capture
    "output_format": "json",
    "interval_seconds": 30,
    "vision_prompt": "Analyze this Fallout 4 screenshot. Return JSON: {location, quest_objective, visible_npcs, nearby_items, threats}",
    "capture_region": "window",  # 'window' or 'screen'
}

class VisionAnalyzer:
    """Vision analysis with KDE native screen capture"""
    
    def __init__(self, model_name="qwen3.5:2b"):
        self.model_name = model_name
        self.messages = []
        self.capture = KDEScreenCapture(VISION_CONFIG)
        self.init_model()
    
    def init_model(self):
        """Initialize the conversation memory"""
        print(f"--- Started session with {self.model_name} ---")
        print("Commands: 'capture' (take screenshot), 'exit' (quit)\n")
    
    def capture_screenshot(self):
        """Take native screen capture"""
        print("[Vision] Capturing screenshot...")
        capture_data = self.capture.capture_once()
        
        if not capture_data:
            print("[Vision] Capture failed")
            return None
        
        # Convert to base64 for LLM
        image_b64 = base64.b64encode(capture_data).decode('utf-8')
        image_path = f"data:image/png;base64,{image_b64}"
        
        print(f"[Vision] Captured {len(capture_data)} bytes ({len(image_path)} char base64)")
        return image_path
    
    def analyze_image(self, image_path, prompt_text=""):
        """Send image to LLM for analysis"""
        new_message = {
            'role': 'user',
            'content': prompt_text or VISION_CONFIG['vision_prompt']
        }
        
        if image_path:
            new_message['images'] = [image_path]
        
        self.messages.append(new_message)
        
        # Call the model
        response = ollama.chat(
            model=self.model_name,
            messages=self.messages
        )
        
        assistant_reply = response['message']['content']
        self.messages.append({
            'role': 'assistant',
            'content': assistant_reply
        })
        
        return assistant_reply
    
    def start_auto_capture(self):
        """Start automatic capture loop"""
        self.capture.start_capture()
        
        import time
        while True:
            try:
                time.sleep(VISION_CONFIG['interval_seconds'])
                latest = self.capture.get_latest_capture()
                if latest:
                    image_path = f"data:image/png;base64,{latest['base64']}"
                    result = self.analyze_image(image_path)
                    print(f"\n=== Analysis Result ===\n{result}\n")
                    
            except KeyboardInterrupt:
                self.capture.stop_capture()
                break
    
    def interactive_mode(self):
        """Interactive command mode"""
        while True:
            user_input = input(">>> ").strip()
            
            if user_input.lower() in ['exit', 'quit']:
                self.capture.stop_capture()
                break
            
            if user_input.lower() == 'capture':
                image_path = self.capture_screenshot()
                if image_path:
                    result = self.analyze_image(image_path)
                    print(f"\n=== Analysis ===\n{result}\n")
                continue
            
            # Default: treat as text prompt (with latest capture if available)
            latest = self.capture.get_latest_capture()
            image_path = None
            if latest:
                image_path = f"data:image/png;base64,{latest['base64']}"
            
            if image_path:
                result = self.analyze_image(image_path, user_input)
                print(f"\n=== Result ===\n{result}\n")
            else:
                print("No capture available. Type 'capture' first.")


def main():
    analyzer = VisionAnalyzer()
    mode = sys.argv[1] if len(sys.argv) > 1 else "auto"
    
    if mode == "auto":
        analyzer.start_auto_capture()
    elif mode == "interactive":
        analyzer.interactive_mode()
    else:
        print(f"Unknown mode: {mode}")
        print("Usage: python vision_analyze_v2.py [auto|interactive]")


if __name__ == "__main__":
    main()
