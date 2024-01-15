from haystack import Pipeline
from haystack.pipelines import ExtractiveQAPipeline
from haystack.nodes import PromptNode, PromptTemplate, AnswerParser

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


def rag_pipeline(retriever_type="BM25", top_k_retriever=1):
    """
    RAG pipeline

    Return: 
        rag_pipeline: rag pipeline
    """
    
    rag_pipeline = Pipeline()

    rag_pipeline.add_node(component=get_retriever(retriever_type, top_k=top_k_retriever), name="retriever", inputs=["Query"])
    rag_pipeline.add_node(component=get_prompt_node(), name="prompt_node", inputs=["retriever"])

    return rag_pipeline



def get_prompt_node():
    """
    Prompt node

    Returns:
        prompt_node: prompt node
    """

    rag_prompt = PromptTemplate(
        prompt="""Synthesize a comprehensive answer from the following text for the given question.
                                Provide a clear and concise response that summarizes the key points and information presented in the text.
                                Your answer should be in your own words and be no longer than 50 words.
                                \n\n Related text: {join(documents)} \n\n Question: {query} \n\n Answer:""",
        output_parser=AnswerParser(),
    )
    
    prompt_node = PromptNode(model_name_or_path="google/flan-t5-base", default_prompt_template=rag_prompt) # uses flan-t5 model by default

    return prompt_node