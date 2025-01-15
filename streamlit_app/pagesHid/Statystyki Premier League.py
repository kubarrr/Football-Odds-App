import streamlit as st
import numpy as np
import pandas as pd
import runpy
import random
from mplsoccer import Pitch
import matplotlib.pyplot as plt


def navbar():
    cols = st.columns(6)
    with cols[0]:
        if st.button(
            "Strona Główna",
            key=f"HomeSPL"
        ):
            st.switch_page("Kursomat.py")
    with cols[1]:
        if st.button(
            "Premier League",
            key=f"PremierLeagueSPL"
        ):
            st.switch_page("pagesVis/Premier League.py")
    with cols[2]:
        st.write("Serie A")
    with cols[3]:
        st.write("Ligue1")
    with cols[4]:
        st.write("Bundesliga")
    with cols[5]:
        st.write("Ligue 1")

navbar()


def create_team_structure(idx, formation, starting_eleven):
    
    formation_parts = list(map(int, formation.split('-')))
    used_players = set()
    starting_eleven["main_pos"] = starting_eleven["position_x"].apply(lambda x: x.split(",")[0])
    starting_eleven["number_of_positions"] = starting_eleven["position_x"].apply(lambda x: len(x.split(",")))
    formation_array = [[starting_eleven[starting_eleven["main_pos"] == "GK"].iloc[0]["player"]]]
    
    for parts in formation_parts:
        formation_array.append(parts * [None])

    used_players.add(formation_array[0][0])
    
    # Central Backs
    cbs = starting_eleven[starting_eleven["main_pos"] == "CB"]
    cbs2 = starting_eleven[(starting_eleven["main_pos"] == "CB") & (starting_eleven["number_of_positions"] == 1)]
    cbs3 = starting_eleven[starting_eleven["position_x"].str.contains("CB")]
    if formation_parts[0] == 3:
        if len(cbs) == 3:
            formation_array[1][0] = cbs.iloc[0]["player"]
            formation_array[1][1] = cbs.iloc[1]["player"]
            formation_array[1][2] = cbs.iloc[2]["player"]
        elif len(cbs2) == 3:
            formation_array[1][0] = cbs2.iloc[0]["player"]
            formation_array[1][1] = cbs2.iloc[1]["player"]
            formation_array[1][2] = cbs2.iloc[2]["player"]
        elif len(cbs3) == 3:
            formation_array[1][0] = cbs3.iloc[0]["player"]
            formation_array[1][1] = cbs3.iloc[1]["player"]
            formation_array[1][2] = cbs3.iloc[2]["player"]
        used_players.add(formation_array[1][0])
        used_players.add(formation_array[1][1])
        used_players.add(formation_array[1][2])
    elif formation_parts[0] == 5:
        if len(cbs) == 3:
            formation_array[1][1] = cbs.iloc[0]["player"]
            formation_array[1][2] = cbs.iloc[1]["player"]
            formation_array[1][3] = cbs.iloc[2]["player"]
        elif len(cbs2) == 3:
            formation_array[1][1] = cbs2.iloc[0]["player"]
            formation_array[1][2] = cbs2.iloc[1]["player"]
            formation_array[1][3] = cbs2.iloc[2]["player"]
        elif len(cbs3) == 3:
            formation_array[1][1] = cbs3.iloc[0]["player"]
            formation_array[1][2] = cbs3.iloc[1]["player"]
            formation_array[1][3] = cbs3.iloc[2]["player"]
        used_players.add(formation_array[1][1])
        used_players.add(formation_array[1][2])
        used_players.add(formation_array[1][3])
    else:
        if len(cbs) == 2:
            formation_array[1][1] = cbs.iloc[0]["player"]
            formation_array[1][2] = cbs.iloc[1]["player"]
        elif len(cbs2) == 2:
            formation_array[1][1] = cbs2.iloc[0]["player"]
            formation_array[1][2] = cbs2.iloc[1]["player"]
        elif len(cbs3) == 2:
            formation_array[1][1] = cbs3.iloc[0]["player"]
            formation_array[1][2] = cbs3.iloc[1]["player"]
        used_players.add(formation_array[1][1])
        used_players.add(formation_array[1][2])

    # Left/Right backs for 4 defenders formation
    lbs = starting_eleven[starting_eleven["main_pos"] == "LB"]
    lbs2 = starting_eleven[(starting_eleven["main_pos"] == "LB") & (starting_eleven["number_of_positions"] == 1)]
    lbs3 = starting_eleven[starting_eleven["position_x"].str.contains("LB")]
    rbs = starting_eleven[starting_eleven["main_pos"] == "RB"]
    rbs2 = starting_eleven[(starting_eleven["main_pos"] == "RB") & (starting_eleven["number_of_positions"] == 1)]
    rbs3 = starting_eleven[starting_eleven["position_x"].str.contains("RB")]

    if formation_parts[0] == 4:
        if len(lbs) == 1:
            formation_array[1][0] = lbs.iloc[0]["player"]
        elif len(lbs2) == 1:
            formation_array[1][0] = lbs2.iloc[0]["player"]
        elif len(lbs3) == 1:
            formation_array[1][0] = lbs3.iloc[0]["player"]
        elif len(lbs3) > 1:
            min_place = 100
            name = "none"
            for indx, player in lbs3.iterrows():
                place = player["position_x"].split(",").index("LB")
                if place < min_place:
                    min_place = place
                    name = player["player"]
            formation_array[1][0] = name
        used_players.add(formation_array[1][0])

        if len(rbs) == 1:
            formation_array[1][3] = rbs.iloc[0]["player"]
        elif len(rbs2) == 1:
            formation_array[1][3] = rbs2.iloc[0]["player"]
        elif len(rbs3) == 1:
            formation_array[1][3] = rbs3.iloc[0]["player"]
        elif len(rbs3) > 1:
            min_place = 100
            name = "none"
            for indx, player in rbs3.iterrows():
                place = player["position_x"].split(",").index("RB")
                if place < min_place:
                    min_place = place
                    name = player["player"]
            formation_array[1][3] = name
        used_players.add(formation_array[1][3])

    elif formation_parts[0] == 5:
        if len(lbs) == 1:
            formation_array[1][0] = lbs.iloc[0]["player"]
        elif len(lbs2) == 1:
            formation_array[1][0] = lbs2.iloc[0]["player"]
        elif len(lbs3) == 1:
            formation_array[1][0] = lbs3.iloc[0]["player"]
        elif len(lbs3) > 1:
            min_place = 100
            name = "none"
            for indx, player in lbs3.iterrows():
                place = player["position_x"].split(",").index("LB")
                if place < min_place:
                    min_place = place
                    name = player["player"]
            formation_array[1][0] = name
        used_players.add(formation_array[1][0])

        if len(rbs) == 1:
            formation_array[1][4] = rbs.iloc[0]["player"]
        elif len(rbs2) == 1:
            formation_array[1][4] = rbs2.iloc[0]["player"]
        elif len(rbs3) == 1:
            formation_array[1][4] = rbs3.iloc[0]["player"]
        elif len(rbs3) > 1:
            min_place = 100
            name = "none"
            for indx, player in rbs3.iterrows():
                place = player["position_x"].split(",").index("RB")
                if place < min_place:
                    min_place = place
                    name = player["player"]
            formation_array[1][4] = name
        used_players.add(formation_array[1][4])

    # Wingers in formation with 3 defenders

    # Forwards
    fws = starting_eleven[starting_eleven["main_pos"] == "FW"]
    fws2 = starting_eleven[(starting_eleven["main_pos"] == "FW") & (starting_eleven["number_of_positions"] == 1)]
    fws3 = starting_eleven[starting_eleven["position_x"].str.contains("FW")]

    if formation_parts[-1] == 2:
        if len(fws) == 2:
            formation_array[-1][0] = fws.iloc[0]["player"]
            formation_array[-1][1] = fws.iloc[1]["player"]
        elif len(fws2) == 2:
            formation_array[-1][0] = fws2.iloc[0]["player"]
            formation_array[-1][1] = fws2.iloc[1]["player"]
        elif len(fws3) == 2:
            formation_array[-1][0] = fws3.iloc[0]["player"]
            formation_array[-1][1] = fws3.iloc[1]["player"]
        elif len(fws3) > 2:
            min_place1 = 100
            min_place2 = 100
            name1 = "none"
            name2 = "none"
            for indx, player in fws3.iterrows():
                place = player["position_x"].split(",").index("FW")
                if place < min_place1:
                    min_place2 = min_place1
                    min_place1 = place
                    name1 = player["player"]
                    name2 = name1
                elif place < min_place2:
                    min_place2 = place
                    name2 = player["player"]
            formation_array[-1][0] = name1
            formation_array[-1][1] = name2
        used_players.add(formation_array[-1][0])
        used_players.add(formation_array[-1][1])

    elif formation_parts[-1] == 1:
        if len(fws) == 1:
            formation_array[-1][0] = fws.iloc[0]["player"]
        elif len(fws2) == 1:
            formation_array[-1][0] = fws2.iloc[0]["player"]
        elif len(fws3) == 1:
            formation_array[-1][0] = fws3.iloc[0]["player"]
        elif len(fws3) > 1:
            min_place = 100
            name = "none"
            for indx, player in fws3.iterrows():
                place = player["position_x"].split(",").index("FW")
                if place < min_place:
                    min_place = place
                    name = player["player"]
            formation_array[-1][0] = name
        used_players.add(formation_array[-1][0])

    elif formation_parts[-1] == 3:
        if len(fws) == 1:
            formation_array[-1][1] = fws.iloc[0]["player"]
        elif len(fws2) == 1:
            formation_array[-1][1] = fws2.iloc[0]["player"]
        elif len(fws3) == 1:
            formation_array[-1][1] = fws3.iloc[0]["player"]
        elif len(fws3) > 1:
            min_place = 100
            name = "none"
            for indx, player in fws3.iterrows():
                place = player["position_x"].split(",").index("FW")
                if place < min_place:
                    min_place = place
                    name = player["player"]
            formation_array[-1][1] = name
        used_players.add(formation_array[-1][1])


    # add the rest randomly
    all_players = starting_eleven['player'].tolist()
    unassigned_players = list(set(all_players) - used_players)
    for arr in formation_array:
        for i, el in enumerate(arr):
            if el is None and unassigned_players:
                arr[i] = random.choice(unassigned_players)
                unassigned_players.remove(arr[i])


    return formation_array

