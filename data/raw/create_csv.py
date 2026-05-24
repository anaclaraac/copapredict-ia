import pandas as pd

df = pd.read_csv(matches.csv)

df.insert(
    0,              # posição da coluna
    "match_id",     # nome
    range(1, len(df)+1)
)

df.to_csv(
    matches.csv,
    index=False
)

print("Coluna criada")



times = pd.concat([
    df["home_team"],
    df["away_team"]
])

times = (
    times
    .drop_duplicates()
    .sort_values()
)