import streamlit as st
from train import load_and_prepare_data
from recommender import recommend_player
import pandas as pd

st.set_page_config(page_title="Cricket Recommender IPL", layout="wide")

# =============================
# LOAD DATA
# =============================
batters, bowlers, sim_bat, sim_bowl = load_and_prepare_data()

# =============================
# 🎨 UI STYLE
# =============================
st.markdown("""
<style>
.title {font-size:45px;font-weight:bold;text-align:center;color:#FFD700;}

.badge {
    display:inline-block;
    padding:6px 12px;
    border-radius:20px;
    font-size:14px;
    font-weight:bold;
}

.batter { background:#1f77b4; color:white; }
.bowler { background:#d62728; color:white; }
.allrounder { background:#2ca02c; color:white; }

.card {
    padding:20px;
    border-radius:12px;
    background:#111;
    margin-top:10px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🏏 Cricket Player Recommender IPL</div>', unsafe_allow_html=True)
st.markdown("---")

# =============================
# 🔍 SEARCH
# =============================
all_players = sorted(set(batters["player"]) | set(bowlers["player"]))

selected_player = st.selectbox(
    "🔍 Search Player",
    options=all_players,
    index=None,
    placeholder="Type player name..."
)

# =============================
# 📊 OUTPUT
# =============================
if selected_player is None:
    st.info("👆 Please search and select a player")

else:

    # =============================
    # ROLE DETECTION
    # =============================
    is_batter = selected_player in batters["player"].values
    is_bowler = selected_player in bowlers["player"].values

    if is_batter and is_bowler:
        role = "allrounder"
    elif is_bowler:
        role = "bowler"
    else:
        role = "batter"

    # =============================
    # 🎖 ROLE BADGE
    # =============================
    if role == "batter":
        badge_html = '<span class="badge batter">🏏 BATTER</span>'
    elif role == "bowler":
        badge_html = '<span class="badge bowler">🎯 BOWLER</span>'
    else:
        badge_html = '<span class="badge allrounder">🔥 ALL-ROUNDER</span>'

    st.markdown(f"## 🎯 Role: {badge_html}", unsafe_allow_html=True)

    # =============================
    # PLAYER STATS
    # =============================
    if role == "allrounder":

        b1 = batters[batters["player"] == selected_player].iloc[0]
        b2 = bowlers[bowlers["player"] == selected_player].iloc[0]

        st.markdown(f"""
        <div class="card">
        📅 Matches: {b1['matches']} <br><br>
        💯 Runs: {b1['total_runs']} <br>
        ⚡ Strike Rate: {b1['strike_rate']} <br><br>
        🧨 Wickets: {b2['wickets']} <br>
        🔥 Economy: {b2['economy']}
        </div>
        """, unsafe_allow_html=True)

    elif role == "batter":

        p = batters[batters["player"] == selected_player].iloc[0]

        st.markdown(f"""
        <div class="card">
        📅 Matches: {p['matches']} <br><br>
        💯 Runs: {p['total_runs']} <br>
        ⚡ Strike Rate: {p['strike_rate']}
        </div>
        """, unsafe_allow_html=True)

    else:

        p = bowlers[bowlers["player"] == selected_player].iloc[0]

        st.markdown(f"""
        <div class="card">
        📅 Matches: {p['matches']} <br><br>
        🧨 Wickets: {p['wickets']} <br>
        🔥 Economy: {p['economy']}
        </div>
        """, unsafe_allow_html=True)

    # =============================
    # 🔥 RECOMMENDATIONS WITH STATS
    # =============================
    players, rec_role = recommend_player(
        selected_player,
        batters,
        bowlers,
        sim_bat,
        sim_bowl
    )

    if players:

        st.markdown("### 🔥 Recommended Players (with Stats)")

        if rec_role == "batter":
            rec_df = batters[batters["player"].isin(players)].copy()
            rec_df = rec_df[["player", "matches", "total_runs", "strike_rate"]]

        elif rec_role == "bowler":
            rec_df = bowlers[bowlers["player"].isin(players)].copy()
            rec_df = rec_df[["player", "matches", "wickets", "economy"]]

        st.dataframe(rec_df, use_container_width=True)

    else:
        st.warning("No recommendations found")