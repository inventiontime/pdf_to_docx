from dotenv import load_dotenv
import os
import json
import google.generativeai as genai


load_dotenv('.env')
api_key = os.environ.get("API_KEY")
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
    prompt = f"Translate the following text to English and output only the translation: '{text}'"
    
    # Generate a response using the Gemini API
    response = model.generate_content(prompt)
    
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

    with open("text_with_translations.json", "w", encoding="utf-8") as file:
        json.dump(json_data, file, ensure_ascii=False, indent=4)

    return json_data