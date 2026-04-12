import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

def generate_ai_content(concept, keywords, title, description):

    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    prompt = f"""
You are a YouTube SEO + Content Expert.

Your goal is to generate output that will score ABOVE 90 using this scoring system.

SCORING LOGIC YOU MUST SATISFY:

1. KEYWORDS:
- Keywords: {keywords}
- Title MUST contain at least 70% of these keywords EXACTLY (same spelling)
- Description MUST contain at least 90% of these keywords EXACTLY

2. HOOK SCORE:
- Title MUST include at least ONE of these power words:
  what if, secret, shocking, amazing, unexpected, truth

3. CURIOSITY SCORE:
- Title MUST include:
  - A question mark (?) OR
  - One of these words: vs, story, journey, meet

4. NATURAL FLOW:
- Do NOT keyword stuff randomly
- Make it readable, clickable, and human-friendly

INPUT:

Concept of Video:
{concept}

Current Title:
{title}

Current Description:
{description}

YOUR TASK:

Generate:

1. Three HIGH-SCORING titles (40–60 characters):
- MUST include keywords
- MUST include at least one power word
- MUST include curiosity trigger ("?" or similar)

2. One optimized description (250–350 characters):
- MUST include almost ALL keywords naturally

3. Relevant hashtags

FINAL CHECK BEFORE OUTPUT:
- Ensure keyword coverage is satisfied
- Ensure hook word is present
- Ensure curiosity trigger is present

STRICT FORMAT (DO NOT CHANGE):

Title 1: ...
Title 2: ...
Title 3: ...

Description:
...

Hashtags:
...
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    return response.text