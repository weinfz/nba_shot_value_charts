# -*- coding: utf-8 -*-
"""
Created on Sat May 23 22:52:24 2015

@author: weinfz18
"""

import pandas as pd
import os

os.chdir('C:\\Users\\weinfz18\\Dropbox\\hudl_project')
## script to maerge the espn and nba data
espn = pd.read_csv("espn_shot_data.csv", index_col=0)
espn_names = list(espn.columns.values)
#espn = espn.ix[:7000]
espn = espn.values.tolist()
def fix_espn_date(date):
    date = date[2:-2]
    day = date.split(',')[1]
    day = day[1:].upper()
    month = day.split(' ')[0]
    month = month[:3]
    day = day.split(' ')[1]
    if len(day)==1:
        day = '0'+day
    year = date.split(',')[2]
    year = year[1:]
    date = month+" "+day+', '+year
    return date
def espn_time_left(desc):
    time = desc.split(" in ")[0][-5:]
    time = time.replace(' ','')
    return time
def round_time(time):
    time = time.replace(':','.')
    time = round(float(time),2)
    return time
for i in range(len(espn)):
    espn[i][1] = round_time(espn_time_left(espn[i][1]))
    espn[i][3] = fix_espn_date(espn[i][3])
espn = pd.DataFrame(espn,columns=espn_names)
espn = espn.sort(['espn_player_id','game_id','espn_shot_id'],ascending=[1, 0,1])
shot_number = [1]
j = 1
for i in range(1,len(espn)):
    if espn.iat[i,5]==espn.iat[i-1,5] and espn.iat[i,8]==espn.iat[i-1,8]:
        j+=1
        shot_number.append(j)
    else:
        j=1
        shot_number.append(j)
espn['shot_number'] = shot_number
     

nba = pd.read_csv("nba_shot_data.csv", index_col=0)
#nba = nba.ix[:1000]
nba_names = list(nba.columns.values)
nba = nba.values.tolist()
for i in range(len(nba)):
    nba[i][1] = nba[i][1].split(' - ')[0]
    nba[i][7] = round_time(nba[i][7])
nba_names[1] = 'date'
nba = pd.DataFrame(nba,columns=nba_names)
player_key = pd.read_csv('espn_nba_player_key.csv')
nba = pd.merge(nba,player_key,left_on=['nba_shooter_id','nba_shooter'],right_on=['nba_id','nba_name'])
all_shots = pd.merge(nba,espn,left_on=['espn_player_id','date','SHOT_NUMBER'],right_on=['espn_player_id','espn_ganme_date','shot_number'])
path_d = 'C:\\Users\\weinfz18\\Dropbox\\hudl_project'
all_shots.to_csv(os.path.join(path_d, 'merged_shots.csv'))






