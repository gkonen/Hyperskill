import os
import requests

import pandas as pd
import numpy as np
from itertools import combinations
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_percentage_error as mape

# checking ../Data directory presence
if not os.path.exists('../Data'):
    os.mkdir('../Data')

# download data if it is unavailable
if 'data.csv' not in os.listdir('../Data'):
    url = "https://www.dropbox.com/s/3cml50uv7zm46ly/data.csv?dl=1"
    r = requests.get(url, allow_redirects=True)
    open('../Data/data.csv', 'wb').write(r.content)

# read data
data = pd.read_csv('../Data/data.csv')
target = 'rating'

# write your code here
# This code is the one that the last test succeeds and does not reflet the work during all the project
# Consider this as a sketch and not a real work in Machine Learning, I will organize myself differently for further project.

mat_corr = data.corr(numeric_only=True)
correlated_features = []
for feat in data.columns:
    if feat != 'salary' and mat_corr.loc[feat, 'salary'] > 0.2:
        correlated_features.append(feat)

#prediction
X = data.drop(columns=['salary'])
y = data['salary']

score = {}
for r in range(1, len(correlated_features)):
    for feat in combinations(correlated_features, r):
        Xc = X.drop(columns= list(feat))
        X_train, X_test, y_train, y_test = train_test_split(Xc, y, test_size=0.3, random_state=100)
        reg = LinearRegression().fit(X_train, y_train)
        score[feat] = mape(y_test, reg.predict(X_test))

best_feature = min(score, key=score.get)
selected = X.drop(columns=list(best_feature))
X_train, X_test, y_train, y_test = train_test_split(selected, y, test_size=0.3, random_state=100)
reg = LinearRegression().fit(X_train, y_train)
y_pred = reg.predict(X_test)

replace_nul = [ 0 if value < 0 else value for value in y_pred ]
median = np.median(y_pred)
replace_median = [ median if value < 0 else value for value in y_pred ]

print(min([mape(y_test, replace_nul), mape(y_test, replace_median)]))
