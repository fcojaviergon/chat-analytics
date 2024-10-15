from langchain_openai import ChatOpenAI
from langsmith import Client
from langsmith.run_helpers import traceable
from dotenv import load_dotenv
# Load environment variables
load_dotenv()

# Configure LangSmith
langsmith_client = Client()

llm = ChatOpenAI()
llm.invoke("Hello, world!")