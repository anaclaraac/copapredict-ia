import pandas as pd

from sklearn.model_selection import train_test_split

from sklearn.metrics import accuracy_score

from sklearn.linear_model import LogisticRegression

from sklearn.tree import DecisionTreeClassifier

from sklearn.ensemble import RandomForestClassifier

from xgboost import XGBClassifier


dados = pd.read_csv(
"data/processed/model_input.csv"
)


X = dados[
[
"home_attack_avg",
"away_attack_avg",
"home_form",
"attack_strength",
"avg_goals"
]
]


y = dados[
"target"
]


X_train,X_test,y_train,y_test = train_test_split(
X,
y,
test_size=0.2,
random_state=42
)


modelos = {

"Regressao_Logistica":
LogisticRegression(),

"Arvore":
DecisionTreeClassifier(),

"RandomForest":
RandomForestClassifier(),

"XGBoost":
XGBClassifier()

}


for nome,modelo in modelos.items():

    modelo.fit(
    X_train,
    y_train
    )

    pred = modelo.predict(
    X_test
    )

    score = accuracy_score(
    y_test,
    pred
    )

    print(
    nome,
    score
    )