import streamlit as st
import pandas as pd
import random
import time

# Dataset import
dataset = pd.read_csv('Data/final_dataset/final_dataset.csv')
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
if current >= len(quiz["questions_index"]):
    st.success("Quiz finished 🎉")
    time.sleep(5)
    st.switch_page("pages/quiz_results.py")
else:
    # Get current question
    question_index = quiz["questions_index"][current]

    st.write(f"<h3>Question {current + 1}</h3>", unsafe_allow_html=True)
    st.write(technical_quiz['question'].iloc[question_index])

    user_answer = st.text_area(
        "Write your answer here:",
        key=f"t_q{current}",
        value=quiz["user_answer"][current]
    )

    if st.button("Next"):
        # Save answer
        quiz["user_answer"][current] = user_answer
        quiz["current_q"] += 1
        st.rerun()
