from google import genai
from google.genai import types
import json
from dotenv import load_dotenv
import os
load_dotenv()
#load once

#class definition
class OpenEndedScoring:
    def __init__(self,question, user_answers, ref_answers):
        self.__user_answers = user_answers
        self.__ref_answers = ref_answers
        self.__question = question
        self.__model = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    def calculate_score(self) -> int:
        prompt = f"""
            Question: {self.__question}
            User's Answer: {self.__user_answers}
            Reference Answer: {self.__ref_answers}

            Evaluate the user's answer against the reference answer and provide ONLY a JSON object with this exact structure:
            {{"score": <number>}}
            Where <number> is a decimal value between 0 and 1 representing overall accuracy.

            First, analyze the user's answer step by step:
            1. Compare the user's answer to the reference answer for factual accuracy
            2. Identify what key points from the reference answer are present or missing
            3. Evaluate the clarity and organization of the response
            4. Assess whether the reasoning process is sound (if applicable)
            5. Check for any irrelevant or incorrect information

            Examples:
            Question: "Explain stack vs queue"
            Reference Answer: "Stack is LIFO, Queue is FIFO with usage examples"
            User Answer: "Stack is LIFO, queue is FIFO"
            Output: {{"score": 0.7}}

            Question: "What is this code's output?"
            Reference Answer: "Output is 6 because loop runs three times"
            User Answer: "It prints 6"
            Output: {{"score": 0.6}}

            Question: "Linked list vs array"
            Reference Answer: "Linked list has nodes with pointers, array has contiguous memory"
            User Answer: ""
            Output: {{"score": 0.0}}

            IMPORTANT:
            - Think through your evaluation carefully before providing the score
            - Return ONLY valid JSON
            - No additional text/explanations
            - No markdown formatting
            - Score must be decimal between 0-1
            """ 
        self.__response = self.__model.models.generate_content(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
                system_instruction=(
                    "You are an evaluator of open-ended questions responses in a cognitive adaptive testing system for the computer sciences skills"
                    "Your task is to evaluate the quality of a user's response to a given question."
                 ),
            ),
            contents=f"{prompt}")
        generated_text = json.loads(self.__response.model_dump_json())
        generated_score = generated_text["candidates"][0]["content"]["parts"][0]["text"]
        return generated_score

    def final_point_calculator(self, threshold=0.7):
        score = json.loads(self.calculate_score())
        score = score["score"]
        if score >= threshold:
            return 1
        else:
            return 0