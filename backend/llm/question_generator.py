from google import genai
from google.genai import types
from dotenv import load_dotenv
import os, re, json
load_dotenv()

def llms_question_generation(dimension, cv):
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    prompt = f"""
    You are an assistant for generating questions in a cognitive adaptive testing system for the computer sciences field.

    Task:
    - Generate 5 question that assesses the dimension: "{dimension}".
    - Candidate CV information (JSON): {cv}
    - Questions should be adapted to the candidate’s CV information when possible:
        * Use the candidate’s skills, education, or experiences to create personalized questions.
        * If a skill/experience is missing but relevant to the dimension, generate a question that tests this gap.
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
    try:        
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
                system_instruction=(
                    "You are an assistant for generating questions in a cognitive adaptive testing system."
                ),
            ),
            contents=f"{prompt}") 
        return response.model_dump_json()
    except Exception as e:
        return e
    

# new question generation function
def questions_generated_parser(generated_questions):
    parsed_response = json.loads(generated_questions)
    raw_text = parsed_response["candidates"][0]["content"]["parts"][0]["text"]
    raw_text = re.sub(r'^```json\n|```$', '', raw_text, flags=re.MULTILINE).strip()
    try:
        questions_list = json.loads(raw_text)  
        parsed_questions = []
        for q in questions_list:
            question_type = q["question_type"]
            question = q["question"]
            if question_type == "open-ended":
                parsed_questions.append({
                    "question_type": question_type,
                    "question": question,
                    "ref_answer": q["ref_answer"]
                })
            elif question_type == "MCQ":
                parsed_questions.append({
                    "question_type": question_type,
                    "question": question,
                    "choices": q["choices"],
                    "correct_answer_index": q["correct_answer_index"]
                })
        return parsed_questions
    except json.decoder.JSONDecodeError as e:
        print("error while parsing questions")
        return e