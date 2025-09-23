import json
from backend.Resume_Parser.TextClassifier import TextClassifier
from pypdf import PdfReader
from collections import defaultdict
from dotenv import load_dotenv
import os
import re
from google import genai
from google.genai import types
load_dotenv()

class ResumeParser:
    def __init__(self, vectorizer_path, model_path):
        print("Parser Initialisation....")
        self.classifier = TextClassifier(vectorizer_path=vectorizer_path, model_path=model_path)
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.categories = [
            "Personal Info",
            "Objective",
            "Summary",
            "Education",
            "Experience",
            "Skills",
            "Qualification & Certification"
        ]

    def split_resume_into_sentences(self, text):
        print("starting splitting text....")
        text = text.replace("\n", ". ")
        parts = re.split(r'\.\s*', text)
        return [p.strip() for p in parts if p.strip()]

    def extract_text_from_pdf(self, pdf_path):
        print("Extarcting text Starts....")
        reader = PdfReader(pdf_path)
        sentences = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                sentences.extend(self.split_resume_into_sentences(text))
        return sentences

    def classify_sentences(self, sentences):
        print("starting Classifiying text....")
        cv_data = []
        for sentence in sentences:
            y_pred, y_prob = self.classifier.predict_texts([sentence])
            label = self.classifier.get_label_name(y_pred)
            prob = round(max(y_prob[0]), 2)
            cv_data.append((sentence, label, prob))
        return cv_data

    def build_resume_prompt(self, predictions):
        print("starting building prompt....")
        grouped = defaultdict(list)
        for sentence, label, prob in predictions:
            if sentence and sentence.strip():
                grouped[label.strip()].append(sentence.strip())

        grouped_full = {cat: grouped.get(cat, []) for cat in self.categories}
        prompt = (
            "You are an expert resume parser. Your task is to process grouped lists of raw sentences "
            "from a resume, classified by a model (~80% accuracy) into categories: "
            "Education, Experience, Objective, Personal Info, Qualification & Certification, Skills, Summary. "
            "The model may misclassify sentences, so use reasoning to correct errors.\n\n"
            "Input:\n"
        )

        for cat in self.categories:
            sentences = grouped_full[cat]
            text = "\n".join(f"- {s}" for s in sentences) if sentences else ""
            prompt += f"- {cat}: {text}\n"

        prompt += """
Steps:
1. Clean: Remove duplicates, fix typos (e.g., ‘Universty’ to ‘University’), and combine fragmented sentences.
2. Reclassify: Move sentences to the correct category if misclassified (e.g., a degree in Experience belongs to Education).
3. Parse: Extract fields (e.g., dates, job titles) and organize into the JSON schema. Infer dates (e.g., ‘Graduated 2019’ → end_date: ‘2019’) and use reverse chronological order for arrays.
4. Handle missing data: Use null for missing fields (e.g., no date → null). Ignore irrelevant text (e.g., page numbers).
5. Output only valid JSON matching this schema:

{
  "personal_info": {
    "name": "string",
    "email": "string",
    "phone": "string",
    "location": "string",
    "linkedin": "string or null",
    "other_links": ["string"]
  },
  "objective": "string",
  "summary": "string",
  "education": [{"degree": "string", "institution": "string", "location": "string or null", "start_date": "string or null", "end_date": "string or null", "gpa": "string or null", "achievements": ["string"]}],
  "experience": [{"job_title": "string", "company": "string", "location": "string or null", "start_date": "string or null", "end_date": "string or null", "responsibilities": ["string"]}],
  "skills": ["string"],
  "qualifications_and_certifications": [{"title": "string", "issuer": "string or null", "date_issued": "string or null", "expiration_date": "string or null", "description": "string or null"}]
}
    4. do not add comments or explanations in the output
    5. Return only valid JSON. 
    6. Do not include ```json, ``` or any other text outside the JSON object.
Output the JSON now.
"""
        return prompt

    def parse_resume(self, pdf_path):
        print("starting parsing resume....")
        sentences = self.extract_text_from_pdf(pdf_path)
        cv_data = self.classify_sentences(sentences)
        prompt = self.build_resume_prompt(cv_data)
        print("starting processing of gemini llm....")
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
                system_instruction=(
                    "You are an expert resume parser. Your task is to process grouped lists of raw sentences "
                    "from a resume, classified by a model (~80% accuracy) into categories: "
                    "Education, Experience, Objective, Personal Info, Qualification & Certification, Skills, Summary. "
                    "The model may misclassify sentences, so use reasoning to correct errors.\n\n"
                ),
            ),
            contents=prompt
        )
        print("starting treatement of reponse....")
        response_json = response.model_dump_json()
        response_data = json.loads(response_json)
        print("Thanks for your waiting.")
        return response_data["candidates"][0]["content"]["parts"][0]["text"]