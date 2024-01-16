from fastapi import FastAPI, File, Form, UploadFile
from preprocessing import get_preprocessor
from pipelines import extractive_qa_pipeline, index_pipeline, query_and_rag_pipeline, rag_pipeline
import os
from document_store import doc_store
from retriever import get_retriever
from haystack.nodes import PreProcessor

# Init FastAPI
app = FastAPI()

doc_dir = '../../data'
@app.get("/query")
async def query(query: str, top_k_reader: int, top_k_retriever: int, retriever_type: str = "BM25", reader_model: str = "deepset/roberta-base-squad2"):
    pipeline = extractive_qa_pipeline(retriever_type= retriever_type, reader_model=reader_model)
    return pipeline.run(query=query, params={"Retriever": {"top_k": top_k_retriever}, "Reader": {"top_k": top_k_reader}})


@app.get("/index")
async def index():
    indexing_pipeline = index_pipeline()
    files_to_index = [doc_dir + "/" + f for f in os.listdir(doc_dir)]
    files_metadata = [{"name": f} for f in os.listdir(doc_dir)]
    return indexing_pipeline.run(file_paths=files_to_index, meta=files_metadata)

@app.get("/rag")
async def rag(query: str, top_k_retriever: int, retriever_type: str = "BM25"):
    pipeline = rag_pipeline(retriever_type= retriever_type, top_k_retriever=top_k_retriever)
    return pipeline.run(query=query)
@app.get("/extractive_qa_rag")
async def extractive_qa_rag(query: str, top_k_reader: int, top_k_retriever: int, retriever_type: str = "BM25", reader_model: str = "deepset/roberta-base-squad2"):
    pipeline = query_and_rag_pipeline(retriever_type= retriever_type, reader_model=reader_model, top_k_reader=top_k_reader, top_k_retriever=top_k_retriever)
    
    return pipeline.run(query=query)

@app.get("/initialized")
async def initialized():
    
    return True

@app.post('/file-upload')
async def upload_file(files: list[UploadFile]= File(...), keep_files=False):
    
    file_paths = []
    files_metadata = []
    indexing_pipeline = index_pipeline()
    for file in files:
        contents = await file.read()
            
        # Keep the file on disk
        file_path = os.path.join(doc_dir, file.filename)
        file_name = file.filename
        with open(file_path, 'wb') as f:
            f.write(contents)
        file_paths.append(file_path)
        files_metadata.append({"name": file_name})
    
    # Index files
    indexing_result = indexing_pipeline.run(file_paths=file_paths, meta=files_metadata)

    # Remove files from disk
    if not keep_files:
        for file_path in file_paths:
            os.remove(file_path)

    return indexing_result



# Document Store
@app.get("/clear_document_store")
async def clear_document_store():
    
    try:
        doc_store.delete_documents()
    
    except Exception as e:
        return e
    
    return True

@app.get("/document_store_stats")
async def get_document_store_stats():
    document_count = doc_store.get_document_count()
    label_count = doc_store.get_label_count()
    embedding_count = doc_store.get_embedding_count()

    return {
        "document_count": document_count,
        "label_count": label_count,
        "embedding_count": embedding_count,
    }


# Tests
@app.get("/test_retriever")
async def test_retriever():
    retriever = get_retriever()
    return retriever.retrieve(query="What is total theorem?", top_k=10)


# Evaluate pipeline
# @app.get("/evaluate")
# async def evaluate(retriever_type: str = "BM25", reader_model: str = "deepset/roberta-base-squad2"):
#     # Clear the document store
#     doc_store.delete_documents()

#     # Fetch, store and preprocess evaluation data
#     # fetch_evaluation_data()

#     # Index evaluation data
#     eval_preprocessor = PreProcessor(
#     split_by="word",
#     split_length=200,
#     split_overlap=0,
#     split_respect_sentence_boundary=False,
#     clean_empty_lines=False,
#     clean_whitespace=False,
# )
#     doc_store.add_eval_data(
#         filename=f"{doc_dir}/evaluation_data/nq_dev_subset_v2.json",
#         preprocessor=eval_preprocessor
#     )

#     qp = query_pipeline(retriever_type= retriever_type, reader_model=reader_model)
    
#     eval_labels = doc_store.get_all_labels_aggregated(drop_negative_labels=True, drop_no_answers=True)
#     eval_result = qp.eval(labels=eval_labels, params={"Retriever": {"top_k": 5}})
    
#     # Calculating Evaluation Metrics
#     metrics = eval_result.calculate_metrics()
#     qp.print_eval_report(eval_result)


#     return metrics