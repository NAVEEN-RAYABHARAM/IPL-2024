# train.py

import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity


def load_and_prepare_data():

    deliveries = pd.read_csv("deliveries.csv")

    if "batter" not in deliveries.columns:
        deliveries.rename(columns={"batsman": "batter"}, inplace=True)

    # ================= BATTERS =================
    batters = deliveries.groupby("batter")["batsman_runs"].sum().reset_index()
    batters.rename(columns={"batter": "player", "batsman_runs": "total_runs"}, inplace=True)

    matches_bat = deliveries.groupby("batter")["match_id"].nunique().reset_index()
    matches_bat.rename(columns={"batter": "player", "match_id": "matches"}, inplace=True)

    balls = deliveries.groupby("batter").size().reset_index(name="balls_faced")
    balls.rename(columns={"batter": "player"}, inplace=True)

    batters = batters.merge(matches_bat, on="player")
    batters = batters.merge(balls, on="player")

    batters["strike_rate"] = batters.apply(
        lambda x: round((x["total_runs"] / x["balls_faced"]) * 100, 2) if x["balls_faced"] > 0 else 0,
        axis=1
    )

    # ================= BOWLERS =================
    deliveries["runs_conceded"] = deliveries["batsman_runs"] + deliveries["extra_runs"]

    matches_bowl = deliveries.groupby("bowler")["match_id"].nunique().reset_index()
    matches_bowl.rename(columns={"bowler": "player", "match_id": "matches"}, inplace=True)

    runs = deliveries.groupby("bowler")["runs_conceded"].sum().reset_index()
    runs.rename(columns={"bowler": "player"}, inplace=True)

    balls_bowled = deliveries.groupby("bowler").size().reset_index(name="balls_bowled")
    balls_bowled.rename(columns={"bowler": "player"}, inplace=True)

    wickets = deliveries[
        (deliveries["is_wicket"] == 1) &
        (deliveries["dismissal_kind"] != "run out")
    ].groupby("bowler").size().reset_index(name="wickets")
    wickets.rename(columns={"bowler": "player"}, inplace=True)

    bowlers = matches_bowl.merge(runs, on="player")
    bowlers = bowlers.merge(balls_bowled, on="player")
    bowlers = bowlers.merge(wickets, on="player")

    bowlers["economy"] = bowlers.apply(
        lambda x: round(x["runs_conceded"] / (x["balls_bowled"] / 6), 2) if x["balls_bowled"] > 0 else 0,
        axis=1
    )

    # ================= MODEL =================
    scaler_bat = StandardScaler()
    sim_bat = cosine_similarity(scaler_bat.fit_transform(
        batters[["total_runs", "matches", "balls_faced", "strike_rate"]]
    ))

    scaler_bowl = StandardScaler()
    sim_bowl = cosine_similarity(scaler_bowl.fit_transform(
        bowlers[["wickets", "runs_conceded", "balls_bowled", "economy", "matches"]]
    ))

    return batters, bowlers, sim_bat, sim_bowl