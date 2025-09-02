import streamlit as st
import pandas as pd
import random
from backend.utils.functions import quiz_generator, questions_generator

st.write("<h1 style='text-align: center;'>Algorithmic and Computational Thinking Section</h1>", unsafe_allow_html=True)

quiz = questions_generator("Algorithmic and Computational Thinking")
current = quiz["current_q"]

quiz_generator(current, quiz, "pages/deduction_quiz_page.py", "Algorithmic and Computational Thinking")