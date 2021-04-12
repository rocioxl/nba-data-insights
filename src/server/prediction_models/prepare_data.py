import numpy as np
import pandas as pd

# FEATURES
ranking_features = [
    "TEAM_ID",
    # TODO: REMOVE -----
    # "G",
    # "W",
    # "L",
    # ------------------
    "W_PCT",
    "HOME_RECORD",
    "ROAD_RECORD",
]

game_features = ["PTS", "FG_PCT", "FT_PCT", "FG3_PCT", "AST", "REB"]

#  GET AGREGATED HISTORICAL RANKINGS DATA


def get_team_rankings_stats_before_date(team_id, date, features, rankings):
    result_df = rankings.loc[
        (rankings["STANDINGSDATE"] < date) & (rankings["TEAM_ID"] == team_id)
    ]

    _prev_season = result_df.loc[result_df["SEASON_ID"] < result_df["SEASON_ID"].max()]
    _prev_season = _prev_season.loc[
        _prev_season["STANDINGSDATE"] == _prev_season["STANDINGSDATE"].max()
    ]

    _current_season = result_df[
        result_df["STANDINGSDATE"] == result_df["STANDINGSDATE"].max()
    ]

    _current_season = _current_season[features]
    _prev_season = _prev_season[features]

    return _current_season.merge(
        _prev_season, on="TEAM_ID", suffixes=("", "_prev")
    ).drop(columns="TEAM_ID")


def get_historical_rankings_data(games, all_rankings):
    def _get_rankings(game, features=ranking_features, all_rankings=all_rankings):
        date = game["GAME_DATE_EST"].values[0]
        home_team = game["TEAM_ID_home"].values[0]
        away_team = game["TEAM_ID_away"].values[0]

        h_rank = get_team_rankings_stats_before_date(
            home_team, date=date, features=features, rankings=all_rankings
        )
        a_rank = get_team_rankings_stats_before_date(
            away_team, date=date, features=features, rankings=all_rankings
        )

        h_rank.columns += "_home"
        a_rank.columns += "_away"

        return pd.concat([h_rank, a_rank], axis=1)

    _games = games.copy()
    _games = _games.groupby("GAME_ID").apply(_get_rankings)
    _games = _games.reset_index().drop(columns="level_1")

    return _games.reset_index(drop=True)


#  GET AGREGATED HISTORICAL GAMES DATA


def get_team_games_stats_before_date(team_id, date, n, features, game_type, games):

    if game_type not in ["all", "home", "away"]:
        raise ValueError("game_type must be all, home or away")

    _games = games.loc[games["GAME_DATE_EST"] < date]
    _games = _games.loc[
        (_games["TEAM_ID_home"] == team_id) | (_games["TEAM_ID_away"] == team_id)
    ]

    _games.loc[:, "is_home"] = _games["TEAM_ID_home"] == team_id

    if game_type == "home":
        _games = _games.loc[_games["is_home"]]

    elif game_type == "away":
        _games = _games.loc[~_games["is_home"]]

    _games.loc[:, "WIN_PRCT"] = _games["is_home"] == _games["HOME_TEAM_WINS"]

    for col in features:
        _games.loc[:, col] = np.where(
            _games["is_home"], _games["%s_home" % col], _games["%s_away" % col]
        )

    cols = ["WIN_PRCT"] + features

    if len(_games) < n:
        return _games[cols]

    return _games.tail(n)[cols]


def get_historical_games_data(games, n, all_games):
    def _get_stats(game, n=n, features=game_features, all_games=all_games):
        date = game["GAME_DATE_EST"].values[0]
        home_team = game["TEAM_ID_home"].values[0]
        away_team = game["TEAM_ID_away"].values[0]

        h_stats = get_team_games_stats_before_date(
            home_team, date, n=n, features=features, game_type="all", games=all_games
        )
        h_stats.columns += "_home_%ig" % n
        h_stats = h_stats.mean().to_frame().T

        a_stats = get_team_games_stats_before_date(
            away_team, date, n, features, game_type="all", games=all_games
        )
        a_stats.columns += "_away_%ig" % n
        a_stats = a_stats.mean().to_frame().T

        return pd.concat([h_stats, a_stats], axis=1)

    _games = games.copy()
    _games = _games.groupby("GAME_ID").apply(_get_stats)
    _games = _games.reset_index().drop(columns="level_1")

    return _games.reset_index(drop=True)


# COMBINE ALL FEATURES


def get_vector_data(games, all_games, all_rankings, prediction=True):
    if not isinstance(games, pd.DataFrame):
        games = pd.DataFrame(games)

    # Get ranking stats before game
    rank_stats = get_historical_rankings_data(games, all_rankings=all_rankings)

    # Get stats before game 3 previous games
    game_stats_3g = get_historical_games_data(games, n=3, all_games=all_games)

    # Get stats before game 20 previous games
    game_stats_20g = get_historical_games_data(games, n=20, all_games=all_games)

    formated_games = rank_stats.merge(game_stats_3g, on="GAME_ID", how="left")
    formated_games = formated_games.merge(game_stats_20g, on="GAME_ID", how="left")

    if prediction:
        formated_games["SEASON"] = [x[:4] for x in games["GAME_DATE_EST"].values]
    else:
        formated_games = formated_games.merge(
            all_games[["GAME_ID", "SEASON", "HOME_TEAM_WINS"]], on="GAME_ID", how="left"
        )
    formated_games = formated_games.reset_index(drop=True)
    return formated_games
