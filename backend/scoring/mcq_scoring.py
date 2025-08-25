import pandas as pd

class MCQScoring:
    def __init__(self, correct_answer: list, user_answer: list):
        self.__correct_answer = correct_answer
        self.__user_answer = user_answer

    def evaluate_quiz(self) -> int:
        points = 0
        # iterate over the shorter list to avoid index errors
        for index in range(min(len(self.__user_answer), len(self.__correct_answer))):
            if self.__correct_answer[index] == self.__user_answer[index]:
                points += 1
        return points