import streamlit as st
import pandas as pd
import random
from backend.utils.functions import quiz_generation_and_scoring


# Dataset
dataset = pd.read_csv('../Data/final_dataset/final_dataset.csv')
culture_dim = dataset[dataset['dimension'] == "General Culture"]
dataset_length = len(culture_dim)

st.write("<h1 style='text-align: center;'>General Culture Section</h1>", unsafe_allow_html=True)

# Initialize quiz once
if "culture_quiz" not in st.session_state:
    questions_index = random.sample(range(dataset_length), 5)
    st.session_state.culture_quiz = {
        "questions_index": questions_index,
        "user_answer": [None] * 5,
        "current_q": 0  # tracks which question we are on
    }

quiz = st.session_state.culture_quiz
current = quiz["current_q"]

quiz_generation_and_scoring(current, quiz, culture_dim, culture_dim["question_type"].unique()[0], "pages/deduction_quiz_page.py", culture_dim["dimension"].unique()[0])