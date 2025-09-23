import streamlit as st
from backend.utils.functions import new_questions_generator, new_quiz_generator


st.write("<h1 style='text-align: center;'>Code Comprehension and Debugging Section</h1>", unsafe_allow_html=True)
cv=st.session_state['cv_candidate']
quiz = new_questions_generator("Code Comprehension and Debugging", cv)
current = quiz["current_q"]

new_quiz_generator(current, quiz, "pages/technical_quiz_page.py", "Code Comprehension and Debugging")