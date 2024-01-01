# Scholar-s-Ally: An extractive QA solution designed to navigate and distill complex educational materials.

Extractive Question Answering (QA) is a type of question-answering system where the answer to a question is extracted directly from a text or a set of texts. In extractive QA, the answer is a segment of text (such as a phrase or sentence) taken verbatim from a document or documents, rather than being generated or summarized. This method relies on identifying and extracting the most relevant parts of the text that directly answer the posed question.


Scholar's Ally. How it works?
1. Integrate educational content: chapters of a specific subject at school (pdfs).
2. Type a question about it.
3. Get the most relevant information from the integrated content and where to find it.
## Installation steps

#### 1. Clone the repository:
```bash
git clone https://github.com/alaeddinehamroun/Scholar-s-Ally.git
cd Scholar-s-Ally
```
#### 2. Create a virtual environment and activate it:
```bash
# Make sure you have python3 and pip installed
python3 -m venv .venv
source .venv/bin/activate

# To  deactivate the environment run:
# deactivate
```
#### 3. Install the required dependencies:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 4. Launch Elasticsearch server:
You can visit the docs of Elasticsearch for more details.
```bash
# Make sure that Docker is available in your environment.
python3 src/launch_es.py
```
or 
```bash
docker pull docker.elastic.co/elasticsearch/elasticsearch:7.9.2
docker run -d -p 9200:9200 -e "discovery.type=single-node" elasticsearch:7.9.2
```
#### 5. Start the API:
```bash
cd src/api
uvicorn main: app --reload
```
For now, two endpoints are available:
1. Index: to index your files availables at data/ folder
2. Query: enter your question and you'll get the top_k answers


#### 6. Start the UI (Soon):
```bash
cd src/
python3 -m streamlit run ui/webapp.py 
```