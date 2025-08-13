import os 
from dotenv import load_dotenv
from langchain_community.llms import Ollama
from langchain_community.document_loaders import PyPDFLoader
folder_path = './sample_pdfs'
load_dotenv()

os.environ['LANGLANGCHAIN_PROJECTCHAIN_API_KEY'] = os.getenv("LANGCHAIN_API_KEY")
os.environ['LANGCHAIN_PROJECT'] = os.getenv('LANGCHAIN_PROJECT')
os.environ['LANGCHAIN_TRACING_V2'] = os.getenv('LANGCHAIN_TRACING_V2')

docs = []

for file in os.listdir(folder_path):
    if file.lower().endswith('.pdf'):
        loader = PyPDFLoader(os.path.join(folder_path, file))
        file_docs = loader.load()
        docs.extend(file_docs)

print(f"Total documents loaded {len(docs)}")
print(docs[0])

print(docs[0].page_content)
print(docs[0].metadata)