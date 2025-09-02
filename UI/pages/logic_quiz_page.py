import streamlit as st
from backend.utils.functions import quiz_generator, questions_generator


st.write("<h1 style='text-align: center;'>Memory and Attention Section</h1>", unsafe_allow_html=True)

quiz = questions_generator("Memory and Attention")
current = quiz["current_q"]

quiz_generator(current, quiz, "pages/Reasoning_quiz_page.py", "Memory and Attention")