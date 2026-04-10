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

Generate:
- 3 SEO optimized titles
- 1 improved description
- hashtags

Format:

Title 1: ...
Title 2: ...
Title 3: ...

Description:
...

Hashtags:
...
"""

    # 🔁 RETRY LOGIC
    for attempt in range(5):
        try:
            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=prompt,
            )
            return response.text

        except Exception as e:
            print(f"Attempt {attempt+1} failed:", e)
            time.sleep(2)

    # 🔥 CLEAN FALLBACK
    short_concept = " ".join(concept.split()[:3])

    return f"""⚠️ AI server is busy. Showing optimized suggestions:

Title 1: Improve {short_concept} SEO Fast
Title 2: Boost Your Video with Smart SEO Tricks
Title 3: Simple {short_concept} Growth Strategy

Description:
Learn how to improve your YouTube videos using simple SEO techniques. Optimize titles, descriptions, and keywords to boost reach and engagement.

Hashtags:
#YouTubeSEO #ContentGrowth #{short_concept.replace(" ", "")}
"""