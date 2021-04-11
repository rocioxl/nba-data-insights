import flask_sqlalchemy

db = flask_sqlalchemy.SQLAlchemy()


class League(db.Model):
    __tablename__ = "league"

    id = db.Column(db.Integer, primary_key=True)

    teams = db.relationship("Team")
    rankings = db.relationship("Ranking")

    def __repr__(self):
        return f"<League {self.id}>"

    def to_json(self, expand=False):
        return {
            "id": self.id,
        }

    players_teams = db.Table(
        "players_teams",
        db.Column(
            "player_id", db.String(255), db.ForeignKey("player.id"), primary_key=True
        ),
        db.Column(
            "team_id", db.String(255), db.ForeignKey("team.id"), primary_key=True
        ),
    )


class Team(db.Model):
    __tablename__ = "team"

    id = db.Column(db.String(255), primary_key=True)
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

    league_id = db.Column(db.Integer, db.ForeignKey("league.id"))
    players = db.relationship('Player', secondary=players_teams, lazy=True',
        backref=db.backref('teams', lazy=True))


    away_games = db.relationship(
        "Game", backref="away_team", lazy=True, foreign_keys="Game.home_team_id"
    )
    home_games = db.relationship(
        "Game", backref="home_team", lazy=True, foreign_keys="Game.away_team_id"
    )
    game_details = db.relationship("GameDetail", backref="team", lazy=True)

    def __repr__(self):
        return f"<Team {self.id}>"

    def to_json(self):
        return {
            "id": self.id,
        }


class Player(db.Model):
    __tablename__ = "player"

    id = db.Column(db.String(255), primary_key=True)
    player_name = db.Column(db.String(100))
    season = db.Column(db.Integer)

    game_details = db.relationship("GameDetail", backref="player", lazy=True)

    def __repr__(self):
        return f"<Player {self.id}>"

    def to_json(self):
        return {"id": self.id}


class Game(db.Model):
    __tablename__ = "game"

    id = db.Column(db.String(255), primary_key=True)
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

    home_team_id = db.Column(db.Integer, db.ForeignKey("team.id"), nullable=False)
    away_team_id = db.Column(db.Integer, db.ForeignKey("team.id"), nullable=False)
    game_details = db.relationship("GameDetail", backref="game", lazy=True)

    def __repr__(self):
        return f"<Game {self.id}>"

    def to_json(self):
        return {"id": self.id}


class GameDetail(db.Model):
    __tablename__ = "game_detail"

    team_abbreviation = db.Column(db.String(10))
    team_city = db.Column(db.String(50))
    player_name = db.Column(db.String(100))
    start_position = db.Column(db.String(5))
    comment = db.Column(db.String(500))
    min = db.Column(db.DateTime)
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

    game_id = db.Column(db.Integer, db.ForeignKey("game.id"), nullable=False, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey("team.id"), nullable=False, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey("player.id"), nullable=False, primary_key=True)

    def __repr__(self):
        return f"<GameDetail {self.id}>"

    def to_json(self):
        return {"id": self.id}


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

    team_id = db.Column(db.Integer, db.ForeignKey("team.id"), primary_key=True)
    league_id = db.Column(db.Integer, db.ForeignKey("league.id"), primary_key=True)
    season_id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return f"<Ranking {self.id}>"

    def to_json(self):
        return {"id": self.id}
