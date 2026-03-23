# GamePlayer Verification Checklist

## Components to Verify:
1. [ ] index.html (UI) - loads correctly, makes API calls
2. [ ] controller_server.py - listens, handles requests
3. [ ] pipboy_relay.py - socket server for game state
4. [ ] GamePlayerBridge.psc - Fallout mod script
5. [ ] Dependency: Ollama running locally
6. [ ] Dependency: Elena-Agent/ElenaPillar2 APIs available
7. [ ] Web Speech API for TTS
8. [ ] Kokoro API for TTS
9. [ ] Fast model (FasterTransformer/Ollama) connectivity

## Files to Check:
- index.html
- controller_server.py
- pipboy_relay.py
- GamePlayerBridge.psc
- test_controller.py