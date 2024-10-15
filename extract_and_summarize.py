# extract_and_summarize.py

import os
import re
import asyncio
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


# Constants for token limits
CHUNK_SIZE = 7000

# Prompt for summarization
SUMMARY_PROMPT = """
You are an expert in summarizing conversations. Your task is to condense the provided text, maintaining the most relevant elements for personality and behavior analysis. Focus on preserving:

1. Main topics discussed
2. Language patterns and frequent expressions
3. Emotional tone and general attitude
4. Social interactions and conversation dynamics
5. Recurring interests and concerns

Provide a concise yet informative summary that captures the essence of the conversations and is useful for subsequent personality analysis.
"""
@traceable(run_type="chain")
def extract_profile_lines(input_file, output_file, name_pattern):
    pattern = r'^\[\d{2}-\d{2}-\d{2},\s\d{1,2}:\d{2}:\d{2}\s[AP]M\]\s' + name_pattern
    
    try:
        with open(input_file, 'r', encoding='utf-8') as infile:
            profile_lines = [line for line in infile if re.match(pattern, line)]
        
        if profile_lines:
            with open(output_file, 'a', encoding='utf-8') as outfile:
                for line in profile_lines:
                    clean_line = re.sub(pattern, '', line).strip()
                    outfile.write(clean_line + "\n")
    except IOError as e:
        print(f"Error processing {input_file}: {e}")
        
@traceable(run_type="chain")
def process_directory(directory, output_file, name_pattern):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.txt'):
                input_file = os.path.join(root, file)
                extract_profile_lines(input_file, output_file, name_pattern)
                print(f"Processed: {input_file}")


@traceable(run_type="chain")
def chunk_text(text, max_tokens=CHUNK_SIZE):
    encoding = tiktoken.encoding_for_model("gpt2")  # Usamos el encoding para GPT-4
    tokens = encoding.encode(text)
    chunks = []
    current_chunk = []
    current_length = 0

    for token in tokens:
        if current_length + 1 > max_tokens:
            chunks.append(encoding.decode(current_chunk))
            current_chunk = []
            current_length = 0
        current_chunk.append(token)
        current_length += 1

    if current_chunk:
        chunks.append(encoding.decode(current_chunk))

    return chunks

@traceable(run_type="chain")
async def summarize_text(text):
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SUMMARY_PROMPT},
            {"role": "user", "content": text}
        ],
        max_tokens=500
    )
    return response.choices[0].message.content

@traceable(run_type="chain")
async def generate_summaries(input_file, summaries_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            text = file.read()

        chunks = chunk_text(text)
        
        with open(summaries_file, 'w', encoding='utf-8') as summary_file:
            for i, chunk in enumerate(chunks):
                print(f"Summarizing chunk {i+1} of {len(chunks)}...")
                summary = await summarize_text(chunk)
                summary_file.write(f"Summary of chunk {i+1}:\n{summary}\n\n")

        print(f"Summaries saved in {summaries_file}")
    except FileNotFoundError:
        print(f"Error: Could not find the file {input_file}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def extract_and_summarize(directory, extracted_file, summaries_file, name_pattern):
    # Clear or create the output file for extraction
    open(extracted_file, 'w').close()
    
    # Extract and clean profile lines
    process_directory(directory, extracted_file, name_pattern)
    print(f"Profile lines have been extracted and saved in {extracted_file}")
    
    # Generate summaries
    asyncio.run(generate_summaries(extracted_file, summaries_file))

if __name__ == "__main__":
    directory = '.'
    extracted_file = 'all_profile_lines.txt'
    summaries_file = 'summaries.txt'
    name_pattern = 'Francisco Gonzalez:'
    extract_and_summarize(directory, extracted_file, summaries_file, name_pattern)