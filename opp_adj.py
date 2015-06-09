# -*- coding: utf-8 -*-
"""
Created on Mon May 25 15:09:28 2015

@author: weinfz18
"""

import pandas as pd
import os
import numpy as np
os.chdir('C:\\Users\\weinfz18\\Dropbox\\hudl_project')
shots = pd.read_csv("shots_for_plots.csv", index_col=0)
shots["mean_pps"] = shots["PTS"].mean()
#player_key = pd.read_csv('espn_nba_player_key.csv')
#shots["shot_worth"] = shots["probs"]*shots["PTS_TYPE"]
#shots["value_added"] = shots["PTS"]-shots["shot_worth"]
#shots = pd.merge(shots,player_key,left_on=['nba_shooter_id'],right_on=['nba_id'])
#names = list(o_points_added.columns.values)
#keep_columns = [9,10,11,14,20,21,23,24,30]
#shots = shots.iloc[:,keep_columns]

#def mean(x):
#    m = sum(x)/len(x)
#    return m
def Off_pts_added(shots):
    ##  calculates offense values added to shots
    o_points_added = shots.groupby("nba_shooter")["value_added","shot_worth","PTS"].sum()
    o_points_added['Shooter'] = o_points_added.index
    o_point_added_per = shots.groupby("nba_shooter")["value_added","shot_worth","SHOT_CLOCK","TOUCH_TIME","DRIBBLES","SHOT_DIST","SHOT_RESULT","CLOSE_DEF_DIST","PTS","probs","mean_pps"].mean()
    o_point_added_per['Shooter'] = o_point_added_per.index
    o_points_added = pd.merge(o_points_added,o_point_added_per,on="Shooter")
    o_points_added['Shot_taken'] = (o_points_added['shot_worth_x']/o_points_added['shot_worth_y']).round()
    o_points_added = o_points_added.iloc[:,(3,0,1,2,15,4,5,12,10,13,14,9,6,11,7,8)]
    return o_points_added
o_points_added = Off_pts_added(shots)   
#path_d = 'C:\\Users\\weinfz18\\Dropbox\\hudl_project'
#o_points_added.to_csv(os.path.join(path_d, 'o_points_added.csv'))

def Def_pts_added(shots):
    ## calculated defensive values added to shots
    d_points_added = shots.groupby("CLOSEST_DEFENDER")["value_added","shot_worth","PTS"].sum()
    d_points_added['Defender'] = d_points_added.index
    d_point_added_per = shots.groupby("CLOSEST_DEFENDER")["value_added","shot_worth","SHOT_CLOCK","TOUCH_TIME","DRIBBLES","SHOT_DIST","SHOT_RESULT","CLOSE_DEF_DIST","PTS","probs","mean_pps"].mean()
    d_point_added_per['Defender'] = d_point_added_per.index
    d_points_added = pd.merge(d_points_added,d_point_added_per,on='Defender')
    d_points_added['Shot_defenses'] = (d_points_added['shot_worth_x']/d_points_added['shot_worth_y']).round()
    d_points_added = d_points_added.iloc[:,(3,0,1,2,15,4,5,12,10,13,14,9,6,11,7,8)]
    return d_points_added
d_points_added = Def_pts_added(shots) 
#d_points_added.to_csv(os.path.join(path_d, 'd_points_added.csv'))
## oppenents adjust
def Off_adj(shots,o_points_added):
    shots = pd.merge(shots,o_points_added[["Shooter","value_added_y","Shot_taken"]],left_on="nba_shooter",right_on="Shooter")
    shots.loc[shots['Shot_taken'] < 250, 'value_added_y'] = 0
    shots["value_added"] = shots["value_added"] + shots["value_added_y"]
    d_points_added = Def_pts_added(shots)
    return d_points_added
#adj_def = Off_adj(shots,o_points_added)

def Def_adj(shots,d_points_added):
    shots = pd.merge(shots,d_points_added[["Defender","value_added_y","Shot_defenses"]],left_on="CLOSEST_DEFENDER",right_on='Defender')
    shots.loc[shots['Shot_defenses'] < 250, 'value_added_y'] = 0
    shots["value_added"] = shots["value_added"] + shots["value_added_y"]
    o_points_added = Off_pts_added(shots)
    return o_points_added
#adj_off = Def_adj(shots,d_points_added)

#sos_matrix = np.empty()

def Opp_adj(shots,o_points_added,d_points_added,n):
    dchanges = np.empty([len(d_points_added),n])
    ochanges = np.empty([len(o_points_added),n])
    tot_change = np.empty(n)
    for i in range(n):
        print(i)
        adj_off = Def_adj(shots,d_points_added)
        adj_def = Off_adj(shots,o_points_added)
        dchanges[:,i] = d_points_added["value_added_x"] - adj_def["value_added_x"]
        ochanges[:,i] = o_points_added["value_added_x"] - adj_off["value_added_x"]
        o_points_added = adj_off
        d_points_added = adj_def
        tot_change[i] = np.linalg.norm(dchanges[:,i],np.inf)+np.linalg.norm(ochanges[:,i],np.inf)
    return adj_off,adj_def ,tot_change
adj_off1,adj_def1,change =  Opp_adj(shots,o_points_added,d_points_added,300)
adj_def1.loc[adj_def1['Shot_defenses'] < 250, 'value_added_y'] = 0
adj_off1.loc[adj_off1['Shot_taken'] < 250, 'value_added_y'] = 0
shots = pd.merge(shots,adj_off1[["Shooter","value_added_y"]],left_on="nba_shooter",right_on="Shooter")  
shots = pd.merge(shots,adj_def1[["Defender","value_added_y"]],left_on="CLOSEST_DEFENDER",right_on="Defender")
shots.rename(columns={'value_added_y_x':"off_value_added"}, inplace=True) 
shots.rename(columns={'value_added_y_y':"def_value_added"}, inplace=True) 
shots.drop('nba_shooter', axis=1, inplace=True)
shots.drop('CLOSEST_DEFENDER', axis=1, inplace=True)

#%%  save
path_d = 'C:\\Users\\weinfz18\\Dropbox\\hudl_project'

#adj_off1.to_csv(os.path.join(path_d, 'adjusted_offense.csv'))
#adj_def1.to_csv(os.path.join(path_d, 'adjusted_defense.csv'))

shots.to_csv(os.path.join(path_d, 'adj_shots_for_plots.csv'))







