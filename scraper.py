import requests
from lxml import html
import pandas as pd
import json
import math

# Go get the data
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

MIN_GAMES = 12

# season: In format "20XX-20XX"
# team: Team's name, capitalized. TODO: What is the format for teams with two words in the name?

def get_team_all_seasons(first_season: int, last_season: int, team: str, league: str):
    all_seasons = {}
    begin_season = first_season
    end_season = begin_season + 1
    while end_season <= last_season:
        season_string = str(begin_season) + "-" + str(end_season)
        all_seasons[season_string] = get_team_season(season_string, team, league)
        begin_season += 1
        end_season += 1 
    return all_seasons

SEASON_LENGTH = 34

"https://fbref.com/en/squads/822bd0ba/2023-2024/matchlogs/c9/shooting/Arsenal-Match-Logs-Premier-League"

TEAM_HASH_CODE = "add600ae"

LEAGUE_CODE = "c20"

def get_team_season(season: str, team: str, league: str):
    url = "https://fbref.com/en/squads/" + TEAM_HASH_CODE + "/" + season + "/matchlogs/" + LEAGUE_CODE + "/shooting/" + team + "-Match-Logs-" + league
    r = requests.get(url)
    this_team_dataframe = pd.read_html(r.content)[0]
    other_team_dataframe = pd.read_html(r.content)[1]
    this_team_data_points = (("For " + team, "Venue"), ("For " + team, "GF"), ("For " + team, "GA"), ("For " + team, "Opponent"), \
                          ("Expected", "xG"))
    other_team_data_point = ("Expected", "xG")
    team_season = []
    for i in range(SEASON_LENGTH):
        gameweek_row = []
        for item in this_team_data_points:
            gameweek_row.append(this_team_dataframe[item][i])
        gameweek_row.append(other_team_dataframe[other_team_data_point][i])
        team_season.append(gameweek_row)
    return team_season

# NOTE: This doesn't work unless Liverpool isn't in the premier league

def find_all_prem_teams(first_season: int, last_season: int):
    TEAM = "Dortmund"
    LEAGUE = "Bundesliga"
    all_seasons_in_timeframe = get_team_all_seasons(first_season, last_season, TEAM, LEAGUE)
    begin_season = first_season
    end_season = begin_season + 1
    all_prem_teams_ever = {}
    while end_season <= last_season:
        season_string = str(begin_season) + "-" + str(end_season)
        this_season = all_seasons_in_timeframe[season_string]
        all_teams = []
        for game in this_season:
            if game[3] not in all_teams:
                all_teams.append(game[3])
        all_teams.append(TEAM)
        all_prem_teams_ever[season_string] = all_teams
        begin_season += 1
        end_season += 1
    return all_prem_teams_ever

# English Premier League data: 2017-2024

def score_to_integers(score: str):
    print(score)
    split_score = score.split('–')
    print(split_score) 
    try:
        home_goals = int(split_score[0])
        away_goals = int(split_score[1])
        return [home_goals, away_goals]
    except:
        return [-1, -1]

# Takes in dataframe, returns (Home team, away team, home team goals, away team goals, home team xg, away team xg)
def parse_games(data: pd.DataFrame):
    all_data = []
    for row in data.index:
        home_team = data["Home"][row]
        if type(home_team) == float: # or math.isnan(data["Attendance"][row]):
            continue
        away_team = data["Away"][row]
        home_xg = data["xG"][row]
        away_xg = data["xG.1"][row]
        score = data["Score"][row]
        split_score = score_to_integers(score)
        home_goals = split_score[0]
        away_goals = split_score[1]
        all_data.append((home_team, away_team, home_xg, away_xg, home_goals, away_goals))
    return all_data

def get_season_data(start_year: str, end_year: str):
    r = requests.get("https://fbref.com/en/comps/13/" + start_year + "-" + end_year + "/schedule/" + start_year + "-" + end_year + "-Ligue-1-Scores-and-Fixtures")
    this_season_dataframe = pd.read_html(r.content)
    this_season_data = parse_games(this_season_dataframe[0])
    final_data = pd.DataFrame(this_season_data, columns=["Home Team", "Away Team", "Home XG", "Away XG", "Home Goals", "Away Goals"])
    csv_name = "ligue_1_" + start_year + "-" + end_year + "_all_games.csv"
    final_data.to_csv(csv_name, index=False)


if __name__ == "__main__":
    """
    items = find_all_prem_teams(2017, 2024)
    teams_by_season = json.dumps(items)
    LEAGUE = "bundesliga"
    with open("teams_by_season_" + LEAGUE + ".json", "w+") as outfile:
        outfile.write(teams_by_season)
    exit()
    """
    get_season_data("2023", "2024")
    #r = requests.get("https://fbref.com/en/comps/9/2023-2024/schedule/2023-2024-Premier-League-Scores-and-Fixtures")
    #this_season_dataframe = pd.read_html(r.content)
    #this_season_data = parse_games(this_season_dataframe[0])
    exit()
    this_team_dataframe = pd.read_html(r.content)[0]
    other_team_dataframe = pd.read_html(r.content)[1]
    list_of_team_games = []
    this_team_data_points = (("For Liverpool", "Venue"), ("For Liverpool", "GF"), ("For Liverpool", "GA"), ("For Liverpool", "Opponent"), \
                          ("Expected", "xG"))
    other_team_data_point = ("Expected", "xG")
    for i in range(len(this_team_dataframe)):
        current_dict = {}
        opp_row = opponent_rows[i]
        points = row.xpath('//td')#[@data-row= ' + current_str + ']')#/td[contains(@data-stat, "xg")]/text()')
        opponent_points = opp_row.xpath('//td')
        for point in points:
            stat_name = point.xpath("@data-stat")[0]
            if stat_name == "xg":
                current_dict["xg"] = point.text
            elif stat_name == "goals_for":
                current_dict["goals_for"] = point.text
            elif stat_name == "venue":
                current_dict["venue"] = point.text
        for opp_point in opponent_points:
            stat_name = opp_point.xpath("@data-stat")[0]
            if stat_name == "xg":
                current_dict["opponent_xg"] = point.text
            elif stat_name == "goals_for":
                current_dict["goals_against"] = point.text
        list_of_team_games.append(current_dict)
    print(list_of_team_games)

        #actual_goals_for = team_rows[i].xpath('/td[@data-stat="goals_for"]')
        #home = team_rows[i].xpath('/td[@data-stat="venue"]')
        #xg_against = opponent_rows[i].xpath('/td[@data-stat="xg"]')
        #actual_goals_against = opponent_rows[i].xpath('/td[@data-stat="xg"]')
        #list_of_games.append(xg_for)#''', xg_for, actual_goals_for, xg_against, actual_goals_against'''
