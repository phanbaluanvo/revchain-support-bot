import streamlit as st
from chatbot import stream_generator, ensure_single_thread_id, initialize_client

# Initialize the OpenAI client
client, assistant_id = initialize_client()

# Streamlit page setup
st.set_page_config(page_title="Revchain Chatbot", page_icon=":speech_balloon:")

hide_streamlit_style = """
                <style>
                div[data-testid="stStatusWidget"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                </style>
                """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

st.title("Revchain Support Chatbot")

# Add Start and Exit buttons
if "start_chat" not in st.session_state:
    st.session_state.start_chat = False

if "messages" not in st.session_state:
    st.session_state.messages = []

# Start Chat button in the sidebar
if st.sidebar.button("Start Chat"):
    st.session_state.start_chat = True
    st.session_state.thread_id = client.beta.threads.create().id
    st.session_state.messages = []

# Exit Chat button
if st.sidebar.button("Exit Chat"):
    st.session_state.start_chat = False
    st.session_state.thread_id = None
    st.session_state.messages = []

# Chat logic only if the chat has started
if st.session_state.start_chat:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input("How can I help you?")
    if prompt:
        thread_id = ensure_single_thread_id(client)  # Ensure thread_id is created before using it
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            response = st.write_stream(stream_generator(prompt, thread_id, client, assistant_id))
        st.session_state.messages.append({"role": "assistant", "content": response})
else:
    st.write("Click 'Start Chat' to begin.")
