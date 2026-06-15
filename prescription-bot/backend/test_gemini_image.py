import os
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash")

image = Image.open("test_data/sample_prescription.png")

prompt = """
You are an AI prescription reader.

Read this prescription image and extract whatever details are visible.

Return the answer in this format:

Patient Name:
Doctor Name:
Medicines:
Dosage:
Frequency:
Duration:
Instructions:
Unclear Text:
Simple Explanation:

Important:
- Do not guess.
- If handwriting is unclear, write "unclear".
- This is only for explanation, not medical advice.
"""

response = model.generate_content([prompt, image])

print(response.text)