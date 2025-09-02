from google import genai
from google.genai import types
from dotenv import load_dotenv
import json
import os
load_dotenv()

def llms_question_generation(dimension):
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    prompt = f"""
    You are an assistant for generating questions in a cognitive adaptive testing system for the computer sciences field.

    Task:
    - Generate 1 question that assesses the dimension: "{dimension}".
    - The questions types are open-ended or MCQ.
    - The difficulty level is variable between:
        - easy: simple recall or straightforward reasoning.
        - medium: requires multi-step reasoning or moderate creativity.
        - hard: abstract reasoning, multiple constraints, or advanced domain knowledge.
    Open-ended Example:
    {{
    "question": "Explain data abstraction in programming.",
    "ref_answer": "Data abstraction is a technique used in programming to separate implementation details of a data type from its interface, allowing changes in implementation without affecting code that uses it. It is achieved through abstract data types, classes, or interfaces and helps reduce software complexity by promoting modularity and flexibility."
    }}

    MCQ Example:
    {{
    "question": "Which of the following sorting algorithms has the best average-case time complexity?",
    "choices": ["Bubble Sort", "Insertion Sort", "Merge Sort", "Selection Sort"],
    "correct_answer_index": 2
    }}  
    Requirements:
    1. If the type is "open-ended", create a question that encourages detailed {dimension}.    
    2. If the type is "MCQ", generate 1 question with 4 answer choices (labeled A–D). Only one must be correct.  
    3. Provide a reference answer that matches the correct/expected response.
    4. do not add comments or explanations in the output
    5. Return only valid JSON. 
    6. Do not include ```json, ``` or any other text outside the JSON object.  

    Output structure:

    if (Open-ended):
    {{
    "question_type": "open-ended",
    "question": "string",
    "ref_answer": "string", # the reference answer must be clean and no strucutural markers (like Step1, Step2, etc) or bullet points
    }}
    else (MCQ):
    {{
    "question_type": "MCQ",
    "question": "string",
    "choices": ["...", "...", "...", "..."],
    "correct_answer_index": integer
    }} 
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction=(
                "You are an assistant for generating questions in a cognitive adaptive testing system."
            ),
        ),
        contents=f"{prompt}") 
    return response.model_dump_json()


def question_generated_parser(generated_question):
    parsed_question = json.loads(generated_question)
    raw_text = parsed_question["candidates"][0]["content"]["parts"][0]["text"]
    parsed_question = json.loads(raw_text)
    question_type = parsed_question["question_type"]
    question = parsed_question["question"]

    if parsed_question["question_type"] == "open-ended":
        reference_answer = parsed_question["ref_answer"]
    elif parsed_question["question_type"] == "MCQ":
        choices = parsed_question["choices"]
        correct_answer_index = parsed_question["correct_answer_index"]
    return {"question_type": question_type, "question": question, "ref_answer": reference_answer} if question_type == "open-ended" else {"question_type": question_type, "question": question, "choices": choices, "correct_answer_index": correct_answer_index}
