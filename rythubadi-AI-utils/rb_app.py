import os 
from dotenv import load_dotenv
from langchain_community.llms import Ollama
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.vectorstores import FAISS
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter

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
# print(f"result: {result[0].page_content}")
# print(repr(split_docs[:5]))

# llm = Ollama(model="llama2")
#document_chain = create_stuff_documents_chain(llm, prompt)
print(f"Total documents loaded {len(docs)}")

prompt = ChatPromptTemplate.from_template("""
Answer the following question based on the context
<context>
{context}
</context>
Question: {input}""")

# document_chain = create_stuff_documents_chain(llm, prompt)
# retriever = db.as_retriever()

# #retrievers
# retrieval_chain = create_retrieval_chain(retriever, document_chain)
# response = retrieval_chain.invoke({"input":"what is farming"})
# response['answer']

#multi source rag using lang chain tools
api_wrapper = WikipediaAPIWrapper(top_k_results=1,doc_content_chars_max=200)
wiki_tool=WikipediaQueryRun(api_wrapper=api_wrapper)

loader = WebBaseLoader("https://docs.langchain.com/langsmith/home")
docs=loader.load()
documents=RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
vectordb=FAISS.from_documents(documents, HuggingFaceEmbeddings)
ret=vectordb.as_retriever()

from langchain.tools.retriever import create_retriever_tool
web_tool = create_retriever_tool(ret,"langsmith_search", "Search for info about langsmith")

tools=[wiki_tool, web_tool]

from dotenv import load_dotenv
load_dotenv()

import os
os.environ['OPENAI_API_KEY']=os.get_env("OPENAI_API_KEY")

from langchain_openai import ChatOpenAI

llm=ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)

from langchain import hub
prompt = hub.pull("hwchase17/openai-functions-agent")
prompt.messages # default prompt templates from openai

from langchain.agents import create_openai_tools_agent
agent=create_openai_tools_agent(llm, tools, prompt)