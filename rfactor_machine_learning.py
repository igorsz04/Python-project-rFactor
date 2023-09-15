# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 00:03:15 2023

@author: igors
"""

import pandas as pd
from rfactor_functions import statistics_folder

"""
#Webscraping of Wikipedia pages
#It is done to download tables with results for MotoGP seasons.

import pandas as pd
import requests
from bs4 import BeautifulSoup
pd.set_option("display.max_columns", 10)
pd.set_option("display.max_colwidth",1000)
pd.set_option("display.width", 1000)
pd.set_option("display.max_rows", 1000)
# get the response in the form of html
table_join_all = pd.DataFrame()
years_table = range(2014,2023)
for year in reversed(years_table):
    i = 8 if (year == 2014 or year == 2020) else 7
    j = 11 if (year == 2014) else 11 if (year == 2020) else 10
    
    wikiurl="https://en.wikipedia.org/wiki/"+str(year)+"_MotoGP_World_Championship"
    table_class="wikitable"
    response=requests.get(wikiurl)
    soup = BeautifulSoup(response.text, "html.parser")
    motogptable = soup.find_all("table")
    motogptable[i]

    table_hist = pd.read_html(str(motogptable[i]))
    table_hist = pd.DataFrame(table_hist[0])
    table_hist.rename(columns= {table_hist.columns[0]:table_hist.columns[0][0:3]}, inplace=True)

    table_team_list = pd.read_html(str(motogptable[j]))
    table_team_list = pd.DataFrame(table_team_list[0])
    table_team_list.rename(columns= {table_team_list.columns[0]:table_team_list.columns[0][0:3]}, inplace=True)
    table_team_list.drop_duplicates("Team",inplace=True)

    table_join = pd.merge(table_hist.iloc[:-1,0:4], table_team_list.iloc[:,0:2], on="Team", how="left").dropna()
    table_join = table_join.iloc[:-1]
    table_join["Pos_x"] = pd.to_numeric(table_join["Pos_x"])
    table_join = table_join[table_join["Pos_x"]<23]
    table_join["year"] = year
    
    table_join_all = pd.concat([table_join_all, table_join])
"""
#table_join_all.to_excel(r"C:\Users\igors\OneDrive\Dokumenty\table_join.all.xlsx")


"""
Loading web-scraped Wikipedia tables
Some changes need to be done for next purposes (change of team names, finding exceptions manually).
Preparing data for machine learning (perceptron deciding if rider stays at team or not, 
                                     comparing rider and team position in tables and
                                     linear regression measuring value of rider on transfer market)
