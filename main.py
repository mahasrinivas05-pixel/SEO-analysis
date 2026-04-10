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

    # 🔥 RETRY LOGIC
    for attempt in range(5):
        try:
            response = client.models.generate_content(
                model="gemini-1.5-flash",   # ✅ stable model
                contents=prompt,
            )
            return response.text

        except Exception as e:
            print(f"Attempt {attempt+1} failed:", e)
            time.sleep(2)

    # 🔥 SMART DYNAMIC FALLBACK
    return f"""⚠️ AI server is busy right now. Showing optimized suggestions:

Title 1: {title} - Improve SEO Fast
Title 2: Boost {concept} with Smart Keywords
Title 3: {concept} Secrets You Must Know

Description:
Learn how to improve {concept} using powerful SEO strategies. This video helps you optimize your title, description, and keywords to increase reach and engagement.

Hashtags:
#{concept.replace(" ", "")} #YouTubeSEO #ContentGrowth
"""