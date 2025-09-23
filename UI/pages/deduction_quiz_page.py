import streamlit as st

from backend.utils.functions import new_questions_generator, new_quiz_generator
# Dataset import

st.write("<h1 style='text-align: center;'>Mathematical Reasoning Section</h1>", unsafe_allow_html=True)
cv=st.session_state['cv_candidate']
quiz = new_questions_generator("Mathematical Reasoning", cv)
current = quiz["current_q"]

new_quiz_generator(current, quiz, "pages/logic_quiz_page.py", "Mathematical Reasoning")