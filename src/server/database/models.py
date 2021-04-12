import flask_sqlalchemy
import numpy as np

db = flask_sqlalchemy.SQLAlchemy()


class PlayersTeams(db.Model):
    __tablename__ = "players_teams"

    player_id = db.Column(db.String(20), db.ForeignKey("player.id"), primary_key=True)
    team_id = db.Column(db.String(20), db.ForeignKey("team.id"), primary_key=True)
    season = db.Column(db.Integer, primary_key=True)

    @staticmethod
    def mapper(csv_data):
        return {
            "team_id": str(csv_data["TEAM_ID"]) if csv_data["TEAM_ID"] else None,
            "player_id": str(csv_data["PLAYER_ID"]) if csv_data["PLAYER_ID"] else None,
            "season": int(csv_data["SEASON"])
            if not np.isnan(csv_data["SEASON"])
            else None,
        }


class League(db.Model):
    __tablename__ = "league"

    id = db.Column(db.String(20), primary_key=True)

    teams = db.relationship("Team")
    rankings = db.relationship("Ranking")

    def __repr__(self):
        return f"<League {self.id}>"

    def to_json(self, expand=False):
        return {
            "id": self.id,
        }

    @staticmethod
    def mapper(csv_data):
        return {"id": str(csv_data["LEAGUE_ID"])}


class Team(db.Model):
    __tablename__ = "team"

    id = db.Column(db.String(20), primary_key=True)
    min_year = db.Column(db.Integer)
    max_year = db.Column(db.Integer)
    abbreviation = db.Column(db.String(10))
    nickname = db.Column(db.String(100))
    yearfounded = db.Column(db.Integer)
    city = db.Column(db.String(100))
    arena = db.Column(db.String(100))
    arenacapacity = db.Column(db.Integer)
    owner = db.Column(db.String(100))
    generalmanager = db.Column(db.String(100))
    headcoach = db.Column(db.String(100))
    dleagueaffiliation = db.Column(db.String(100))

    league_id = db.Column(db.String(20), db.ForeignKey("league.id"), default="0")
    players = db.relationship(
        "Player", secondary="players_teams", back_populates="teams"
    )
    home_games = db.relationship(
        "Game", foreign_keys="Game.home_team_id", backref="home_team", lazy="dynamic"
    )
    away_games = db.relationship(
        "Game", foreign_keys="Game.away_team_id", backref="away_team", lazy="dynamic"
    )
    game_details = db.relationship("GameDetail", backref="team", lazy=True)

    def __repr__(self):
        return f"<Team {self.id}>"

    def to_json(self):
        return {
            "id": self.id,
        }

    @property
    def games(self):
        return self.home_games.union(self.away_games)

    @staticmethod
    def mapper(csv_data):
        return {
            "league_id": str(csv_data["LEAGUE_ID"]) if csv_data["LEAGUE_ID"] else None,
            "id": str(csv_data["TEAM_ID"]) if csv_data["TEAM_ID"] else None,
            "min_year": int(csv_data["MIN_YEAR"])
            if not np.isnan(csv_data["MIN_YEAR"])
            else None,
            "max_year": int(csv_data["MAX_YEAR"])
            if not np.isnan(csv_data["MAX_YEAR"])
            else None,
            "abbreviation": str(csv_data["ABBREVIATION"])
            if csv_data["ABBREVIATION"]
            else None,
            "nickname": str(csv_data["NICKNAME"]) if csv_data["NICKNAME"] else None,
            "yearfounded": int(csv_data["YEARFOUNDED"])
            if not np.isnan(csv_data["YEARFOUNDED"])
            else None,
            "city": str(csv_data["CITY"]) if csv_data["CITY"] else None,
            "arena": str(csv_data["ARENA"]) if csv_data["ARENA"] else None,
            "arenacapacity": int(csv_data["ARENACAPACITY"])
            if not np.isnan(csv_data["ARENACAPACITY"])
            else None,
            "owner": str(csv_data["OWNER"]) if csv_data["OWNER"] else None,
            "generalmanager": str(csv_data["GENERALMANAGER"])
            if csv_data["GENERALMANAGER"]
            else None,
            "headcoach": str(csv_data["HEADCOACH"]) if csv_data["HEADCOACH"] else None,
            "dleagueaffiliation": str(csv_data["DLEAGUEAFFILIATION"])
            if csv_data["DLEAGUEAFFILIATION"]
            else None,
        }


