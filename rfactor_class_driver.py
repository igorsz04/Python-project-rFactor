# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 23:55:28 2023

@author: igors
"""

import copy
import numpy as np
from rfactor_functions import table_full
from rfactor_functions import max_pts
from rfactor_functions import rcd_file
from rfactor_functions import year
from rfactor_functions import table_grid
from rfactor_functions import race_tracks
from rfactor_functions import table_position_after_lap1


class Driver:
    """
    Class to keep drivers data, 
    to assign them new skills after season based on their results,
    to show their skills,
    to show their overall (based on skills),
    to return their names,
    to save their skills in game files.
    """
    def __init__(self, name, nationality, dateofbirth, starts, poles, wins, champs, 
                 aggression, reputation, courtesy, composure, speed,
                 qualify, wetspeed, start, crash, recovery, completed, minracing):
        self.name = name
        self.nationality = nationality
        self.dateofbirth = dateofbirth
        self.starts = starts
        self.poles = poles
        self.wins = wins
        self.champs = champs
        self.aggression = aggression
        self.reputation = reputation
        self.courtesy = courtesy
        self.composure = composure
        self.speed = speed
        self.qualify = qualify
        self.wetspeed = wetspeed
        self.start = start
        self.crash = crash
        self.recovery = recovery
        self.completed = completed
        self.minracing = minracing
        self.age = year - dateofbirth

    def set_new_skills(self):
        self.old_aggression = self.aggression
        if self.aggression * np.random.normal(1,0.1) <= 100:    
            self.aggression = self.aggression * np.random.normal(1,0.1)
        else: 
            self.aggression = 100
        
        self.old_composure = self.composure
        if self.composure + 0.2*(self.age-40) <= 100:
            self.composure = self.composure + 0.2*(self.age-40)
        else:
            self.composure = 100
            
        ###testy formuły self speed
        #agx = range(10,45)
        #age = 30
        #for i in agx:
        #    age = age -0.2*(i-28) -0.1*(i-18)
        #    if i > 18:
        #        age = age + 0.9*1000/(i)**2
        #    print(i, age)
        #koniec testów
        
        self.old_speed = self.speed
        try:
            self.rider_pts = table_full[table_full.iloc[:,0]==self.name].iloc[0,-1]
        except IndexError:
            self.rider_pts = 0.1*max_pts
            
        self.speed = self.speed + np.random.normal(1,0.2) * (self.rider_pts/max_pts* \
                                                             1000/(self.age)**2) - \
                                    np.random.normal(1,0.1) * 0.2*(self.age - 28) - \
                                    np.random.normal(1,0.1) * 0.1*(self.age - 18)

        self.speed = 100 if self.speed > 100 else self.speed
        
        self.old_qualify = self.qualify
        try:
            self.qualify = 100 - (table_grid[table_grid["Rider"]==self.name]["Sum Grid Pos"].iloc[0])/len(race_tracks)* np.random.normal(1,0.2)*2.5 
        except IndexError:
            self.qualify = self.qualify + 2
        
        
        self.old_wetspeed = self.wetspeed
        if self.wetspeed * np.random.normal(1,0.2) <= 100:
            self.wetspeed = self.wetspeed * np.random.normal(1,0.2)
        else:
            self.wetspeed = 100
        
        self.old_start = self.start
        try:
            self.start = self.start + 5*np.random.normal(1,0.2) \
            * (table_position_after_lap1[table_position_after_lap1["Rider"]==self.name]["Points Total"].iloc[0])\
                /len(race_tracks)
        except IndexError:
            self.start = self.start + 2*np.random.normal(1,0.2)
        
        self.start = 100 if self.start > 100 else self.start
        
        
        self.old_crash = self.crash
        if self.crash * np.random.normal(1,0.2) > 0:
            self.crash = self.crash - 0.2*(np.sqrt(abs(self.age-35)))
        else:
            self.crash = 0
        
        self.old_completed = self.completed
        if self.completed - 0.2*(self.age-35) <= 100:
            self.completed = self.completed - 0.2*(self.age-35)
        else:
            self.completed = 100
        
        self.old_minracing = self.minracing
        try:
            self.minracing = 100 - 3 * (table_full[table_full["Rider"]==self.name].iloc[0,3:-1].std())
        except IndexError:
            self.minracing = self.minracing
        
        
        print(self.old_aggression ,"->", self.aggression)
        print(self.old_composure ,"->", self.composure)
        print(self.old_speed ,"->", self.speed)
        print(self.old_qualify ,"->", self.qualify)
        print(self.old_wetspeed ,"->", self.wetspeed)
        print(self.old_start ,"->", self.start)
        print(self.old_crash ,"->", self.crash)
        print(self.old_completed ,"->", self.completed)
        print(self.old_minracing ,"->", self.minracing)
        
    
    def show_skills(self):
        print(self.name, self.nationality, self.age)
        print("Aggression: ", self.aggression)
        print("Composure: ", self.composure)
        print("Speed: ", self.speed)
        print("Qualify: ", self.qualify)
        print("WetSpeed: ", self.wetspeed)
        print("Start: ", self.start)
        print("Crash: ", self.crash)
        print("CompletedLaps: ", self.completed)
        print("MinRacingSkill: ", self.minracing)
        print("Overall: ", round(self.aggression * 0.04 + self.composure * 0.03 + self.speed * 0.65 \
                                 + self.qualify * 0.1 + self.wetspeed * 0.05 + self.start * 0.03 \
                                 - self.crash + self.completed * 0.05 + self.minracing * 0.05))

    def show_overall(self):
        return round(self.aggression * 0.04 + self.composure * 0.03 + self.speed * 0.65 \
                     + self.qualify * 0.1 + self.wetspeed * 0.05 + self.start * 0.03 \
                         - self.crash + self.completed * 0.05 + self.minracing * 0.05)
    
    def name(self):
        return self.name
    
    def save_skills(self):
            
            with open(rcd_file,"rt") as file:           
                with open(rcd_file[:-3] + "txt","wt") as fout:
                    i=0
                    g=0
                    for line in file:
                        i=i+1
                        if line.strip() == self.name:
                            g=copy.deepcopy(i)
                        if g>0:
                            if i==g+8:
                                fout.write("Aggression = " + str(round(self.aggression,2)) + "\n")
                            elif i==g+11:
                                fout.write("Composure = " + str(round(self.composure,2)) + "\n")
                            elif i==g+12:
                                fout.write("Speed = " + str(round(self.speed,2)) + "\n")
                            elif i==g+13:
                                fout.write("QualifySpeed = " + str(round(self.qualify,2)) + "\n")
                            elif i==g+14:
                                fout.write("WetSpeed = " + str(round(self.wetspeed,2)) + "\n")
                            elif i==g+15:
                                fout.write("StartSkill = " + str(round(self.start,2)) + "\n")
                            elif i==g+16:
                                fout.write("Crash = " + str(round(self.crash,2)) + "\n")
                            elif i==g+18:
                                fout.write("CompletedLaps = " + str(round(self.completed,2)) + "\n")
                            elif i==g+19:
                                fout.write("MinRacingSkill = " + str(round(self.minracing,2)) + "\n")
                            else:
                                fout.write(line)
                        else:
                            fout.write(line)

    def save_new_skills(self):
        pass
    
@staticmethod
def overall(aggression, composure, speed, qualify, wetspeed, start, crash, completed, minracing):
    return round(aggression * 0.04 + composure * 0.03 + speed * 0.65 + qualify * 0.1 + wetspeed * 0.05 
    + start * 0.03 - crash + completed * 0.05 + minracing * 0.05)

