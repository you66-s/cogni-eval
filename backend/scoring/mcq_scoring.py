import pandas as pd

class MCQScoring:
    def __init__(self, dataset: pd.DataFrame, question_index: list, user_answers: list, dimension: str):
        self.__dataset = dataset
        self.__questions_index = question_index
        self.__user_answers = user_answers
    
    def get_correct_answers(self) -> list:
        self.__answers = [] * len(self.__questions_index)
        for i in self.__questions_index:
            self.__answers.append(self.__dataset['answer_index'].iloc[i])
        return self.__answers

    def evaluate_quiz(self) -> int:
        points = 0
        for index in range(len(self.__user_answers)):
            if self.__user_answers[index] == self.__answers[index]:
                points += 1
        return points