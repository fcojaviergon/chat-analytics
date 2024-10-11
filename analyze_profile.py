# analyze_profile.py

import asyncio
import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
import tiktoken
from langsmith import Client
from langsmith.run_helpers import traceable

# Load environment variables
load_dotenv()

# Configure LangSmith
langsmith_client = Client()

# Configure your OpenAI API key
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Constants
MAX_TOKENS = 8192
RESERVE_TOKENS = 1500  # Reserve tokens for the response

# Prompt for detailed analysis
ANALYSIS_PROMPT = """
Eres un analista experto en perfiles psicológicos y comportamiento humano. Basándote en el resumen de conversaciones proporcionado, genera un análisis detallado del perfil de la persona, incluyendo:

    1. Rasgos de personalidad dominantes
    2. Intereses y pasiones
    3. Patrones de comunicación
    4. Estilo de interacción social
    5. Posibles motivaciones y valores
    6. Estado emocional general
    7. Nivel de formalidad y educación
    8. Uso del humor y creatividad
    9. Asertividad y liderazgo
    10. Preocupaciones o temas recurrentes

    Proporciona un análisis detallado y fundamentado, citando ejemplos específicos del resumen cuando sea posible. Concluye con un perfil psicológico conciso pero completo de la persona.
    Generar esto en formato markdown.
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