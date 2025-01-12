import streamlit as st
import json
import google.generativeai as genai
from time import sleep

model = None

def init(api_key):
    global model
    genai.configure(api_key=api_key)

    # Create the model
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
    }

    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash-exp",
        generation_config=generation_config,
    )



# Function to translate text using Gemini API
def translate_text(text):
    '''Translates text to English using the Gemini API.'''

    # Create a prompt for translation
    prompt = f"Translate the following text to '{st.session_state['language']}' and output only the translation: '{text}'"
    
    # Generate a response using the Gemini API
    response = model.generate_content(prompt)
    sleep(4)
    
    # Extract the translated text
    if response:
        return response.text.strip()
    return "Translation failed"

# Add translations to the JSON data
def translate_json(json_data):
    '''Translates text in a JSON object using the Gemini API.'''

    # Translate text in each object
    for page_data in json_data:
        for block_data in page_data:
            text = block_data.get("text", "")
            block_data["old_text"] = text
            block_data["text"] = translate_text(text)

    with open("output2.json", "w", encoding="utf-8") as file:
        json.dump(json_data, file, ensure_ascii=False, indent=4)

    return json_data