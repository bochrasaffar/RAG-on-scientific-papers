from langchain_community.vectorstores import FAISS
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import os
from faiss import IndexFlatL2
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain.embeddings import SentenceTransformerEmbeddings
from config import Config
from pdf_process import get_chunks_pdf

def get_embedder():
    embedder = SentenceTransformerEmbeddings(model_name=Config.EMBEDDING_MODEL)
    return embedder

def create_empty_index(embedder):
    index = FAISS(
    embedding_function=embedder,
    index=IndexFlatL2(Config.FAISS_INDEX_DIM),
    docstore=InMemoryDocstore(),
    index_to_docstore_id={},
    normalize_L2=False
)
    print("creating empty index")
    return index

def load_index(embedder):
    if os.path.exists(Config.INDEX_FILE):
        index = FAISS.load_local(Config.INDEX_FILE,embedder,allow_dangerous_deserialization=True)
        print("loading persistent index")
    else:
        index = create_empty_index(embedder)
    return index

def save_index(index):
    FAISS.save_local(index, Config.INDEX_FILE)

def add_documents_to_index(index, documents):
    index.add_documents(documents)
    save_index(index)

def add_paper_to_index(index,pdf_file_name):
    print(f'Adding paper {pdf_file_name} to index')
    chunks = get_chunks_pdf(pdf_file_name)
    add_documents_to_index(index, chunks)
    
def search_index(index, query, top_k=5):
    results = index.similarity_search(query,k=top_k)
    #papers extracted using regex expressions
    papers = []
    return results

def remove_document_from_index(index,pdf_file_name):
    all_documents = index.docstore._dict
    ids_to_delete = []
    ids_to_delete = [doc_id for doc_id in all_documents if pdf_file_name in all_documents[doc_id].metadata.get('source')]
    
    # Delet these documents
    index.delete(ids_to_delete)
    
    # Save the updated index
    save_index(index)
    if len(ids_to_delete) == 0:
        return False 
    else:
        return True