class Player(db.Model):
    __tablename__ = "player"

    id = db.Column(db.String(20), primary_key=True)
    player_name = db.Column(db.String(100))

    game_details = db.relationship("GameDetail", backref="player", lazy=True)
    teams = db.relationship("Team", secondary="players_teams", back_populates="players")

    def __repr__(self):
        return f"<Player {self.id}>"

    def to_json(self):
        return {"id": self.id}

    @staticmethod
    def mapper(csv_data):
        return {
            "player_name": str(csv_data["PLAYER_NAME"])
            if csv_data["PLAYER_NAME"]
            else None,
            "id": str(csv_data["PLAYER_ID"]) if csv_data["PLAYER_ID"] else None,
        }


class Game(db.Model):
    __tablename__ = "game"

    id = db.Column(db.String(20), primary_key=True)
    game_date_est = db.Column(db.DateTime)
    game_status_text = db.Column(db.String(50))
    season = db.Column(db.Integer)
    pts_home = db.Column(db.Integer)
    fg_pct_home = db.Column(db.Float)
    ft_pct_home = db.Column(db.Float)
    fg3_pct_home = db.Column(db.Float)
    ast_home = db.Column(db.Integer)
    reb_home = db.Column(db.Integer)
    pts_away = db.Column(db.Integer)
    fg_pct_away = db.Column(db.Float)
    ft_pct_away = db.Column(db.Float)
    fg3_pct_away = db.Column(db.Float)
    ast_away = db.Column(db.Integer)
    reb_away = db.Column(db.Integer)
    home_team_wins = db.Column(db.Integer)

    home_team_id = db.Column(db.String(20), db.ForeignKey("team.id"))
    away_team_id = db.Column(db.String(20), db.ForeignKey("team.id"))
    game_details = db.relationship("GameDetail", backref="game", lazy=True)

    def __repr__(self):
        return f"<Game {self.id}>"

    def to_json(self):
        return {"id": self.id}

    @staticmethod
    def mapper(csv_data):
        return {
            "game_date_est": csv_data["GAME_DATE_EST"]
            if csv_data["GAME_DATE_EST"]
            else None,
            "id": str(csv_data["GAME_ID"]) if csv_data["GAME_ID"] else None,
            "game_status_text": str(csv_data["GAME_STATUS_TEXT"])
            if csv_data["GAME_STATUS_TEXT"]
            else None,
            "season": int(csv_data["SEASON"])
            if not np.isnan(csv_data["SEASON"])
            else None,
            "home_team_id": str(csv_data["TEAM_ID_home"])
            if csv_data["TEAM_ID_home"]
            else None,
            "pts_home": int(csv_data["PTS_home"])
            if not np.isnan(csv_data["PTS_home"])
            else None,
            "fg_pct_home": float(csv_data["FG_PCT_home"])
            if not np.isnan(csv_data["FG_PCT_home"])
            else None,
            "ft_pct_home": float(csv_data["FT_PCT_home"])
            if not np.isnan(csv_data["FT_PCT_home"])
            else None,
            "fg3_pct_home": float(csv_data["FG3_PCT_home"])
            if not np.isnan(csv_data["FG3_PCT_home"])
            else None,
            "ast_home": int(csv_data["AST_home"])
            if not np.isnan(csv_data["AST_home"])
            else None,
            "reb_home": int(csv_data["REB_home"])
            if not np.isnan(csv_data["REB_home"])
            else None,
            "away_team_id": str(csv_data["TEAM_ID_away"])
            if csv_data["TEAM_ID_away"]
            else None,
            "pts_away": int(csv_data["PTS_away"])
            if not np.isnan(csv_data["PTS_away"])
            else None,
            "fg_pct_away": float(csv_data["FG_PCT_away"])
            if not np.isnan(csv_data["FG_PCT_away"])
            else None,
            "ft_pct_away": float(csv_data["FT_PCT_away"])
            if not np.isnan(csv_data["FT_PCT_away"])
            else None,
            "fg3_pct_away": float(csv_data["FG3_PCT_away"])
            if not np.isnan(csv_data["FG3_PCT_away"])
            else None,
            "ast_away": int(csv_data["AST_away"])
            if not np.isnan(csv_data["AST_away"])
            else None,
            "reb_away": int(csv_data["REB_away"])
            if not np.isnan(csv_data["REB_away"])
            else None,
            "home_team_wins": int(csv_data["HOME_TEAM_WINS"])
            if not np.isnan(csv_data["HOME_TEAM_WINS"])
            else None,
        }


