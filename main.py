# Import libraries 
import os 
from google import genai 
from dotenv import load_dotenv 
 
# Load environment variables 
load_dotenv() 
 
# Function to generate AI content 
def generate_ai_content(concept, keywords, title, description): 
 
    # Create client 
    client = genai.Client( 
        api_key=os.environ.get("GEMINI_API_KEY") 
    ) 
 
    # Prompt for AI 
    prompt = f""" 
You are a YouTube SEO + Content Expert. 
 
INPUT: 
Concept of Video: 
{concept} 
 
Keywords: 
21  
{keywords} 
 
Current Title: 
{title} 
 
Current Description: 
{description} 
 
YOUR TASK: 
 
Improve the content (DO NOT keyword stuff) 
 
Generate 3 BETTER titles: - Length: 40–60 characters - Use keywords naturally - Add curiosity + hook 
 
Generate 1 optimized description: - Length: 250–350 characters 
 
STRICT FORMAT: 
 
Title 1: ... 
Title 2: ... 
Title 3: ... 
 
Description: 
... 
 
22  
Hashtags: 
... 
""" 
 
    # Generate response 
    response = client.models.generate_content( 
        model="gemini-2.5-flash", 
        contents=prompt 
    ) 
 
    return response.text