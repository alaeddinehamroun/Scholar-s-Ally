from haystack.utils import fetch_archive_from_http
import os

from haystack.document_stores import ElasticsearchDocumentStore
from haystack.utils import launch_es
import time
from haystack.nodes import PreProcessor
from haystack.nodes import FARMReader
from haystack.nodes import BM25Retriever
from haystack.pipelines import ExtractiveQAPipeline


# Make sure Elasticsearch is running

doc_dir = "data/evaluation_data"
def get_eval_data():
    if not os.path.exists("data/evaluation_data/nq_dev_subset_v2.json"):
        # Download evaluation data, which is a subset of Natural Questions development set containing 50 documents with one question per document and multiple annotated answers
        s3_url = "https://s3.eu-central-1.amazonaws.com/deepset.ai-farm-qa/datasets/nq_dev_subset_v2.json.zip"
        fetch_archive_from_http(url=s3_url, output_dir=doc_dir)




def get_eval_document_store(doc_index = 'eval_docs', label_index = 'eval_labels'):


    # Connect to Elasticsearch
    document_store = ElasticsearchDocumentStore(
        host='localhost',
        username="",
        password="",
        index=doc_index,
        label_index=label_index,
        embedding_field="emb",
        embedding_dim=768,
        excluded_meta_data=["emb"]
        )

    return document_store

def get_eval_preprocessor():
    eval_preprocessor = PreProcessor(
        split_by="word",
        split_length=200,
        split_overlap=0,
        split_respect_sentence_boundary=False,
        clean_empty_lines=False,
        clean_whitespace=False,
    )
    return eval_preprocessor

if __name__ == "__main__":
    doc_index = 'eval_docs'
    label_index = 'eval_labels'
    get_eval_data()

    document_store = get_eval_document_store()
    
    eval_preprocessor = get_eval_preprocessor()
    document_store.delete_documents(index=doc_index)
    document_store.delete_documents(index=label_index)

    # The add_eval_data() method converts the given dataset in json format into Haystack document and label objects. Those objects are then indexed in their respective document and label index in the document store. The method can be used with any dataset in SQuAD format.
    document_store.add_eval_data(
        filename="data/evaluation_data/nq_dev_subset_v2.json",
        doc_index=doc_index,
        label_index=label_index,
        preprocessor=eval_preprocessor,
    )

    # Query pipeline
    retriever = BM25Retriever(document_store=document_store)
    reader = FARMReader("deepset/roberta-base-squad2", top_k=4, return_no_answer=True)

    qp = ExtractiveQAPipeline(reader=reader, retriever=retriever)



    # Load evaluation labels from the document store
    eval_labels = document_store.get_all_labels_aggregated(drop_negative_labels=True, drop_no_answers=True)

    # Evaluate
    eval_result = qp.eval(labels=eval_labels, params={"Retriever": {"top_k": 5}})

    # Save the evaluation result so that we can reload it later and calculate evaluation metrics without running the pipeline again.
    eval_result.save("../")

    print(eval_result.calculate_metrics())