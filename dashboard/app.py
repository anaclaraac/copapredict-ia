import streamlit as st
import requests

st.set_page_config(
    page_title="CopaPredict IA",
    page_icon="⚽",
    layout="wide"
)

st.title(
    "⚽ CopaPredict IA"
)

st.write(
    "Sistema de previsão de partidas usando Machine Learnig"
)

col1, col2 = st.columns(2)

with col1:

    home_attack_avg = st.number_input(
        "Ataque Mandante",
        value=2.0
    )

    home_defense_avg = st.number_input(
        "Defesa Mandante",
        value=1.0
    )

    home_form = st.number_input(
        "Forma Mandante",
        value=0.8
    )

    win_streak = st.number_input(
        "Sequência de Vitórias",
        value=3
    )


with col2:

    away_attack_avg = st.number_input(
        "Ataque Visitante",
        value=1.5
    )

    away_defense_avg = st.number_input(
        "Defesa Visitante",
        value=1.2
    )

    away_form = st.number_input(
        "Forma Visitante",
        value=0.5
    )

    loss_streak = st.number_input(
        "Sequência de Derrotas",
        value=1
    )


if st.button(
    "🔮 Fazer previsão"
):
    dados = {

        "home_attack_avg": home_attack_avg,
        "away_attack_avg": away_attack_avg,

        "home_defense_avg": home_defense_avg,
        "away_defense_avg": away_defense_avg,

        "home_form": home_form,
        "away_form": away_form,

        "win_streak": win_streak,
        "loss_streak": loss_streak,

        "home_advantage": 1,

        "tournament_weight": 5,

        "home_continent_code": 1,
        "away_continent_code": 1,

        "same_continent": 0,

        "attack_strength": 1.5,

        "avg_goals": 2.4

    }   

    resposta = requests.post(
        "http://127.0.0.1:8000/predict",
        json=dados
    )


    if resposta.status_code == 200:

        resultado = resposta.json()
        probs = resultado["probabilities"]

        if "prediction" in resultado:

            mapa = {

                0: "Derrota",
                1: "Empate",
                2: "Vitória"

            }

            classe = resultado["prediction"]

            st.success(
                f"Resultado previsto: {mapa[classe]}"
            )

        else:

            st.error(
                resultado
            )
        st.markdown("## 📊 Probabilidades")

        col_prob1, col_prob2, col_prob3 = st.columns(3)

        with col_prob1:

            st.metric(
                "Vitória",
                f"{probs['vitoria'] * 100:.1f}%"
            )

        with col_prob2:

            st.metric(
                "Empate",
                f"{probs['empate'] * 100:.1f}%"
            )

        with col_prob3:

            st.metric(
                "Derrota",
                f"{probs['derrota'] * 100:.1f}%"
            )