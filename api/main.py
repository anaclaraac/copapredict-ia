from fastapi import FastAPI

import pandas as pd
import joblib


app = FastAPI()

modelo = joblib.load(
    "ml/model.pkl"
)


@app.get("/prever")

def prever():

    entrada = pd.DataFrame({
        "home_attack_avg":[2.0],
        "away_attack_avg":[1.5],
        "home_form":[0.8],
        "attack_strength":[2.1],
        "avg_goals":[2.5]
    })

    resultado = modelo.predict(
        entrada
    )

    return {
        "previsao":
        int(resultado[0])
    }