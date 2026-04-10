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
                model="gemini-2.5-flash",
                contents=prompt,
            )
            return response.text

        except Exception as e:
            print(f"Attempt {attempt+1} failed:", e)
            time.sleep(2)

    # 🔥 FALLBACK CONTENT (if API fails)
    return """⚠️ AI server is busy right now.

Title 1: Improve Your Video SEO Fast
Title 2: Boost YouTube Growth with Smart SEO
Title 3: Simple Tricks to Rank Your Videos

Description:
This video explains how to improve YouTube SEO using simple strategies. Learn how to optimize your title, description, and keywords to increase reach and engagement.

Hashtags:
#YouTubeSEO #ContentGrowth #VideoOptimization
"""