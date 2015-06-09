# -*- coding: utf-8 -*-
"""
Created on Tue May 26 23:24:06 2015

@author: weinfz18
"""

from bokeh.plotting import figure, show, output_file, hplot
from bokeh.models import HoverTool, Callback, ColumnDataSource, Range1d 
from collections import OrderedDict
import numpy as np
import pandas as pd
import os
from scipy.misc import imread

os.chdir('C:\\Users\\weinfz18\\Dropbox\\hudl_project')   ##  switch to correct directory
img = imread("court.png")                                ##  court image 
shots = pd.read_csv('adj_shots_for_plots.csv', index_col=0)  ##  shot data for all players
#%%
player = "Davis, Anthony"   ##   select player for plots make sure in the corect format "Last, First"
## "Rubio, Ricky"             ##   TO DO write something to allow errors in player input                                 
## "Wiggins, Andrew"
## "Green, Draymond"
## "Paul, Chris"
## "James, LeBron"
## "LaVine, Zach"
## "Pekovic, Nikola"            ## These names are in tyhe correct format
## "Love, Kevin"
## "Korver, Kyle"
## "Jordan, DeAndre" 


def player_shots(player,shots):
    ## function to get the right shots for the selectted player and adjusts for the shooter or defender
    o_shots = shots.loc[shots["Shooter"]==player,:]
    o_shots.loc[:,"shot_worth"] = o_shots["shot_worth"] + o_shots["def_value_added"]
    o_shots.loc[:,"value_added"] = o_shots["value_added"] - o_shots["def_value_added"]
    d_shots = shots.loc[shots["Defender"]==player,:]
    d_shots.loc[:,"shot_worth"] = d_shots["shot_worth"] + d_shots["off_value_added"]
    d_shots.loc[:,"value_added"] = d_shots["value_added"] - d_shots["off_value_added"]
    
    return o_shots,d_shots

o_shots,d_shots = player_shots(player,shots)
if len(o_shots)==0:
    print("player not found... make sure formeting and names match form 'nba_names'... also LeBron has a capital 'B'")
    ## name check
shots = None  ## commment out if you want to run many times with different players
def shot_density(shots,smooth):
    ## function to get the summary statistics for each each stat for each location on the floor
    ##  smooth is for plotting, it takes the stats for each floor lacation and the surrounding locations 
    i=0
    dense = np.empty(2601)
    fg_percent = np.empty(2601)
    mean = np.empty(2601)
    attempts = np.empty(2601)
    makes = np.empty(2601)
    shot_clock = np.empty(2601)
    distance = np.empty(2601)
    dribbles = np.empty(2601)
    touch_time = np.empty(2601)
    pts = np.empty(2601)
    close = np.empty(2601)
    worth = np.empty(2601)
    prob = np.empty(2601)
    value = np.empty(2601)
    x_shot = np.empty(2601)
    y_shot = np.empty(2601)
    for x in range(-25,26):
        isx = shots[shots['x'] == x]
        t = list(range(x-smooth,x+smooth+1))
        isx1 = shots[shots.x.isin(t)]
        for y in range(-6,45): 
            t = list(range(y-smooth,y+smooth+1))
            dense[i] = len(isx1[isx1.y.isin(t)])
            if dense[i] == 0:
                mean[i]=0
            else:
                mean[i] = isx1[isx1.y.isin(t)].mean()["value_added"]
            isy = isx[isx['y'] == y]
            attempts[i] = len(isy)
            if attempts[i] == 0:
                makes[i] = 0
                fg_percent[i] = 0
                shot_clock[i] = 0
                distance[i] = 0
                dribbles[i] = 0
                touch_time[i] = 0
                pts[i] = 0
                close[i] = 0
                worth[i] = 0
                prob[i] = 0
                value[i] = 0
            else:
                makes[i] = isy["SHOT_RESULT"].sum()
                shot_clock[i] = isy["SHOT_CLOCK"].mean()
                fg_percent[i] = makes[i]/attempts[i]
                distance[i] = isy["SHOT_DIST"].mean()
                dribbles[i] = isy["DRIBBLES"].mean()
                touch_time[i] = isy["TOUCH_TIME"].mean()
                pts[i] = isy["PTS"].mean()
                close[i] = isy["CLOSE_DEF_DIST"].mean()
                worth[i] = isy["shot_worth"].mean()
                prob[i] = isy["probs"].mean()
                value[i] = isy["value_added"].mean()
            y_shot[i] = y
            x_shot[i] = x
            i+=1
    data=dict(x=x_shot.tolist(),y=y_shot.tolist(),mean=mean.tolist(),dense=np.minimum(dense,11).tolist(),prob=prob.tolist(),value=value.tolist(),worth=worth.tolist(),close=close.tolist(),pts=pts.tolist(),
              touch_time=touch_time.tolist(),dribbles=dribbles.tolist(),distance=distance.tolist(),shot_clock=shot_clock.tolist(),makes=makes.tolist(),attempts=attempts.tolist(),fg_percent=fg_percent.tolist())
    data = pd.DataFrame(data)
    data = data[data['dense']!=0]
    data = data.reset_index(drop=True)
    data = data.to_dict("list")
    return data