def get_starters(group):
    starters = []
    group = group.sort_index()
    used_indices = set()
    for idx, row in group.iterrows():
        if idx in used_indices:
            continue

        if row['minutes'] == 90:
            starters.append(group.index.get_loc(idx))
            used_indices.add(idx)
        elif row['minutes'] < 90:
            starters.append(group.index.get_loc(idx))
            used_indices.add(idx)
            minutes_sum = row['minutes']
            next_row = row
            next_idx_global = idx
            while minutes_sum < 90 and next_row['cards_red'] < 1:
                next_idx = group.index.get_loc(next_idx_global) + 1
                next_idx_global = next_idx_global + 1
                if next_idx < len(group):
                    next_row = group.iloc[next_idx]
                    minutes_sum += next_row['minutes']
                    if minutes_sum > 91:
                        starters.append(next_idx)
                    used_indices.add(next_idx_global)
                else:
                    minutes_sum = 90
                    
    group = group.iloc[starters]
    return group


def load_data():
    players = st.session_state["playersPL"].copy()
    matches = st.session_state["dfPL"].copy()
    odds = st.session_state["oddsPL"].copy()
    return players, matches, odds

players, matches, odds = load_data()
matches2 = matches.copy()

team_name_mapping = {
    'Burnley': 'Burnley',
    'Arsenal': 'Arsenal',
    'Bournemouth': 'Bournemouth',
    'Brighton': 'Brighton & Hove Albion',
    'Everton': 'Everton',
    'Sheffield United': 'Sheffield United',
    'Newcastle': 'Newcastle United',
    'Brentford': 'Brentford',
    'Chelsea': 'Chelsea',
    'Man United': 'Manchester United',
    "Nott'm Forest": 'Nottingham Forest',
    'Fulham': 'Fulham',
    'Liverpool': 'Liverpool',
    'Wolves': 'Wolverhampton Wanderers',
    'Tottenham': 'Tottenham Hotspur',
    'Man City': 'Manchester City',
    'Aston Villa': 'Aston Villa',
    'West Ham': 'West Ham United',
    'Crystal Palace': 'Crystal Palace',
    'Luton': 'Luton Town',
    'Leeds': 'Leeds United',
    'Leicester': 'Leicester City',
    'Southampton': 'Southampton',
    'Watford': 'Watford',
    'Norwich': 'Norwich City',
    'West Brom': 'West Bromwich Albion',
    'Huddersfield': 'Huddersfield Town',
    'Cardiff': 'Cardiff City'
}

