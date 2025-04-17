# Chat Analysis Project

## Overview
This project is designed to analyze chat logs, particularly from WhatsApp, and generate psychological profiles based on conversation patterns. It uses OpenAI's GPT-4 model to process and analyze text data, providing insights into personality traits, communication styles, and behavioral patterns.

## Features
- Extracts and cleans chat logs from WhatsApp export files
- Generates summaries of chat content
- Performs in-depth psychological analysis using GPT-4
- Handles large volumes of text by chunking and truncating as necessary
- Securely manages API keys using environment variables
- Integrates LangSmith for monitoring API usage and performance

## Prerequisites
- Python 3.7+
- OpenAI API key
- LangSmith API key
  
[![Watch the video](https://img.youtube.com/vi/Z40RBqmlUY4/hqdefault.jpg)](https://www.youtube.com/watch?v=Z40RBqmlUY4)


## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/chat-analysis-project.git
   cd chat-analysis-project
   ```

2. Install required packages:
   ```
   pip install openai tiktoken python-dotenv langsmith
   ```

3. Set up your environment variables:
   Create a `.env` file in the project root and add your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   LANGCHAIN_API_KEY=your_langsmith_api_key_here
   LANGCHAIN_PROJECT=your_langsmith_project_name
   ```

## Usage

1. Export your WhatsApp chat and place the .txt file in the project directory.

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

## LangSmith Integration
This project now integrates LangSmith for enhanced monitoring and optimization:

- Tracks API calls and token usage
- Provides insights into performance and costs
- Helps in debugging and optimizing the AI model interactions

To view your project's metrics:
1. Log in to your LangSmith account
2. Navigate to the project dashboard
3. Analyze the tracked runs, including API usage, response times, and more

## Important Notes
- Ensure your `.env` file is included in `.gitignore` to keep your API keys secure.
- The project is set up to analyze WhatsApp chats. Modify the `name_pattern` in `orchestrator.py` to analyze different users or chat formats.
- Large chat logs may result in truncation to fit within GPT-4's token limits. The script will warn you if this occurs.
- Monitor your LangSmith dashboard to keep track of API usage and costs.

## Contributing
Contributions to improve the project are welcome. Please feel free to submit pull requests or open issues to discuss potential changes or enhancements.

## License
MIT

## Disclaimer
This tool is for research and personal use only. Always respect privacy and obtain necessary permissions before analyzing someone's chat logs. The psychological insights provided should not be considered as professional psychological advice.
