import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted
from dotenv import load_dotenv
import os
import json

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found in .env file"
    )

genai.configure(
    api_key=API_KEY
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


def analyze_images(uploaded_files):

    try:

        prompt = """
Analyze all uploaded civic issue images together.

If multiple issues are present, summarize them collectively.

Return ONLY valid JSON.

{
    "category":"",
    "severity":"",
    "department":"",
    "summary":"",
    "title":"",
    "description":""
}
"""

        contents = [prompt]

        for image in uploaded_files:

            contents.append(
                {
                    "mime_type": image.type,
                    "data": image.getvalue()
                }
            )

        response = model.generate_content(
            contents
        )

        return response.text

    except ResourceExhausted:

        return json.dumps(
            {
                "category": "Unknown",
                "severity": "Unknown",
                "department": "Municipal Department",
                "summary": "Gemini API quota exceeded.",
                "title": "Quota Exceeded",
                "description": "The AI service has reached its usage limit. Please try again later."
            }
        )

    except Exception as e:

        return json.dumps(
            {
                "category": "Error",
                "severity": "Unknown",
                "department": "System",
                "summary": str(e),
                "title": "Processing Error",
                "description": str(e)
            }
        )