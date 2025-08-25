import streamlit as st
import pandas as pd
from backend.scoring.scoring_engine import ScoringEngine
import numpy as np
import time

def mcq_choices_parser(choices) -> list:
    choices_dict = eval(choices, {"array": np.array})
    choices = list(choices_dict['text'])
    labels = list(choices_dict['label'])
    return choices, labels

def quiz_generation_and_scoring(current, quiz, dataset: pd.DataFrame, qst_type: str, switch_page: str, dimension):
    if "score_crr_answer" not in quiz:
        quiz["score_crr_answer"] = []
        # Build correct answers only once per quiz
        for i in range(len(quiz["questions_index"])):
            if qst_type == "open-ended":
                quiz["score_crr_answer"].append(dataset["answer"].iloc[quiz["questions_index"][i]])
            elif qst_type == "MCQ":
                quiz["score_crr_answer"].append(dataset["answer_index"].iloc[quiz["questions_index"][i]])
    
    if "score_user_answer" not in quiz:
        quiz["score_user_answer"] = []
    
    # Show current question
    if current >= len(quiz["questions_index"]):
        print(f"{dimension} section answers")
        print(f"user answers {quiz["score_user_answer"]}")
        print(f"correct answers {quiz["score_crr_answer"]}")
        scoring = ScoringEngine("open-ended", quiz["score_user_answer"], quiz["score_crr_answer"])
        st.session_state['score'].append({dimension: scoring.evaluate_quiz()})

        # Clearing the scoring arrays for the next quiz
        quiz["score_user_answer"] = []
        quiz["score_crr_answer"] = []
        st.switch_page(switch_page)
    else:
        # Get current question
        question_index = quiz["questions_index"][current]
        #DEBUG
        st.write("Correct answer index:", dataset["answer_index"].iloc[question_index])
        st.write("Choices:", dataset["choices"].iloc[question_index])
        #---------------------------END OF DEBUG----------------------------------
        st.write(f"<h3>Question {current + 1}</h3>", unsafe_allow_html=True)
        st.write(dataset['question'].iloc[question_index])

        # generation of the answer widget type based on the question type
        if qst_type == "open-ended":
            user_answer = st.text_area(
                "Write your answer here:",
                key=f"c_q{current}",
                value=quiz["user_answer"][current]
            )

            if st.button("Next"):
                # Save answer
                quiz["user_answer"][current] = user_answer
                quiz["score_user_answer"].append(user_answer)
                quiz["current_q"] += 1
                st.rerun()
        elif qst_type == "MCQ":
            choices = list(eval(dataset['choices'].iloc[question_index]))

            # Use the actual question_index in key 
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