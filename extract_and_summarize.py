# extract_and_summarize.py

import os
import re
import asyncio
from dotenv import load_dotenv
from openai import AsyncOpenAI
from transformers import GPT2Tokenizer

# Load environment variables
load_dotenv()

# Configure your OpenAI API key
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# Constants for token limits
CHUNK_SIZE = 7000

# Prompt for summarization
SUMMARY_PROMPT = """
Eres un experto en resumir conversaciones. Tu tarea es condensar el texto proporcionado, manteniendo los elementos más relevantes para un análisis de personalidad y comportamiento. Enfócate en preservar:
    1. Temas principales discutidos
    2. Patrones de lenguaje y expresiones frecuentes
    3. Tono emocional y actitud general
    4. Interacciones sociales y dinámicas de conversación
    5. Intereses y preocupaciones recurrentes
    Proporciona un resumen conciso pero informativo que capture la esencia de las conversaciones y sea útil para un análisis posterior de personalidad.
"""

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

def process_directory(directory, output_file, name_pattern):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.txt'):
                input_file = os.path.join(root, file)
                extract_profile_lines(input_file, output_file, name_pattern)
                print(f"Processed: {input_file}")

def chunk_text(text, max_tokens=CHUNK_SIZE):
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    tokens = tokenizer.encode(text)
    chunks = []
    current_chunk = []
    current_length = 0

    for token in tokens:
        if current_length + 1 > max_tokens:
            chunks.append(tokenizer.decode(current_chunk))
            current_chunk = []
            current_length = 0
        current_chunk.append(token)
        current_length += 1

    if current_chunk:
        chunks.append(tokenizer.decode(current_chunk))

    return chunks

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