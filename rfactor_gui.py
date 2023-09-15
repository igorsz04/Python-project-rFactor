# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 00:35:59 2023

@author: igors
"""

import PySimpleGUI as sg
import os
import rfactor_functions
import rfactor_class_driver
import rfactor_data_classes
import rfactor_machine_learning
import rfactor_transfers
from rfactor_transfers import prepare_transfers
from rfactor_transfers import new_liveries
from rfactor_transfers import choose_team
from rfactor_data_classes import new_season_riders
from rfactor_data_classes import team_save_info


layout = [
    [sg.Text('File'), sg.InputText(), sg.FileBrowse(),
     ],
    [sg.Checkbox('Transfers'), sg.Checkbox('New Liveries'), 
     sg.Checkbox('New Skills'), sg.Checkbox("Team Info")
     ],
    [sg.Listbox(values=list(choose_team), size=(25,20), select_mode="single"), sg.Output(size=(25, 20))],
    [sg.Submit("New Season"), sg.Submit("Show Tables"), sg.Cancel()]
]
window = sg.Window('Season Manager rFactor2', layout)
while True:                             # The Event Loop
    event, values = window.read()
    # print(event, values) #debug
    if event in (None, 'Exit', 'Cancel'):
        break
    if event == "New Season":
        print("Loading new season...")
        rfactor_functions
        print("Functions loaded")
        rfactor_class_driver
        print("Class driver loaded")
        rfactor_data_classes
        print("Data classes loaded")
        rfactor_machine_learning
        print("Machine learning loaded")
        rfactor_transfers
        print("Transfers loaded")
        x = list(choose_team).index(values[5][0])
        if values[1] == True:
            prepare_transfers(x)
            print("Transfers done")
        if values[2] == True:
            new_liveries()
            print("New liveries saved")
        if values[3] == True:
            new_season_riders()
            print("New skills saves")
        if values[4] == True:
            team_save_info()
            print("Team info saved")
        rfactor_functions.set_new_season()
        print("NEW SEASON STARTED!")
    
    if event == "Show Tables":
        os.system("start EXCEL.EXE C:/Users/igors/OneDrive/Dokumenty/team_info.xlsx")

                
        
        


