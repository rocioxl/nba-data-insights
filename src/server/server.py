import json

from flask import request

from . import create_app
from .database import repository
from .database.models import *

app = create_app()

ENTITY_MAPPER = {
    "players": Player,
    "teams": Team,
    "games": Game,
    "gamedetails": GameDetail,
    "leagues": League,
    "rankings": Ranking,
}


@app.route("/", methods=["GET"])
def index():
    return json.dumps({"entities": list(ENTITY_MAPPER.keys())}), 200


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
