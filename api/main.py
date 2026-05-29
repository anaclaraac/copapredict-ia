from fastapi import FastAPI
from .predict import prever

app = FastAPI()

@app.get("/")

def home():
    return {
    "status":"ok"
    }

@app.post("/predict")

def prediction(
dados:dict
):

    resultado = prever(
    dados
    )

    return resultado