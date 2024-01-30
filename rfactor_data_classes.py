# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 23:56:21 2023

@author: igors
"""

from rfactor_functions import driver_test
from rfactor_functions import rcd_file
from rfactor_functions import yourname
from rfactor_functions import riders_table
from rfactor_functions import statistics_folder
from rfactor_functions import book
from rfactor_functions import team_table
from rfactor_class_driver import Driver
import pandas as pd
import shutil

"""
Using class Driver
"""

"""
Adding class objects. All stored in "rider_class" list.
"""

driver_test[0]  
rider_class = list()
for rider in driver_test[1:]:
    rider_data_list = list()
    rider_data_list.append(rider[0])
    rider_data_list.append(rider[2][rider[2].index("=")+2:])
    rider_data_list.append(int(rider[3][-4:]))
    for y in range(4,8):
        rider_data_list.append(int(rider[y][rider[y].index("=")+2:]))
    for z in range(8,20):
        rider_data_list.append(float(rider[z][rider[z].index("=")+2:]))
    rider_class.append(Driver(*rider_data_list))




"""
Loop for all riders in rider_class to set new skills for them
"""
def new_season_riders():
    for i in range(len(rider_class)):
        rider_class[i].name
        rider_class[i].show_overall()
        rider_class[i].show_skills()
        rider_class[i].set_new_skills()
        rider_class[i].save_skills()
        shutil.move(rcd_file[:-3] + "txt", rcd_file)

#new_season_riders()


"""
Creating dataframe with all riders (also those not driving in a season), their overall and age
"""
overalls = []
riders_table2 = riders_table.iloc[:,:2]
for i in range(len(rider_class)):
    overalls.append([rider_class[i].name, rider_class[i].show_overall(), rider_class[i].age])
overalls = pd.DataFrame(overalls)
team_ov = pd.merge(riders_table2, overalls[[0,1]], left_on = "Rider", right_on= 0)
team_ov = team_ov[["Rider","Team",1]]
overalls.columns = ["Rider", "Overall", "Age"]
overalls = overalls.append({"Rider":yourname, "Overall": 80, "Age": 25}, ignore_index=True)
#team_ov[team_ov["Team"]=="Red Bull"][1].mean()




class Team:
    """
    Class to assign teams,
    set their prestige,
    showing their info
    """
    def __init__(self, name, car, new_position, prestige):
        self.name = name
        self.car = car
        self.new_position = new_position
        self.prestige = prestige

    def set_teamdata(self):
        if (self.prestige <= 100) & (self.prestige > 0):
            self.prestige = 0.7*self.prestige + 40*(1/self.new_position)
        elif self.prestige > 100:
            self.prestige = 100
        elif self.prestige == 0:
            self.prestige = 0.7*(team_ov[team_ov["Team"]==self.name][1].mean()) + 40*(1/self.new_position)
        else:
            self.prestige

         
    def info(self):
        print("Name: " + self.name)
        print("Car: " + self.car)
        print("New position: " + str(self.new_position))
        print("Prestige: " + str(self.prestige))
        
    
    def prestige(self):
        return self.prestige




"""
Using class Team
"""

def team_save_info():
    """
    Function adding class "team" elements to list "team_info", 
    those contain team names, cars, prestiges, positions in new season,
    later it is saved to tab "Teams" in Excel statistics file.
    """
    team_info = []
    for i in range(len(team_class)):
        team_class[i].set_teamdata()
        team_info.append([
            team_class[i].name,
            team_class[i].car,
            team_class[i].prestige,
            team_class[i].new_position
            ])
    team_info_pd = pd.DataFrame(team_info)
    team_info_pd.columns = ["Team", "Car", "Prestige", "Position"]


    writer = pd.ExcelWriter(statistics_folder + "team_info.xlsx", engine = "openpyxl")
    writer.book = book
    team_info_pd.to_excel(writer, sheet_name = "Teams")
    writer.close()




"""
Adding teams from team-table to team_data_list (name, car, new position, prestige).
Prestige is loaded from excel file "Teams" tab. If not exists, it assigns 0 (changed by team_save_info function).
And then saving via team_save_info function.
"""    
team_class=[]
for team in team_table["Team"]:
    team_data_list = []
    team_data_list.append(team)
    team_data_list.append(team_table[team_table["Team"]==team].iat[0,1])
    team_data_list.append(int(team_table[team_table["Team"]==team].index[0]))
    try:
        team_prestige = pd.read_excel(statistics_folder + "team_info.xlsx", sheet_name = "Teams")
        team_data_list.append(team_prestige[team_prestige["Team"]==team]["Prestige"].item())
    except:
        team_data_list.append(0)
    team_class.append(Team(*team_data_list))
#team_save_info()


"Loading Teams tab for next functions"
team_info_pd = pd.read_excel(statistics_folder + "team_info.xlsx", sheet_name = "Teams")




