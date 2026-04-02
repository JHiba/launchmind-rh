# import requests
# import json
# import re

# def call_llm(prompt):
#     try:
#         response = requests.post(
#             "http://localhost:11434/api/generate",
#             json={
#                 "model": "llama3",
#                 "prompt": prompt,
#                 "stream": False
#             }
#         )

#         result = response.json()
#         text = result["response"]

#         # extract JSON safely
#         match = re.search(r"\{.*\}", text, re.DOTALL)
#         if match:
#             return match.group()
#         else:
#             return text

#     except Exception as e:
#         print("⚠️ Ollama error:", e)
#         return """
#         {
#           "value_proposition": "Fallback product",
#           "personas": [],
#           "features": [],
#           "user_stories": []
#         }
#         """



import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def call_llm(prompt):
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # fast + free
            messages=[
                {"role": "system", "content": "You are a helpful AI."},
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        print("⚠️ Groq error:", e)
        return "{}"