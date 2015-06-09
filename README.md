# nba_shot_value_charts
The scrapers nba_scrapper_w_ids.py, and  espn_scrapper.py scrape all the shot data from espn and nba.com of all shots taken in the 2014-2015 regular season and merged them(the code used to merge them is in merge.py and merge2.py, also the espn_nba_player_key.csv was used to to match the players between the two). I took both because the espn shot data had the x,y coordindates of each shot while the nba didn't but had data on the defender.  

Next, I made a model the predict the likelihood of each shot going in using logisticregression and random forests, all the variables were originally included. After tuning the model using cross validation and  the area under the ROC curve as the metric, the best model was a tuned random forest using the x,y coordinates, time left on the shot clock, and the defender distance.(code in the RF_CV.py file). Then using the expected shot values i was able calculate the expected points of all the shots, and compare that to the actual points scored and get the points added by each player offensively and defensively. The o and d points added csv file contain the raw results. But these result don't take into account the skill of the defender/shooter. So to that that into account I used an iterative approach of adjusting the ratings based on the opponents strength until the changes of each iteration become sufficiently small (code in opp_adj.py and the results are in adjusted_defense.csv and adjusted_ofense.csv). Right now I'm working on making a matrix algrebra alternative to do the adjustment but the results should be the same.  

Here positive points added on offense is good and negative points added is good for defense. another interesting to look at is the average shot worth that each player took and defended. The way I think of it is shot_worth_per_shot describes the difficulty of each players shots on offense or the ability of a defender to get opponents to take tough shots, and the value_added_per_shot represents a players skill above average of hitting or defending those shots. These should be taken in context to each other as a player may force his opponents take tough shots but could also allow him to make those shots more than they should or the other way around. 

For the visualization I created interactive defensive and offensive shot charts for each player using the bohek python library. Here the color of each box represents the value added or allowed from each location on the floor(red is good for offense and bad for defense) and the size of each box is the amount of shots from each location on the floor and if you hover over each location on the floor you can get all the information about the shot from that location. Also, the user can use the box select tool to select regions of the floor and then get the information for that entire area. and if you want select a region thats not a rectangle you hold shift and can select multiple regions at once, and if you want to undo the selection just select an area with no shots taken.

The code for the plots is in the Value_added_plotter.py file, you may need to install the bokeh library to run it, also it requires the adj_shots_for_plots.csv file for the data and the court.png for the court image. Just save those two files in a folder somewhere and change os.chdir('C:\\Users\\weinfz18\\Dropbox\\hudl_project') at the top of Value_added_plotter.py to the directory for the folder. Also switch the player if you want, right now its set to "Paul, Chris" but you can switch it to any player you want just make sure the its in the right format and capitalization matches the names the NBA.com has or just check onbe of the csv files. 

You may notice from the plots the that some of the floor locations say 0 attempts but the squares has some size that because for the size and color of each square i took into account the that particular square and the eight surrounding squares because i though it made more sense to smooth it out a little. I also included a screen shot of me playing around with Kyle Korvers shot chart in kyle_korver.png, and the html output from one i made with andrew wiggins. You can also turn off and on the box select and hover tool by clicking on the things the upper right corner.
