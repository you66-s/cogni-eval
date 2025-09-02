import streamlit as st
import pandas as pd
import random
from backend.utils.functions import quiz_generator, questions_generator

st.write("<h1 style='text-align: center;'>Creativity and Problem-Solving Section</h1>", unsafe_allow_html=True)

quiz = questions_generator("Creativity and Problem-Solving")
current = quiz["current_q"]

# Show current question
quiz_generator(current, quiz, "pages/quiz_results.py", "Creativity and Problem-Solving")