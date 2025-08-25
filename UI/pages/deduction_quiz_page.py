import streamlit as st
import pandas as pd
import random
from backend.utils.functions import quiz_generation_and_scoring
# Dataset import
dataset = pd.read_csv('../Data/final_dataset/final_dataset.csv')
deduction_dim = dataset[dataset['dimension'] == "Deduction & Induction"]
dataset_length = len(deduction_dim)
st.write("<h1 style='text-align: center;'>Deduction & Induction Section</h1>", unsafe_allow_html=True)
# Initialize quiz only once
if "deduction_quiz" not in st.session_state:
    questions_index = random.sample(range(dataset_length), 5)
    st.session_state.deduction_quiz = {
        "questions_index": questions_index,
        "user_answer": [""] * 5,
        "current_q": 0  # step tracker
    }

quiz = st.session_state.deduction_quiz
current = quiz["current_q"]

quiz_generation_and_scoring(current, quiz, deduction_dim, deduction_dim["question_type"].unique()[0], "pages/logic_quiz_page.py", deduction_dim["dimension"].unique()[0])