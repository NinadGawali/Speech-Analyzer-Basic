# 🗣️ Speech Analyzer

A powerful and interactive web application that allows users to explore and query **famous persuasive speeches** using **natural language**. This project combines **web scraping**, **text chunking**, **vector embeddings**, and a **local LLM (Ollama Mistral)** to answer questions based on the content of historical speeches.


## Project Structure

- `app.py` — Streamlit app providing the frontend interface for user interaction.  
- `basic.ipynb` — Jupyter Notebook that handles data ingestion, text splitting, and vector database preparation.  
- `requirements.txt` — List of required Python packages for easy installation.  
- `Video.mp4` — A sample demo video showing the project in action.  
- `vectorstore/` — Directory containing the saved FAISS vector index.  
- `data/` — Directory containing the scraped speeches saved as JSON.
## Features

- Scrapes famous persuasive speeches from a public website.  
- Splits long speeches into meaningful chunks for embedding.  
- Uses Ollama’s local **Mistral** model to generate vector embeddings.  
- Stores embeddings efficiently with **FAISS** for fast similarity search.  
- Interactive question-answering interface using **Streamlit**.  
- Answers are contextually grounded in the original speech content.


## Setup Instructions

### 1. Create and activate a virtual environment (using Python 3.10)

### On macOS/Linux:
```bash
python3.10 -m venv venv
source venv/bin/activate
```

### On Windows
```bash
python3.10 -m venv venv
venv\Scripts\activate
```

### 2. Install required packages

Run:

```bash
pip install -r requirements.txt
```


### 3. Install Ollama and pull the Mistral model

Make sure [Ollama](https://ollama.com/) is installed on your machine. Then pull the Mistral model with:

```bash
ollama pull mistral
```


### 4. Run the Streamlit application

Start the app by running:

```bash
streamlit run app.py
```


    
## About the Notebook (`basic.ipynb`)

This notebook covers:

- Scraping speech titles, texts, and backgrounds from a public website.  
- Saving the scraped data into JSON files.  
- Splitting speeches into chunks with overlap to preserve context.  
- Generating vector embeddings using Ollama Mistral.  
- Creating and saving a FAISS vector store for semantic search.
## Demo Video

You can view a sample video demonstration in the included `Video.mp4` file to see how the application works in practice.
![Video](https://github.com/user-attachments/assets/db77e45a-85cf-46d5-833a-6b28f490d171)

## Tech Stack

This project leverages a modern, efficient, and scalable tech stack designed for local, high-performance natural language processing and interactive applications.

- **Python 3.10**  
  Utilized as the core programming language for its versatility and rich ecosystem of libraries.

- **BeautifulSoup**  
  For robust and flexible web scraping to extract and parse HTML content efficiently.

- **LangChain**  
  Employed for advanced text chunking, document indexing, and pipeline management to structure and process large text corpora.

- **FAISS (Facebook AI Similarity Search)**  
  Integrated to enable fast and scalable vector similarity search for high-dimensional embedding retrieval.

- **Ollama Mistral LLM**  
  Used locally to generate high-quality embeddings and provide intelligent, context-aware question answering without relying on external APIs.

- **Streamlit**  
  Powers the interactive and user-friendly frontend, facilitating rapid prototyping and deployment of the web app.

## Authors

- [@Ninad Gawali](https://github.com/NinadGawali)


## License

[MIT](https://choosealicense.com/licenses/mit/)