odds['HomeTeam'] = odds['HomeTeam'].map(team_name_mapping)
odds['AwayTeam'] = odds['AwayTeam'].map(team_name_mapping)

odds['Date'] = pd.to_datetime(odds['Date'], format='%d/%m/%Y')
matches['date'] = pd.to_datetime(matches['date'])
odds = odds[["Date", "HomeTeam", "AwayTeam", "B365H", "B365D", "B365A"]]
odds.rename(columns={
    'HomeTeam': 'home_team',
    'AwayTeam': 'away_team'
}, inplace=True)

merged_df = pd.merge(
    matches,
    odds,
    how='inner',
    left_on=['home_team', 'away_team', 'date'],
    right_on=['home_team', 'away_team', 'Date']
)
merged_df.drop(columns=['Date'], inplace=True)
merged_df["B365probsH"] = 1 / merged_df["B365H"] / (1 / merged_df["B365H"] + 1 / merged_df["B365D"] + 1 / merged_df["B365A"])
merged_df["B365probsD"] = 1 / merged_df["B365D"] / (1 / merged_df["B365H"] + 1 / merged_df["B365D"] + 1 / merged_df["B365A"])
merged_df["B365probsA"] = 1 / merged_df["B365A"] / (1 / merged_df["B365H"] + 1 / merged_df["B365D"] + 1 / merged_df["B365A"])


