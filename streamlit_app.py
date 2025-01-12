import streamlit as st
import translate
import pdf_to_json
import json_to_docx

# Show title and description.
st.title("📄 Document converter")
st.write(
    "Upload a document below and ask a question about it – GPT will answer! "
    "To use this app, you need to provide an Gemini API key, which you can get [here](https://platform.openai.com/account/api-keys). "
)

# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
openai_api_key = st.text_input("Gemini API Key", type="password")
if not openai_api_key:
    st.info("Please add your Gemini API key to continue.", icon="🗝️")
else:

    uploaded_file = st.file_uploader(
        "Upload a PDF", type=("pdf")
    )

    do_translate = st.toggle(
        "Translate"
    )

    language = st.text_area(
        "What language should the file be translated to?",
        placeholder="Pirate Speak",
        disabled=not uploaded_file or not do_translate,
    )

    started = False
    if uploaded_file and (not do_translate or language):
        if not started: 
            st.button("Start")
        else:
            st.progress(20, "Loading")
            json_data = pdf_to_json.extract("sample.pdf")
            if do_translate:
                json_data = translate.translate_json(json_data)
            json_to_docx.create_document(json_data)

        

        
