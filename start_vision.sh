#!/bin/bash
# Fallout Vision - Quick Launch Script
# Usage: ./start_vision.sh [tui|auto [interval]]

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== Fallout Vision Quick Start ===${NC}"

# Check dependencies
check_deps() {
    if ! python3 -c "import ollama" 2>/dev/null; then
        echo -e "${GREEN}[SETUP]${NC} Install ollama client..."
        pip install ollama
    fi
    
    if ! python3 -c "from PyQt6.QtWidgets import QApplication" 2>/dev/null; then
        echo -e "${GREEN}[SETUP]${NC} Install PyQt6..."
        pip install PyQt6
    fi
    
    # Check Ollama is running
    if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        echo -e "${GREEN}[WARN]${NC} Ollama not running. Start it with: ollama serve"
    fi
}

# Run vision CLI
if [ "$1" == "tui" ]; then
    echo -e "${GREEN}[RUN]${NC} TUI Interactive Mode..."
    python3 vision_cli.py --tui
else
    echo -e "${GREEN}[RUN]${NC} Snapshot Mode..."
    python3 vision_cli.py
fi
