import streamlit as st

st.write("<h1 style='text-align: center;'>Cognitive Adaptive Test</h1>", unsafe_allow_html=True)
st.write("This comprehensive test is designed to evaluate key aspects of your mental agility. You will complete six distinct sections:")
st.write("<ul><li>Creativity</li><li>Technical Thinking</li><li>Reasoning</li><li>General Culture</li><li>Logical Thinking</li><li>Deduction & Induction</li></ul>", unsafe_allow_html=True)
st.write("Each section contains 5 questions. Upon completion, you will receive a detailed results breakdown highlighting your cognitive strengths and areas for potential improvement.")
st.write("This test will assess your cognitive abilities and adapt to your performance. Please ensure you are in a quiet environment and have ample time to complete the test.")
start_test_btn = st.button("Start the test")
if start_test_btn:
    if "starting_test" not in st.session_state:
        st.session_state["starting_test"] = True
if 'score' not in st.session_state:
    st.session_state['score'] = []
if start_test_btn:
    st.switch_page("pages/creativity_quiz_page.py")