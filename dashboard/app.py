import streamlit as st
import requests
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
from datetime import datetime

from features import (
    gerar_features,
    listar_times,
    calcular_ataque,
    calcular_defesa,
    calcular_forma,
    ultimos_jogos,
    ranking_forca
)

BASE_DIR = Path(__file__).resolve().parent.parent

HISTORY_FILE = (
    BASE_DIR
    / "history"
    / "predictions.csv"
)


def salvar_previsao(
    home_team,
    away_team,
    prediction,
    probs
):
    HISTORY_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    novo = pd.DataFrame([
        {
            "data_hora": datetime.now(),
            "home_team": home_team,
            "away_team": away_team,
            "prediction": prediction,
            "prob_vitoria": probs["vitoria"],
            "prob_empate": probs["empate"],
            "prob_derrota": probs["derrota"]
        }
    ])

    if HISTORY_FILE.exists():

        novo.to_csv(
            HISTORY_FILE,
            mode="a",
            header=False,
            index=False
        )

    else:

        novo.to_csv(
            HISTORY_FILE,
            index=False
        )


# ---------------- CONFIGURAÇÃO ----------------

st.set_page_config(
    page_title="CopaPredict IA",
    page_icon="⚽",
    layout="wide"
)

st.title("⚽ CopaPredict IA")

st.write(
    "Sistema de previsão de partidas usando Machine Learning"
)

# ---------------- DADOS ----------------

@st.cache_data
def carregar_times():
    return listar_times()

times = carregar_times()


@st.cache_data
def carregar_ranking():
    return ranking_forca()

ranking = carregar_ranking()

# ---------------- SELEÇÃO ----------------

st.markdown("## Seleções")

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

st.info(f"{home_team} x {away_team}")

# ---------------- ESTATÍSTICAS ----------------

col_stats1, col_stats2 = st.columns(2)

with col_stats1:

    st.markdown(f"### {home_team}")

    st.write(
        f"⚔️ Ataque: {calcular_ataque(home_team):.2f}"
    )

    st.write(
        f"🛡️ Defesa: {calcular_defesa(home_team):.2f}"
    )

    st.write(
        f"📈 Forma: {calcular_forma(home_team):.2f}"
    )

with col_stats2:

    st.markdown(f"### {away_team}")

    st.write(
        f"⚔️ Ataque: {calcular_ataque(away_team):.2f}"
    )

    st.write(
        f"🛡️ Defesa: {calcular_defesa(away_team):.2f}"
    )

    st.write(
        f"📈 Forma: {calcular_forma(away_team):.2f}"
    )

# ---------------- HISTÓRICO DE JOGOS ----------------

st.markdown("## Últimos jogos")

col_hist1, col_hist2 = st.columns(2)

with col_hist1:

    st.dataframe(
        ultimos_jogos(home_team)
    )

with col_hist2:

    st.dataframe(
        ultimos_jogos(away_team)
    )

# ---------------- RANKING ----------------

st.markdown("## Ranking IA")

st.dataframe(
    ranking.head(20)
)

# ---------------- PREVISÃO ----------------

if st.button("🔮 Fazer previsão"):

    dados = gerar_features(
        home_team,
        away_team
    )

    st.write(dados)

    resposta = requests.post(
        "http://127.0.0.1:8000/predict",
        json=dados,
        timeout=10
    )

    if resposta.status_code != 200:

        st.error(
            f"Erro na API ({resposta.status_code})"
        )

    else:

        resultado = resposta.json()

        if "prediction" not in resultado:

            st.error(resultado)

        else:

            probs = resultado["probabilities"]

            prob_vitoria = round(
                probs["vitoria"] * 100,
                2
            )

            prob_empate = round(
                probs["empate"] * 100,
                2
            )

            prob_derrota = round(
                probs["derrota"] * 100,
                2
            )

            mapa = {
                0: "Derrota",
                1: "Empate",
                2: "Vitória"
            }

            classe = resultado["prediction"]

            salvar_previsao(
                home_team,
                away_team,
                mapa[classe],
                probs
            )

            if classe == 2:

                st.success(
                    f"🏆 Resultado previsto: {mapa[classe]}"
                )

            elif classe == 1:

                st.warning(
                    f"🤝 Resultado previsto: {mapa[classe]}"
                )

            else:

                st.error(
                    f"❌ Resultado previsto: {mapa[classe]}"
                )

            st.subheader("Probabilidades")

            st.write(
                f"🏆 Vitória ({prob_vitoria}%)"
            )

            st.progress(
                prob_vitoria / 100
            )

            st.write(
                f"🤝 Empate ({prob_empate}%)"
            )

            st.progress(
                prob_empate / 100
            )

            st.write(
                f"❌ Derrota ({prob_derrota}%)"
            )

            st.progress(
                prob_derrota / 100
            )

            st.markdown("## 📊 Probabilidades")

            col_prob1, col_prob2, col_prob3 = st.columns(3)

            with col_prob1:

                st.metric(
                    "Vitória",
                    f"{prob_vitoria:.1f}%"
                )

            with col_prob2:

                st.metric(
                    "Empate",
                    f"{prob_empate:.1f}%"
                )

            with col_prob3:

                st.metric(
                    "Derrota",
                    f"{prob_derrota:.1f}%"
                )

            fig, ax = plt.subplots(
                figsize=(4, 2.5)
            )

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

            ax.set_ylim(0, 1)

            ax.set_ylabel(
                "Probabilidade"
            )

            st.pyplot(
                fig,
                use_container_width=False
            )

# ---------------- HISTÓRICO DE PREVISÕES ----------------

if HISTORY_FILE.exists():

    st.markdown(
        "## 📜 Histórico de Previsões"
    )

    def carregar_historico():
        return pd.read_csv(HISTORY_FILE)

    historico = carregar_historico()

    st.dataframe(
        historico.tail(10)
    )