from dotenv import load_dotenv
import os
import google.generativeai as genai
import json
from pdf2image import convert_from_path
import PIL.Image


load_dotenv('.env')
apiKeys = os.environ.get("API_KEY")
genai.configure(api_key=apiKeys)

#Choose a Gemini model.
model = genai.GenerativeModel(model_name="gemini-2.0-flash-exp")

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "application/json",
}

model = genai.GenerativeModel(
  model_name="gemini-2.0-flash-exp",
  generation_config=generation_config,
)

def load_pdf(file):
    if os.path.exists('images'):
        os.system('rm -r images')
    os.system('mkdir images')
    images = convert_from_path(file)
    num_pages = len(images)

    for i in range(len(images)):
        images[i].save('images/' + 'page'+ str(i) + '.jpg', 'JPEG')

    image_paths = ['images/page{i}.jpg'.format(i=i) for i in range(num_pages)]

    images = list(map(lambda x : PIL.Image.open(x), image_paths))

    return images


def extract(file):
  images = load_pdf(file)
  # prompt = "Translate the following document from hindi to English. Return a json file which each block of text as a separate object. Add attributes to each block of text to indicate color, font, size, alignment and the like. "
  prompt = "Extract text from the following document. Return a json file which each block of text as a separate object. Add attributes to each block of text to indicate color, alignment, font family, weight, size and the like. "

  extracted_text = []
  for i in range(len(images)):
      response = model.generate_content([prompt,images[i]])
      extracted_text.append(json.loads(response.text))
  return extracted_text