import streamlit as st
from backend.utils.functions import new_quiz_generator, new_questions_generator


st.write("<h1 style='text-align: center;'>Memory and Attention Section</h1>", unsafe_allow_html=True)
print("Starting question generation...")
cv = st.session_state['cv_candidate']
quiz = new_questions_generator("Memory and Attention", cv=cv)
current = quiz["current_q"]
print("Starting quiz generation...")
new_quiz_generator(current, quiz, "pages/Reasoning_quiz_page.py", "Memory and Attention")