"""

table_join_all = pd.read_excel(statistics_folder + "table_join.all.xlsx")    

"Changes of name for easier recognition of teams"
table_join_all["Team"]=table_join_all["Team"].str.replace(r"(^.*Ducati.*$)", "Ducati Factory")
table_join_all["Team"]=table_join_all["Team"].str.replace(r"(^.*Yamaha MotoGP.*$)", "Yamaha Factory")
table_join_all["Team"]=table_join_all["Team"].str.replace(r"(^.*Aprilia.*$)", "Aprilia Factory")
table_join_all["Team"]=table_join_all["Team"].str.replace(r"(^.*Repsol Honda.*$)", "Honda Factory")
table_join_all["Team"]=table_join_all["Team"].str.replace(r"(^.*Pramac.*$)", "Pramac")
table_join_all["Team"]=table_join_all["Team"].str.replace(r"(^.*Yamaha SRT.*$)", "Yamaha Private")
table_join_all["Team"]=table_join_all["Team"].str.replace(r"(^.*Yamaha RNF.*$)", "Yamaha Private")
table_join_all["Team"]=table_join_all["Team"].str.replace(r"(^.*Yamaha Tech.*$)", "Yamaha Private")
table_join_all["Team"]=table_join_all["Team"].str.replace(r"(^.*Suzuki.*$)", "Suzuki Factory")
table_join_all["Team"]=table_join_all["Team"].str.replace(r"(^.*LCR.*$)", "LCR")
table_join_all["Team"]=table_join_all["Team"].str.replace(r"(^.*Marc VDS.*$)", "Marc VDS")
table_join_all["Team"]=table_join_all["Team"].str.replace(r"(^.*Bull KTM Factory.*$)", "KTM Factory")
table_join_all["Team"]=table_join_all["Team"].str.replace(r"(^.*Esponsorama.*$)", "Gresini")
table_join_all["Team"]=table_join_all["Team"].str.replace(r"(^.*Avintia.*$)", "Gresini")
table_join_all["Team"]=table_join_all["Team"].str.replace(r"(^.*Nieto.*$)", "Aspar")
table_join_all["Team"]=table_join_all["Team"].str.replace(r"(^.*Aspar.*$)", "Aspar")
table_join_all["Team"]=table_join_all["Team"].str.replace(r"(^.*Tech3.*$)", "Tech3")

table_join_all_1=table_join_all.copy()
table_join_all_1["year"] = table_join_all_1["year"].apply(lambda x: int(x) - 1)
table_with_transfers = pd.merge(table_join_all,table_join_all_1[["Rider","Team","year"]], on=["Rider","year"], how="left")
table_with_transfers=table_with_transfers.loc[table_with_transfers["Rider"] != "Michele Pirro"]

    
table_right = table_with_transfers[["Pos_y","year","Team_x"]]
table_right=table_right.rename(columns={"Team_x":"Team_y"})
table_right.drop_duplicates(inplace=True)
table_with_transfers_2 = pd.merge(table_with_transfers[["Pos_x","Rider","Team_x","Pos_y","year","Team_y"]], table_right, on=["Team_y","year"], how="left")
table_with_transfers_2["Changed"]=(table_with_transfers_2["Team_x"]!=table_with_transfers_2["Team_y"])
table_with_transfers_2["Factory"]=table_with_transfers_2["Team_x"].str.contains("Factory")
#table_with_transfers_2.dropna(inplace=True)
table_with_transfers_2["Changed"]=table_with_transfers_2["Changed"].astype(int)
table_with_transfers_2["Factory"]=table_with_transfers_2["Factory"].astype(int)


table_with_transfers_2 = table_with_transfers_2[table_with_transfers_2.year != 2022]
table_with_transfers_2.reset_index(inplace=True)
table_with_transfers_2.drop(columns="index", inplace=True)
    
"Exceptions done manually, it assigns new positions to improve dataset for further using"
table_with_transfers_2.iloc[4,6] = 4
table_with_transfers_2.iloc[4,7] = 0
table_with_transfers_2.iloc[8,6] = 4
table_with_transfers_2.iloc[8,7] = 0
table_with_transfers_2.iloc[17,6] = 13
table_with_transfers_2.iloc[18,6] = 13
table_with_transfers_2.iloc[19,6] = 13
table_with_transfers_2.iloc[34,6] = 8
table_with_transfers_2.iloc[40,6] = 13
table_with_transfers_2.iloc[41,6] = 13
table_with_transfers_2.iloc[42,6] = 1
table_with_transfers_2.iloc[42,7] = 0
table_with_transfers_2.iloc[76,6] = 13
table_with_transfers_2.iloc[78,6] = 13
table_with_transfers_2.iloc[80,6] = 13
table_with_transfers_2.iloc[89,6] = 8
table_with_transfers_2.iloc[89,7] = 0
    
"Droping some cases which in my opinion would not be correct for later analysis. It required some knowledge about this data"
table_with_transfers_2.dropna(subset="Pos_y_y", inplace=True)
table_with_transfers_2.drop([5,7,10,12,14,15,22,25,26,27,29,31,35,36,39,45,49,51,60,66,68,69,82,89,93,96,97,106,110,113,116,119,122,131,133,140], inplace=True)
riders_2014_2023 = table_with_transfers_2["Rider"].drop_duplicates().values
table_with_transfers_skills = [95, 95, 90, 90, 85, 100, 90, 90, 80, 85,
                                   70, 85, 70, 85, 90, 75, 80, 65, 65, 95, 95, 
                                   65, 80, 90, 100, 85, 85, 75, 70, 85]
riders_2014_2023_skills = pd.DataFrame((riders_2014_2023, 
                                            table_with_transfers_skills)).transpose()
riders_2014_2023_skills.columns=["Rider", "Overall"]
    
table_with_transfers_2 = pd.merge(table_with_transfers_2, riders_2014_2023_skills, on="Rider", how="left")
table_with_transfers_2.Changed.sum()
    
    
    
    
table_with_transfers_2.rename(columns={"Pos_x":"Pos_rider",
                                           "Pos_y_x":"Pos_old_team",
                                           "Pos_y_y":"Pos_new_team"},
                                  inplace=True)
table_with_transfers_2.dtypes
table_with_transfers_2["Pos_old_team"]=pd.to_numeric(table_with_transfers_2["Pos_old_team"])
table_with_transfers_2["Pos_new_team"]=pd.to_numeric(table_with_transfers_2["Pos_new_team"])
table_with_transfers_2["Overall"]=pd.to_numeric(table_with_transfers_2["Overall"])

table_last = table_with_transfers_2[["Pos_rider", "Pos_old_team", "Pos_new_team",
                                         "Factory", "Overall", "Changed"]]
ml_changed_data = table_with_transfers_2[["Pos_rider", "Pos_old_team",
                                         "Factory", "Overall"]]
ml_changed_target = table_with_transfers_2["Changed"]

"""
Preparing data for perceptron which will be deciding if rider leaves the team or not, checking data
"""
changed = table_with_transfers_2[table_with_transfers_2["Changed"]==1]

ml_transfer_data = changed[["Pos_rider", "Pos_old_team", "Factory", "Overall"]]
ml_transfer_target = changed["Pos_new_team"]
    
"""
Checking data on plots to choose proper variables
"""
import seaborn as sns
import matplotlib.pyplot as plt
corr = table_last.corr()
"checking correlation between variables"
sns.heatmap(data=corr, square=True, annot=True, cbar=True)
sns.pairplot(table_last)

"density of overall values"
sns.kdeplot(table_last["Overall"])
    
sns.jointplot(x="Pos_rider", y="Pos_old_team", data=table_last)
sns.jointplot(x="Pos_rider", y="Pos_new_team", data=table_last)
sns.jointplot(x="Pos_rider", y="Overall", data=table_last)
sns.jointplot(x="Pos_new_team", y="Overall", data=table_last)

"Assigning specific for dataset colours for plots"
palette_motogp = ["blue","red","deepskyblue",
                                   "orange","gold","green",
                                   "teal","yellow","lightcoral",
                                   "skyblue","silver","white","purple"]
sns.set_palette(palette_motogp)

"showing box plots, bar plots"
sns.catplot(x="Team_y", y="Overall", data=table_with_transfers_2,
                   kind="box", aspect=2.6)
sns.catplot(x="Team_y", y="Pos_rider", data=table_with_transfers_2,
                   kind="box", aspect=2.6)
    
sns.set_palette("RdBu",10)
labels = changed.Pos_old_team.value_counts()
labels.index
labels.values
sns.barplot(x=labels.index, y=labels.values)
    
"Preparing sets - target and independent variables"
ml2_changed_data = table_with_transfers_2[["Pos_rider", "Pos_old_team",
                                     "Factory", "Overall"]]
ml2_changed_target = table_with_transfers_2["Changed"]

ml2_changed_data["Pos_rider_team"] = abs(ml2_changed_data["Pos_rider"] - ml2_changed_data["Pos_old_team"]*2)
ml2_changed_data = ml2_changed_data[["Pos_rider_team"]]


"""
Machine learning perceptron procedure with results at the bottom
"""
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Perceptron
from sklearn.metrics import confusion_matrix
    
X_train, X_test, y_train, y_test = train_test_split(ml2_changed_data, ml2_changed_target, test_size=0.1)

"Standarizing variables"    
sc = StandardScaler()
sc.fit(ml2_changed_data)

X_train_std = sc.transform(X_train)
X_test_std = sc.transform(X_test)

"Preparing perceptron with number of iterations and coefficient eta"
perceptron = Perceptron(max_iter=20, eta0=0.001)
perceptron.fit(X_train_std, y_train)

"Predictions"
y_pred = perceptron.predict(X_test_std)
y_test
y_pred

"Returning differences betwen y_pred and y_test"
[(a,b) for (a,b) in zip(y_pred[y_pred != y_test], y_test[y_pred != y_test])]

"Some additional things like score, coefficient, etc"
print(perceptron.score(X_test_std, y_test))
print(perceptron.coef_)
print(perceptron.intercept_)
print(perceptron.n_iter_)
print(perceptron.t_)

"Confusion matrix, important table, returning False positive, False negative, True positive, True negative"
print(confusion_matrix(y_test, y_pred))


"""
New set for linear regression model
"""
changed

"Scatter (dot) plots with overall and pos_rider values"
plt.figure(figsize=(7,5))
plt.scatter(changed["Pos_new_team"], changed["Pos_rider"], color="red")
plt.scatter(changed["Pos_new_team"], changed["Overall"], color="blue")

"Some statistics like count, mean, min, max, quartiles"
changed.describe()

changed = changed[["Pos_rider", "Pos_old_team", "Factory", "Pos_new_team", "Overall"]]
changed_data = changed[["Pos_rider", "Overall"]]
changed_target = changed["Pos_new_team"]

"Correlation between variables"
cor_mat = np.corrcoef(changed.values.T)

fig, ax = plt.subplots(figsize=(5,5))
sns.heatmap(data = cor_mat,
            square = True,
            cbar = True,
            annot = True,
            fmt = ".2f",
            annot_kws = {"size":15},
            xticklabels = changed.columns,
            yticklabels = changed.columns
            )
ax.xaxis.tick_top()

"""
Machine learning linear regression
"""
from sklearn.linear_model import LinearRegression


scaler = StandardScaler()
scaler.fit(changed_data)
changed_data = scaler.transform(changed_data)

"Dividing data on trained and tested (both dependent and independent variables)"
X_train, X_test, y_train, y_test = train_test_split(changed_data, changed_target, test_size=0.2)

lr = LinearRegression()
lr.fit(X_train, y_train)

y_pred = lr.predict(X_test)
y_pred_train = lr.predict(X_train)

lr.score(X_test, y_test)
lr.coef_

plt.figure(figsize = (7,7))
plt.scatter(y_test, y_pred, edgecolors = "blue")

fig, ax = plt.subplots(1, 2, figsize=(6,3))
ax[0].scatter(y_train, y_pred_train - y_train, color = "green")
ax[1].scatter(y_test, y_pred - y_test, color = "orange")


"""
Model (perceptron) does not predict well, but its not the aim.
Model cannot predict fully correctly as there are too many unmeasurable features included
in feature "if rider changes a team".
The problem is that model too much predicts same values for dataset (predicted "0" in 90-100% cases for some
                                                                     test values, while there should be around 50%).
This issue must be (and is) modified with additional functions later.

Linear regression model predicts value (the lower value, the better rider) on market.
"""
