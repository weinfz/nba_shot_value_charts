# -*- coding: utf-8 -*-
"""
Created on Sun May 24 01:53:08 2015

@author: weinfz18
"""

import pandas as pd
import os
from sklearn.ensemble import RandomForestClassifier
import sklearn
import numpy as np
import random
os.chdir('C:\\Users\\weinfz18\\Dropbox\\hudl_project')
shots = pd.read_csv("merged_shots.csv", index_col=0)

names = list(shots.columns.values)
keep_columns = [5,7,10,13,20,21]
shots = shots.iloc[:,keep_columns]
#shots = shots.dropna()
shots["SHOT_CLOCK"] = shots["SHOT_CLOCK"].fillna(shots["SHOT_CLOCK"].mean())
shots['SHOT_RESULT'] = shots['SHOT_RESULT'] == 'made'
names = list(shots.columns.values)
random.seed(123)

def RF_CV(folds,shots,y_row,N_feature,split):
    ## function to do random forest cross validation
    indices = np.array([random.randint(0,folds-1) for i in range(len(shots))])
    roc = []
    importance = []
    for i in range(folds):
        print(i)
        test = shots[indices==i]
        train = shots[indices!=i]
        rf = RandomForestClassifier(n_jobs=500,max_features=N_feature, criterion='entropy',min_samples_split=split)
        rf.fit(train.drop([train.columns[y_row]],axis=1),train.iloc[:,y_row])
        probs = rf.predict_proba(test.drop([test.columns[y_row]],axis=1))
        roc.append(sklearn.metrics.roc_auc_score(test.iloc[:,y_row], probs[:,1], average='macro', sample_weight=None))
        importance.append(rf.feature_importances_)
    names = list(shots.columns.values)
    names.pop(y_row)
    importance = pd.DataFrame(importance,columns=names)
    return(roc,importance)
#preds = rf.predict(test.iloc[:,[0,2,3,4]])
#pd.crosstab(test['SHOT_RESULT'], preds, rownames=['actual'], colnames=['preds'])
roc1,importance1 = RF_CV(5,shots,2,2,1200)
roc2,importance2 = RF_CV(5,shots,2,2,1300)
roc3,importance3 = RF_CV(5,shots,2,2,1400)
roc4,importance4 = RF_CV(5,shots,2,2,1500)
roc5,importance5 = RF_CV(5,shots,2,2,1600)
mean1 = sum(roc1)/len(roc1)
mean2 = sum(roc2)/len(roc2)
mean3 = sum(roc3)/len(roc3)
mean4 = sum(roc4)/len(roc4)
mean5 = sum(roc5)/len(roc5)

rf = RandomForestClassifier(n_jobs=500,max_features=2, criterion='entropy',min_samples_split=1500)
rf.fit(shots.iloc[:,[0,1,3,4,5]],shots['SHOT_RESULT'])
probs = rf.predict_proba(shots.iloc[:,[0,1,3,4,5]])
shots = shots.join(pd.DataFrame(probs[:,1],columns=["probs"]))
mean_pps = shots["PTS"].mean()
shots["shot_worth"] = shots["probs"]*shots["PTS_TYPE"]
shots["value_added"] = shots["PTS"]-shots["shot_worth"]
path_d = 'C:\\Users\\weinfz18\\Dropbox\\hudl_project'
shots.to_csv(os.path.join(path_d, 'shots_for_plots.csv'))






