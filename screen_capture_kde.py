#!/usr/bin/env python3
"""
KDE Native Screen Capture Module for Fallout Vision
Uses Qt's QScreen API for direct screen capture without filesystem dependency
"""

import sys
import io
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QImage, QScreen
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QRect
from PyQt5.QtCore import pyqtSlot
import base64
import json

# === Config ===
CONFIG = {
    "game": "Fallout 4",
    "appid": "377160",
    "window_title_contains": "Fallout 4",
    "capture_region": "window",  # 'window' or 'screen'
    "capture_interval_ms": 5000,
}

class ScreenCaptureWorker(QThread):
    """KDE native screen capture worker - no FS needed"""
    
    # Signal to emit captured image data
    image_captured = pyqtSignal(bytes, str)  # (image_bytes, timestamp)
    
    def __init__(self, capture_region="window"):
        super().__init__()
        self.capture_region = capture_region
        self.running = False
        self.app = None
        self.target_window = None
        self.window_title = CONFIG.get("window_title_contains", "Fallout 4")
    
    def run(self):
        """Main capture loop"""
        self.running = True
        
        # Initialize Qt application if not already done
        if not self.app:
            self.app = QApplication.instance() or QApplication([])
        
        # Find target window
        self.find_game_window()
        
        while self.running:
            screenshot = self.capture_screen()
            if screenshot:
                self.image_captured.emit(screenshot, "now")
            
            self.msleep(CONFIG.get("capture_interval_ms", 5000))
    
    def find_game_window(self):
        """Find the game window by title"""
        screens = self.app.screens()
        for screen in screens:
            # Get all windows on this screen
            window_manager = screen.windowManager()
            if hasattr(window_manager, 'windows'):
                for window in window_manager.windows():
                    if self.window_title.lower() in window.title().lower():
                        self.target_window = window
                        print(f"[KDE Capture] Found window: {window.title()}")
                        break
                if self.target_window:
                    break
    
    @pyqtSlot()
    def capture_screen(self):
        """Capture screen using Qt native API - returns bytes directly"""
        screens = self.app.screens()
        
        if not screens:
            print("[KDE Capture] No screens found")
            return None
        
        # Get primary screen
        primary_screen = self.app.primaryScreen()
        
        if primary_screen:
            # Native capture - no filesystem needed
            image = primary_screen.grabWindow(0)
            
            if self.target_window and self.capture_region == "window":
                # Capture specific window region
                geometry = self.target_window.frameGeometry()
                image = primary_screen.grabWindow(
                    self.target_window.winId(),
                    geometry.x(),
                    geometry.y(),
                    geometry.width(),
                    geometry.height()
                )
            
            # Convert to bytes (no FS write)
            buffer = io.BytesIO()
            image.save(buffer, format='PNG')
            buffer.seek(0)
            
            return buffer.getvalue()
        
        return None
    
    def stop(self):
        """Stop capture loop"""
        self.running = False


class KDEScreenCapture:
    """Wrapper for KDE native screen capture"""
    
    def __init__(self, config=None):
        self.config = config or CONFIG
        self.worker = None
        self.capures = []
        
        # Initialize Qt application
        self.app = QApplication.instance() or QApplication(sys.argv)
    
    def start_capture(self):
        """Start screen capture thread"""
        self.worker = ScreenCaptureWorker(
            capture_region=self.config.get("capture_region", "window")
        )
        self.worker.image_captured.connect(self.on_image_captured)
        self.worker.start()
        print("[KDE Capture] Started")
    
    def on_image_captured(self, image_bytes, timestamp):
        """Handle captured image"""
        print(f"[KDE Capture] Captured {len(image_bytes)} bytes at {timestamp}")
        self.capures.append({
            "data": image_bytes,
            "timestamp": timestamp,
            "base64": base64.b64encode(image_bytes).decode('utf-8')
        })
        
        # Keep only last 10 captures in memory
        if len(self.capures) > 10:
            self.capures.pop(0)
    
    def get_latest_capture(self):
        """Get latest capture as bytes"""
        if self.capures:
            return self.capures[-1]
        return None
    
    def capture_once(self):
        """Single capture (non-blocking)"""
        return self.worker.capture_screen()
    
    def stop_capture(self):
        """Stop screen capture"""
        if self.worker:
            self.worker.stop()
            print("[KDE Capture] Stopped")


# === Example Usage ===
if __name__ == "__main__":
    print("--- KDE Native Screen Capture (No FS) ---")
    
    capture = KDEScreenCapture()
    capture.start_capture()
    
    # Process events
    import time
    try:
        while True:
            time.sleep(1)
            latest = capture.get_latest_capture()
            if latest:
                print(f"Latest capture: {len(latest['data'])} bytes")
    except KeyboardInterrupt:
        capture.stop_capture()
        sys.exit(0)
