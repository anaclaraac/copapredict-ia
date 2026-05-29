from pathlib import Path
import joblib
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "ml" / "model.pkl"

modelo = joblib.load(
    MODEL_PATH
)

def prever(dados):

    entrada = pd.DataFrame([dados])

    pred = modelo.predict(
        entrada
    )[0]

    probs = modelo.predict_proba(
        entrada
    )[0]

    return {

        "prediction": int(pred),

        "probabilities": {

            "derrota": float(probs[0]),
            "empate": float(probs[1]),
            "vitoria": float(probs[2])

        }

    }