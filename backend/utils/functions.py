import streamlit as st
from backend.scoring.scoring_engine import ScoringEngine
from backend.llm.question_generator import llms_question_generation, questions_generated_parser


def new_questions_generator(dimension: str, cv):
    session_name = f"{dimension}_quiz"
    if session_name not in st.session_state:
        questions = []
        qst_type = []
        choices = []
        correct_answer_index = []
        ref_answer = []

        # Generate questions once (returns a list of 5 questions)
        model_response = llms_question_generation(dimension, cv=cv)
        parsed_questions = questions_generated_parser(model_response)  # returns list of dicts

        for parsed_question in parsed_questions:
            questions.append(parsed_question["question"])
            qst_type.append(parsed_question["question_type"])
            if parsed_question["question_type"] == "open-ended":
                ref_answer.append(parsed_question.get("ref_answer", ""))
                choices.append(None)
                correct_answer_index.append(None)
            elif parsed_question["question_type"] == "MCQ":
                choices.append(parsed_question.get("choices", []))
                correct_answer_index.append(parsed_question.get("correct_answer_index", None))
                ref_answer.append(None)

        st.session_state[session_name] = {
            "questions": questions,
            "question_type": qst_type,
            "choices": choices,
            "correct_answer_index": correct_answer_index,
            "ref_answer": ref_answer,
            "user_answer": [""] * len(parsed_questions),
            "current_q": 0
        }

    return st.session_state[session_name]

# new quiz generation function
def new_quiz_generator(current, quiz, switch_page: str, dimension):
    # Build correct answers only once per quiz
    if "score_crr_answer" not in quiz:
        quiz["score_crr_answer"] = []
        for i in range(len(quiz["questions"])):
            if quiz["question_type"][i] == "open-ended":
                quiz["score_crr_answer"].append(quiz.get("ref_answer", [])[i])
            elif quiz["question_type"][i] == "MCQ":
                quiz["score_crr_answer"].append(quiz.get("correct_answer_index", [])[i])

    if "score_user_answer" not in quiz:
        quiz["score_user_answer"] = []

    # Check if quiz is finished
    if current >= len(quiz["questions"]):
        score = 0
        for i in range(len(quiz["questions"])):
            q_type = quiz["question_type"][i]
            user_ans = quiz["score_user_answer"][i]
            correct_ans = quiz["score_crr_answer"][i]
            scoring = ScoringEngine(q_type, user_ans, correct_ans)
            score += scoring.evaluate_quiz()

        # Save score in session state
        if "score" not in st.session_state:
            st.session_state["score"] = []
        st.session_state["score"].append({dimension: score})

        # Clear answers for next quiz
        quiz["score_user_answer"] = []
        quiz["score_crr_answer"] = []
        st.switch_page(switch_page)

    else:
        # Show current question
        st.write(f"<h3>Question {current + 1}</h3>", unsafe_allow_html=True)
        st.write(quiz["questions"][current])

        # Render answer widget based on question type
        q_type = quiz["question_type"][current]
        if q_type == "open-ended":
            user_answer = st.text_area(
                "Write your answer here:",
                key=f"{dimension}_q{current}",
                value=quiz["user_answer"][current]
            )

            if st.button("Next"):
                quiz["user_answer"][current] = user_answer
                quiz["score_user_answer"].append(user_answer)
                quiz["current_q"] += 1
                st.rerun()

        elif q_type == "MCQ":
            choices = quiz.get("choices", [])[current] or []
            selected = st.radio(
                "Select the answer",
                options=choices,
                key=f"{dimension}_q{current}"
            )

            if st.button("Next"):
                quiz["user_answer"][current] = choices.index(selected) if selected else None
                quiz["score_user_answer"].append(quiz["user_answer"][current])
                quiz["current_q"] += 1
                st.rerun()
