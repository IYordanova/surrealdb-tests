# SurrealDB Chatbot with Ollama and RAG

## Setting up the project

Run the following commands:
```shell
uv init
uv add surrealdb streamlit ollama python-dotenv 
uv add --dev ruff
```

## Running the app

### Launch the app in a new window
```shell
streamlit run app.py 
```

### Launch the app silently
```shell
streamlit run app.py --server.headless=True
```



