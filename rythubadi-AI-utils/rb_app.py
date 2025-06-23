import os 
from dotenv import load_dotenv
from langchain_community.llms import Ollama
load_dotenv()

os.environ['LANGLANGCHAIN_PROJECTCHAIN_API_KEY'] = os.getenv("LANGCHAIN_API_KEY")
os.environ['LANGCHAIN_PROJECT'] = os.getenv('LANGCHAIN_PROJECT')
os.environ['LANGCHAIN_TRACING_V2'] = os.getenv('LANGCHAIN_TRACING_V2')

