from google import genai
from google.genai import types
from dotenv import load_dotenv
import json
import os
load_dotenv()

def llms_question_generation(dimension):
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    prompt = f"""
    You are an assistant for generating questions in a cognitive adaptive testing system.

    Task:
    - Generate 1 question that assesses the dimension: "{dimension}".
    - The questions types are open-ended or MCQ.
    - The difficulty level is variable between:
        - easy: simple recall or straightforward reasoning.
        - medium: requires multi-step reasoning or moderate creativity.
        - hard: abstract reasoning, multiple constraints, or advanced domain knowledge.
    Example 1 (Open-ended):
    {{
    "question": "You spilled red wine on the hotel carpet and want to clean it up before the housekeeping staff reports this. Tools available: a bottle opener, a plastic cup, a toothbrush, a bottle of mineral water that is sealed shut, a pack of sugar, a white bath towel, a bar of soap, a hair dryer. How do you clean up the wine stain using only these items?",
    "ref_answer": "Step1: Open the bottle of mineral water with the bottle opener. Step2: Wet the white bath towel with your mineral water. Step3: Dab, don't rub, the wine stain with your wet towel. Step4: Use soap and a bit of water to form soap suds and apply to the stain.Step5: Scrub gently with the toothbrush.Step6: Rinse with more mineral water.Step7: Dry using the hairdryer."
    }}
    Example 2 (Open-ended):
    {{
    "question": "Explain data abstraction.",
    "ref_answer": "Data abstraction is a technique used in computer programming to separate the implementation details of a data type from its interface, allowing the implementation to be changed without affecting the code that uses it. This is often achieved through the use of abstract data types (ADTs), which are defined by the operations they support rather than their specific implementation, or through the use of interfaces and classes in object-oriented programming languages. Data abstraction helps to reduce the complexity of software systems by allowing code to be written in a modular and flexible way and by hiding the underlying details of data types from the user."
    }}
    Example 3 (MCQ):
    {{
    "question": "A new commercial radio station in Greenfield plans to play songs that were popular hits fifteen to twenty-five years ago. It hopes in this way to attract an audience made up mainly of people between thirty-five and forty-five years old and thereby to have a strong market appeal to advertisers. Each of the following, if true, strengthens the prospects that the radio station's plan will succeed EXCEPT:",
    "choices": ['The thirty-five- to forty-five-year-old age group is one in which people tend to have comparatively high levels of income and are involved in making household purchases.', 'People in the thirty-five- to forty-five-year-old age group are more likely to listen to the radio for news than for music.', 'In a number of cities demographically similar to Greenfield, radio stations that play recordings of popular music from fifteen to twenty-five years ago have succeeded commercially.', 'Among the few radio stations in the Greenfield area, there is none that plays music from this particular period for more than a few hours per week.'],
    "correcte answer index": 1
    }}
    Example 4 (MCQ):
    {{
    "question": "Clearly, fitness consultants who smoke cigarettes cannot help their clients become healthier. If they do not care about their own health, they cannot really care for their clients' health, and if they do not care for their clients' health, they cannot help them to become healthier. The conclusion follows logically if which one of the following is assumed?",
    "choices": ['Anyone who does not care for his or her own health cannot help others become healthier.', 'Anyone who cares about his or her own health does not smoke.', 'Anyone who cares about the health of others can help others become healthier.', 'Anyone who does not care for the health of others cannot help them become healthier.'],
    "correcte answer index": 1
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
    question_type = parsed_question["question_type"]
    question = parsed_question["question"]

    if parsed_question["question_type"] == "open-ended":
        reference_answer = parsed_question["ref_answer"]
    elif parsed_question["question_type"] == "MCQ":
        choices = parsed_question["choices"]
        correct_answer_index = parsed_question["correct_answer_index"]
    return {"question_type": question_type, "question": question, "ref_answer": reference_answer} if question_type == "open-ended" else {"question_type": question_type, "question": question, "choices": choices, "correct_answer_index": correct_answer_index}
#-------------------------Testing the function-------------------------
questions = llms_question_generation("computer science")
generated_json = json.loads(questions)
generated_question = generated_json["candidates"][0]["content"]["parts"][0]["text"]


print("-------------------Parsed Generated Questions------------------")
print(question_generated_parser(generated_question))