date = st.session_state['stats_id']["date"]
home_team = st.session_state['stats_id']["home_team"]
away_team = st.session_state['stats_id']["away_team"]

home_goals = st.session_state['stats_id']["home_goals"]
away_goals = st.session_state['stats_id']["away_goals"]

formation_home = st.session_state['stats_id']["formation_home"]
formation_away = st.session_state['stats_id']["formation_away"]

home_team_players = players[(players["date"]==date) & (players["team"]==home_team)]
away_team_players = players[(players["date"]==date) & (players["team"]==away_team)]

structure_away = create_team_structure(0, formation_away, get_starters(players[(players["team"] == away_team) & (players["date"] == date)]))
structure_home = create_team_structure(0, formation_home, get_starters(players[(players["team"] == home_team) & (players["date"] == date)]))


width = 100
pitch = Pitch(pitch_color='grass', line_color='white', stripe=False)
fig, ax = pitch.draw(figsize=(16, 8))

width = 120
height = 80
size = 36*36
y_shift_length = 15

color1 = '#2b83ba'
color2 = '#d7191c'

formation_3_x = [6, 24, 37, 50]
formation_4_x = [6, 21, 32, 43, 54]

formation_3_y = [0, 18, 18, 12]
formation_4_y = [0, 18, 18, 18, 12]


if len(structure_home) == 4:
    formation_x = formation_3_x
    formation_y = formation_3_y
else:
    formation_x = formation_4_x
    formation_y = formation_4_y
