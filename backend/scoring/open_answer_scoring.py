from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import re
import time
import nltk
from nltk.corpus import stopwords
import pandas as pd

#load once
nltk.download('stopwords')
STOPWORDS = set(stopwords.words("english"))
model = SentenceTransformer("gtr-t5-base")

#class definition
class OpenEndedScoring:
    def __init__(self, user_answers: list, ref_answers: list):
        self.__user_answers = user_answers
        self.__ref_answers = ref_answers
        self.__similarity = []
        self.__score = 0

    def text_processing(self, text: str) -> str:
        text = text.lower()
        text = re.sub(r'https?://\S+|www\.\S+', '', text)
        text = re.sub(r'[^a-z\s]', ' ', text)
        words = [w for w in text.split() if w not in STOPWORDS]
        return ' '.join(words)
    
    def calculate_similarity(self) -> list:
        for i in range(len(self.__user_answers)):
            self.__user_answer = self.text_processing(text=self.__user_answers[i])
            self.__ref_answer = self.text_processing(text=self.__ref_answers[i])
            self.__embeddings = model.encode([self.__user_answer, self.__ref_answer], convert_to_tensor=True)
            self.__similarity.append(model.similarity(self.__embeddings[0], self.__embeddings[1]))
        return self.__similarity
    
    def final_point_calculator(self, threshold=0.8):
        points = 0
        for similarity in range(len(self.__similarity)):
            if self.__similarity[similarity][0][0] >= threshold:
                points += 1
        return points