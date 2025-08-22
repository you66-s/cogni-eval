from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import re
import time
import nltk
from nltk.corpus import stopwords

#load once
nltk.download('stopwords')
STOPWORDS = set(stopwords.words("english"))
model = SentenceTransformer("gtr-t5-base")

#class definition
class OpenEndedScoring:
    def __init__(self, user_answer: str, ref_answer: str):
        self.__user_answer = user_answer
        self.__ref_answer = ref_answer
        self.__similarity = 0

    def text_processing(self, text: str) -> str:
        text = text.lower()
        text = re.sub(r'https?://\S+|www\.\S+', '', text)
        text = re.sub(r'[^a-z\s]', ' ', text)
        words = [w for w in text.split() if w not in STOPWORDS]
        return ' '.join(words)
    
    def calculate_similarity(self) -> float:
        start_time = time.time()
        self.__user_answer = self.text_processing(text=self.__user_answer)
        self.__ref_answer = self.text_processing(text=self.__ref_answer)
        self.__embeddings = model.encode([self.__user_answer, self.__ref_answer])
        self.__similarity = float(cosine_similarity([self.__embeddings[0]], [self.__embeddings[1]]))
        end_time = time.time()
        elapsed = end_time - start_time
        print("time to calculate the similarity: ", round(elapsed, 2))
        return self.__similarity