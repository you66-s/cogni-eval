import streamlit as st

from backend.utils.functions import quiz_generator, questions_generator
# Dataset import

st.write("<h1 style='text-align: center;'>Mathematical Reasoning Section</h1>", unsafe_allow_html=True)

quiz = questions_generator("Mathematical Reasoning")
current = quiz["current_q"]

quiz_generator(current, quiz, "pages/logic_quiz_page.py", "Mathematical Reasoning")