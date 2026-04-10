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
 
       Improve the content (DO NOT keyword stuff) 
 
       Generate 3 BETTER titles: - Length: 40–60 characters - Use keywords naturally - Add curiosity + hook 
 
        Generate 1 optimized description: - Length: 250–350 characters 
 
         STRICT FORMAT: 
 
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