odata = shot_density(o_shots,1)
ddata = shot_density(d_shots,1)

###   because the offense faces the opposite direction 
odata['y'] = [-odata['y'][i] for i in range(len(odata['y']))]
odata['x'] = [-odata['x'][i] for i in range(len(odata['x']))]

def color_map(x):
    ##  Linear color map function 
    Palette  = ["#053061", "#2166ac", "#4393c3", "#92c5de", "#d1e5f0", "#f7f7f7", "#fddbc7", "#f4a582", "#d6604d", "#b2182b", "#67001f"]
    i = int(round(x*8)+5)
    i = min(10,i)
    i = max(i,0)
    color = Palette[i]
    return color
odata['colors'] = [color_map(odata['mean'][i]) for i in range(len(odata['mean']))]
ddata['colors'] = [color_map(ddata['mean'][i]) for i in range(len(ddata['mean']))]

def make_court_images(img):
    ## format the court image 
    (m,n,k) = img.shape
    imgo = np.empty((m,n), dtype=np.uint32)
    viewo = imgo.view(dtype=np.uint8).reshape((m, n, 4))
    for i in range(m):
        for j in range(n):
            viewo[i,j,0] = max(img[i,j,0]-20,0)
            viewo[i,j,1] = max(img[i,j,1]-20,0)
            viewo[i,j,2] = max(img[i,j,2]-20,0)
            viewo[i,j,3] = 255
    imgd = np.empty((m,n), dtype=np.uint32)
    viewd = imgd.view(dtype=np.uint8).reshape((m, n, 4))
    for i in range(m):
        for j in range(n):
            viewd[m-i-1,j,0] = max(img[i,j,0]-20,0)
            viewd[m-i-1,j,1] = max(img[i,j,1]-20,0)
            viewd[m-i-1,j,2] = max(img[i,j,2]-20,0)
            viewd[m-i-1,j,3] = 255
    return imgd,imgo
