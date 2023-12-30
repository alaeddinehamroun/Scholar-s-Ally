
from haystack.nodes import BM25Retriever, TfidfRetriever, EmbeddingRetriever, DensePassageRetriever
from document_store import doc_store
from abc import ABC, abstractmethod







def get_retriever(retriever_type="bm25"):
    """
    """
    

    if retriever_type == "bm25":
        retriever = BM25Retriever(document_store=doc_store)

    return retriever