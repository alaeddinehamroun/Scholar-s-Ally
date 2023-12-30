from fastapi import FastAPI
from pipelines import query_pipeline, index_pipeline
import os


# Init FastAPI
app = FastAPI()

doc_dir = '../../data'
@app.get("/query")
async def query(q):
    pipeline = query_pipeline()
    return pipeline.run(query=q, params={"Retriever": {"top_k": 1}, "Reader": {"top_k": 5}})


@app.get("/index")
async def index():
    indexing_pipeline = index_pipeline()
    files_to_index = [doc_dir + "/" + f for f in os.listdir(doc_dir)]
    return indexing_pipeline.run_batch(file_paths=files_to_index)

