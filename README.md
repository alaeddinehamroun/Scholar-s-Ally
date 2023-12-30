
uvicorn api:app --reload

localhost:8000/query



Steps:
clone the repo
create a venv and activate it
install requirements

launch es search:
python3 src/launch_es.py

launch the api:
cd src/api
uvicorn main:app --reload


Index files -> Query


launch the ui
streamlit