import streamlit as st
import pandas as pd
import random

from backend.utils.functions import quiz_generation_and_scoring

# Dataset import
dataset = pd.read_csv('../Data/final_dataset/final_dataset.csv')
creativity_dim = dataset[dataset['dimension'] == "Creativity"]

st.write("<h1 style='text-align: center;'>Creativity Section</h1>", unsafe_allow_html=True)
# Initialize quiz only once
if "creativity_quiz" not in st.session_state:
    questions_index = random.sample(range(len(creativity_dim)), 5)
    st.session_state.creativity_quiz = {
        "questions_index": questions_index,
        "user_answer": [""] * 5,
        "current_q": 0
    }
quiz = st.session_state.creativity_quiz
current = quiz["current_q"]

quiz_generation_and_scoring(current, quiz, creativity_dim, "open-ended", "pages/culture_quiz_page.py", "Creativity")