import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from prompts import system_prompt
from call_function import call_function, available_functions

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()
messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]



response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=messages,
    config=types.GenerateContentConfig(
        tools=[available_functions], system_instruction=system_prompt
    ),
)
if response.usage_metadata == None:
    raise RuntimeError("Usage Metadata is empty, failed API request?")
if args.verbose:
    print(
        f"User prompt: {args.user_prompt}\nPrompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}"
    )
tool_results = []

if response.function_calls:
    for function_call_part in response.function_calls:
        # actually call the function
        function_call_result = call_function(
            function_call_part,
            verbose=args.verbose,
        )

        # sanity check: make sure we got a function_response back
        if (
            not function_call_result.parts
            or not function_call_result.parts[0].function_response
            or function_call_result.parts[0].function_response.response is None
        ):
            raise RuntimeError("Function call did not return a valid function_response")

        # store the tool result (we’ll use these later)
        tool_results.append(function_call_result.parts[0])

        # if verbose, show the result dict
        if args.verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
else:
    print(response.text)

