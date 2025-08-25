from backend.scoring.open_answer_scoring import OpenEndedScoring
from backend.scoring.mcq_scoring import MCQScoring
import pandas as pd

class ScoringEngine:
    def __init__(self, question_type, user_answer: list, correct_answer: list):
        self.__question_type = question_type
        self.__user_answer = user_answer
        self.__correct_answer = correct_answer
        self.__open_ended_similarity = OpenEndedScoring(self.__user_answer, self.__correct_answer)
        self.__mcq_score = MCQScoring(self.__user_answer, self.__correct_answer)

    def evaluate_quiz(self):
        if self.__question_type == "MCQ":
            return self.__mcq_score.evaluate_quiz()
        elif self.__question_type == "open-ended":
            similartiy = self.__open_ended_similarity.calculate_similarity()
            print("similarity calculated: ", similartiy)
            return self.__open_ended_similarity.final_point_calculator()