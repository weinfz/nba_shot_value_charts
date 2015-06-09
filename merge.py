# -*- coding: utf-8 -*-
"""
Created on Sat May 23 19:48:34 2015

@author: weinfz18
"""

import lxml.html
import pandas as pd
import string
import os

os.chdir('C:\\Users\\weinfz18\\Dropbox\\hudl_project')
espn = pd.read_csv("espn_shot_data.csv", index_col=0)
nba = pd.read_csv("nba_shot_data.csv", index_col=0)
espn_names = list(espn.columns.values)
nba_names = list(nba.columns.values)
nba_players_s = list(set(nba['nba_shooter']))
nba_players_d = list(set(nba['CLOSEST_DEFENDER']))
nba_players_d = pd.DataFrame(nba_players_d,columns= ["players"])
nba_players_ids = nba[['CLOSEST_DEFENDER_PLAYER_ID','CLOSEST_DEFENDER']]
nba_players_ids = nba_players_ids.drop_duplicates()
nba_players_ids = nba_players_ids.sort('CLOSEST_DEFENDER')
nba_players_ids[nba_players_ids.duplicated('CLOSEST_DEFENDER')]
nba_players = []
for row in nba_players_ids.iterrows():
    index, data = row
    nba_players.append(data.tolist())

nba_ids = []
for row in nba_players:
    name = row[1]
    name = name.replace('  ',' ')
    name = name.replace('  ',' ')
    try:
        first = name.split(',')[1].lower()
        first = first.replace(' ','')
        first = first.translate(str.maketrans("","", string.punctuation))
        last = name.split(',')[0].lower()
        last = last.replace(' ','')
        last = last.translate(str.maketrans("","", string.punctuation))
    except:
        first = ''
        last = name.split(',')[0].lower()
        last = last.replace(' ','')
        last = last.translate(str.maketrans("","", string.punctuation))
    row.append(first)
    row.append(last)
    nba_ids.append(row)
nba_ids = pd.DataFrame(nba_ids,columns=['nba_id','nba_name','nba_first','nba_last'])

espn_nba_play_key = pd.merge(espn_players,nba_ids,left_on=['espn_first_name_lower','espn_last_name_lower'],right_on=['nba_first','nba_last'],how='outer')
path_d = 'C:\\Users\\weinfz18\\Dropbox\\hudl_project'
espn_nba_play_key.to_csv(os.path.join(path_d, 'espn_nba_player_key.csv')) 
## all this is unneeded after i created the player key


espn_players = espn[['espn_player_name','espn_player_id','espn_first_name_lower','espn_last_name_lower']]
espn_players = espn_players.drop_duplicates()
espn_players[espn_players.duplicated('espn_player_id')]

path_d = 'C:\\Users\\weinfz18\\Dropbox\\hudl_project'
players.to_csv(os.path.join(path_d, 'all_nba_players.csv'))   

espn_players = set(espn['espn_player_name'])

missing_shooter_nba = nba_players_d - nba_players_s