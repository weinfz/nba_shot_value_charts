# -*- coding: utf-8 -*-
"""
Created on Sat May 23 21:05:42 2015

@author: weinfz18
"""


import pandas as pd
import requests
import json 
import os

#links = link.xpath('//*[@id="tab-stats"]/@href')
players = pd.read_csv('C:\\Users\weinfz18\\Dropbox\\hudl_project\\all_nba_players1415.csv')
## just manullay grabbed the player names 
## and used only names that were in the espn data
player_ids = []
for row in players.iterrows():
    index, data = row
    player_ids.append(data.tolist())

def get_nba_shot_data(ids_plus_shooter_name):
    all_shots = []
    for x in ids_plus_shooter_name:
        id = str(x[0])
        player = str(x[1])
        print(id)
        site = "http://stats.nba.com/stats/playerdashptshotlog?DateFrom=&DateTo=&GameSegment=&LastNGames=0&LeagueID=00&Location=&Month=0&OpponentTeamID=0&Outcome=&Period=0&PlayerID="+id+"&Season=2014-15&SeasonSegment=&SeasonType=Regular%20Season&TeamID=0&VsConference=&VsDivision="
        dom = requests.get(site)
        dom.raise_for_status() # raise exception if invalid response
        shot_data = json.loads(dom.text)
        shots = shot_data['resultSets'][0]['rowSet']
        for shot in shots:
            shot.append(player)
            shot.append(id)
        headers = shot_data['resultSets'][0]['headers']
        headers.append("nba_shooter")
        headers.append("nba_shooter_id")
        all_shots.extend(shots)
    return [all_shots,headers]
nba_shots = get_nba_shot_data(player_ids)
len(nba_shots[0])
bad_shots = []
for shot in nba_shots[0]:
    if len(shot)!=19:
        bad_shots.extend(shot)
nba_shot_data = pd.DataFrame(nba_shots[0],columns=nba_shots[1]) 

path_d = 'C:\\Users\\weinfz18\\Dropbox\\hudl_project'
nba_shot_data.to_csv(os.path.join(path_d, 'nba_shot_data.csv'))   
