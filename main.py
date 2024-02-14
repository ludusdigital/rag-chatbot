import streamlit as st
from llama_index.core import VectorStoreIndex, ServiceContext, Document
from llama_index.llms.openai import OpenAI
import openai
from llama_index.core import SimpleDirectoryReader

st.set_page_config(page_title="RAG chatbot",
                   page_icon="🤖",
                   layout="centered",
                   initial_sidebar_state="auto",
                   menu_items=None)
openai.api_key = st.secrets.openai_key
st.title("Razgovor sa mojim znanjem 🧠")

if "messages" not in st.session_state.keys(
):  # Initialize the chat messages history
  st.session_state.messages = [{
      "role":
      "assistant",
      "content":
      "Baza vašeg znanja je učitana i spreman sam za pitanja 🧠🚀"
  }]


@st.cache_resource(show_spinner=False)
def load_data():
  with st.spinner(
      text="Učitavam podatke iz baze! Ovo može da potraje 1-2 minuta."):
    reader = SimpleDirectoryReader(input_dir="./data", recursive=True)
    docs = reader.load_data()
    service_context = ServiceContext.from_defaults(llm=OpenAI(
        model="gpt-3.5-turbo-1106",
        temperature=0.5,
        system_prompt=
        "Ti si ekspert za davanje preciznih i efikasnih odgovora vezano za moju bazu znanja. Jezik: svaki odgovor isključivo piši na srpskom jeziku, koristeći srpsku gramatiku."
    ))
    index = VectorStoreIndex.from_documents(docs,
                                            service_context=service_context)
    return index


index = load_data()

if "chat_engine" not in st.session_state.keys():  # Initialize the chat engine
  st.session_state.chat_engine = index.as_chat_engine(
      chat_mode="condense_question", verbose=True)

if prompt := st.chat_input(
    "Tvoje pitanje"):  # Prompt for user input and save to chat history
  st.session_state.messages.append({"role": "user", "content": prompt})

# Display the prior chat messages with custom avatars
for message in st.session_state.messages:
  role = message["role"]
  content = message["content"]
  if role == "user":
    with st.chat_message(role, avatar="🤔"):  # Change to desired user avatar
      st.write(content)
  elif role == "assistant":
    with st.chat_message(role,
                         avatar="🧠"):  # Change to desired assistant avatar
      st.write(content)

# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
  with st.chat_message("assistant",
                       avatar="🧠"):  # Assistant's response with custom avatar
    with st.spinner("Razmišljam..."):
      response = st.session_state.chat_engine.chat(prompt)
      st.write(response.response)
      message = {"role": "assistant", "content": response.response}
      st.session_state.messages.append(
          message)  # Add response to message history
