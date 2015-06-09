# -*- coding: utf-8 -*-
"""
Created on Fri May 22 20:25:24 2015

@author: weinfz18
"""
import lxml.html
import lxml
import pandas as pd
import datetime
from bs4 import BeautifulSoup as bs
import string
import requests
def get_espn_gameids(start_date,end_date):
    # function to grab espn nba games ids between two date date entered as YYYYMMDD
    start = datetime.date(int(str(start_date)[:4]), int(str(start_date)[4:6]), int(str(start_date)[6:8]))
    end = datetime.date(int(str(end_date)[:4]), int(str(end_date)[4:6]), int(str(end_date)[6:8]))
    delta = datetime.timedelta(days=7)
    a = [start.strftime('%Y%m%d')]
    while start < end:       
        start = start + delta
        a.append(start.strftime('%Y%m%d'))
    links = []
    for date in a:
        print(date)
        dom = lxml.html.parse('http://espn.go.com/nba/schedule?date=' + date).getroot()
        link = dom.xpath('//@href')
        links.extend([x for x in link if "recap" in x])
        ids = [x.split("gameId=")[1] for x in links]
    ids.sort()
    return ids

def get_espn_shot_data(id):
    ## function to grab the shot data from espn
    link = "http://sports.espn.go.com/nba/gamepackage/data/shot?gameId=" + id
    dom = requests.get(link)
    soup = bs(dom.text)
    shots = soup.find_all('shot')
    shot_data = []
    for shot in shots:
        shot_data.append(format_shot(shot,id))
    return shot_data
    
def format_shot(shot,game_id):
    #  helper function that takes shpot information and output a formatted dictionary 
    d = {}
    d['espn_shot_id'] = shot['id']
    d['espn_player_id'] = shot['pid']
    d['qtr'] = shot['qtr']
    if shot['t'] == 'h':
        d['home'] = True
    elif shot['t'] == 'a':
        d['home'] = False
    else:
        raise Exception("not h or a WTF?!?!?")

    # normalize shot pos
    (x,y) = _transform_coords(shot['x'],shot['y'],d['home'])
    d['pos'] = (x,y)
    d['x'] = x
    d['y'] = y
    d['distance'] = (x**2+y**2)**0.5  
    if shot['made'] == 'true':
        d['made'] = True
    elif shot['made'] == 'false':
        d['made'] = False
    else:
        raise Exception("not a make of miss... stuck on backboard?")
    name = shot['p']
    name = name.replace('  ',' ')
    name = name.replace('  ',' ')
    name = name.translate(str.maketrans("","", string.punctuation))
    try:
        d['espn_first_name_lower'] = name.split(' ')[0].lower()
        d['espn_last_name_lower'] = name.split(' ')[1].lower()
        d['espn_player_name'] = name.replace('  ',' ').lower()
    except:
        d['espn_first_name_lower'] = "john"
        d['espn_last_name_lower'] = "doe"
        d['espn_player_name'] = "john doe"
    d['espn_description'] = shot['d']
    d['game_id'] = game_id    
    return d        
        
def _transform_coords(x,y,is_home):
    ## espn plots all shots on an absolute court, not relative to the basket
    ## that the shot is attempted on. this function corrects the positions s.t.
    ## they are now relative to the basket that the shot is attempted on.
    ## x is distance from the hoop left to right. y is distance from the hoop
    ## front to back.
    ## (0,0) corresponds to the basket, (-25,-5) corresponds to a jumper from the
    ## left-most corner. (the rim is ~6 feet from the baseline).
    ## the court is 50 x 94 ft
    x = float(x)
    y = float(y)
    if is_home:
        x = 50 - x
        y = 94 - y
    # sanity check
    if not (x >= 0 and y >= 0):
        # error with data
        pass
    x = abs(50-x)-25
    y = y-6
    return (x,y)

start_date = 20141025
end_date = 20150417
ids = get_espn_gameids(start_date,end_date)
shot_data = []
j=1
for id in ids:
    ## print on percent done
    total = len(ids)
    print(j/total)
    shot_data.extend(get_espn_shot_data(id))
    j+=1
shot_data = pd.DataFrame(shot_data)  
   
  