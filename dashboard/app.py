import streamlit as st
import requests
import matplotlib.pyplot as plt
import pandas as pd
from features import (gerar_features, listar_times)

teams = pd.read_csv("data/processed/teams.csv")
lista_times = teams["team"].tolist()

st.set_page_config(
    page_title="CopaPredict IA",
    page_icon="⚽",
    layout="wide"
)

st.title(
    "⚽ CopaPredict IA"
)

times = listar_times()

st.write(
    "Sistema de previsão de partidas usando Machine Learnig"
)

st.markdown(
    "## Seleções"
)

col_time1, col_time2 = st.columns(2)

with col_time1:

    home_team = st.selectbox(
        "Mandante",
        lista_times
    )

with col_time2:

    away_team = st.selectbox(
        "Visitante",
        lista_times,
        index=1
    )

col1, col2 = st.columns(2)

with col1:

    home_team = st.selectbox(
        "Mandante",
        times,
        index=times.index("Brazil")
    )

with col2:

    away_team = st.selectbox(
        "Visitante",
        times,
        index=times.index("Argentina")
    )


st.info(
    f"{home_team} x {away_team}"
)

if st.button(
    "🔮 Fazer previsão"
):
    dados = gerar_features(home_team, away_team)

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
        fig, ax = plt.subplots(figsize=(3, 2))

        ax.bar(
            ["Vitória", "Empate", "Derrota"],
            [
                probs["vitoria"],
                probs["empate"],
                probs["derrota"]
            ]
        )

        ax.set_title(
            "Probabilidades Previstas"
        )
        
        ax.set_ylim(0,1)

        ax.set_ylabel(
            "Probabilidade"
        )

        st.pyplot(fig,use_container_width=False)