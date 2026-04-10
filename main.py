import os
import time
from google import genai
from dotenv import load_dotenv

load_dotenv()

def generate_ai_content(concept, keywords, title, description):
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

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

    # --- RETRY LOGIC TO FIX 503 ERROR ---
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=prompt,
            )
            return response.text
        except Exception as e:
            # If the server is busy (503), wait and try again
            if "503" in str(e) and attempt < 2:
                time.sleep(3)  # Wait 3 seconds
                continue
            else:
                # If it's a different error or we ran out of retries
                return "AI_ERROR_UNAVAILABLE"