for i in range(len(structure_home)):
    arr = structure_home[i]
    y_shift_length = formation_y[i]
    y_start = 40 - (len(arr) - 1) * y_shift_length / 2
    for j in range(len(arr)):
        ax.scatter(formation_x[i], y_start + y_shift_length*j, c=color1, s=size, edgecolors='black', label='Team A')
        ax.text(formation_x[i], y_start + y_shift_length*j + 5.5, arr[j].split()[-1], horizontalalignment='center', fontsize = 13)

if len(structure_away) == 4:
    formation_x = formation_3_x
    formation_y = formation_3_y
else:
    formation_x = formation_4_x
    formation_y = formation_4_y
for i in range(len(structure_away)):
    arr = structure_away[i]
    y_shift_length = formation_y[i]
    if i == len(structure_away) - 1 and len(arr) > 2:
        y_shift_length = 28
    y_start = 40 - (len(arr) - 1) * y_shift_length / 2
    for j in range(len(arr)):
        ax.scatter(width - formation_x[i], y_start + y_shift_length*j, c=color2, s=size, edgecolors='black', label='Team A')
        ax.text(width - formation_x[i], y_start + y_shift_length*j + 5.5, arr[j].split()[-1], horizontalalignment='center', fontsize = 13)

plt.show()

st.markdown(f"""
                <p style='text-align: center; font-size: 40px;'>{home_team}  {home_goals} - {away_goals}  {away_team}</p>
                """, unsafe_allow_html=True)


categories = ['Home Win', 'Draw', 'Away Win']
probabilities = [merged_df[(merged_df["date"]==date) & (merged_df["home_team"] == home_team)]["B365probsH"], merged_df[(merged_df["date"]==date) & (merged_df["home_team"] == home_team)]["B365probsD"], merged_df[(merged_df["date"]==date) & (merged_df["home_team"] == home_team)]["B365probsA"]]
colors = ['green', 'gray', 'blue']

fig2, ax = plt.subplots(figsize=(6, 1))
start = 0

for prob, color in zip(probabilities, colors):
    ax.barh(0, prob, left=start, color=color, edgecolor='none', height=0.5)
    start += prob

start = 0
for prob, color in zip(probabilities, colors):
    ax.text(start + prob / 2, 0, f"{int(prob * 100)}%", color='black', va='center', ha='center', fontsize=10)
    start += prob

ax.set_xlim(0, 1)
ax.axis('off')  # Turn off the axis
plt.title('Prawdopodbieństwo zdarzeń', pad=10)
plt.show()
plt.tight_layout()

col2, col3 = st.columns(2)


home_matches = matches[(matches["date"] < date) &
    ((matches["home_team"] == home_team) | (matches["away_team"] == home_team)) ]
away_matches = matches[(matches["date"] < date) &
    ((matches["home_team"] == away_team) | (matches["away_team"] == away_team)) ]
