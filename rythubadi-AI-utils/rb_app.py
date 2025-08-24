import os 
from dotenv import load_dotenv
from langchain_community.llms import Ollama
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.vectorstores import FAISS
from langchain.chains.combine_documents import create_stuff_documents_chain

folder_path = './sample_pdfs'
load_dotenv()

os.environ['LANGLANGCHAIN_PROJECTCHAIN_API_KEY'] = os.getenv("LANGCHAIN_API_KEY")
os.environ['LANGCHAIN_PROJECT'] = os.getenv('LANGCHAIN_PROJECT')
os.environ['LANGCHAIN_TRACING_V2'] = os.getenv('LANGCHAIN_TRACING_V2')

docs = []

# for file in os.listdir(folder_path):
#     if file.lower().endswith('.pdf'):
#         loader = PyPDFLoader(os.path.join(folder_path, file))
#         file_docs = loader.load()
#         docs.extend(file_docs)
#         text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 200)
#         split_docs = text_splitter.split_documents(docs)
#         db = Chroma.from_documents(split_docs[:20], HuggingFaceEmbeddings())
#         query = "how to start farming?"
#         result = db.similarity_search(query)
#         print(repr(split_docs[:5]))


loader = PyPDFLoader(os.path.join(folder_path, 'agriculture-03-00443.pdf'))
file_docs = loader.load()
docs.extend(file_docs)
text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 200)
split_docs = text_splitter.split_documents(docs)
#db = Chroma.from_documents(split_docs[:20], HuggingFaceEmbeddings())
db = FAISS.from_documents(docs[:20], HuggingFaceEmbeddings())
query = "causes of erosion"
result = db.similarity_search(query)
print(f"result: {result[0].page_content}")
# print(repr(split_docs[:5]))



llm = Ollama(model="llama2")
#document_chain = create_stuff_documents_chain(llm, prompt)
print(f"Total documents loaded {len(docs)}")
