import streamlit as st
import pandas as pd
import altair as alt
import plotly.graph_objects as go

st.write("<h1 style='text-align: center;'>Your Cognitive Test Results</h1>", unsafe_allow_html=True)

# Example: replace this with st.session_state['score'] in production
# st.session_state['score'] = [
#     {"Creativity": 80},
#     {"General Culture": 65},
#     {"Deduction & Induction": 50},
#     {"Logical Thinking": 70},
#     {"Reasoning": 55},
#     {"Technical Thinking": 90}
# ]

scores = st.session_state.score

if not scores:
    st.warning("No scores found. Please complete the test first.")
else:
    # Flatten the list of dicts into DataFrame
    df = pd.DataFrame([{"Dimension": k, "Score": v*20} for d in scores for k, v in d.items()])

    st.subheader("Bar Chart")
    bar_chart = alt.Chart(df).mark_bar(color="#4CAF50").encode(
        x=alt.X('Dimension', sort=None),
        y='Score',
        tooltip=['Dimension', 'Score']
    )
    st.altair_chart(bar_chart, use_container_width=True)

    st.subheader("Radar Chart")
    labels = df['Dimension'].tolist()
    values = df['Score'].tolist()

    radar_fig = go.Figure(data=go.Scatterpolar(
        r=values,
        theta=labels,
        fill='toself',
        name='Cognitive Profile'
    ))
    radar_fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0,100])
        ),
        showlegend=False
    )
    st.plotly_chart(radar_fig, use_container_width=True)

    st.subheader("Progress Bars")
    for _, row in df.iterrows():
        st.write(f"**{row['Dimension']}**: {row['Score']}%")
        st.progress(int(row['Score']))
