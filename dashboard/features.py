import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "matches_clean.csv"
)

matches = pd.read_csv(
    DATA_PATH
)

def obter_jogos_time(time):

    jogos = matches[
        (matches["home_team"] == time)
        |
        (matches["away_team"] == time)
    ]

    jogos = jogos.dropna(
        subset=[
            "home_score",
            "away_score"
        ]
    )

    jogos = jogos.sort_values(
        "date"
    )

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

    jogos = obter_jogos_time(
        time
    )

    vitorias = 0

    for _, jogo in jogos.iterrows():

        if (

            jogo["home_team"] == time

            and

            jogo["home_score"] >
            jogo["away_score"]

        ):

            vitorias += 1

        elif (

            jogo["away_team"] == time

            and

            jogo["away_score"] >
            jogo["home_score"]

        ):

            vitorias += 1

    return vitorias / len(jogos)

def calcular_win_streak(time):

    jogos = obter_jogos_time(
        time
    )

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
            jogo["home_score"] >
            jogo["away_score"]
        ):
            venceu = True

        elif (
            jogo["away_team"] == time
            and
            jogo["away_score"] >
            jogo["home_score"]
        ):
            venceu = True

        if venceu:

            sequencia += 1

        else:

            break

    return sequencia

def calcular_loss_streak(time):

    jogos = obter_jogos_time(
        time
    )

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
            jogo["home_score"] <
            jogo["away_score"]
        ):
            perdeu = True

        elif (
            jogo["away_team"] == time
            and
            jogo["away_score"] <
            jogo["home_score"]
        ):
            perdeu = True

        if perdeu:

            sequencia += 1

        else:

            break

    return sequencia

print(
    "Ataque Brasil:",
    calcular_ataque("Brazil")
)

print(
    "Defesa Brasil:",
    calcular_defesa("Brazil")
)

print(
    "Forma Brasil:",
    calcular_forma(
        "Brazil"
    )
)

print(
    "Sequência:",
    calcular_win_streak(
        "Brazil"
    )
)

print(
    "Derrotas seguidas:",
    calcular_loss_streak(
        "Brazil"
    )
)