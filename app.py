

import streamlit as st
import json
from langchain.vectorstores import FAISS
from langchain.embeddings import OllamaEmbeddings
from langchain.chains import RetrievalQA
from langchain.llms import Ollama
import time

# Configure page
st.set_page_config(
    page_title="Speech Analyzer Pro",
    page_icon="🎤",
    layout="wide"
)

# Ultra Modern CSS with animations and graphics
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        font-family: 'Inter', sans-serif;
        min-height: 100vh;
    }
    
    /* Animated Background Shapes */
    .background-shapes {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        overflow: hidden;
        z-index: -1;
        pointer-events: none;
    }
    
    .shape {
        position: absolute;
        border-radius: 50%;
        animation: float 20s infinite linear;
        opacity: 0.1;
    }
    
    .shape:nth-child(1) {
        width: 100px;
        height: 100px;
        background: radial-gradient(circle, #ff6b6b, #ee5a24);
        top: 20%;
        left: 10%;
        animation-delay: 0s;
    }
    
    .shape:nth-child(2) {
        width: 150px;
        height: 150px;
        background: radial-gradient(circle, #4834d4, #686de0);
        top: 60%;
        right: 10%;
        animation-delay: -7s;
    }
    
    .shape:nth-child(3) {
        width: 80px;
        height: 80px;
        background: radial-gradient(circle, #00d2d3, #54a0ff);
        top: 80%;
        left: 20%;
        animation-delay: -14s;
    }
    
    .shape:nth-child(4) {
        width: 120px;
        height: 120px;
        background: radial-gradient(circle, #ff9ff3, #f368e0);
        top: 10%;
        right: 30%;
        animation-delay: -3s;
    }
    
    @keyframes float {
        0% { transform: translateY(0px) rotate(0deg); }
        33% { transform: translateY(-30px) rotate(120deg); }
        66% { transform: translateY(30px) rotate(240deg); }
        100% { transform: translateY(0px) rotate(360deg); }
    }
    
    /* Glassmorphism Container */
    .glass-container {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        padding: 2rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .glass-container:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.2);
    }
    
    /* Animated Header */
    .main-header {
        font-size: 4rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(45deg, #fff, #f1c40f, #e74c3c, #9b59b6);
        background-size: 400% 400%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradient 4s ease-in-out infinite;
        text-shadow: 0 5px 15px rgba(0,0,0,0.3);
        position: relative;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: -10px;
        left: -10px;
        right: -10px;
        bottom: -10px;
        background: linear-gradient(45deg, #ff0000, #ff7300, #fffb00, #48ff00, #00ffd5, #002bff, #7a00ff, #ff00c8, #ff0000);
        border-radius: 20px;
        z-index: -1;
        animation: spin 3s linear infinite;
        filter: blur(20px);
        opacity: 0.3;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Neon Speech Quote */
    .speech-quote {
        background: rgba(0, 0, 0, 0.7);
        border: 2px solid #00ffff;
        border-radius: 15px;
        padding: 2rem;
        margin: 2rem 0;
        font-size: 1.2rem;
        line-height: 1.8;
        color: #ffffff;
        position: relative;
        overflow: hidden;
        animation: neonGlow 2s ease-in-out infinite alternate;
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.5);
    }
    
    .speech-quote::before {
        content: '"';
        position: absolute;
        top: -20px;
        left: 20px;
        font-size: 5rem;
        color: #00ffff;
        opacity: 0.3;
        font-family: serif;
    }
    
    .speech-quote::after {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
        animation: shine 3s infinite;
    }
    
    @keyframes neonGlow {
        from { box-shadow: 0 0 20px rgba(0, 255, 255, 0.5), inset 0 0 20px rgba(0, 255, 255, 0.1); }
        to { box-shadow: 0 0 30px rgba(0, 255, 255, 0.8), inset 0 0 30px rgba(0, 255, 255, 0.2); }
    }
    
    @keyframes shine {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    /* Animated Buttons and Inputs */
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.9) !important;
        border-radius: 15px !important;
        border: 2px solid transparent !important;
        background-clip: padding-box !important;
        transition: all 0.3s ease !important;
        color: black !important;
    }
    
    .stSelectbox > div > div:hover {
        transform: scale(1.02) !important;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2) !important;
    }
    
    .stSelectbox select {
        color: black !important;
    }
    
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.9) !important;
        border-radius: 15px !important;
        border: 2px solid #667eea !important;
        transition: all 0.3s ease !important;
        font-size: 1.1rem !important;
        padding: 12px 20px !important;
        color: black !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #00ffff !important;
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.3) !important;
        transform: scale(1.02) !important;
    }
    
    /* Floating Action Elements */
    .floating-icon {
        display: inline-block;
        animation: bounce 2s infinite;
        font-size: 2rem;
        margin: 0 10px;
    }
    
    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
        40% { transform: translateY(-10px); }
        60% { transform: translateY(-5px); }
    }
    
    /* Premium Answer Section */
    .answer-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        padding: 0;
        margin: 2rem 0;
        overflow: hidden;
        position: relative;
        animation: slideIn 0.5s ease-out;
    }
    
    .answer-header {
        background: rgba(255, 255, 255, 0.1);
        padding: 1.5rem;
        color: white;
        font-size: 1.5rem;
        font-weight: 600;
        border-bottom: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .answer-content {
        background: rgba(255, 255, 255, 0.95);
        padding: 2rem;
        color: #333;
        font-size: 1.1rem;
        line-height: 1.8;
        border-radius: 0 0 20px 20px;
        position: relative;
    }
    
    .answer-content::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: linear-gradient(to bottom, #667eea, #764ba2);
        animation: pulse 2s infinite;
    }
    
    @keyframes slideIn {
        from { transform: translateX(-100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes pulse {
        0% { opacity: 0.5; }
        50% { opacity: 1; }
        100% { opacity: 0.5; }
    }
    
    /* Loading Animation */
    .custom-spinner {
        display: inline-block;
        width: 40px;
        height: 40px;
        border: 4px solid rgba(0, 255, 255, 0.3);
        border-radius: 50%;
        border-top-color: #00ffff;
        animation: spin 1s ease-in-out infinite;
        margin-right: 10px;
    }
    
    /* Section Headers */
    .section-header {
        font-size: 1.8rem;
        font-weight: 600;
        color: white;
        text-align: center;
        margin: 2rem 0 1rem 0;
        text-shadow: 0 2px 10px rgba(0,0,0,0.3);
    }
    
    /* Footer */
    .footer {
        background: rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        color: white;
        margin-top: 3rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
</style>
""", unsafe_allow_html=True)

# Animated Background Shapes
st.markdown("""
<div class="background-shapes">
    <div class="shape"></div>
    <div class="shape"></div>
    <div class="shape"></div>
    <div class="shape"></div>
</div>
""", unsafe_allow_html=True)

# Animated Header with floating icons
st.markdown("""
<h1 class="main-header">
    <span class="floating-icon">🎤</span>
    Speech Analysis Pro
    <span class="floating-icon">🚀</span>
</h1>
""", unsafe_allow_html=True)

# Load speech data
try:
    with open("data/speeches.json") as f:
        speeches = json.load(f)
except FileNotFoundError:
    st.error("❌ Speech data file not found. Please ensure 'data/speeches.json' exists.")
    st.stop()

# Speech selection in glassmorphism container
st.markdown("<hr style='border: 1px solid #bbb;'>", unsafe_allow_html=True)
st.markdown('<h2 class="section-header">📋 Select Your Speech</h2>', unsafe_allow_html=True)
titles = [s["title"] for s in speeches]
selected_title = st.selectbox(
    "Choose from our curated collection:",
    titles,
    help="Select a speech to analyze with our AI-powered system"
)
st.markdown('</div>', unsafe_allow_html=True)

# Get selected speech
selected_speech = next(s for s in speeches if s["title"] == selected_title)

# Display speech content with neon styling
st.markdown('<h2 class="section-header">✨ Speech Content</h2>', unsafe_allow_html=True)
speech_html = f"""
<div class="speech-quote">
    <div style="font-size: 1.4rem; font-weight: 600; color: #00ffff; margin-bottom: 1rem;">
        "{selected_speech['title']}"
    </div>
    <div style="font-style: italic;">
        {selected_speech['text'].replace(chr(10), '<br><br>')}
    </div>
</div>
"""
st.markdown(speech_html, unsafe_allow_html=True)

# Question section in glassmorphism container
st.markdown("<hr style='border: 1px solid #bbb;'>", unsafe_allow_html=True)
st.markdown('<h2 class="section-header">🤔 Ask Your Question</h2>', unsafe_allow_html=True)
question = st.text_input(
    "What insights would you like to discover?",
    placeholder="e.g., What emotions does this speech convey?",
    help="Ask anything about the speech - themes, emotions, rhetorical devices, historical context..."
)
st.markdown('</div>', unsafe_allow_html=True)

# Process question with premium styling
if question:
    # Custom loading animation
    loading_placeholder = st.empty()
    loading_placeholder.markdown("""
    <div style="text-align: center; padding: 2rem;">
        <div class="custom-spinner"></div>
        <span style="color: white; font-size: 1.2rem; margin-left: 10px;">
            🧠 AI is analyzing your speech...
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    try:
        # Load FAISS with Ollama embeddings
        embedding = OllamaEmbeddings(model="mistral")
        db = FAISS.load_local("vectorstore/faiss_index", embedding, allow_dangerous_deserialization=True)
        
        # Filter to only chunks belonging to the selected speech title
        def metadata_filter(metadata):
            return metadata.get("title") == selected_title
        
        retriever = db.as_retriever(search_kwargs={"k": 5, "filter": metadata_filter})
        
        # Setup retrieval QA chain
        llm = Ollama(model="mistral")
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm, 
            retriever=retriever, 
            return_source_documents=True
        )
        
        # Query the chain
        result = qa_chain({"query": question})
        
        # Clear loading animation
        loading_placeholder.empty()
        
        # Display answer in premium container
        st.markdown(f"""
        <div class="answer-container">
            <div class="answer-header">
                <span class="floating-icon">✨</span>
                AI Analysis Results
                <span class="floating-icon">🎯</span>
            </div>
            <div class="answer-content">
                {result["result"]}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        print(result)
        
    except Exception as e:
        loading_placeholder.empty()
        st.markdown(f"""
        <div class="glass-container">
            <h3 style="color: #ff6b6b; text-align: center;">❌ Oops! Something went wrong</h3>
            <p style="color: white; text-align: center; font-size: 1.1rem;">
                {str(e)}
            </p>
            <p style="color: #00ffff; text-align: center;">
                💡 Make sure Ollama is running and the FAISS index exists
            </p>
        </div>
        """, unsafe_allow_html=True)

# Premium Footer
st.markdown("""
<div class="footer">
    <div style="font-size: 1.2rem; font-weight: 500; margin-bottom: 0.5rem;">
        🚀 Project by Ninad Gawali
    </div>
    <div style="opacity: 0.8;">
        Userinterface with Streamlit ⚡ | AI Engine using Ollama & LangChain 🤖
    </div>
</div>
""", unsafe_allow_html=True)