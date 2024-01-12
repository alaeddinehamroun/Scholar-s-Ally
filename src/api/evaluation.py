from haystack.utils import fetch_archive_from_http
import os

from haystack.document_stores import ElasticsearchDocumentStore
from haystack.utils import launch_es
import time
from haystack.nodes import PreProcessor

launch_es()

time.sleep(30)

# Download evaluation data, which is a subset of Natural Questions development set containing 50 documents with one question per document and multiple annotated answers
doc_dir = "data/evaluation_data"
s3_url = "https://s3.eu-central-1.amazonaws.com/deepset.ai-farm-qa/datasets/nq_dev_subset_v2.json.zip"
fetch_archive_from_http(url=s3_url, output_dir=doc_dir)
