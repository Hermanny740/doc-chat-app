import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

from html_Templates import css, bot_template, user_template

import os   ### NEU


def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


def get_conversation_chain(vectorstore):
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    llm = ChatOpenAI()
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory)
    return conversation_chain


def get_vectorstore(text_chunks=None):
    """Erstellt oder lädt eine lokale Vektordatenbank."""
    embeddings = OpenAIEmbeddings()
    index_path = "faiss_index"

    # Fall 1: es gibt schon eine DB und KEINE neuen Texte -> nur laden
    if text_chunks is None and os.path.exists(index_path):
        vectorstore = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
        return vectorstore

    # Fall 2: neue Texte wurden übergeben
    if text_chunks:
        if os.path.exists(index_path):
            # bestehende DB laden
            vectorstore = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
            # neue Texte einfügen
            new_store = FAISS.from_texts(text_chunks, embeddings)
            vectorstore.merge_from(new_store)   ### NEU: Erweiterung
        else:
            # komplett neue DB anlegen
            vectorstore = FAISS.from_texts(text_chunks, embeddings)

        # immer speichern
        vectorstore.save_local(index_path)
        return vectorstore

    return None  # falls nichts passt


def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def handle_user_input(user_question):
    response = st.session_state.conversation({"question": user_question})
    
    st.session_state.chat_history = response["chat_history"]    
    chat_html = '<div class="chat-container">'
    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:  # User message
            chat_html += user_template.replace("{{MSG}}", message.content)
        else:  # Bot message
            chat_html += bot_template.replace("{{MSG}}", message.content)
    chat_html += "</div>"
    st.write(chat_html, unsafe_allow_html=True)


def main():
    load_dotenv()

    st.set_page_config(page_title="PDF Chat", page_icon=":books:")
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("PDF Chat")

    # Automatisch versuchen, bestehende DB zu laden
    if st.session_state.conversation is None:
        vectorstore = get_vectorstore()   ### NEU: lädt nur
        if vectorstore:
            st.session_state.conversation = get_conversation_chain(vectorstore)
            st.success("Lokale Vektordatenbank geladen!")

    user_question = st.text_input("Ask a question about your PDF:")

    if user_question and st.session_state.conversation:
        handle_user_input(user_question)
    elif user_question and st.session_state.conversation is None:
        st.warning("Bitte zuerst ein PDF hochladen und verarbeiten.")

    with st.sidebar:
        st.subheader("Kontext-Generierung")
        context_method = st.radio(
        "Wähle die Methode:",
        ["Nur Text", "Multimodal"],
        index=0  # Standard auf "Nur Text"
    )

    st.write(f"Aktuell gewählte Methode: {context_method}") 

    with st.sidebar:
        st.subheader("Settings")
        pdf_docs = st.file_uploader("Upload your PDF and click on process", type=["pdf"], accept_multiple_files=True)
        if st.button("Process", key="process_pdf"):
            with st.spinner("Processing PDF..."):
                raw_text = get_pdf_text(pdf_docs)
                text_chunks = get_text_chunks(raw_text)

                # Vektorstore erstellen/erweitern
                vectorstore = get_vectorstore(text_chunks)
                st.session_state.conversation = get_conversation_chain(vectorstore)

                st.success("PDF processed successfully!")
                st.write("You can now ask questions about your PDF.")


if __name__ == "__main__":
    main()