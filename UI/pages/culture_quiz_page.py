import streamlit as st
import pandas as pd
import random
import numpy as np
import time

def mcq_choices_parser(choices) -> list:
    choices_dict = eval(choices, {"array": np.array})
    choices = list(choices_dict['text'])
    labels = list(choices_dict['label'])
    return choices, labels

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

# Stop if quiz finished
if current >= len(quiz["questions_index"]):
    st.success("Quiz finished 🎉")
    time.sleep(5)
    st.switch_page("pages/deduction_quiz_page.py")
else:
    # Get current question
    question_index = quiz["questions_index"][current]

    st.write(f"<h3>Question {current + 1}</h3>", unsafe_allow_html=True)
    st.write(culture_dim['question'].iloc[question_index])

    choices, labels = mcq_choices_parser(culture_dim['choices'].iloc[question_index])

    # Use the actual question_index in key → unique per question
    selected = st.radio(
        "Select the answer",
        options=choices,
        key=f"qst_{question_index}"
    )

    if st.button("Next"):
        # Save answer
        quiz["user_answer"][current] = choices.index(selected) if selected else None
        quiz["current_q"] += 1
        st.rerun()
