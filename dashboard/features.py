import pandas as pd
from pathlib import Path
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "matches_clean.csv"
)

matches = pd.read_csv(DATA_PATH)

SELECOES_COPA_2026 = [
    "Algeria",
    "Argentina",
    "Australia",
    "Austria",
    "Belgium",
    "Bosnia and Herzegovina",
    "Brazil",
    "Canada",
    "Cape Verde",
    "Colombia",
    "Curaçao",
    "Czechia",
    "DR Congo",
    "Ecuador",
    "Egypt",
    "England",
    "France",
    "Germany",
    "Ghana",
    "Haiti",
    "Iran",
    "Iraq",
    "Ivory Coast",
    "Japan",
    "Jordan",
    "Mexico",
    "Morocco",
    "Netherlands",
    "New Zealand",
    "Norway",
    "Panama",
    "Paraguay",
    "Portugal",
    "Qatar",
    "Saudi Arabia",
    "Scotland",
    "Senegal",
    "South Africa",
    "South Korea",
    "Spain",
    "Sweden",
    "Switzerland",
    "Tunisia",
    "Türkiye",
    "United States",
    "Uruguay",
    "Uzbekistan"
]


def obter_jogos_time(time):

    jogos = matches[
        (matches["home_team"] == time)
        |
        (matches["away_team"] == time)
    ]

    jogos = jogos[
    jogos["home_team"].isin(
        SELECOES_COPA_2026
    )
    &
    jogos["away_team"].isin(
        SELECOES_COPA_2026
    )
    ]

    jogos = jogos.dropna(
        subset=[
            "home_score",
            "away_score"
        ]
    )

    jogos = jogos.sort_values("date")

    jogos = jogos.tail(10)

    return jogos


def calcular_ataque(time):

    jogos = obter_jogos_time(time)

    gols = []

    for _, jogo in jogos.iterrows():

        if jogo["home_team"] == time:

            gols.append(
                jogo["home_score"]
            )

        else:

            gols.append(
                jogo["away_score"]
            )

    return sum(gols) / len(gols)


def calcular_defesa(time):

    jogos = obter_jogos_time(time)

    sofridos = []

    for _, jogo in jogos.iterrows():

        if jogo["home_team"] == time:

            sofridos.append(
                jogo["away_score"]
            )

        else:

            sofridos.append(
                jogo["home_score"]
            )

    return sum(sofridos) / len(sofridos)


def calcular_forma(time):

    jogos = obter_jogos_time(time)

    vitorias = 0

    for _, jogo in jogos.iterrows():

        if (
            jogo["home_team"] == time
            and
            jogo["home_score"] > jogo["away_score"]
        ):

            vitorias += 1

        elif (
            jogo["away_team"] == time
            and
            jogo["away_score"] > jogo["home_score"]
        ):

            vitorias += 1

    return vitorias / len(jogos)


def calcular_win_streak(time):

    jogos = obter_jogos_time(time)

    sequencia = 0

    jogos = jogos.sort_values(
        "date",
        ascending=False
    )

    for _, jogo in jogos.iterrows():

        venceu = False

        if (
            jogo["home_team"] == time
            and
            jogo["home_score"] > jogo["away_score"]
        ):

            venceu = True

        elif (
            jogo["away_team"] == time
            and
            jogo["away_score"] > jogo["home_score"]
        ):

            venceu = True

        if venceu:

            sequencia += 1

        else:

            break

    return sequencia


def calcular_loss_streak(time):

    jogos = obter_jogos_time(time)

    sequencia = 0

    jogos = jogos.sort_values(
        "date",
        ascending=False
    )

    for _, jogo in jogos.iterrows():

        perdeu = False

        if (
            jogo["home_team"] == time
            and
            jogo["home_score"] < jogo["away_score"]
        ):

            perdeu = True

        elif (
            jogo["away_team"] == time
            and
            jogo["away_score"] < jogo["home_score"]
        ):

            perdeu = True

        if perdeu:

            sequencia += 1

        else:

            break

    return sequencia


def gerar_features(
    home_team,
    away_team
):

    home_attack = calcular_ataque(
        home_team
    )

    away_attack = calcular_ataque(
        away_team
    )

    home_defense = calcular_defesa(
        home_team
    )

    away_defense = calcular_defesa(
        away_team
    )

    home_form = calcular_forma(
        home_team
    )

    away_form = calcular_forma(
        away_team
    )

    win_streak = calcular_win_streak(
        home_team
    )

    loss_streak = calcular_loss_streak(
        away_team
    )

    return {

        "home_attack_avg": home_attack,

        "away_attack_avg": away_attack,

        "home_defense_avg": home_defense,

        "away_defense_avg": away_defense,

        "home_form": home_form,

        "away_form": away_form,

        "win_streak": win_streak,

        "loss_streak": loss_streak,

        "home_advantage": 1,

        "tournament_weight": 5,

        "home_continent_code": 1,

        "away_continent_code": 1,

        "same_continent": 0,

        "attack_strength":
            home_attack / away_defense,

        "avg_goals":
            (home_attack + away_attack) / 2

    }

@st.cache_data
def listar_times():

    times = set(
        matches["home_team"]
    )

    times.update(
        matches["away_team"]
    )

    times = times.intersection(
        SELECOES_COPA_2026
    )

    return sorted(
        list(times)
    )

@st.cache_data
def ultimos_jogos(time):

    jogos = obter_jogos_time(time)

    return jogos[
        [
            "date",
            "home_team",
            "away_team",
            "home_score",
            "away_score"
        ]
    ].tail(5)


def ranking_forca():

    ranking = []

    for time in listar_times():

        try:

            score = (
                calcular_ataque(time)
                +
                calcular_forma(time)
                -
                calcular_defesa(time)
            )

            ranking.append(
                [time, score]
            )

        except:

            pass

    ranking = pd.DataFrame(
        ranking,
        columns=[
            "team",
            "score"
        ]
    )

    ranking = ranking.sort_values(
        "score",
        ascending=False
    )

    ranking = ranking.reset_index(
        drop=True
    )

    ranking.index += 1

    return ranking


print(
    gerar_features(
        "Brazil",
        "Argentina"
    )
)

print(
    listar_times()[:20]
)