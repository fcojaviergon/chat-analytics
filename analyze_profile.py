# analyze_profile.py

import asyncio
import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
import tiktoken
from langsmith import Client
from langsmith.run_helpers import traceable
from langsmith.wrappers import wrap_openai

# Load environment variables
load_dotenv()

# Configure LangSmith
langsmith_client = Client()

# Envuelve el cliente de OpenAI con LangSmith
client = wrap_openai(AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY")))

# Constants
MAX_TOKENS = 8192
RESERVE_TOKENS = 1500  # Reserve tokens for the response

# Prompt for detailed analysis
ANALYSIS_PROMPT = """
You are an expert analyst in psychological profiles and human behavior. Based on the provided conversation summary, generate a detailed analysis of the person's profile, including:

1. Dominant personality traits
2. Interests and passions
3. Communication patterns
4. Social interaction style
5. Possible motivations and values
6. General emotional state
7. Level of formality and education
8. Use of humor and creativity
9. Assertiveness and leadership
10. Recurring concerns or themes

Provide a detailed and well-founded analysis, citing specific examples from the summary when possible. Conclude with a concise yet comprehensive psychological profile of the person.

Generate this response in markdown format, using appropriate headers, bullet points, and emphasis where necessary.
"""

def truncate_text(text, max_tokens):
    encoding = tiktoken.encoding_for_model("gpt2")
    tokens = encoding.encode(text)
    
    if len(tokens) <= max_tokens:
        return text
    
    truncated_tokens = tokens[:max_tokens]
    truncated_text = encoding.decode(truncated_tokens)
    
    # Ensure the truncated text ends with a complete sentence
    last_period = truncated_text.rfind('.')
    if last_period != -1:
        truncated_text = truncated_text[:last_period + 1]
    
    return truncated_text

@traceable(run_type="chain")
async def analyze_summaries(summaries_file):
    with open(summaries_file, 'r', encoding='utf-8') as file:
        combined_summary = file.read()

    # Calculate available tokens
    encoding = tiktoken.encoding_for_model("gpt2")
    prompt_tokens = len(encoding.encode(ANALYSIS_PROMPT))
    available_tokens = MAX_TOKENS - RESERVE_TOKENS - prompt_tokens

    # Truncate the combined summary if it exceeds the token limit
    truncated_summary = truncate_text(combined_summary, available_tokens)

    original_tokens = len(encoding.encode(combined_summary))
    truncated_tokens = len(encoding.encode(truncated_summary))

    if original_tokens != truncated_tokens:
        print(f"Warning: The summary was truncated from {original_tokens} tokens to {truncated_tokens} tokens to fit within the token limit.")

    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": ANALYSIS_PROMPT},
            {"role": "user", "content": truncated_summary}
        ],
        max_tokens=RESERVE_TOKENS
    )
    return response.choices[0].message.content

@traceable(run_type="chain")
def analyze_profile(summaries_file, output_file):
    print("Performing final analysis on summaries...")
    final_analysis = asyncio.run(analyze_summaries(summaries_file))

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(final_analysis)

    print(f"Complete analysis saved in {output_file}")
    return final_analysis

if __name__ == "__main__":
    summaries_file = 'summaries.txt'
    analysis_file = 'profile_analysis.txt'
    analyze_profile(summaries_file, analysis_file)