class GameDetail(db.Model):
    __tablename__ = "game_detail"

    team_abbreviation = db.Column(db.String(10))
    team_city = db.Column(db.String(50))
    player_name = db.Column(db.String(100))
    start_position = db.Column(db.String(5))
    comment = db.Column(db.String(500))
    min = db.Column(db.String(50))
    fgm = db.Column(db.Integer)
    fga = db.Column(db.Integer)
    fg_pct = db.Column(db.Float)
    fg3m = db.Column(db.Integer)
    fg3a = db.Column(db.Integer)
    fg3_pct = db.Column(db.Float)
    ftm = db.Column(db.Integer)
    fta = db.Column(db.Integer)
    ft_pct = db.Column(db.Float)
    oreb = db.Column(db.Integer)
    dreb = db.Column(db.Integer)
    reb = db.Column(db.Integer)
    ast = db.Column(db.Integer)
    stl = db.Column(db.Integer)
    blk = db.Column(db.Integer)
    to = db.Column(db.Integer)
    pf = db.Column(db.Integer)
    pts = db.Column(db.Integer)
    plus_minus = db.Column(db.Integer)

    game_id = db.Column(db.String(20), db.ForeignKey("game.id"), primary_key=True)
    team_id = db.Column(db.String(20), db.ForeignKey("team.id"), primary_key=True)
    player_id = db.Column(db.String(20), db.ForeignKey("player.id"), primary_key=True)

    def __repr__(self):
        return f"<GameDetail {self.id}>"

    def to_json(self):
        return {
            "game_id": self.game_id,
            "team_id": self.team_id,
            "player_id": self.player_id,
        }

    @staticmethod
    def mapper(csv_data):
        return {
            "game_id": str(csv_data["GAME_ID"]) if csv_data["GAME_ID"] else None,
            "team_id": str(csv_data["TEAM_ID"]) if csv_data["TEAM_ID"] else None,
            "team_abbreviation": str(csv_data["TEAM_ABBREVIATION"])
            if csv_data["TEAM_ABBREVIATION"]
            else None,
            "team_city": str(csv_data["TEAM_CITY"]) if csv_data["TEAM_CITY"] else None,
            "player_id": str(csv_data["PLAYER_ID"]) if csv_data["PLAYER_ID"] else None,
            "player_name": str(csv_data["PLAYER_NAME"])
            if csv_data["PLAYER_NAME"]
            else None,
            "start_position": str(csv_data["START_POSITION"])
            if csv_data["START_POSITION"]
            else None,
            "comment": str(csv_data["COMMENT"]) if csv_data["COMMENT"] else None,
            "min": str(csv_data["MIN"]) if csv_data["MIN"] else None,
            "fgm": int(csv_data["FGM"]) if not np.isnan(csv_data["FGM"]) else None,
            "fga": int(csv_data["FGA"]) if not np.isnan(csv_data["FGA"]) else None,
            "fg_pct": float(csv_data["FG_PCT"])
            if not np.isnan(csv_data["FG_PCT"])
            else None,
            "fg3m": int(csv_data["FG3M"]) if not np.isnan(csv_data["FG3M"]) else None,
            "fg3a": int(csv_data["FG3A"]) if not np.isnan(csv_data["FG3A"]) else None,
            "fg3_pct": float(csv_data["FG3_PCT"])
            if not np.isnan(csv_data["FG3_PCT"])
            else None,
            "ftm": int(csv_data["FTM"]) if not np.isnan(csv_data["FTM"]) else None,
            "fta": int(csv_data["FTA"]) if not np.isnan(csv_data["FTA"]) else None,
            "ft_pct": float(csv_data["FT_PCT"])
            if not np.isnan(csv_data["FT_PCT"])
            else None,
            "oreb": int(csv_data["OREB"]) if not np.isnan(csv_data["OREB"]) else None,
            "dreb": int(csv_data["DREB"]) if not np.isnan(csv_data["DREB"]) else None,
            "reb": int(csv_data["REB"]) if not np.isnan(csv_data["REB"]) else None,
            "ast": int(csv_data["AST"]) if not np.isnan(csv_data["AST"]) else None,
            "stl": int(csv_data["STL"]) if not np.isnan(csv_data["STL"]) else None,
            "blk": int(csv_data["BLK"]) if not np.isnan(csv_data["BLK"]) else None,
            "to": int(csv_data["TO"]) if not np.isnan(csv_data["TO"]) else None,
            "pf": int(csv_data["PF"]) if not np.isnan(csv_data["PF"]) else None,
            "pts": int(csv_data["PTS"]) if not np.isnan(csv_data["PTS"]) else None,
            "plus_minus": int(csv_data["PLUS_MINUS"])
            if not np.isnan(csv_data["PLUS_MINUS"])
            else None,
        }


