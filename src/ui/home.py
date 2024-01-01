import streamlit as st
import os
import logging
from json import JSONDecodeError
from ui.utils import haystack_is_ready, query, get_backlink, upload_doc
from annotated_text import annotation
from markdown import markdown

# Adjust to a question that you would like users to see in the search bar when they load the UI:
DEFAULT_QUESTION_AT_STARTUP = "Who is me?"
DEFAULT_ANSWER_AT_STARTUP = "Alaeddine"
DEFAULT_NUMBER_OF_ANSWERS = 3
DEFAULT_DOCS_FROM_RETRIEVER = 3

def set_state_if_absent(key, value):
    if key not in st.session_state:
        st.session_state[key] = value

def main():
    st.set_page_config("EduAssistant Demo")

    # Persisten state
    set_state_if_absent("question", DEFAULT_QUESTION_AT_STARTUP)
    set_state_if_absent("answer", DEFAULT_ANSWER_AT_STARTUP)
    set_state_if_absent("results", None)
    set_state_if_absent("raw_json", None)

    # Callback to reset the interface in case the text of the question changes
    def reset_results(*args):
        st.session_state.answer = None
        st.session_state.results = None
        st.session_state.raw_json = None

    # Title
    st.write("# Learning Assistant Demo")
    st.markdown(
        """
Ask a question and see if Haystack can find the correct answer to your query!
        """,
        unsafe_allow_html=True,
    )

    # Sidebar
    st.sidebar.header("Options")
    top_k_reader = st.sidebar.slider(
        "Max. number of answers",
        min_value=1,
        max_value=10,
        value=DEFAULT_NUMBER_OF_ANSWERS,
        step=1,
        on_change=reset_results,
    )
    top_k_retriever = st.sidebar.slider(
        "Max. number of documents from retriever",
        min_value=1,
        max_value=10,
        value=DEFAULT_DOCS_FROM_RETRIEVER,
        step=1,
        on_change=reset_results
    )
    debug = st.sidebar.checkbox("Debug mode")

    # File upload block
    st.sidebar.write('## File Upload:')
    data_files = st.sidebar.file_uploader(
        "upload", type=['pdf'], accept_multiple_files=True, label_visibility="hidden"
    )
    for data_file in data_files:
        # Upload file
        if data_file:
            try:
                raw_json = upload_doc(data_file)
                st.sidebar.write(str(data_file.name) + " &nbsp;&nbsp; ✅ ")
                if debug:
                    st.subheader("REST API JSON response")
                    st.sidebar.write(raw_json)
            except Exception as e:
                st.sidebar.write(str(data_file.name) + " &nbsp;&nbsp; ❌ ")
                st.sidebar.write("_This file could not be parsed, see the logs for more information._")


    # Search bar
    question = st.text_input(
        value=st.session_state.question,
        max_chars=100,
        on_change=reset_results,
        label="Question",
        label_visibility="hidden"
    )
    col1, col2 = st.columns(2)
    col1.markdown("<style>.stButton button {width:100%;}</style>", unsafe_allow_html=True)
    # col2.markdown("<style>.stButton button {width:100%;}</style>", unsafe_allow_html=True)

    # Run button
    run_pressed = col1.button("Run")

    run_query = (
        run_pressed or question != st.session_state.question
    )

    # Check to connection
    with st.spinner("⌛️ &nbsp;&nbsp; API is starting..."):
        if not haystack_is_ready():
            st.error("🚫 &nbsp;&nbsp; Connection Error. Is API running?")
            run_query = False
            reset_results()

    # Get results for query
    if run_query and question:
        reset_results()
        st.session_state.question = question

        with st.spinner(
            "🧠 &nbsp;&nbsp; Performing neural search on documents... \n "
        ):
            try:
                st.session_state.results, st.session_state.raw_json = query(
                    question, top_k_reader=top_k_reader, top_k_retriever=top_k_retriever
                )
            except JSONDecodeError as je:
                st.error("👓 &nbsp;&nbsp; An error occurred reading the results. Is the document store working?")
                return
            except Exception as e:
                logging.exception(e)
                if "The server is busy processing requests" in str(e) or "503" in str(e):
                    st.error("🧑‍🌾 &nbsp;&nbsp; All our workers are busy! Try again later.")
                else:
                    st.error("🐞 &nbsp;&nbsp; An error occurred during the request.")
                return
    
    if st.session_state.results:

  
        st.write("## Results:")

        for count, result in enumerate(st.session_state.results):
            if result['answer']:
                answer, context = result['answer'], result['context']
                start_idx = context.find(answer)
                end_idx = start_idx + len(answer)   
                st.write(
                    markdown(context[:start_idx] + str(annotation(answer, "ANSWER", "#8ef")) + context[end_idx:]),
                    unsafe_allow_html=True,
                )
                source = ""
                url, title = get_backlink(result)
                if url and title:
                    source = f"[{result['document']['meta']['title']}]({result['document']['meta']['url']})"
                else:
                    source = f"{result['source']}"
                st.markdown(f"**Relevance:** {result['relevance']} -  **Source:** {source}")
            

            else: 
                st.info(
                    "🤔 &nbsp;&nbsp; Unsure whether any of the documents contain an answer to your question. Try to reformulate it!"
                )
                st.write("**Relevance:** ", result["relevance"])

            st.write("____")

        if debug:
            st.subheader("REST API JSON response")
            st.write(st.session_state.raw_json)

main()