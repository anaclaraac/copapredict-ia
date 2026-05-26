from fastapi import FastAPI

app = FastAPI()


@app.get("/")

def home():

    return {

        "projeto":
        "CopaPredict AI",

        "status":
        "ativo"

    }