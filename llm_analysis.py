import os
from dotenv import load_dotenv
from groq import Groq
from PIL import Image
import pytesseract
from screenshot import capture_screenshot
from ocr import extract_text
from ui import show_explanation  # Import the show_explanation function

# Load environment variables from .env file
load_dotenv()

# Securely access API key
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def analyze_screenshot(image_path):
    print(f"Processing image at: {image_path}")  # Debugging line
    image = Image.open(image_path)
    extracted_text = pytesseract.image_to_string(image)
    
    
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"Analyze the following screen content:\n{extracted_text}",
            }
        ],
        model="llama-3.3-70b-versatile",
        stream=False,
    )
    return chat_completion.choices[0].message.content

if __name__ == "__main__":
    # Capture screenshot
    screenshot_path = capture_screenshot()  # This should return the path where the screenshot is saved.
    print(f"Screenshot saved at: {screenshot_path}")  # Debugging line
    
    # Extract text from screenshot
    text = extract_text(screenshot_path)  # Using the OCR function
    print(f"Extracted text: {text}")  # Debugging line
    
    # Analyze the screenshot using LLM
    explanation = analyze_screenshot(screenshot_path)  # Pass the screenshot path for analysis
    print(f"Explanation: {explanation}")  # Debugging line
    
    # Display the explanation in the UI
    show_explanation(explanation)

