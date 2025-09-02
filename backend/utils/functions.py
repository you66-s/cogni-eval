import streamlit as st
import pandas as pd
import numpy as np
from backend.scoring.scoring_engine import ScoringEngine
from backend.database.supabase import SupabaseDB
from backend.llm.question_generator import question_generated_parser, llms_question_generation

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
        if qst_type == "open-ended":
            scoring = ScoringEngine("open-ended", quiz["score_user_answer"], quiz["score_crr_answer"])
        elif qst_type == "MCQ":
            scoring = ScoringEngine("MCQ", quiz["score_user_answer"], quiz["score_crr_answer"])
        st.session_state['score'].append({dimension: scoring.evaluate_quiz()})

        # Clearing the scoring arrays for the next quiz
        quiz["score_user_answer"] = []
        quiz["score_crr_answer"] = []
        st.switch_page(switch_page)
    else:
        # Get current question
        question_index = quiz["questions_index"][current]
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
                quiz["score_user_answer"].append(quiz["user_answer"][current])
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
                quiz["score_user_answer"].append(quiz["user_answer"][current])
                quiz["current_q"] += 1
                st.rerun()

def questions_generator(dimension: str):
    session_name = f"{dimension}_quiz"
    if session_name not in st.session_state:
        questions = []
        qst_type = []
        choices = []
        correct_answer_index = []
        ref_answer = []
        for i in range(5):
            model_question = llms_question_generation(dimension)
            parsed_question = question_generated_parser(model_question)
            questions.append(parsed_question["question"])
            qst_type.append(parsed_question["question_type"])
            if parsed_question["question_type"] == "open-ended":
                ref_answer.append(parsed_question["ref_answer"])
                choices.append(None)
                correct_answer_index.append(None)
            elif parsed_question["question_type"] == "MCQ":
                choices.append(parsed_question["choices"])
                correct_answer_index.append(parsed_question["correct_answer_index"])
                ref_answer.append(None) 
        st.session_state[session_name] = {
                    "questions": questions,
                    "question_type": qst_type,
                    "choices": choices,
                    "correct_answer_index": correct_answer_index,
                    "ref_answer": ref_answer,
                    "user_answer": [""] * 5,
                    "current_q": 0
                }
    return st.session_state[session_name]


def quiz_generator(current, quiz, switch_page: str, dimension):
    if "score_crr_answer" not in quiz:
        quiz["score_crr_answer"] = []
        # Build correct answers only once per quiz
        for i in range(len(quiz["questions"])):
            if quiz["question_type"][i] == "open-ended":
                quiz["score_crr_answer"].append(quiz["ref_answer"][i])
            elif quiz["question_type"][i] == "MCQ":
                quiz["score_crr_answer"].append(quiz["correct_answer_index"][i])
    
    if "score_user_answer" not in quiz:
        quiz["score_user_answer"] = []
    
    # Show current question
    if current >= len(quiz["questions"]):
        score = 0
        for i in range(len(quiz["questions"])):
            if quiz["question_type"][i] == "open-ended":
                scoring = ScoringEngine("open-ended", quiz["score_user_answer"][i], quiz["score_crr_answer"][i])
                score += scoring.evaluate_quiz()
            elif quiz["question_type"][i] == "MCQ":
                scoring = ScoringEngine("MCQ", quiz["score_user_answer"][i], quiz["score_crr_answer"][i])
                score += scoring.evaluate_quiz()
        st.session_state['score'].append({dimension: score})

        # Clearing the scoring arrays for the next quiz
        quiz["score_user_answer"] = []
        quiz["score_crr_answer"] = []
        st.switch_page(switch_page)
    else:
        # Get current question
        st.write(f"<h3>Question {current + 1}</h3>", unsafe_allow_html=True)
        st.write(quiz["questions"][current])

        # generation of the answer widget type based on the question type
        if quiz["question_type"][current] == "open-ended":
            user_answer = st.text_area(
                "Write your answer here:",
                key=f"{dimension}_q{current}",
                value=quiz["user_answer"][current]
            )

            if st.button("Next"):
                # Save answer
                quiz["user_answer"][current] = user_answer
                quiz["score_user_answer"].append(quiz["user_answer"][current])
                quiz["current_q"] += 1
                st.rerun()
        elif quiz["question_type"][current] == "MCQ":
            choices = quiz['choices'][current]

            # Use the actual question_index in key 
            selected = st.radio(
                "Select the answer",
                options=choices,
                key=f"qst_{current}"
            )
            if st.button("Next"):
                # Save answer
                quiz["user_answer"][current] = choices.index(selected) if selected else None
                quiz["score_user_answer"].append(quiz["user_answer"][current])
                quiz["current_q"] += 1
                st.rerun()
