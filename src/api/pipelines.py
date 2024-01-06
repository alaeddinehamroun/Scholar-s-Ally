from haystack import Pipeline
from haystack.pipelines import ExtractiveQAPipeline

from reader import get_reader
from retriever import get_retriever
from document_store import doc_store
from preprocessing import get_converter, get_preprocessor 
def query_pipeline(retriever_type="BM25", reader_model="deepset/roberta-base-squad2"):
    """
    Query pipeline

    Returns:
        pipeline: query pipeline
    """
    
    pipeline = ExtractiveQAPipeline(
        reader=get_reader(model_name_or_path=reader_model),
        retriever=get_retriever(retriever_type)
    )

    return pipeline


def index_pipeline():
    """
    Index pipeline

    Returns:
        indexing_pipeline: indexing pipeline
    """
    
    indexing_pipeline = Pipeline()

    # Converter
    indexing_pipeline.add_node(component=get_converter(), name="Converter", inputs=["File"])
    
    # Preprocessing
    indexing_pipeline.add_node(component=get_preprocessor(), name="PreProcessor", inputs=["Converter"])

    # Document_store
    indexing_pipeline.add_node(component=doc_store, name="Document Store", inputs=["PreProcessor"])

    return indexing_pipeline