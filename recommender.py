# recommender.py

def recommend_player(player_name, batters, bowlers, sim_bat, sim_bowl, top_n=5):

    if player_name in bowlers["player"].values:
        idx = bowlers[bowlers["player"] == player_name].index[0]
        scores = list(enumerate(sim_bowl[idx]))
        scores = sorted(scores, key=lambda x: x[1], reverse=True)[1:top_n+1]
        return [bowlers.iloc[i[0]]["player"] for i in scores], "bowler"

    elif player_name in batters["player"].values:
        idx = batters[batters["player"] == player_name].index[0]
        scores = list(enumerate(sim_bat[idx]))
        scores = sorted(scores, key=lambda x: x[1], reverse=True)[1:top_n+1]
        return [batters.iloc[i[0]]["player"] for i in scores], "batter"

    return [], None