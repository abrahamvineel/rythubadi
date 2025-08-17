import os 
from dotenv import load_dotenv
from langchain_community.llms import Ollama
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
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
        text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 200)
        split_docs = text_splitter.split_documents(docs)
        db = Chroma.from_documents(split_docs[:20], OpenAIEmbeddings())
        print(repr(split_docs[:5]))

print(f"Total documents loaded {len(docs)}")