class Ranking(db.Model):
    __tablename__ = "ranking"

    standingsdate = db.Column(db.DateTime)
    conference = db.Column(db.String(10))
    team = db.Column(db.String(100))
    g = db.Column(db.Integer)
    w = db.Column(db.Integer)
    l = db.Column(db.Integer)
    w_pct = db.Column(db.Float)
    home_record = db.Column(db.String(10))
    road_record = db.Column(db.String(10))
    returntoplay = db.Column(db.Integer)

    team_id = db.Column(db.String(20), db.ForeignKey("team.id"), primary_key=True)
    league_id = db.Column(
        db.String(20), db.ForeignKey("league.id"), primary_key=True, default="0"
    )
    season_id = db.Column(db.String(20), primary_key=True)

    def __repr__(self):
        return f"<Ranking {self.id}>"

    def to_json(self):
        return {
            "team_id": self.team_id,
            "league_id": self.league_id,
            "season_id": self.season_id,
        }

    @staticmethod
    def mapper(csv_data):
        return {
            "team_id": str(csv_data["TEAM_ID"]) if csv_data["TEAM_ID"] else None,
            "league_id": str(csv_data["LEAGUE_ID"]) if csv_data["LEAGUE_ID"] else None,
            "season_id": str(csv_data["SEASON_ID"]) if csv_data["SEASON_ID"] else None,
            "standingsdate": csv_data["STANDINGSDATE"]
            if csv_data["STANDINGSDATE"]
            else None,
            "conference": str(csv_data["CONFERENCE"])
            if csv_data["CONFERENCE"]
            else None,
            "team": str(csv_data["TEAM"]) if csv_data["TEAM"] else None,
            "g": int(csv_data["G"]) if not np.isnan(csv_data["G"]) else None,
            "w": int(csv_data["W"]) if not np.isnan(csv_data["W"]) else None,
            "l": int(csv_data["L"]) if not np.isnan(csv_data["L"]) else None,
            "w_pct": float(csv_data["W_PCT"])
            if not np.isnan(csv_data["W_PCT"])
            else None,
            "home_record": str(csv_data["HOME_RECORD"])
            if csv_data["HOME_RECORD"]
            else None,
            "road_record": str(csv_data["ROAD_RECORD"])
            if csv_data["ROAD_RECORD"]
            else None,
            "returntoplay": int(csv_data["RETURNTOPLAY"])
            if not np.isnan(csv_data["RETURNTOPLAY"])
            else None,
        }


ENTITY_MAPPER = {
    "players": Player,
    "teams": Team,
    "games": Game,
    "games_details": GameDetail,
    "leagues": League,
    "rankings": Ranking,
    "players_teams": PlayersTeams,
}