home_matches = home_matches[["date", "time", "home_team", "home_goals", "away_goals", "away_team"]]
home_matches = home_matches.sort_values(by="date", ascending=False)
away_matches = away_matches[["date", "time", "home_team", "home_goals", "away_goals", "away_team"]]
away_matches = away_matches.sort_values(by="date", ascending=False)
with col2:
    data = f"""
                <div style="text-align: center; font-size: 15px;
                    background-color: #f8f9fa; 
                    border-radius: 10px; 
                    padding: 5px; 
                    margin: 5px;
                    box-shadow: 4px 4px 8px rgba(0.2, 0.2, 0.2, 0.2);">
                <div style="display: flex; justify-content: center; margin-bottom: 5px; font-size: 25px; font-weight:bold;">Ostatnie mecze {home_team}</div>
                """
    
    if len(home_matches) == 0:
        data += "<div style='font-size: 20px;'>Brak danych na temat ostatnich meczów</div>"

    for j in range(min(5, len(home_matches))):
        data += f"""
        <div style="display: flex; justify-content: center; margin-bottom: 5px;">
            <div style="width: 120px;">{home_matches.iloc[j]['date'].date()} {home_matches.iloc[j]['time']}</div>
            <div style="width: 200px;">{home_matches.iloc[j]['home_team']}</div>
            <div style="width: 100px;">{home_matches.iloc[j]['home_goals']} - {home_matches.iloc[j]['away_goals']}</div>
            <div style="width: 200px;">{home_matches.iloc[j]['away_team']}</div>
        """
        if home_matches.iloc[j]['home_team'] == home_team:
            if home_matches.iloc[j]['home_goals'] > home_matches.iloc[j]['away_goals']:
                data += "<div style='width: 50px; background-color: green;'>W</div>"
            elif home_matches.iloc[j]['home_goals'] < home_matches.iloc[j]['away_goals']:
                data += "<div style='width: 50px; background-color: red;'>L</div>"
            else:
                data += "<div style='width: 50px; background-color: gray;'>D</div>"
        else:
            if home_matches.iloc[j]['home_goals'] > home_matches.iloc[j]['away_goals']:
                data += "<div style='width: 50px; background-color: red;'>L</div>"
            elif home_matches.iloc[j]['home_goals'] < home_matches.iloc[j]['away_goals']:
                data += "<div style='width: 50px; background-color: green;'>W</div>"
            else:
                data += "<div style='width: 50px; background-color: gray;'>D</div>"
        data+="</div>"
    data += "</div>"
    st.markdown(data, unsafe_allow_html=True)
    st.pyplot(fig2)
    st.write(fig)

