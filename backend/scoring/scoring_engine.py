from backend.scoring.open_answer_scoring import OpenEndedScoring
from backend.scoring.mcq_scoring import MCQScoring
import pandas as pd

class ScoringEngine:
    def __init__(self, question_type, user_answer=None, ref_answer=None):
        self.__question_type = question_type
        self.__user_answer = user_answer
        self.__ref_answer = ref_answer
        self.__open_ended_similarity = OpenEndedScoring(user_answers=self.__user_answer, ref_answers=self.__ref_answer)
        self.__mcq_score = MCQScoring(user_answer=self.__user_answer, correct_answer=self.__ref_answer)

    def evaluate_quiz(self):
        if self.__question_type == "MCQ":
            return self.__mcq_score.evaluate_quiz()
        elif self.__question_type == "open-ended":
            self.__open_ended_similarity.calculate_similarity()
            return self.__open_ended_similarity.final_point_calculator()