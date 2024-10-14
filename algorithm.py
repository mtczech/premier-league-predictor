import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
import math

def split_x_and_y_and_metadata(paths: list[str]):
    initial_input = None
    initial_results = None
    for path in paths:
        pandas_array = pd.read_csv(path, encoding='latin-1')
        input = pandas_array[["HG","HXG","HGC",'HXGC',"AG",'AXG',"AGC",'AXGC']].to_numpy()
        results = pandas_array[["outcome"]].to_numpy()
        metadata = pandas_array[["hometeam","awayteam","season"]].to_numpy()
        if initial_input is None:
            initial_input = input
            initial_results = results
        else:
            initial_input = np.vstack((initial_input, input))
            initial_results = np.vstack((initial_results, results))
    return initial_input, initial_results, metadata

def translate_inputs_and_outputs(np_array: np.array, outcomes: list[str]):
    training_inputs = []
    outcomes_list = []
    for i in range(len(np_array)):
        row = np_array[i]
        if any(np.isnan(row)):
            continue
        new_row = []
        for item in row:
            new_row.append(item.item())
        training_inputs.append(new_row)
        letter = outcomes[i]
        if letter == "H":
            outcomes_list.append(1)
        elif letter == "D":
            outcomes_list.append(0)
        else:
            outcomes_list.append(-1)
    return training_inputs, outcomes_list

def codes_to_numeric(outcomes):
    outcomes_list = []
    for outcome in outcomes:
        letter = outcome[0]
        if letter == "H":
            outcomes_list.append(1)
        elif letter == "D":
            outcomes_list.append(0)
        else:
            outcomes_list.append(-1)
    return outcomes_list

def is_worth_bet(percent_chance: float, odds: int):
    if odds > 0:
        worth_it_threshold = float(100/(odds + 100))
    else:
        placeholder = (-1 * odds)
        worth_it_threshold = float((placeholder + 100)/placeholder)
    if (worth_it_threshold * 1.05) < percent_chance:
        return True
    return False

if __name__ == "__main__":
    lines = [-278,503,665]
    chances = [0.59686299, 0.24642968, 0.15670734]
    for i in range(len(lines)):
        if is_worth_bet(chances[i], lines[i]):
            if i == 0:
                print("Bet on away team")
            elif i == 1:
                print("Bet on tie")
            elif i == 2:
                print("Bet on home team")
    exit()
    train_x, train_y, train_metadata = split_x_and_y_and_metadata(["bucket_2.csv", "bucket_3.csv", "bucket_4.csv", "bucket_5.csv"])
    test_x, test_y, test_metadata = split_x_and_y_and_metadata(["bucket_1.csv"])
    epl_x, epl_y, epl_metadata = split_x_and_y_and_metadata(['EPL_2023_TESTS.csv'])
    logisticRegr = LogisticRegression(penalty="l1", solver="saga")
    train_x, train_y = translate_inputs_and_outputs(train_x, train_y)
    test_x, test_y = translate_inputs_and_outputs(test_x, test_y)
    # 1 = home win, 0 = draw, -1 = away win
    trained = logisticRegr.fit(train_x, train_y)
    predictions = logisticRegr.predict_proba(epl_x)
    for i in range(219, 239):
        print(predictions[i], epl_metadata[i])

"""
Best predictions-last gameweek:
Arsenal vs Everton: Tie (-10)
Brentford vs Newcastle: None really worth it
Brighton vs Man United: Brighton (-10)
Burnley vs Forest: None really worth it
Chelsea vs Bournemouth: Bournemouth (-10)
Wolves vs Liverpool: Liverpool to not win (-10)
Fulham vs Luton: None really worth it
West Ham vs City: West Ham (-10)
Sheffield vs Tottenham: Tie (-10)
----------------------------------------
Burnley vs Tottenham: Miss (-10)
Sheffield vs Everton: None really worth it
Brighton vs Newcastle: Brighton (-10)
Brentford vs Bournemouth: Brentford (hit), (+22.70)
Chelsea vs Forest: Tie (-10)
Arsenal vs United: Against Arsenal (-10)
Villa vs Liverpool: None really worth it
City vs Spurs: Against City (-10)
Brighton vsd Chelsea: Tie (-10)
United vs Newcastle: None really worth it
"""

"""
[0.12524434 0.17805816 0.69669749] ['Tottenham' 'Burnley' '2023-2024'] Tie (-10)
[0.1094015  0.20435207 0.68624643] ['Everton' 'Sheffield Utd' '2023-2024'] None worth it
[0.22569224 0.18757011 0.58673764] ['Newcastle Utd' 'Brighton' '2023-2024'] Brighton (-10)
[0.34639913 0.25106848 0.40253239] ['Bournemouth' 'Brentford' '2023-2024'] Brentford (+22.70)
[0.48271352 0.2684045  0.24888198] ["Nott'ham Forest" 'Chelsea' '2023-2024'] Tie (-10)
[0.67668586 0.17451497 0.14879917] ['Manchester Utd' 'Arsenal' '2023-2024'] Arsenal to not win (-10)
[0.55232515 0.21831542 0.22935943] ['Aston Villa' 'Liverpool' '2023-2024'] None worth it 
[0.61322814 0.18356818 0.20320368] ['Tottenham' 'Manchester City' '2023-2024'] City to not win (-10)
[0.43453955 0.25471756 0.3107429 ] ['Brighton' 'Chelsea' '2023-2024'] None worth it
[0.43719369 0.24637761 0.3164287 ] ['Manchester Utd' 'Newcastle Utd' '2023-2024'] None worth it
[0.40900191 0.27758904 0.31340905] ['Luton Town' 'Fulham' '2023-2024'] Tie (-10)
[0.59686299 0.24642968 0.15670734] ['Sheffield Utd' 'Tottenham' '2023-2024'] Spurs to not win (-10)
[0.0671586 0.1338813 0.7989601] ['Manchester City' 'West Ham' '2023-2024']
[0.09997859 0.17033283 0.72968858] ['Arsenal' 'Everton' '2023-2024']
[0.24262546 0.25695833 0.5004162 ] ['Brighton' 'Manchester Utd' '2023-2024']
[0.40769695 0.25452132 0.33778173] ['Brentford' 'Newcastle Utd' '2023-2024']
[0.19737481 0.18265275 0.61997245] ['Chelsea' 'Bournemouth' '2023-2024']
[0.39378826 0.28221301 0.32399873] ['Crystal Palace' 'Aston Villa' '2023-2024']
[0.07429514 0.12137158 0.80433328] ['Liverpool' 'Wolves' '2023-2024']
[0.42198097 0.27488431 0.30313472] ['Burnley' "Nott'ham Forest" '2023-2024']
"""