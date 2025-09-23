import streamlit as st
from io import BytesIO
from backend.Resume_Parser.resume_information_extraction import ResumeParser
import os, json
from dotenv import load_dotenv

st.write("<h1 style='text-align: center;'>Cognitive Adaptive Test</h1>", unsafe_allow_html=True)
st.write("This comprehensive test is designed to evaluate key aspects of your CV. You will complete six distinct sections:")
st.write("Each section contains 5 questions. Upon completion, you will receive a detailed results breakdown highlighting your cognitive strengths and areas for potential improvement.")
st.write("This test will assess your cognitive abilities and adapt to your performance. Please ensure you are in a quiet environment and have ample time to complete the test.")
st.write("Please Upload your resume first")

cv_file_uploader = st.file_uploader(label="Choose a file", type=['pdf', 'docx'])

if cv_file_uploader is not None:
    file_bytes = cv_file_uploader.getvalue()
    try:   
        parser = ResumeParser(vectorizer_path=r"..\saved_models\tfidf_vectorizer.pkl", model_path=r"..\saved_models\xgb_model.json")
        st.write("resume parsing start....")
        parsed_txt = parser.parse_resume(BytesIO(file_bytes))
        st.session_state['cv_candidate'] = parsed_txt
        st.write(f"Resume Parsed Successfly, you can start the test now.")
        start_test_btn = st.button("Start the test")
        if start_test_btn:
            if "starting_test" not in st.session_state:
                st.session_state["starting_test"] = True
        if 'score' not in st.session_state:
            st.session_state['score'] = []
        if start_test_btn:
            st.switch_page("pages/creativity_quiz_page.py")
    except Exception as e:
        st.write(f"Error wwhile parsing Resume")
        st.write(e)




