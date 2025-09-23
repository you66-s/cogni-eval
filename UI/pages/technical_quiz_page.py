import streamlit as st
import pandas as pd
import random
from backend.utils.functions import new_quiz_generator, new_questions_generator

st.write("<h1 style='text-align: center;'>Creativity and Problem-Solving Section</h1>", unsafe_allow_html=True)
cv=st.session_state['cv_candidate']
quiz = new_questions_generator("Creativity and Problem-Solving", cv)
current = quiz["current_q"]

# Show current question
new_quiz_generator(current, quiz, "pages/quiz_results.py", "Creativity and Problem-Solving")