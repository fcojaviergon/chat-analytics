# Whatsapp Chat Analysis Project

## Overview
This project is designed to analyze chat logs and generate psychological profiles based on the conversation patterns. It uses OpenAI's GPT-4 model to process and analyze text data, providing insights into personality traits, communication styles, and behavioral patterns.

## Features
- Extracts and cleans chat logs from text files
- Generates summaries of chat content
- Performs in-depth psychological analysis using GPT-4
- Handles large volumes of text by chunking and truncating as necessary
- Securely manages API keys using environment variables

## Prerequisites
- Python 3.7+
- OpenAI API key

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/fcojaviergon/chat-analyzer.git
   cd chat-analysis-project
   ```

2. Install required packages:
   ```
   pip install openai tiktoken python-dotenv
   ```

3. Set up your environment variables:
   Create a `.env` file in the project root and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

1. Place your chat log text files in the project directory.

2. Run the orchestrator script:
   ```
   python orchestrator.py
   ```

3. The script will process the chat logs, generate summaries, and perform the analysis. You'll be prompted to confirm before proceeding with the final analysis step.

4. Check the output files:
   - `all_profile_lines.txt`: Contains extracted and cleaned chat lines
   - `summaries.txt`: Contains summaries of the chat content
   - `profile_analysis.txt`: Contains the final psychological profile analysis

## Project Structure
- `extract_and_summarize.py`: Handles extraction of chat lines and generation of summaries
- `analyze_profile.py`: Performs the final analysis using GPT-4
- `orchestrator.py`: Coordinates the entire process and handles user interaction

## Important Notes
- Ensure your `.env` file is included in `.gitignore` to keep your API key secure.
- The project is set up to analyze chats from a specific user (default: "Francisco Gonzalez"). Modify the `name_pattern` in `orchestrator.py` to analyze different users.
- Large chat logs may result in truncation to fit within GPT-4's token limits. The script will warn you if this occurs.

## Contributing
Contributions to improve the project are welcome. Please feel free to submit pull requests or open issues to discuss potential changes or enhancements.

## License
[Specify your chosen license here, e.g., MIT, GPL, etc.]

## Disclaimer
This tool is for research and personal use only. Always respect privacy and obtain necessary permissions before analyzing someone's chat logs. The psychological insights provided should not be considered as professional psychological advice.