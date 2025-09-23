from backend.scoring.open_answer_scoring import OpenEndedScoring
from backend.scoring.mcq_scoring import MCQScoring

class ScoringEngine:
    def __init__(self, question_type, user_answer, correct_answer, question=None):
        self.__question = question
        self.__question_type = question_type
        self.__user_answer = user_answer
        self.__correct_answer = correct_answer
        self.__open_ended_socre = OpenEndedScoring(self.__question, self.__user_answer, self.__correct_answer)
        self.__mcq_score = MCQScoring(self.__user_answer, self.__correct_answer)

    def evaluate_quiz(self):
        if self.__question_type == "MCQ":
            return self.__mcq_score.evaluate_quiz()
        elif self.__question_type == "open-ended":
            return self.__open_ended_socre.final_point_calculator()