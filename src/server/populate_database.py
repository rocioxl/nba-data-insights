import json
import os
import sys

import pandas as pd
import requests

from database.models import *

BASE_URL = "http://127.0.0.1:5000"

# Data normalization


def get_players_from_players_csv(csv_dir="../../data/nba_dataset/players.csv"):
    df = pd.read_csv(csv_dir)
    print(len(df))
    df = df.drop_duplicates(subset=["PLAYER_ID"])
    print(len(df))
    df = df[["PLAYER_ID", "PLAYER_NAME"]]
    return df


def get_players_from_game_details_csv(
    csv_dir="../../data/nba_dataset/games_details.csv",
):
    df = pd.read_csv(csv_dir)
    print(len(df))
    df = df.drop_duplicates(subset=["PLAYER_ID"])
    print(len(df))
    df = df[["PLAYER_ID", "PLAYER_NAME"]]
    return df


def extract_players(
    dataset_dir: str = "../../data/nba_dataset", to: str = "../../data/nba_dataset"
):
    df1 = get_players_from_players_csv(f"{dataset_dir}/players.csv")
    df2 = get_players_from_game_details_csv(f"{dataset_dir}/games_details.csv")
    df = pd.concat([df1, df2])
    df = df.drop_duplicates(subset=["PLAYER_ID"])
    df.to_csv(f"{to}/cleaned_players.csv", index=False)


# Database population


def populate_table(data_dir: str, entity: str, limit: int = None):
    if not data_dir or not entity:
        raise ValueError("data_dir and entity are needed")

    df = pd.read_csv(data_dir)
    total = len(df)

    url = f"{BASE_URL}/add/{entity}"
    entity = ENTITY_MAPPER[entity]

    inserted = 0
    for index, data in df.iterrows():
        headers = {"Content-type": "application/json"}
        payload = json.dumps(entity.mapper(dict(data)))
        response = requests.request("POST", url, headers=headers, data=payload)
        if response.status_code == 200:
            inserted += 1
            if limit is not None and inserted >= limit:
                break

        print(f"{index}/{total}: {response.status_code} - {response.text}")


def populate_database(dataset_dir="../../data/nba_dataset", limit=10000):
    if not os.path.exists(dataset_dir):
        raise ValueError("Invalid dataset path")

    if not os.path.exists(f"{dataset_dir}/cleaned_players.csv"):
        print("\n... Extracting cleaned players")

        extract_players(dataset_dir=dataset_dir, to=dataset_dir)

    print("\n... Populating table: leagues")
    populate_table(data_dir=f"{dataset_dir}/leagues.csv", entity="leagues", limit=limit)

    print("\n... Populating table: teams")
    populate_table(data_dir=f"{dataset_dir}/teams.csv", entity="teams", limit=limit)

    print("\n... Populating table: players")
    populate_table(
        data_dir=f"{dataset_dir}/cleaned_players.csv", entity="players", limit=limit
    )

    print("\n... Populating table: players_teams")
    populate_table(
        data_dir=f"{dataset_dir}/players.csv", entity="players_teams", limit=limit
    )

    print("\n... Populating table: games")
    populate_table(data_dir=f"{dataset_dir}/games.csv", entity="games", limit=limit)

    print("\n... Populating table: games_details")
    populate_table(
        data_dir=f"{dataset_dir}/games_details.csv", entity="games_details", limit=limit
    )

    print("\n... Populating table: rankings")
    populate_table(
        data_dir=f"{dataset_dir}/ranking.csv", entity="rankings", limit=limit
    )


if __name__ == "__main__":
    dataset_dir = "../../data/nba_dataset"
    limit = None

    if len(sys.argv) > 1:
        dataset_dir = sys.argv[1]
    if len(sys.argv) > 2:
        limit = int(sys.argv[2])

    if dataset_dir=="--help" or dataset_dir=="-h":
            print(f"USAGE: {sys.argv[0]} NBA_DATASET_DIR LIMIT")
    else:
        populate_database(dataset_dir=dataset_dir, limit=limit)
