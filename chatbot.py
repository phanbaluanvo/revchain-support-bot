import openai
import time
import streamlit as st
from openai import OpenAI
import re

# Initialize the OpenAI client and assistant_id
def initialize_client():
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    assistant_id = st.secrets["ASSISTANT_ID"]
    return client, assistant_id

# Function to ensure that a single thread is created
def ensure_single_thread_id(client):
    if "thread_id" not in st.session_state or st.session_state.thread_id is None:
        thread = client.beta.threads.create()
        st.session_state.thread_id = thread.id
    return st.session_state.thread_id

# Stream response from OpenAI assistant
def stream_generator(prompt, thread_id, client, assistant_id):
    with st.spinner("Please wait... Your helpful bot is responding..."):
        message = client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=prompt
        )

        stream = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id,
            stream=True
        )

    pattern = r'【\d+:\d+†source】'

    for event in stream:
        if event.data.object == "thread.message.delta":
            for content in event.data.delta.content:
                if content.type == 'text':
                    if re.search(pattern, content.text.value):
                        continue  # Skip if it matches the pattern
                    yield content.text.value
                    time.sleep(0.02)
        else:
            pass
