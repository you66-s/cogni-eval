import joblib
import xgboost as xgb
import numpy as np
import pandas as pd
import nltk
from scipy.sparse import hstack
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
import re
import string

class TextClassifier:
    def __init__(self, vectorizer_path: str, model_path: str):
        try:
            nltk.data.find('tokenizers/punkt')
            nltk.data.find('corpora/stopwords')
        except LookupError:
            print("Downloading required NLTK data...")
            nltk.download('punkt')
            nltk.download('stopwords')
        self.ENGLISH_STOPWORDS = set(stopwords.words('english'))

        self.FEATURE_NAMES = [
            'token_count', 'char_count', 'avg_word_length', 'unique_word_ratio', 'stopword_ratio',
            'punctuation_count', 'comma_count', 'period_count', 'digit_count', 'uppercase_ratio',
            'bullet_point_flag', 'contains_year', 'special_char_count', 'avg_sentence_length',
            'long_word_ratio', 'titlecase_ratio'
        ]
        #vectorizer and model
        print("Loading model and vectorizer...")
        self.vectorizer = joblib.load(vectorizer_path)
        self.model = xgb.XGBClassifier()
        self.model.load_model(model_path)
        self.labels = {
            'Education': 0, 'Experience': 1, 'Objective': 2, 'Personal Info': 3,
            'Qualification & Certification': 4, 'Skills': 5, 'Summary': 6
        }

    def _compute_writing_style_features(self, text: str) -> dict:
        if not text or not isinstance(text, str):
            return {f: 0 for f in self.FEATURE_NAMES}
        
        tokens = [t for t in word_tokenize(text.lower()) if any(c.isalnum() for c in t)]
        clean = [re.sub(r'[^\w]', '', t) for t in tokens if re.sub(r'[^\w]', '', t)]
        token_count = len(tokens)
        char_count = len(text)
        avg_word_length = np.mean([len(t) for t in clean]) if clean else 0
        unique_word_ratio = len(set(tokens)) / token_count if token_count else 0
        stopword_ratio = sum(1 for t in tokens if t in self.ENGLISH_STOPWORDS) / token_count if token_count else 0
        punctuation_count = sum(1 for c in text if c in string.punctuation)
        comma_count, period_count = text.count(','), text.count('.')
        digit_count = sum(1 for c in text if c.isdigit())
        alpha_chars = [c for c in text if c.isalpha()]
        uppercase_ratio = sum(1 for c in alpha_chars if c.isupper()) / len(alpha_chars) if alpha_chars else 0
        bullet_point_flag = int(any(re.match(p, text) for p in [r'^\s*[-•*]', r'^\s*\d+[\.\)]', r'^\s*[a-zA-Z][\.\)]']))
        contains_year = int(bool(re.search(r'\b(19|20)\d{2}\b', text)))
        special_char_count = sum(1 for c in text if c in set('@/-'))
        
        try:
            sentences = [s for s in sent_tokenize(text) if s.strip()]
            avg_sentence_length = np.mean([len([t for t in word_tokenize(s.lower()) if any(c.isalnum() for c in t)]) for s in sentences]) if sentences else 0
        except:
            parts = [s for s in re.split(r'[.!?]+', text) if s.strip()]
            avg_sentence_length = np.mean([len(s.split()) for s in parts]) if parts else 0
        
        long_word_ratio = len([t for t in clean if len(t) > 6]) / len(clean) if clean else 0
        original_tokens = [t for t in word_tokenize(text) if any(c.isalpha() for c in t)]
        titlecase_ratio = len([t for t in original_tokens if t.istitle()]) / len(original_tokens) if original_tokens else 0
        
        return {
            'token_count': token_count,
            'char_count': char_count,
            'avg_word_length': round(avg_word_length, 2),
            'unique_word_ratio': round(unique_word_ratio, 4),
            'stopword_ratio': round(stopword_ratio, 4),
            'punctuation_count': punctuation_count,
            'comma_count': comma_count,
            'period_count': period_count,
            'digit_count': digit_count,
            'uppercase_ratio': round(uppercase_ratio, 4),
            'bullet_point_flag': bullet_point_flag,
            'contains_year': contains_year,
            'special_char_count': special_char_count,
            'avg_sentence_length': round(avg_sentence_length, 2),
            'long_word_ratio': round(long_word_ratio, 4),
            'titlecase_ratio': round(titlecase_ratio, 4)
        }

    def predict_texts(self, texts: list) -> tuple:
        X_text = self.vectorizer.transform(texts).toarray()
        style_features = pd.DataFrame([self._compute_writing_style_features(t) for t in texts])[self.FEATURE_NAMES].values
        X_full = np.hstack([X_text, style_features])
        
        # Predict
        y_pred = self.model.predict(X_full)
        y_prob = self.model.predict_proba(X_full)
        return y_pred, y_prob

    def get_label_name(self, pred: int) -> str:
        return next((name for name, idx in self.labels.items() if idx == pred), "Unknown")