import streamlit as st
import pandas as pd
import random
import numpy as np
from backend.utils.functions import questions_generator, quiz_generator


st.write("<h1 style='text-align: center;'>Code Comprehension and Debugging Section</h1>", unsafe_allow_html=True)

quiz = questions_generator("Code Comprehension and Debugging")
current = quiz["current_q"]

quiz_generator(current, quiz, "pages/technical_quiz_page.py", "Code Comprehension and Debugging")