#!/usr/bin/env python3
"""Fallout Vision Agent - Merged from screen_capture_kde.py, vision_analyze_v2.py, controller_server.py"""

import sys, asyncio, time, json, base64, io
from datetime import datetime
import ollama
from flask import Flask, request, jsonify
from flask_cors import CORS
