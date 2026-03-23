#!/usr/bin/env python3
"""
KDE Portal Screen Capture for Wayland
Uses xdg-desktop-portal protocol for proper Wayland support
"""

import sys
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('GtkosxApplication', '1.0')
from gi.repository import Gtk, Gio
import base64
import time
import threading

class PortalScreenCapture:
    """
    KDE Portal screen capture using xdg-desktop-portal
    
    Supports:
    - Full screen capture
    - Window capture
    - Monitor selection
    - Wayland native
    """
    
    def __init__(self):
        self.captures = []
        self.portal = None
        self.selection_done = threading.Event()
        self.selected_stream = None
        
    def setup_portal(self):
        """Initialize xdg-desktop-portal connection"""
        from gi.repository import GLib
        
        # Create D-Bus connection
        bus = Gio.bus_get_sync(Gio.BusType.SESSION, None)
        
        # Portal proxy
        portal_info = bus.get_object_sync(
            "org.freedesktop.portal.Desktop",
            "/org/freedesktop/portal/desktop",
            "org.freedesktop.portal.Screenshot",
            None
        )
        
        self.portal = portal_info
        print("[Portal] Connected to xdg-desktop-portal")
        return True
    
    def capture_fullscreen(self):
        """Capture full screen via portal"""
        options = {
            "interactive": True,
            "type": 0,  # Full screen
        }
        
        self._call_capture(options)
    
    def capture_window(self):
        """Capture window selection via portal"""
        options = {
            "interactive": True,
            "type": 1,  # Window
        }
        
        self._call_capture(options)
    
    def capture_selection(self):
        """Capture arbitrary selection via portal"""
        options = {
            "interactive": True,
            "type": 2,  # Selection
        }
        
        self._call_capture(options)
    
    def _call_capture(self, options):
        """Call screenshot portal"""
        if not self.portal:
            self.setup_portal()
        
        # Call Screenshot portal method
        self.portal.call(
            "Screenshot",
            ("a{sv}",),
            [options],
            Gio.DBCallFlags.NONE,
            -1,
            None,
            self._on_capture_complete
        )
    
    def _on_capture_complete(self, object, res, user_data):
        """Handle portal callback"""
        try:
            result = self.portal.call_finish(res)
            stream = Gio.unix_input_stream_new_from_fd(result[0])
            
            # Read the image data
            buffer = Gio.BytesIO()
            stream.transfer_to_buffer(
                buffer,
                None,
                None,
                None
            )
            
            image_data = buffer.steal_bytes().get_data()
            self.captures.append({
                "data": image_data,
                "timestamp": time.time(),
                "base64": base64.b64encode(image_data).decode('utf-8')
            })
            
            print(f"[Portal] Captured {len(image_data)} bytes")
            
            if len(self.captures) > 10:
                self.captures.pop(0)
                
        except Exception as e:
            print(f"[Portal] Error: {e}")
    
    def get_latest_capture(self):
        """Get latest capture"""
        if self.captures:
            return self.captures[-1]
        return None
    
    def list_monitors(self):
        """List available monitors"""
        # Use portal to get monitors
        pass


if __name__ == "__main__":
    print("--- KDE Portal Screen Capture (Wayland) ---")
    
    capture = PortalScreenCapture()
    capture.setup_portal()
    
    print("\nPress:")
    print("  1 - Capture fullscreen")
    print("  2 - Capture window")
    print("  3 - Capture selection")
    print("  q - Quit")
    
    while True:
        key = input("\nAction: ").strip().lower()
        
        if key == "1":
            capture.capture_fullscreen()
        elif key == "2":
            capture.capture_window()
        elif key == "3":
            capture.capture_selection()
        elif key == "q":
            break
