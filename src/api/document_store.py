
from haystack.document_stores import ElasticsearchDocumentStore

# Init Elasticsearch Document Store
doc_store = ElasticsearchDocumentStore(
        host="localhost", 
        username="", 
        password="", 
        index="document",
)

