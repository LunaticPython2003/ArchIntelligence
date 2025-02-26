from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

class VectorStore:
    def __init__(self, embeddings_model_name):
        self.embeddings_model_name = embeddings_model_name

    def create(self, documents):
        embeddings = HuggingFaceEmbeddings(model_name=self.embeddings_model_name)
        vector_store = FAISS.from_documents(documents, embeddings)
        return vector_store
