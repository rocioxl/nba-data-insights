import json

import joblib
import pandas as pd
from flask import request
from sklearn.tree import DecisionTreeClassifier
from sqlalchemy.sql import text

from . import create_app
from .database import repository
from .database.models import *
from .prediction_models.prepare_data import get_vector_data

# INSTANCIATE FLASK APP

app = create_app()
engine = db.get_engine(app=app)

# LOAD PREDICTION MODEL

MODEL_DIR = "./models/nba_sklearn_model.pkl"
model_clf = joblib.load(MODEL_DIR)
print(f" * Prediction Model: {type(model_clf)}")

ALL_GAMES = pd.read_csv("./data/model_dataset/formated_games.csv")
ALL_RANKINGS = pd.read_csv("./data/model_dataset/formated_rankings.csv")
print(f" * Loaded dataset (games and rankings)")

# ENDPOINTS


@app.route("/", methods=["GET"])
def index():
    return json.dumps({"entities": list(ENTITY_MAPPER.keys())}), 200


@app.route("/players/week/<date>", methods=["GET"])
def week_best_players(date: str):
    data = request.get_json()
    limit = 1
    if data:
        limit = data.get("limit", 1)

    with engine.connect() as con:
        statement = text(
            """
            SELECT game_detail.player_name,game_detail.reb ,game_detail.ast ,  game_detail.pts ,game_detail.reb + game_detail.ast  +  game_detail.pts as total_stats, game.game_date_est 
            FROM game_detail, game
            WHERE
                game_detail.game_id = game.id
                AND
                YEARWEEK(:date) = YEARWEEK(game.game_date_est)
            ORDER BY total_stats DESC
            LIMIT  :limit;
            """
        )

        rs = con.execute(statement, **{"date": date, "limit": limit})

    return json.dumps([{k: str(v) for k, v in dict(r).items()} for r in rs]), 200


@app.route("/players/season/<year>", methods=["GET"])
def season_best_player(year: str):
    data = request.get_json()
    limit = 1
    if data:
        limit = data.get("limit", 1)

    result = []
    with engine.connect() as con:
        for week in range(1, 54):

            statement = text(
                """
                SELECT game_detail.player_name,game_detail.reb ,game_detail.ast ,  game_detail.pts ,game_detail.reb + game_detail.ast  +  game_detail.pts as total_stats, game.game_date_est 
                FROM game_detail, game
                WHERE
                    game_detail.game_id = game.id
                    AND
                    :yearweek = YEARWEEK(game.game_date_est)
                ORDER BY total_stats DESC
                LIMIT  :limit;
                """
            )

            rs = con.execute(statement, **{"yearweek": f"{year}{week}", "limit": limit})
            players = [{k: str(v) for k, v in dict(r).items()} for r in rs]
            if players:
                result.append({"week": week, "best_players": players})

    return json.dumps(result), 200


@app.route("/<entity>", methods=["GET"])
def fetch_all(entity):
    records = repository.get_all(ENTITY_MAPPER[entity])
    all_records = [rec.to_json() for rec in records]
    return json.dumps(all_records), 200


@app.route("/add/<entity>", methods=["POST"])
def add(entity):
    data = request.get_json()
    if not data:
        json.dumps("None is not valid as input"), 400
    repository.insert(ENTITY_MAPPER[entity], **data)
    return json.dumps("Added"), 200


@app.route("/remove/<entity>/<record_id>", methods=["DELETE"])
def remove(entity, record_id):
    repository.delete(ENTITY_MAPPER[entity], id=record_id)
    return json.dumps("Deleted"), 200


@app.route("/edit/<entity>/<record_id>", methods=["PATCH"])
def edit(entity, record_id):
    data = request.get_json()
    repository.edit(ENTITY_MAPPER[entity], id=record_id, **data)
    return json.dumps("Edited"), 200


@app.route("/match", methods=["POST"])
def match():
    data = request.get_json()
    vector = get_vector_data(
        games=data, all_games=ALL_GAMES, all_rankings=ALL_RANKINGS, prediction=True
    ).values
    prediction = model_clf.predict(vector)
    return json.dumps({"HOME_TEAM_WINS_PREDICTION": prediction.item()}), 200

