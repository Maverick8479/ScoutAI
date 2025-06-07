# 🤖 ScoutAI – LLaMA-Powered Hiring Assistant Chatbot

ScoutAI is an intelligent, interactive Streamlit-based chatbot that simplifies the technical hiring process. It collects candidate details through natural conversation and generates tailored technical interview questions using LLaMA 2 models (via `llama-cpp-python`). Designed for offline use, ScoutAI is privacy-compliant and ideal for lightweight AI-powered screening.

---

## 🛠️ Project Overview

ScoutAI serves as a virtual hiring assistant that:
- Collects structured candidate information
- Generates role-appropriate technical interview questions based on the candidate’s tech stack
- Provides an intuitive and chat-like UI for a seamless candidate experience
- Can run **locally and privately**, without relying on cloud APIs (thanks to LLaMA)

---
Download LLaMA Model

Place a quantized LLaMA model .gguf file inside the /models/ directory (llama-2-7b-chat.Q4_K_M.gguf).
models/
├── llama_model.py
├── llama-2-7b-chat.Q4_K_M.gguf

Run the App:

streamlit run app.py
