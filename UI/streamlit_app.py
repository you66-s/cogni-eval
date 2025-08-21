import streamlit as st

# pages definition
main_page = st.Page("main_page.py", title="Main Page")
logic_quiz_page = st.Page("pages/logic_quiz_page.py", title="Logic Quiz Page")
deduction_quiz_page = st.Page("pages/deduction_quiz_page.py", title="Deduction & Induction Quiz Page")
culture_quiz_page = st.Page("pages/culture_quiz_page.py", title="General Culture Quiz Page")
creativty_quiz_page = st.Page("pages/creativity_quiz_page.py", title="Culture Quiz Page")
reasoning_quiz_page = st.Page("pages/Reasoning_quiz_page.py", title="Reasoning Quiz Page")
technical_quiz_page = st.Page("pages/technical_quiz_page.py", title="Technical Quiz Page")
quiz_results = st.Page("pages/quiz_results.py", title="Quiz Results")

pages = st.navigation([main_page, logic_quiz_page, deduction_quiz_page, culture_quiz_page, creativty_quiz_page, reasoning_quiz_page, technical_quiz_page, quiz_results], position="hidden")

pages.run()