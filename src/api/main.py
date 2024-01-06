from fastapi import FastAPI, File, Form, UploadFile
from pipelines import query_pipeline, index_pipeline
import os
from document_store import doc_store
from retriever import get_retriever

# Init FastAPI
app = FastAPI()

doc_dir = '../../data'
@app.get("/query")
async def query(query: str, top_k_reader: int, top_k_retriever: int):
    pipeline = query_pipeline()
    return pipeline.run(query=query, params={"Retriever": {"top_k": top_k_retriever}, "Reader": {"top_k": top_k_reader}})


@app.get("/index")
async def index():
    indexing_pipeline = index_pipeline()
    files_to_index = [doc_dir + "/" + f for f in os.listdir(doc_dir)]
    files_metadata = [{"name": f} for f in os.listdir(doc_dir)]
    return indexing_pipeline.run(file_paths=files_to_index, meta=files_metadata)


@app.get("/initialized")
async def initialized():
    
    return True

@app.post('/file-upload')
async def upload_file(files: list[UploadFile]= File(...), keep_files=False):
    
    file_paths = []
    indexing_pipeline = index_pipeline()
    for file in files:
        contents = await file.read()
            
        # Keep the file on disk
        file_path = os.path.join(doc_dir, file.filename)
        with open(file_path, 'wb') as f:
            f.write(contents)
        file_paths.append(file_path)
    
    # Index files
    indexing_result = indexing_pipeline.run_batch(file_paths=file_paths)

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
    return retriever.retrieve(query="Who is the father of Arya Stark?", top_k=10)