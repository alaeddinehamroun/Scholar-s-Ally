import requests


API_ENDPOINT = 'http://localhost:8000/api'
DOC_REQUEST = "query"
DOC_UPLOAD = "file-upload"


def query(query, filters={}, top_k_reader=5, top_k_retriever=5):
    """
    Send a query to the REST API and parse the answer.
    Returns both a ready-to-use representation of the results and the raw JSON.
    """

    url = f"{API_ENDPOINT}/{DOC_REQUEST}"
    params = {
        "query": query,
        "filters": filters,
        "top_k_reader": top_k_reader,
        "top_k_retriever": top_k_retriever,
    }
    req = {"query": query, "params": params}
    response_raw = requests.post(url, json=req)

    if response_raw.status_code >=400 and response_raw.status_code !=503:
        raise Exception(f"{vars(response_raw)}")
    
    response = response_raw.json()
    if 'errors' in response:
        raise Exception(", ".join(response["errors"]))
    
    # Format response
    results = []
    answers = response["answers"]

    for answer in answers:
        if answer.get("answer", None):
            results.append(
                {
                    "context": "..." + answer["context"] + "...",
                    "answer": answer.get("answer", None),
                    "source": answer["meta"]["name"],
                    "relevance": round(answer["score"] * 100, 2),
                    "document": [doc for doc in response["documents"] if doc["id"] in answer["document_ids"]][0],
                    "offset_start_in_doc": answer["offsets_in_document"][0]["start"],
                    "_raw": answer,
                }
            )
        else:
            results.append(
                {
                    "context": None,
                    "answer": None,
                    "document": None,
                    "relevance": round(answer["score"] * 100, 2),
                    "_raw": answer,
                }
            )
    return results, response




def upload_doc(file):
    url = f"{API_ENDPOINT}/{DOC_UPLOAD}"
    files = [("files", files)]
    response = requests.post(url, files=files).json()
    return response

