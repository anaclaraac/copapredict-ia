import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression


dados = pd.read_csv(
    "data/processed/model_input.csv"
)


dados = dados.replace(
    [np.inf, -np.inf],
    np.nan
)

features = [

    "home_attack_avg",

    "away_attack_avg",

    "home_form",

    "attack_strength",

    "avg_goals"

]

dados = dados.dropna(
    subset=features + ["target"]
)


X = dados[
    features
]


y = dados[
    "target"
]


X_train, X_test, y_train, y_test = train_test_split(

    X,

    y,

    test_size=0.2,

    random_state=42

)


modelo = LogisticRegression(
    max_iter=1000
)


modelo.fit(
    X_train,
    y_train
)


score = modelo.score(
    X_test,
    y_test
)

print(
    "Acurácia:",
    score
)



joblib.dump(
    modelo,
    "ml/model.pkl"
)

print(
    "Modelo salvo"
)