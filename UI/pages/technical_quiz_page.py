import streamlit as st
import pandas as pd
import random
from backend.utils.functions import quiz_generation_and_scoring

# Dataset import
dataset = pd.read_csv('../Data/final_dataset/final_dataset.csv')
technical_quiz = dataset[dataset['dimension'] == "Technical Thinking"]
dataset_length = len(technical_quiz)
st.write("<h1 style='text-align: center;'>Technical Skills Section</h1>", unsafe_allow_html=True)
# Initialize quiz only once
if "techincal_quiz" not in st.session_state:
    questions_index = random.sample(range(dataset_length), 5)
    st.session_state.techincal_quiz = {
        "questions_index": questions_index,
        "user_answer": [""] * 5,
        "current_q": 0  # step tracker
    }

quiz = st.session_state.techincal_quiz
current = quiz["current_q"]

# Show current question
quiz_generation_and_scoring(current, quiz, technical_quiz, technical_quiz["question_type"].unique()[0], "pages/quiz_results.py", technical_quiz["dimension"].unique()[0])