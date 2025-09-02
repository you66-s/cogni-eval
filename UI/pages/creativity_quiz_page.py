import streamlit as st
import pandas as pd
import random

from backend.utils.functions import quiz_generator, questions_generator


st.write("<h1 style='text-align: center;'>Logical and Analytical Reasoning Section</h1>", unsafe_allow_html=True)
#questions generations
quiz = questions_generator("Logical and Analytical Reasoning")
current = quiz["current_q"]

quiz_generator(current, quiz, "pages/culture_quiz_page.py", "Logical and Analytical Reasoning")