with col3:
    data = f"""
                <div style="text-align: center; font-size: 15px;
                    background-color: #f8f9fa; 
                    border-radius: 10px; 
                    padding: 5px; 
                    margin: 5px;
                    box-shadow: 4px 4px 8px rgba(0.2, 0.2, 0.2, 0.2);">
                <div style="display: flex; justify-content: center; margin-bottom: 5px; font-size: 25px; font-weight:bold;">Ostatnie mecze {away_team}</div>
                """
    
    if len(away_matches) == 0:
        data += "<div style='font-size: 20px;'>Brak danych na temat ostatnich meczów</div>"

    for j in range(min(5, len(away_matches))):
        data += f"""
        <div style="display: flex; justify-content: center; margin-bottom: 5px;">
            <div style="width: 120px;">{away_matches.iloc[j]['date'].date()} {away_matches.iloc[j]['time']}</div>
            <div style="width: 200px;">{away_matches.iloc[j]['home_team']}</div>
            <div style="width: 100px;">{away_matches.iloc[j]['home_goals']} - {away_matches.iloc[j]['away_goals']}</div>
            <div style="width: 200px;">{away_matches.iloc[j]['away_team']}</div>
        """
        if away_matches.iloc[j]['home_team'] == home_team:
            if away_matches.iloc[j]['home_goals'] > away_matches.iloc[j]['away_goals']:
                data += "<div style='width: 50px; background-color: green;'>W</div>"
            elif away_matches.iloc[j]['home_goals'] < away_matches.iloc[j]['away_goals']:
                data += "<div style='width: 50px; background-color: red;'>L</div>"
            else:
                data += "<div style='width: 50px; background-color: gray;'>D</div>"
        else:
            if away_matches.iloc[j]['home_goals'] > away_matches.iloc[j]['away_goals']:
                data += "<div style='width: 50px; background-color: red;'>L</div>"
            elif away_matches.iloc[j]['home_goals'] < away_matches.iloc[j]['away_goals']:
                data += "<div style='width: 50px; background-color: green;'>W</div>"
            else:
                data += "<div style='width: 50px; background-color: gray;'>D</div>"
        data+="</div>"
    data += "</div>"
    st.markdown(data, unsafe_allow_html=True)
    filtr1, filtr2 = st.columns(2)

    css = """
    .st-key-team_filter *, .st-key-stat_filter *, .st-key-team_filter, .st-key-stat_filter{
                cursor: pointer;
            }
    """

    st.html(f"<style>{css}</style>")

    with filtr1:
        team_filter = st.selectbox("Wybierz drużynę", options=[home_team, away_team], key="team_filter")
    with filtr2:
        stat_filter = st.selectbox("Wybierz statystykę", options=["goals", "corner_kicks"], key="stat_filter")

    def select_last_matches(df, team, date, n, where="all"):
        if where == "home":
            team_matches = df[(df["home_team"] == team) & (df["date"]<date)]
        elif where == "away":
            team_matches = df[(df["away_team"] == team) & (df["date"]<date)]
        else:
            team_matches = df[((df["home_team"] == team) | (df["away_team"] == team)) & (df["date"]<date)]
        team_matches_sorted = team_matches.sort_values(by="date", ascending=False)
        return team_matches_sorted.head(n)

    def get_stat(df, team, stat):
        df[stat] = df.apply(lambda x: x["home_" + stat] if x["home_team"] == team else x["away_" + stat], axis=1)
        df["new_date"] = df["date"].apply(lambda x: str(x)[5:7]+"."+str(x)[8:10])
        return df[[stat, "new_date"]]

    team = team_filter
    stat = stat_filter
    n = 10
    last_matches = select_last_matches(matches, team, date, n)
    stat_df = get_stat(last_matches, team, stat)
    threshold = 1.5

    # Set colors: green if above threshold, red otherwise
    colors = ["green" if val > threshold else "red" for val in stat_df[stat]]

    # Plot the bar chart
    fig3 = plt.figure(figsize=(10, 6))
    bars = plt.bar(stat_df["new_date"], stat_df[stat], color=colors)

    # Add threshold line
    plt.axhline(y=threshold, color="gray", linestyle="--", label=f"Linia = {threshold}")

    # Add value labels on top of bars
    for bar in bars:
        height = bar.get_height()
        if height == 0:
            plt.text(bar.get_x() + bar.get_width() / 2, height, str(height),
                ha="center", va="bottom", fontsize=20)
        else:
            plt.text(bar.get_x() + bar.get_width() / 2, height-0.4, str(height),
                ha="center", va="bottom", fontsize=20)

    # Chart styling
    plt.title(stat.capitalize() + " dla " + team + " w ostatnich " + str(n) + " meczach")
    plt.xlabel("Mecze")
    plt.ylabel(stat)
    plt.legend()
    plt.tight_layout()

    # Show plot
    plt.show()
    st.write(fig3)

    h2h = matches2[((matches2["home_team"] == home_team) & (matches2["away_team"] == away_team)) |
            ((matches2["home_team"] == away_team) & (matches2["away_team"] == home_team))]
    h2h = h2h[["date", "time", "home_team", "home_goals", "away_goals", "away_team"]]
    h2h = h2h.sort_values(by="date", ascending=False)
    data = """
                <div style="text-align: center; font-size: 15px;
                    border-radius: 10px; 
                    padding: 5px; 
                    margin: 5px;
                    box-shadow: 4px 4px 8px rgba(0.2, 0.2, 0.2, 0.2);">
                <div style="display: flex; justify-content: center; margin-bottom: 5px; font-size: 25px; font-weight:bold;">Ostatnie mecze pomiędzy drużynami</div>
                """
    
    if len(h2h) == 0:
        data += "<div style='font-size: 20px;'>Brak danych na temat meczów pomiędzy drużynami</div>"
    for j in range(len(h2h)):
        if h2h.iloc[j]['date'] == date:
            data += """<div style="display: flex; justify-content: center; margin-bottom: 5px; font-size: 15px; background-color:Aqua;">"""
        else:
            data += """<div style="display: flex; justify-content: center; margin-bottom: 5px;">"""
        data += f"""
            <div style="width: 120px;">{h2h.iloc[j]['date']} {h2h.iloc[j]['time']}</div>
            <div style="width: 200px;">{h2h.iloc[j]['home_team']}</div>
            <div style="width: 100px;">{h2h.iloc[j]['home_goals']} - {h2h.iloc[j]['away_goals']}</div>
            <div style="width: 200px;">{h2h.iloc[j]['away_team']}</div>
        </div>
        """
    data += "</div>"
    st.markdown(data, unsafe_allow_html=True)