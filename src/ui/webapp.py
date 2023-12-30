import streamlit as st
import os

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
    set_state_if_absent("random_question_requested", False)

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
    eval_mode = st.sidebar.checkbox("Evaluation mode")
    debug = st.sidebar.checkbox("Debug mode")

    # File upload block





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
    wit 