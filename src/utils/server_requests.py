import json
from pathlib import Path

import pandas as pd
import requests

BASE_URL = "http://127.0.0.1:5000"


def populate_table(data_dir, entity=None):
    if not data_dir:
        raise ValueError("data_dir must be specified")

    df = pd.read_csv(data_dir)
    total = len(df)

    if not entity:
        path = Path(data_dir)
        entity = path.stem

    url = f"{BASE_URL}/add/{entity}"
    for index, data in df.iterrows():

        headers = {"Content-type": "application/json"}

        payload = json.dumps({k.lower(): v.item() for k, v in dict(data).items()})
        response = requests.request("POST", url, headers=headers, data=payload)

        print(f"{index}/{total}: {response.text}")
