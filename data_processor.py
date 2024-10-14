import pandas as pd
import random
import numpy as np

# Stats needed:
# Average XG against for a given team
# Goalie's goals conceded vs XG as a measure of how good they are compared to average
# The above can be represented as a "save coefficient" (XG/Goals Conceded)
# Average XG for by a given team
# Percentage of progressive runs/carries and expected assists that are in the team
# Team's XG as well as the total "scoring coefficient" of the team 
# (the reciprocal of the "save coefficient"), calculated with only the players actually
# in the team
# Whether or not the team is playing at home

# Is Manchester City fucky because they have so many good players that they bench legitimately 
# important contributors?

"""
Step 1: For the first 12 weeks, give each team an average goals for, goals against, XG for, XG against.

Step 2: Sort every other game into 5 buckets randomly. Four of these buckets are for training, one is for testing.

Step 3: For these games, add the data and the score.
"""

TEAMS_GAMES_DICT = {} # This is in format "team: [avg goals for, avg xg for, avg goals against, avg xg against, games played]"

def recalculate_dict(team_name: str, season: pd.DataFrame, game_index: int):
    dictionary_entry = TEAMS_GAMES_DICT[team_name]
    games_played = dictionary_entry[4]
    goals_scored = dictionary_entry[0] * games_played
    total_xg = dictionary_entry[1] * games_played
    opponent_goals_scored = dictionary_entry[2] * games_played
    opponent_total_xg = dictionary_entry[3] * games_played
    if season["Home Team"][game_index] == team_name:
        goals_scored += season["Home Goals"][game_index]
        total_xg += season["Home XG"][game_index]
        opponent_goals_scored += season["Away Goals"][game_index]
        opponent_total_xg += season["Away XG"][game_index]
    else:
        goals_scored += season["Away Goals"][game_index]
        total_xg += season["Away XG"][game_index]
        opponent_goals_scored += season["Home Goals"][game_index]
        opponent_total_xg += season["Home XG"][game_index]
    games_played += 1
    TEAMS_GAMES_DICT[team_name] = [goals_scored / games_played,
                                   total_xg / games_played,
                                   opponent_goals_scored / games_played, 
                                   opponent_total_xg / games_played, 
                                   games_played]
    

def build_introduction_weeks(season: pd.DataFrame, index: int):
    home_team = season["Home Team"][index]
    away_team = season["Away Team"][index]
    if home_team not in TEAMS_GAMES_DICT.keys():
        TEAMS_GAMES_DICT[home_team] = [season["Home Goals"][index], season["Home XG"][index], season["Away Goals"][index], season["Away XG"][index], 1.0]
    else:
        recalculate_dict(home_team, season, index)
    if away_team not in TEAMS_GAMES_DICT.keys():
        TEAMS_GAMES_DICT[away_team] = [season["Away Goals"][index], season["Away XG"][index], season["Home Goals"][index], season["Home XG"][index], 1.0]
    else:
        recalculate_dict(away_team, season, index)


# The order the points are put in is:
# home team avg goals, home avg xg, home avg goals conceded, home avg xg conceded, away avg goals, away avg xg, away avg goals conceded, away avg xg conceded
# (Win loss or tie), Home Team Name, Away Team Name, Year

def build_data_points(season: pd.DataFrame, index: int, current_season: str):
    home_team = season["Home Team"][index]
    away_team = season["Away Team"][index]
    home_stats = TEAMS_GAMES_DICT[home_team]
    away_stats = TEAMS_GAMES_DICT[away_team]
    data_point = []
    for i in range(4):
        data_point.append(home_stats[i])
    for j in range(4):
        data_point.append(away_stats[j])
    home_goals = season["Home Goals"][index]
    away_goals = season["Away Goals"][index]
    if home_goals > away_goals:
        data_point.append("H")
    elif away_goals > home_goals:
        data_point.append("A")
    else:
        data_point.append("D")
    data_point.append(home_team)
    data_point.append(away_team)
    data_point.append(current_season)
    recalculate_dict(home_team, season, index)
    recalculate_dict(away_team, season, index)
    bucket_choice = str(random.randint(1, 5))
    TEST_FILE = "EPL_2023_TESTS.csv"
    this_bucket = open(TEST_FILE, "a")
    for x in data_point:
        this_bucket.write(str(x))
        this_bucket.write(",")
    this_bucket.write('\n')

TRAINING_WEEKS = 14
GAMES_PER_WEEK = 10 # Equal to (teams in league)/2

def process_data_table(folder_name: str, current_season: int):
    current_season_string = str(current_season) + "-" + str(current_season + 1)
    FILE_NAME = folder_name + current_season_string + "_all_games.csv"
    this_csv = pd.read_csv(FILE_NAME)
    for row in this_csv.index:
        if row <= TRAINING_WEEKS * GAMES_PER_WEEK:
            build_introduction_weeks(this_csv, row)
        else:
            build_data_points(this_csv, row, current_season_string)

#HG,HXG,HGC,HXGC,AG,AXG,AGC,AXGC,outcome,hometeam,awayteam,season,empty

if __name__ == "__main__":
    FOLDER_STRING = "Premier League Seasons\\epl_"
    for i in range(2023, 2023):
        process_data_table(FOLDER_STRING, i)
        TEAMS_GAMES_DICT = {}
