import sys
from llama_cpp import Llama

techs = sys.argv[1]
prompt = f"""
You are a technical interviewer. For each of the following technologies, generate 3 concise and relevant technical interview questions to test proficiency.

Technologies: {techs}

Format:
[Technology]
1. Question
2. Question
3. Question
"""


llm = Llama(model_path="./models/llama-2-7b-chat.Q4_K_M.gguf", n_ctx=2048, n_threads=8)
response = llm(prompt, max_tokens=256, echo=False)
print(response["choices"][0]["text"].strip())
