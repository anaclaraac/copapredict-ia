from pathlib import Path
import joblib
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "ml" / "model.pkl"

modelo = joblib.load(
    MODEL_PATH
)

def prever(
dados
):

    entrada = pd.DataFrame([dados])

    pred = modelo.predict(entrada)[0]

    return {

    "prediction":
    int(pred)

    }