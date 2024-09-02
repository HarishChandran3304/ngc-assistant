from embedchain import App
import streamlit as st
from dotenv import load_dotenv
load_dotenv()
from os import listdir

cfg = {
    "llm": {
        "provider": "huggingface",
        "config": {
            "model": "mistralai/Mistral-7B-Instruct-v0.2",
            "top_p": 0.5
        }
    },
    "embedder": {
        "provider": "huggingface",
        "config": {
            "model": "sentence-transformers/all-mpnet-base-v2",
        }
    },
}

app = App.from_config(config=cfg)

# for pdf_file in listdir("ic/week2"):
#     app.add(f"ic/week2/{pdf_file}", data_type="pdf_file")


st.title("NGC Helper")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm NGC Helper. Ask me your NGC quiz questions and receive instant answers 🙂"}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask away :)"):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.spinner("Thinking..."):
        response = app.query(prompt)
        print(response)
        response = response.split("Answer:\n")[1]

    st.chat_message("assistant").markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
