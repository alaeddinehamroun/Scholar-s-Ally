from haystack import Pipeline
from haystack.pipelines import ExtractiveQAPipeline
from haystack.nodes import PromptNode, PromptTemplate, AnswerParser, JoinAnswers
from reader import get_reader
from retriever import get_retriever
from document_store import doc_store
from preprocessing import get_converter, get_preprocessor 


def extractive_qa_pipeline(retriever_type="BM25", reader_model="deepset/roberta-base-squad2"):
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
    # By default, an indexing pipeline receives a root node File as the entry point to the pipeline graph.
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

def extqa_and_rag_pipeline(retriever_type="BM25", reader_model="deepset/roberta-base-squad2", top_k_retriever=1, top_k_reader=1):
    """
    ExtractiveQA and RAG pipeline
    
    Keyword arguments:
    argument -- description
    Return: return_description
    """
    
    p = Pipeline()
    p.add_node(component=get_retriever(retriever_type, top_k=top_k_retriever), name="retriever", inputs=["Query"])
    p.add_node(component=get_reader(model_name_or_path=reader_model, top_k_reader=top_k_reader), name="QAReader", inputs=["retriever"])
    p.add_node(component=get_prompt_node(), name="QAPromptNode", inputs=["retriever"])
    
    # Setting sort_by_score to False because answers coming from the generator have no score.
    p.add_node(component=JoinAnswers('concatenate', sort_by_score=False), name="JoinAnswers", inputs=["QAReader", "QAPromptNode"])
    # p.draw()
    return p

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
