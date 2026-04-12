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

Your goal is to generate HIGH-QUALITY, NATURAL, and HIGH-PERFORMING content.

-------------------------
GUIDELINES
-------------------------

Keywords:
{keywords}

1. TITLE:
- Include important keywords naturally (no stuffing)
- Make it engaging and clickable
- Use emotional or power words where suitable
- Add curiosity (question / intrigue / contrast)
- Keep it human and realistic

2. DESCRIPTION:
- Use keywords naturally across sentences
- Make it informative and engaging
- Avoid repetition and keyword stuffing
- Write like a real YouTube description

3. HASHTAGS:
- Relevant and based on keywords

-------------------------
INPUT
-------------------------

Concept:
{concept}

Current Title:
{title}

Current Description:
{description}

-------------------------
OUTPUT
-------------------------

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