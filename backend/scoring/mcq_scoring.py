import pandas as pd

class MCQScoring:
    def __init__(self, dataset, question_index, user_answers):
        self.__dataset = dataset
        self.__questions = question_index
        self.__answers = user_answers
        self.__correct_answers = None
    
    def get_questions(self):
        