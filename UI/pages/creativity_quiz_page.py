import streamlit as st
import pandas as pd
import random
from backend.utils.functions import new_quiz_generator, new_questions_generator


st.write("<h1 style='text-align: center;'>Logical and Analytical Reasoning Section</h1>", unsafe_allow_html=True)
cv=st.session_state['cv_candidate']

#questions generations
quiz = new_questions_generator("Logical and Analytical Reasoning", cv=cv)
current = quiz["current_q"]

new_quiz_generator(current, quiz, "pages/culture_quiz_page.py", "Logical and Analytical Reasoning")