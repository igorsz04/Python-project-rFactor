# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 00:04:56 2023

@author: igors
"""

import pandas as pd
import numpy as np
import os
import re
import random
import shutil
from rfactor_functions import season
from rfactor_data_classes import team_info_pd
from rfactor_functions import statistics_folder
from rfactor_functions import riders_table
from rfactor_functions import team_table
from rfactor_functions import yourname
from rfactor_functions import team_files_path
from rfactor_machine_learning import sc
from rfactor_machine_learning import perceptron
from rfactor_machine_learning import scaler
from rfactor_machine_learning import lr
from rfactor_data_classes import overalls



"""
Loading old teams table from previous season (if first season, load table with prestige)
"""
if season<2:
    team_table_old = team_info_pd
else:
    team_table_old = pd.read_excel(statistics_folder + "team_info.xlsx", sheet_name = "Teams - Season " + str(season-1))

"""
Assignment of positions (index + 1)
"""
team_table_old["Position"] = range(len(team_table_old))
team_table_old["Position"] = team_table_old["Position"] + 1

riders_table_new = riders_table
riders_table_new["Position"] = range(len(riders_table_new))
riders_table_new["Position"] = riders_table_new["Position"] + 1

"""
Extracting 3 columns + merge with old teams table to provide differences in expectations
"""
riders_table_new=riders_table_new[["Rider","Team","Position"]]
riders_changed = riders_table_new.merge(team_table_old[["Team","Position"]], on="Team")
riders_changed["Pos_rider_team"] = abs(riders_changed["Position_x"] - riders_changed["Position_y"]*2)

"""
Changes for using created perceptron
"""
riders_changed["Pos_rider_team"].array.reshape(1,-1)
t1 = pd.DataFrame(riders_changed["Pos_rider_team"])

changed_std = sc.transform(t1)
changed_pred = perceptron.predict(t1)

"""
Checking how model predicted values + counting "0" values
"""
riders_changed["Changed"] = changed_pred.tolist()
try:
    count = riders_changed["Changed"].value_counts()[1]
except:
    count = riders_changed["Changed"].value_counts()[0]
len(riders_changed["Changed"])
riders_changed.sort_values("Pos_rider_team", ascending = False, inplace=True)

"""
In case we have too many/too few "0" values, additional function to balance values.
25% - 75% - should have "0" values
"""
for n in range(int(len(riders_changed["Changed"])/2)):
    if riders_changed[riders_changed["Rider"] == yourname].iloc[0,-1] == 0:
        riders_changed.loc[riders_changed["Rider"] == yourname, ["Changed"]] = 1
    if 0.75*len(riders_changed["Changed"]) <= count:
        riders_changed.iloc[n, -1] = 1
    if 0.25*len(riders_changed["Changed"]) >= count:
        last = len(riders_changed["Changed"]) - count
        riders_changed.iloc[last-1, -1] = 0

"""
Merge current riders with riders in database who were not assigned to any team.
There is a need to assign them position for team and for rider.
All are assign with "1" value for "Changed" field, so they will attend in transfer market.
Only adults will take part, youngsters must wait for next seasons.
"""
test1 = riders_changed.merge(overalls, on="Rider", how="right")
test1["Position_y"].fillna(10, inplace=True)    
test1["Position_x"].fillna(15, inplace=True)   
test1["Changed"].fillna(1,inplace=True) 
test1 = test1[test1["Age"] > 17]
riders_changed = test1.iloc[:,:6]

"""
Taking free riders and free teams.
"""
free_riders = riders_changed[riders_changed["Changed"]==1][["Rider","Position_x","Position_y"]]
free_teams = riders_changed[riders_changed["Changed"]==1][["Team", "Position_y"]]

free_riders = free_riders.merge(overalls[["Rider", "Overall"]], on="Rider")
free_riders.columns.values[1] = "Pos_rider"
free_riders.columns.values[2] = "Pos_old_team"
free_riders.columns.values[3] = "Overall"

free_riders.iloc[:,[1,3]]

"""
Prediction of linear regression to set "prestige" of drivers
"""
free_riders_changed_data = free_riders.iloc[:,[1,3]]
free_riders_changed_data = scaler.transform(free_riders_changed_data)
free_riders_predict = lr.predict(free_riders_changed_data)
free_riders["Prestige"] = free_riders_predict.tolist()

"Assigning position to free teams and prestige"
team_table["Position"] = team_table.index
free_teams = free_teams.merge(team_table[["Team","Position"]], how="left", on="Team")
free_teams = free_teams.merge(team_info_pd[["Team","Prestige"]], how="left", on="Team")

"""
Sorting tables with teams and riders by prestige to have best teams and best riders on top.
For rider the lower prestige -> the better value
For team the higher prestige -> the better value
"""
free_teams.sort_values("Prestige", ascending=False, inplace=True)
free_riders.sort_values("Prestige", ascending=True, inplace=True)
free_teams.reset_index(inplace=True)
free_riders.reset_index(inplace=True)
free_teams.dropna(subset=["Team"], inplace=True)


"""
Choosing team by real player for next season.
It brings possibility to choose from free seats after old season.
Player has to choose team by putting number in loop function.
"""
choose_team = free_teams["Team"]
choose_team.index


def prepare_transfers(x):
    """
    while True:
        try:
            print(choose_team, "\nChoose new team (provide only number):")
            x = int(input())
            print("You chose " + str(x))
            if x not in choose_team.index:
                raise ValueError
            break
        except ValueError:
            print("Please enter an integer")
    """

    global free_riders
    "Dropping team chosen by player from free_teams list"
    free_teams.drop(x, inplace=True)
    free_teams.reset_index(inplace=True)
    free_riders.reset_index(inplace=True)

    "Choosing same amount of free riders as free seats in teams"
    j = len(free_teams)
    free_riders = free_riders.iloc[0:j]

    "Concat of free_teams and free_riders table to combine riders to new teams"
    transfers = pd.concat([free_teams["Team"], free_riders["Rider"]], axis = 1, ignore_index=True)
    transfers.columns = ["Team_new","Rider"]
    transfers = transfers.merge(riders_changed[["Team","Rider"]], on="Rider", how="left" )


    "Assigning player to table of transfers. Needs to be done for later change in files"
    #riders_to_replace = list(transfers["Rider"])
    riders_new_teams = transfers[["Rider","Team_new"]]
    riders_changed_1 = riders_changed[riders_changed["Changed"]==1][["Rider","Team"]]
    riders_changed_1.sort_values("Team", ascending = True, inplace=True)
    riders_new_teams = riders_new_teams.append({"Rider":yourname, "Team_new":choose_team[x]}, ignore_index = True)
    riders_new_teams.sort_values("Team_new", ascending = True, inplace=True)
    riders_new_teams.columns.values[0] = "Rider_new"

    m = len(riders_new_teams)
    riders_changed_1 = riders_changed_1.iloc[0:m]

    riders_changed_1.reset_index(drop=True, inplace=True)
    riders_new_teams.reset_index(drop=True, inplace=True)


    "Removing possible duplicates between tables with riders who left teams and new riders"
    riders_new_teams.columns = ["Rider", "Team"]
    riders_left = riders_changed_1.merge(riders_new_teams, left_on = ["Rider","Team"], right_on = ["Rider", "Team"],
                           how = "left", indicator = True)
    riders_right = riders_changed_1.merge(riders_new_teams, left_on = ["Rider","Team"], right_on = ["Rider", "Team"],
                           how = "right", indicator = True)
    riders_changed_1 = riders_left[riders_left["_merge"]=="left_only"]
    riders_new_teams = riders_right[riders_right["_merge"]=="right_only"]
    riders_changed_1.sort_values("Team", ascending = True, inplace=True)
    riders_new_teams.sort_values("Team", ascending = True, inplace=True)
    riders_changed_1.reset_index(drop=True, inplace=True)
    riders_new_teams.reset_index(drop=True, inplace=True)


    "prepared table with rider who left team (left) and rider who will join (right)"
    transfers_table = pd.concat([riders_changed_1, riders_new_teams], axis = 1, ignore_index = True)

    "finding team files where I can assign new rider, those files are with extension .veh"
    team_files_list = os.listdir(team_files_path)
    r = re.compile(".*.veh|.*.VEH")
    team_files = list(filter(r.match, team_files_list))


    """
    loop for all VEH files of teams
    to change old rider for a new rider with transfers_table above
    loop for a file and adding lines to new variable lines_new
    """
    print("almost loop...")
    for file in team_files:
        with open(team_files_path + file, "r") as f:
            lines = f.read().splitlines()
            print(file, team_files_path, "!")

        for i in range(len(lines)):
            if "Driver=" in lines[i]:
                for driver in transfers_table[0]:
                    if driver in lines[i]:
                        lines[i]=lines[i].replace(driver,transfers_table.iloc[np.where(transfers_table[0] == driver)[0][0],3])
                        print("driver in lines")
                        with open(team_files_path + file,"w") as output:
                            for j in lines:
                                output.write(str(j) + "\n")
                                print("output")
                                print("...")
                        break
    print("...loop ended")

def new_liveries():
    """Changing sponsors (livery) for a team. 
    If team gains/loses many positions comparing to old season,
    it means that they attract new sponsors or lose interest of current sponsors.
    Then sponsors are changing and with this also livery -> texture.
    This function implements new liveries saved in directory for teams.
    """
    veh_teams = []
    files_list = os.listdir(team_files_path)
    r = re.compile(".*.veh|.*.VEH")
    veh_files = list(filter(r.match, files_list))
    
    for team in team_table_old["Team"]:
        for v_file in veh_files:
            with open(team_files_path + v_file, "r") as f:
                lines = f.read().splitlines()

            for i in range(len(lines)):
                if team in lines[i]:
                    for i in range(len(lines)):
                        if "DefaultLivery" in lines[i]:
                            dds = lines[i]
                            dds = dds[dds.index("=") +2 : -1]
                            if [team, dds] not in veh_teams:
                                veh_teams.append([team, dds])
    
    "team table old <- already assigned later in a code"
    team_pos_compare = pd.merge(team_table_old[["Team","Position"]], 
                                team_table[["Team","Position"]], 
                                on="Team", how="inner")
    team_pos_compare["Change"] = team_pos_compare["Position_x"] - team_pos_compare["Position_y"]
    #team_pos_compare["Change"] = 1   
    "setting percentages for sponsors change depending on position and copying random texture"
    for team in team_pos_compare["Team"]:
        liveries = os.listdir(team_files_path + "Liveries\\" + team)
        if len(liveries) > 0:
            liv_num = random.randint(0, len(liveries)-1)
        change = team_pos_compare[team_pos_compare["Team"] == team]
        change = int(change["Change"])
        if random.random() < change*0.08:
            for pair in veh_teams:
                if pair[0] == team:
                    if len(liveries)>0:
                        shutil.copy(team_files_path + "Liveries\\" + team + "\\" + liveries[liv_num],
                                    team_files_path + pair[1])

