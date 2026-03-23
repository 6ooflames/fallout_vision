#!/usr/bin/env bash
# Fallout Vision - Quick TUI Launcher

set -e

cd "$(dirname "$0")"

echo "Fallout Vision TUI"
echo "=================="
echo ""

# Check dependencies
echo "Checking dependencies..."
python3 -c "import PyQt6, ollama" 2>/dev/null || {
  echo "Missing dependencies. Run: pip install -r requirements.txt"
  exit 1
}
echo "Dependencies OK"

# Check if Ollama is running
curl -s http://localhost:11434/api/tags > /dev/null 2>&1 || {
  echo "Note: Ollama not running. Start with: ollama serve"
}

# Run vision analyzer
echo ""
echo "Starting vision analyzer..."
python3 vision_analyze_v2.py "$@"
