import streamlit as st
import pandas as pd
import random
from backend.utils.functions import new_questions_generator, new_quiz_generator

st.write("<h1 style='text-align: center;'>Algorithmic and Data Structure Section</h1>", unsafe_allow_html=True)
cv=st.session_state['cv_candidate']

quiz = new_questions_generator("Algorithmic and Data Structure", cv)
current = quiz["current_q"]

new_quiz_generator(current, quiz, "pages/deduction_quiz_page.py", "Algorithmic and Data Structure")