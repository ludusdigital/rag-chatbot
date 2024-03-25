import streamlit as st
from llama_index.core import VectorStoreIndex, ServiceContext, Document
from llama_index.llms.openai import OpenAI
import openai
from llama_index.core import SimpleDirectoryReader
import os
import shutil
import docx2txt 

st.set_page_config(page_title="RAG chatbot", page_icon="🤖", layout="centered")

openai.api_key = os.environ['OPENAI_API_KEY']

st.title("Ask my knowledge 🧠")

if 'messages' not in st.session_state:
    st.session_state['messages'] = []


if not os.path.exists('data'):
    os.makedirs('data')

uploaded_file = st.file_uploader("Upload .txt, .pdf ili .docx fajl", type=['txt', 'pdf', 'docx'])
if uploaded_file is not None:
    if uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        # Ako je fajl .docx, koristite docx2txt za ekstrakciju teksta
        text = docx2txt.process(uploaded_file)
        file_path = os.path.join('data', uploaded_file.name.replace('.docx', '.txt'))
        with open(file_path, "w") as text_file:
            text_file.write(text)
        st.success(f"'{uploaded_file.name}' je uspešno sačuvan kao tekst.")
    else:
        # Obrada za .txt i .pdf ostaje ista
        file_path = os.path.join('data', uploaded_file.name)
        with open(file_path, "wb") as f:
            shutil.copyfileobj(uploaded_file, f)
        st.success(f"'{uploaded_file.name}' je uspešno sačuvan.")
    
    def load_data():
        with st.spinner(text="Loading data from the database. This may take 1-2 minutes."):
            reader = SimpleDirectoryReader(input_dir="./data", recursive=True)
            docs = reader.load_data()
            service_context = ServiceContext.from_defaults(llm=OpenAI(
                model="gpt-3.5-turbo-1106",
                temperature=0.5,
                system_prompt="Ti si ekspert za davanje preciznih i efikasnih odgovora vezano za moju bazu znanja. Jezik: svaki odgovor isključivo piši na srpskom jeziku, koristeći srpsku gramatiku."
            ))
            index = VectorStoreIndex.from_documents(docs, service_context=service_context)
            return index
    
    index = load_data()
    st.session_state.chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)
    st.session_state.data_loaded = True  # Označava da su podaci učitani
    # Postavljanje poruke o uspešnom učitavanju podataka
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Baza vašeg znanja je učitana i spreman sam za pitanja 🧠🚀"}]

if prompt := st.chat_input("Your question"):
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages:
    role = message["role"]
    content = message["content"]
    if role == "user":
        with st.chat_message(role, avatar="🤔"):
            st.write(content)
    elif role == "assistant":
        with st.chat_message(role, avatar="🧠"):
            st.write(content)

# Pre nego što pokušate da pristupite poslednjoj poruci, proverite da li lista sadrži neke poruke
if len(st.session_state.messages) > 0 and st.session_state.messages[-1]["role"] != "assistant" and "data_loaded" in st.session_state:
    with st.chat_message("assistant", avatar="🧠"):
        with st.spinner("Thinking..."):
            response = st.session_state.chat_engine.chat(prompt)
            st.write(response.response)
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message)

