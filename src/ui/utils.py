import requests
import logging
from time import sleep
from typing import Tuple, Optional

API_ENDPOINT = 'http://localhost:8000'
DOC_REQUEST = "query"
DOC_UPLOAD = "file-upload"
STATUS = "initialized"


def query(query, top_k_reader=5, top_k_retriever=2):
    """
    Send a query to the REST API and parse the answer.
    Returns both a ready-to-use representation of the results and the raw JSON.
    """

    url = f"{API_ENDPOINT}/{DOC_REQUEST}"
    params = {
        "query": query,
        "top_k_reader": top_k_reader,
        "top_k_retriever": top_k_retriever,
    }
    response_raw = requests.get(url, params=params)

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


def haystack_is_ready():
    """
    Use the REST API to check if Haystack is ready to answer questions.
    """
    url = f"{API_ENDPOINT}/{STATUS}"

    try:
        if requests.get(url).status_code < 400:
            return True
    except Exception as e:
        logging.exception(e)
        sleep(1)  # To avoid spamming a non-existing endpoint at startup
    return False


def get_backlink(result) -> Tuple[Optional[str], Optional[str]]:
    if result.get("document", None):
        doc = result["document"]
        if isinstance(doc, dict):
            if doc.get("meta", None):
                if isinstance(doc["meta"], dict):
                    if doc["meta"].get("url", None) and doc["meta"].get("title", None):
                        return doc["meta"]["url"], doc["meta"]["title"]
    return None, None


def upload_doc(file):
    url = f"{API_ENDPOINT}/{DOC_UPLOAD}"
    files = [("files", file)]
    response = requests.post(url, files=files).json()
    return response