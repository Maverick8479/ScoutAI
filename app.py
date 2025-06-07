import streamlit as st
from llama_cpp import Llama
import time

from models.llama_model import get_llm


# ===== Function to Generate Tech Questions Using LLaMA =====
from models.llama_model import get_llm

import subprocess
import json

def generate_technical_questions(tech_list):
    try:
        result = subprocess.run(
            ["python", "test.py", ",".join(tech_list)],
            capture_output=True, text=True, timeout=120
        )
        return result.stdout.strip()
    except Exception as e:
        return f"❌ Failed to call LLaMA subprocess: {e}"


# ===== Streamlit UI Configuration =====
st.set_page_config(page_title="ScoutAI", layout="centered")
st.title("🤖 ScoutAI: Your Intelligent Tech Hiring Assistant")

# ===== Chat Workflow Setup =====
questions = [
    ("full_name", "Please enter your full legal name as it appears on official documents."),
    ("email", "Kindly provide a valid email address (e.g., abcd@example.com)."),
    ("phone", "Enter your 10-digit mobile number (numbers only, no spaces or dashes)."),
    ("experience", "Mention your total professional experience in years (e.g., 3.5)"),
    ("position", "Specify the exact job title you're applying for (e.g., Frontend Developer)"),
    ("location", "Enter your current city and country (e.g., Mumbai, India)"),
    ("tech_stack", "List technologies/tools you're proficient in (comma-separated, e.g., Python, React, MySQL)"),
]

# ===== Restart Chat Button =====
if st.button("🔄 Restart Chat"):
    st.session_state.chat_history = [
        ("ScoutAI", "👋 Hi! I'm ScoutAI, your hiring assistant. I’ll guide you through a few questions to help match you with the right tech job. Type `exit` anytime to end."),
        ("ScoutAI", questions[0][1])
    ]
    st.session_state.candidate_info = {}
    st.session_state.question_index = 0
    st.session_state.pending_rerun = False
    st.session_state.temp_input = ""
    st.stop()

# ===== Session State Init =====
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        ("ScoutAI", "👋 Hi! I'm ScoutAI, your hiring assistant. I’ll guide you through a few questions to help match you with the right tech job. Type `exit` anytime to end."),
        ("ScoutAI", questions[0][1])
    ]
if "candidate_info" not in st.session_state:
    st.session_state.candidate_info = {}
if "question_index" not in st.session_state:
    st.session_state.question_index = 0
if "pending_rerun" not in st.session_state:
    st.session_state.pending_rerun = False

if st.session_state.pending_rerun:
    st.session_state["temp_input"] = ""
    st.session_state["pending_rerun"] = False

# ===== Text Input Box =====
user_input = st.text_input("You:", value="", key="temp_input")

# ===== Bot Logic =====
def generate_response(msg):
    if msg.strip().lower() in ["exit", "quit", "bye"]:
        return "Thank you for your time! We’ll be in touch soon. 👋"

    if st.session_state.question_index < len(questions):
        key, _ = questions[st.session_state.question_index]

        # ==== Field Validation ====
        if key == "email":
            if "@" not in msg or "." not in msg or " " in msg:
                return "❌ That doesn’t look like a valid email. Please try again."

        elif key == "phone":
            if not msg.isdigit() or len(msg) != 10:
                return "📱 Please enter a valid 10-digit phone number."

        elif key == "experience":
            try:
                years = float(msg)
                if years < 0:
                    return "📉 Experience can’t be negative. Please enter a valid number."
            except:
                return "🔢 Please enter a number for your experience in years."

        # ==== Store valid answer ====
        st.session_state.candidate_info[key] = msg
        st.session_state.question_index += 1

    # ==== Ask Next Question or Move to GPT ====
    if st.session_state.question_index < len(questions):
        return questions[st.session_state.question_index][1]
    else:
        tech_input = st.session_state.candidate_info.get("tech_stack", "")
        tech_list = [tech.strip() for tech in tech_input.split(",") if tech.strip()]

        if "tech_questions" not in st.session_state:
            try:
                generated_qs = generate_technical_questions(tech_list)
                st.session_state.tech_questions = generated_qs
                return "🧠 Based on your tech stack, here are some questions for you:\n\n" + generated_qs
            except Exception as e:
                return f"❌ Failed to generate questions:\n{e}"

        return "✅ You can review your technical questions below."

# ===== Handle User Input =====
if user_input:
    st.session_state.chat_history.append(("User", user_input))
    bot_reply = generate_response(user_input)
    st.session_state.chat_history.append(("ScoutAI", bot_reply))
    st.session_state.pending_rerun = True
    st.experimental_rerun()

# ===== Display Chat History =====
for role, msg in st.session_state.chat_history:
    st.markdown(f"**{role}:** {msg}")

# ===== Show Summary & Tech Questions =====
if st.session_state.question_index == len(questions):
    st.markdown("---")
    st.subheader("📋 Collected Info")
    for k, v in st.session_state.candidate_info.items():
        st.markdown(f"- **{k.replace('_', ' ').title()}**: {v}")
    if "tech_questions" in st.session_state:
        st.markdown("---")
        st.subheader("🧪 LLaMA-Generated Technical Questions")
        st.markdown(st.session_state.tech_questions)
