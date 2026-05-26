import streamlit as st


st.title(
"CopaPredict AI"
)


home_attack = st.number_input(
"Média ofensiva mandante",
value=2.0
)


away_attack = st.number_input(
"Média ofensiva visitante",
value=1.5
)


home_form = st.number_input(
"Forma recente",
value=0.7
)


st.button(
"Prever"
)