imgd,imgo = make_court_images(img) 
#%%
def Make_Plot(ddata,odata,imgo,imgd,player):  
    ### function the does the actual plotting
    sd1 = ColumnDataSource(ddata)
    sd2 = ColumnDataSource(ddata)
    so1 = ColumnDataSource(odata)
    so2 = ColumnDataSource(odata)
    #output_file("wiggins_shot_charts.html", title="Gettin' Wiggy Wit it")
    output_file("gettin_wiggy_wit_it.html")
    defense = player + " - Defensive Value Added Chart"
    offense = player + " - Offensive Value Added Chart"
    op = figure(tools="box_select,hover", title=offense)
    dp = figure(tools="box_select,hover", title=defense)
    #p1.image_rgba(image=[img1],x=[-31], y=[-17.5], dw=[62], dh=[117.5])# use with tWolves court
    op.image_rgba(image=[imgo],x=[-25], y=[-41], dw=[50], dh=[47])
    dp.image_rgba(image=[imgd],x=[-25], y=[-6], dw=[50], dh=[47])
    op.scatter(x='x',y= 'y',size="dense", fill_color='colors', source=so1, alpha=1,marker="square", line_color=None,width=1000,height=1000)
    dp.scatter(x='x',y= 'y',size="dense", fill_color='colors', source=sd1, alpha=1,marker="square", line_color=None,width=1000,height=1000)
    hover = op.select(dict(type=HoverTool))
    hover.tooltips = OrderedDict([
        ("total shot taken", "@attempts"),
        ("total shot made",  "@makes"),
        ("field goal percentage", "@fg_percent"),
        ("average shot probability", "@prob"),
        ("points per shot", "@pts"),
        ("average Exected Value of shots", "@worth"),
        ("average Value added to shot", "@value"),
        ("average defender distance", "@close"), 
        ("average time on shot clock", "@shot_clock"),
        ("average shot distance", "@distance"),
        ("average touch time", "@touch_time"),
        ("average number of dribbles", "@dribbles")
    ])
    hover = dp.select(dict(type=HoverTool))
    hover.tooltips = OrderedDict([
        ("total shot taken", "@attempts"),
        ("total shot made",  "@makes"),
        ("field goal percentage", "@fg_percent"),
        ("average shot probability", "@prob"),
        ("points per shot", "@pts"),
        ("average Exected Value of shots", "@worth"),
        ("average Value allowed added to shot", "@value"),  
        ("average defender distance", "@close"), 
        ("average time on shot clock", "@shot_clock"),
        ("average shot distance", "@distance"),
        ("average touch time", "@touch_time"),
        ("average number of dribbles", "@dribbles")
    ])
    sd1.callback = Callback(args=dict(sd2=sd2,sd1=sd1), code="""
        var attempts = 0;
        var makes = 0;
        var value = 0;
        var fg_per = 0;
        var prob = 0;
        var value = 0;
        var pps = 0;
        var worth = 0;
        var close = 0;
        var shot_clock = 0;
        var distance = 0;
        var touch_time = 0;
        var dribbles = 0;
        var palette = ["#053061", "#2166ac", "#4393c3", "#92c5de", "#d1e5f0", "#f7f7f7", "#fddbc7", "#f4a582", "#d6604d", "#b2182b", "#67001f"]
        var inds = cb_obj.get('selected')['1d'].indices;
        var d1 = cb_obj.get('data');
        var d2 = sd2.get('data');   
        for (i = 0; i < inds.length; i++) {
            attempts += d2['attempts'][inds[i]]
            makes += d2['makes'][inds[i]]
            value += d2['value'][inds[i]]
            prob += d2['attempts'][inds[i]]*d2['prob'][inds[i]]
            value += d2['attempts'][inds[i]]*d2['value'][inds[i]]
            pps += d2['attempts'][inds[i]]*d2['pts'][inds[i]]
            worth += d2['attempts'][inds[i]]*d2['worth'][inds[i]]
            close += d2['attempts'][inds[i]]*d2['close'][inds[i]]
            shot_clock += d2['attempts'][inds[i]]*d2['shot_clock'][inds[i]]
            distance += d2['attempts'][inds[i]]*d2['distance'][inds[i]]
            touch_time += d2['attempts'][inds[i]]*d2['touch_time'][inds[i]]
            dribbles += d2['attempts'][inds[i]]*d2['dribbles'][inds[i]]
        }
        for (i = 0; i < d1['x'].length; i++) {
            d1['attempts'][i] = d2['attempts'][i]
            d1['makes'][i] = d2['makes'][i]
            d1['colors'][i] = d2['colors'][i]
            d1['value'][i] = d2['value'][i]
            d1['fg_percent'][i] = d2['fg_percent'][i]
            d1['prob'][i] = d2['prob'][i]
            d1['dense'][i] = d2['dense'][i]
            d1['value'][i] = d2['value'][i]
            d1['pts'][i] = d2['pts'][i]
            d1['worth'][i] = d2['worth'][i]
            d1['close'][i] = d2['close'][i]
            d1['shot_clock'][i] = d2['shot_clock'][i]
            d1['distance'][i] = d2['distance'][i]
            d1['touch_time'][i] = d2['touch_time'][i]
            d1['dribbles'][i] = d2['dribbles'][i]
        }
        value = value/attempts
        var color_index = Math.round(value*8)+5;
        color_index = Math.max(color_index,0)
        color_index = Math.min(color_index,10)
        var color = palette[color_index];
        for (i = 0; i < inds.length; i++) {
            d1['attempts'][inds[i]] = attempts
            d1['makes'][inds[i]] = makes
            d1['colors'][inds[i]] = color
            d1['value'][inds[i]] = value
            d1['fg_percent'][inds[i]] = makes/attempts
            d1['prob'][inds[i]] = prob/attempts
            d1['dense'][inds[i]] = 11
            d1['value'][inds[i]] = value/attempts
            d1['pts'][inds[i]] = pps/attempts
            d1['worth'][inds[i]] = worth/attempts
            d1['close'][inds[i]] = close/attempts
            d1['shot_clock'][inds[i]] = shot_clock/attempts
            d1['distance'][inds[i]] = distance/attempts
            d1['touch_time'][inds[i]] = touch_time/attempts
            d1['dribbles'][inds[i]] = dribbles/attempts
        }
        sd1.trigger('change');
    """)
    so1.callback = Callback(args=dict(so2=so2,so1=so1), code="""
        var attempts = 0;
        var makes = 0;
        var value = 0;
        var fg_per = 0;
        var prob = 0;
        var value = 0;
        var pps = 0;
        var worth = 0;
        var close = 0;
        var shot_clock = 0;
        var distance = 0;
        var touch_time = 0;
        var dribbles = 0;
        var palette = ["#053061", "#2166ac", "#4393c3", "#92c5de", "#d1e5f0", "#f7f7f7", "#fddbc7", "#f4a582", "#d6604d", "#b2182b", "#67001f"]
        var inds = cb_obj.get('selected')['1d'].indices;
        var d1 = cb_obj.get('data');
        var d2 = so2.get('data');   
        for (i = 0; i < inds.length; i++) {
            attempts += d2['attempts'][inds[i]]
            makes += d2['makes'][inds[i]]
            value += d2['value'][inds[i]]
            prob += d2['attempts'][inds[i]]*d2['prob'][inds[i]]
            value += d2['attempts'][inds[i]]*d2['value'][inds[i]]
            pps += d2['attempts'][inds[i]]*d2['pts'][inds[i]]
            worth += d2['attempts'][inds[i]]*d2['worth'][inds[i]]
            close += d2['attempts'][inds[i]]*d2['close'][inds[i]]
            shot_clock += d2['attempts'][inds[i]]*d2['shot_clock'][inds[i]]
            distance += d2['attempts'][inds[i]]*d2['distance'][inds[i]]
            touch_time += d2['attempts'][inds[i]]*d2['touch_time'][inds[i]]
            dribbles += d2['attempts'][inds[i]]*d2['dribbles'][inds[i]]
        }
        for (i = 0; i < d1['x'].length; i++) {
            d1['attempts'][i] = d2['attempts'][i]
            d1['makes'][i] = d2['makes'][i]
            d1['colors'][i] = d2['colors'][i]
            d1['value'][i] = d2['value'][i]
            d1['fg_percent'][i] = d2['fg_percent'][i]
            d1['prob'][i] = d2['prob'][i]
            d1['dense'][i] = d2['dense'][i]
            d1['value'][i] = d2['value'][i]
            d1['pts'][i] = d2['pts'][i]
            d1['worth'][i] = d2['worth'][i]
            d1['close'][i] = d2['close'][i]
            d1['shot_clock'][i] = d2['shot_clock'][i]
            d1['distance'][i] = d2['distance'][i]
            d1['touch_time'][i] = d2['touch_time'][i]
            d1['dribbles'][i] = d2['dribbles'][i]
        }
        value = value/attempts
        var color_index = Math.round(value*8)+5;
        color_index = Math.max(color_index,0)
        color_index = Math.min(color_index,10)
        var color = palette[color_index];
        for (i = 0; i < inds.length; i++) {
            d1['attempts'][inds[i]] = attempts
            d1['makes'][inds[i]] = makes
            d1['colors'][inds[i]] = color
            d1['value'][inds[i]] = value
            d1['fg_percent'][inds[i]] = makes/attempts
            d1['prob'][inds[i]] = prob/attempts
            d1['dense'][inds[i]] = 11
            d1['value'][inds[i]] = value/attempts
            d1['pts'][inds[i]] = pps/attempts
            d1['worth'][inds[i]] = worth/attempts
            d1['close'][inds[i]] = close/attempts
            d1['shot_clock'][inds[i]] = shot_clock/attempts
            d1['distance'][inds[i]] = distance/attempts
            d1['touch_time'][inds[i]] = touch_time/attempts
            d1['dribbles'][inds[i]] = dribbles/attempts
        }
        so1.trigger('change');
    """)
    op.x_range = Range1d(-25, 25)
    dp.x_range = Range1d(-25, 25)
    op.y_range = Range1d(-41, 6)
    dp.y_range = Range1d(-6, 41)
    layout = hplot(op, dp)
    show(layout)


### do the plot
Make_Plot(ddata,odata,imgo,imgd,player)

