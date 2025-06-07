# models/llama_model.py
import streamlit as st
from llama_cpp import Llama

@st.cache_resource(show_spinner="🦙 Loading LLaMA model...")
def get_llm():
    return Llama(
        model_path="./models/llama-2-7b-chat.Q4_K_M.gguf",  # ensure correct path
        n_ctx=2048,
        n_threads=8,
        verbose=True
    )
