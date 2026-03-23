import ollama
# === Fallout 4 Vision Analysis Config ===
CONFIG = {
    "game": "Fallout 4",
    "appid": "377160",
    "screenshot_dir": "/home/david/Pictures",
    "output_format": "json",
    "interval_seconds": 30,
    "vision_prompt": "Analyze this Fallout 4 screenshot. Return JSON: {location, quest_objective, visible_npcs, nearby_items, threats}"
}

# 1. Initialize the conversation memory
messages = []
model_name = "qwen3.5:2b"

print(f"--- Started session with {model_name} ---")
print("Type 'exit' to quit. To include an image, type its path in your prompt.\n")

while True:
    user_input = input(">>> You: ")
    if user_input.lower() in ['exit', 'quit']:
        break

    # 2. Check if the user provided a file path in the prompt
    # (For this simple loop, we'll assume if it ends in .png or .jpg, it's an image path)
    image_paths = []
    text_prompt = user_input

    # Simple logic to split the prompt and the image path if you type something like:
    # "What color is the car in ./car.jpg"
    words = user_input.split()
    for word in words:
        if word.endswith(('.png', '.jpg', '.jpeg')):
            image_paths.append(word)
            text_prompt = text_prompt.replace(word, "").strip() # Remove path from text

    # 3. Construct the message
    new_message = {
        'role': 'user',
        'content': text_prompt
    }

    # If an image was found, attach it natively
    if image_paths:
        new_message['images'] = image_paths

    # Add user message to history
    messages.append(new_message)

    # 4. Call the model (it reuses the loaded VRAM and knows the whole history)
    response = ollama.chat(
        model=model_name,
        messages=messages
    )

    # 5. Get the answer and add it to the history
    assistant_reply = response['message']['content']
    print(f"\nModel: {assistant_reply}\n")

    messages.append({
        'role': 'assistant',
        'content': assistant_reply
    })
