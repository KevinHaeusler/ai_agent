import os
from dotenv import load_dotenv
from google import genai
import argparse

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
args = parser.parse_args()
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=args.user_prompt,
)
if response.usage_metadata == None:
    raise RuntimeError("Usage Metadata is empty, failed API request?")
print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}")
print(response.text)
