import os
import pytorch
import PyPDF2
from constants import BASE_MODEL
from transformers import (AutoTokenizer, AutoModelForCausalLM)


from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from dotenv import load_dotenv

load_dotenv()
folder_path = "./sample_pdfs"

def extract_text_from_pdf():
    all_docs = []

    for file in os.listdir(folder_path):
        if file.endswith(".pdf"):
            loader = PyPDF2.PdfReader(os.path.join(folder_path, file))
            docs = loader.load()
            all_docs.extend(docs)
    return all_docs

model = AutoModelForCausalLM.from_pretrained(BASE_MODEL)

all_docs = extract_text_from_pdf()

splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
split_docs = splitter.split_documents(all_docs)

embeddings = OpenAIEmbeddings()
vectordb = FAISS.from_documents(split_docs, embeddings)
vectordb.save_local("pdf_index")