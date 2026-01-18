import os
from pathlib import Path

import ollama
import streamlit as st
from dotenv import load_dotenv
from surrealdb import Surreal

# Load environment variables from .env file
env_path = Path(__file__).resolve().parent.parent / ".env"

load_dotenv(dotenv_path=env_path)

OLLAMA_URL = os.getenv("OLLAMA_URL")
SURREALDB_URL = os.getenv("SURREALDB_URL")
model_name = "llama3.2"

db = Surreal(SURREALDB_URL)
db.signin(
    {"username": os.getenv("SURREALDB_USER"), "password": os.getenv("SURREALDB_PW")}
)
db.use("chatbot-rag-test", "chatbot-rag-test")


def initialize_db(db=db):
    db.query("""
    DEFINE TABLE IF NOT EXISTS chunks;
    DEFINE INDEX IF NOT EXISTS embedding_index ON chunks 
        FIELDS embedding
        MTREE DIMENSION 3072
        DIST COSINE;
    """)
    return st.success("Database initialized successfully!")


def split_text(text, chunk_size=500, overlap=100):
    """Simple text splitter with overlap"""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks


def store_chunks(chunks, db=db):
    """Store text chunks with embeddings in SurrealDB"""

    for chunk in chunks:
        embedding = ollama.embed(model=model_name, input=chunk)["embeddings"][0]

        query = """
        INSERT INTO chunks {
            text: $text,
            embedding: $embedding
        };
        """

        response = db.query(query, {"text": chunk, "embedding": embedding})
    return response


def retrieve_context(query, k=3, db=db):
    """Retrieve relevant context from SurrealDB"""

    query_embedding = ollama.embed(model=model_name, input=query)["embeddings"][0]

    surreal_query = """
    SELECT VALUE text FROM (
        SELECT text, vector::similarity::cosine(embedding, $embedding) AS similarity 
        FROM chunks
        WHERE embedding <|1|> $embedding
        ORDER BY similarity DESC 
        LIMIT $k
    );
    """

    response = db.query(surreal_query, {"embedding": query_embedding, "k": k})

    return response


st.title("RAG chatbot")
initialize_db()

uploaded_file = st.file_uploader("Upload a document", type=["txt"])
if uploaded_file:
    text = uploaded_file.read().decode("utf-8")
    chunks = split_text(text)
    res = store_chunks(chunks)
    print(res)
    st.success(f"Processed {len(chunks)} chunks!")

if "ollama_model" not in st.session_state:
    st.session_state["ollama_model"] = model_name

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What do you want to know?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Retrieve context and generate response
    context = retrieve_context(prompt)
    with st.chat_message("assistant"):
        # Add context as a system message
        system_message = {
            "role": "system",
            "content": f"Use the following context to answer the user's question:\n\n{context}",
        }
        chat_history = [system_message] + [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ]

        # Generate streamed response
        stream = ollama.chat(
            model=st.session_state["ollama_model"],
            messages=chat_history,
            stream=True,
        )
        response = st.write_stream(chunk["message"]["content"] for chunk in stream)

    st.session_state.messages.append({"role": "assistant", "content": response})
