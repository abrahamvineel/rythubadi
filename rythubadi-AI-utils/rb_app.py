import os
from langchain_community.document_loaders import PyPDFLoader
from dotenv import load_dotenv

load_dotenv()
folder_path = "./sample_pdfs"

all_docs = []

for file in os.listdir(folder_path):
    if file.endswith(".pdf"):
        loader = PyPDFLoader(os.path.join(folder_path, file))
