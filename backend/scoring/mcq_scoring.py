import pandas as pd

class MCQScoring:
    def __init__(self, correct_answer, user_answer):
        self.__correct_answer = correct_answer
        self.__user_answer = user_answer

    def evaluate_quiz(self) -> int:
        if self.__correct_answer == self.__user_answer:
            return 1
        return 0