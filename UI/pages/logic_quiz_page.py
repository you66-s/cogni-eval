import streamlit as st
import pandas as pd
import random
import numpy as np
from backend.utils.functions import quiz_generation_and_scoring

def mcq_choices_parser(choices) -> list:
    choices_dict = eval(choices, {"array": np.array})
    choices = list(choices_dict['choices'])
    labels = list(choices_dict['answers'])
    return choices, labels

# Dataset
dataset = pd.read_csv('../Data/final_dataset/final_dataset.csv')
logic_dim = dataset[dataset['dimension'] == "Logical Thinking"]
dataset_length = len(logic_dim)

st.write("<h1 style='text-align: center;'>Logical Thinking Section</h1>", unsafe_allow_html=True)

# Initialize quiz once
if "logic_quiz" not in st.session_state:
    questions_index = random.sample(range(dataset_length), 5)
    st.session_state.logic_quiz = {
        "questions_index": questions_index,
        "user_answer": [None] * 5,
        "current_q": 0
    }

quiz = st.session_state.logic_quiz
current = quiz["current_q"]

quiz_generation_and_scoring(current, quiz, logic_dim, logic_dim["question_type"].unique()[0], "pages/Reasoning_quiz_page.py", logic_dim["dimension"].unique()[0])