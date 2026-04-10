import os
import streamlit as st
from google import genai

def generate_ai_content(concept, keywords, title, description):

    # ✅ Works both locally + cloud
    api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("API key not found. Add it in Streamlit secrets or .env")

    client = genai.Client(api_key=api_key)

    prompt = f"""
You are a YouTube SEO + Content Expert.

INPUT:
Concept of Video:
{concept}

Keywords:
{keywords}

Current Title:
{title}

Current Description:
{description}

YOUR TASK:

1. Improve the content (DO NOT keyword stuff)

2. Generate 3 BETTER titles:
- Length: 40–60 characters
- Use keywords naturally
- Add curiosity + hook

3. Generate 1 optimized description:
- Length: 250–350 characters

STRICT FORMAT:

Title 1: ...
Title 2: ...
Title 3: ...

Description:
...

Hashtags:
...
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",   # ✅ FIXED MODEL
            contents=prompt,
        )

        return response.text

    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return f"Error: {str(e)}"