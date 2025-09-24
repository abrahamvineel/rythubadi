from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings

embeddings = OpenAIEmbeddings()
vectordb = FAISS.load_local("pdf_index", embeddings)

query = "how to check soil moisture?"
docs = vectordb.similarity_search(query, k=3)
print(docs[0].page_content)