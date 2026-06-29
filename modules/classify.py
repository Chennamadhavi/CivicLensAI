import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted
from dotenv import load_dotenv
import os

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


def classify_issue(user_text):

    prompt = f"""
You are an AI civic complaint classifier.

Analyze the complaint and return ONLY valid JSON.

{{
    "category":"",
    "severity":"",
    "department":"",
    "summary":""
}}

Complaint:
{user_text}
"""

    try:

        response = model.generate_content(
            prompt
        )

        if not response.text:

            return """
{
    "category":"Unknown",
    "severity":"Unknown",
    "department":"Unknown",
    "summary":"No response received from Gemini."
}
"""

        return response.text

    except ResourceExhausted:

        return """
{
    "category":"Quota Exceeded",
    "severity":"N/A",
    "department":"N/A",
    "summary":"Gemini free-tier limit reached. Try again later."
}
"""

    except Exception as e:

        return f"""
{{
    "category":"Error",
    "severity":"N/A",
    "department":"N/A",
    "summary":"{str(e)}"
}}
"""