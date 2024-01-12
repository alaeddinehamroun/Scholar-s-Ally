
from haystack.nodes import BM25Retriever, TfidfRetriever, EmbeddingRetriever, DensePassageRetriever
from document_store import doc_store
from abc import ABC, abstractmethod







def get_retriever(retriever_type="BM25"):
    """
    """
    

    if retriever_type == "BM25":
        # Recommended, does not need a neural network for indexing
        retriever = BM25Retriever(document_store=doc_store)
    elif retriever_type == "TFIDF":
        # Not recommended as BM25 is an improved version of tfidf
        retriever = TfidfRetriever(document_store=doc_store)
    elif retriever_type == "Embedding-deepset-sentence-bert":
        # Recommended, but requires a sentence similarity model
        retriever = EmbeddingRetriever(document_store=doc_store, embedding_model="deepset/sentence_bert", use_gpu=True)
    elif retriever_type == "DPR":
        # Computationally expensive, needs two models.
        retriever =  DensePassageRetriever(document_store=doc_store, query_embedding_model="facebook/dpr-question_encoder-single-nq-base", passage_embedding_model="facebook/dpr-ctx_encoder-single-nq-base")
    return retriever

