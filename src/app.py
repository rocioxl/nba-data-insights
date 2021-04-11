from utils.server_requests import populate_table
from server.database.models import  *

populate_table(data_dir="../data/nba_dataset/leagues.csv", entity="leagues")

