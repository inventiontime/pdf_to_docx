import streamlit as st
import translate
import pdf_to_json
import json_to_docx

if 'progress' not in st.session_state:
    st.session_state['progress'] = 0
if 'language' not in st.session_state:
    st.session_state['language'] = "None"

def start_conversion():
    convert()

def convert():
    st.session_state['progress'] = 10
    json_data = pdf_to_json.extract("sample.pdf")
    st.session_state['progress'] = 40
    if do_translate:
        json_data = translate.translate_json(json_data)
    st.session_state['progress'] = 70
    json_to_docx.create_document(json_data)
    st.session_state['progress'] = 100

# Show title and description.
st.title("📄 Document converter")
st.write(
    "Upload a PDF below and get it converted to a DOCX in any language! "
    "To use this app, you need to provide an Gemini API key, which you can get [here](https://platform.openai.com/account/api-keys). "
)

# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
api_key = st.text_input("Gemini API Key", type="password")
if not api_key:
    st.info("Please add your Gemini API key to continue.", icon="🗝️")
else:
    if 'api_key' not in st.session_state:
        st.session_state['api_key'] = api_key
        pdf_to_json.init(api_key)
        translate.init(api_key)
    uploaded_file = st.file_uploader(
        "Upload a PDF", type=("pdf")
    )
    if uploaded_file is not None:
        with open("sample.pdf", "wb") as file:
            file.write(uploaded_file.getvalue())

    do_translate = st.toggle(
        "Translate"
    )

    language = st.text_area(
        "What language should the file be translated to?",
        placeholder="Pirate Speak",
        disabled=not uploaded_file or not do_translate,
    )
    st.session_state['language'] = language if do_translate else "None"

    if uploaded_file and (not do_translate or language):
        if st.session_state['progress'] == 0: 
            st.button("Convert", on_click=start_conversion)
        else:
            if st.session_state['progress'] != 100:
                st.progress(st.session_state['progress'], "Loading")
            else:
                with open("output.docx", "rb") as file:
                    st.download_button("Download DOCX", file, file_name="output.docx")

        

        
