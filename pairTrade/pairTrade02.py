# Mohd Aadil (aadilsaifi71@gmail.com)
# python 2.7.13

import csv
import numpy as np
import statsmodels.api as sm
from numpy import array
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.datasets import load_boston
import statsmodels.tsa.stattools as ts
from table import Table
from prettytable import PrettyTable

stock01 = "ICICIBank"
stock02 = "HDFCBank"

A = list()  # Stock1
B = list()  # Stock2

# with open('/Users/ashok/king/Study/T/system/new_data_pipeline/data-pipeline/data/'+stock01+'_'+stock02+'.csv', mode='r', encoding='utf-8-sig') as csvfile:
with open('/Users/ashok/king/Study/T/system/new_data_pipeline/data-pipeline/pairTrade/stockData.csv', mode='r', encoding='utf-8-sig') as csvfile:
    next(csvfile)
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        A.append(float(row[1].replace('"','').replace(',', '').strip()))
        B.append(float(row[2].replace('"','').replace(',', '').strip()))

###############################
###### A as Y and B as X ######
###############################
Y = array(A).reshape(-1, 1)
X = array(B).reshape(-1, 1)

regr = linear_model.LinearRegression()
regr.fit(X, Y)

residuals = list()
for i in range(len(B)):
    Predicted_Y = (B[i] * regr.coef_) + regr.intercept_
    residual = A[i] - Predicted_Y
    residuals.append(residual[0][0])

standard_error1 = np.std(residuals)

X2 = sm.add_constant(X)
models = sm.OLS(Y, X2)
result = models.fit()
standard_error_of_intercept1 = result.bse[0]

adf_result1 = ts.adfuller(residuals)[1]
adf_result1per = (1 - adf_result1) * 100

error_ratio1 = (standard_error_of_intercept1 / standard_error1)
intercept1 = regr.intercept_
slope1 = regr.coef_

###############################
###### A as X and B as Y ######
###############################
X = array(A).reshape(-1, 1)
Y = array(B).reshape(-1, 1)

regr = linear_model.LinearRegression()
regr.fit(X, Y)

residuals = list()
for i in range(len(A)):
    Predicted_Y = (A[i] * regr.coef_) + regr.intercept_
    residual = B[i] - Predicted_Y
    residuals.append(residual[0][0])

standard_error2 = np.std(residuals)

X2 = sm.add_constant(X)
models = sm.OLS(Y, X2)
result = models.fit()
standard_error_of_intercept2 = result.bse[0]

adf_result2 = ts.adfuller(residuals)[1]
adf_result2per = (1 - adf_result2) * 100

error_ratio2 = (standard_error_of_intercept2 / standard_error2)
intercept2 = regr.intercept_
slope2 = regr.coef_

print('\n\n')

t = PrettyTable([stock01, stock02, "Intercept", "Slope (Beta)", "Error Ratio", "p-Value"])
if(error_ratio1 < error_ratio2):
    final_adf_result = round(adf_result1, 4)
    t.add_row(["   Y", " X", float(str(round(intercept1[0], 4))), float(str(round(slope1[0][0], 4))),
      float(str(round(error_ratio1, 4))), str(round(adf_result1, 4))])
else:
    final_adf_result = round(adf_result2, 4)
    t.add_row(["   X", " Y", float(str(round(intercept2[0], 4))), float(str(round(slope2[0][0], 4))),
      float(str(round(error_ratio2, 4))), str(round(adf_result2, 4))])

print(t)
print("Is the time series stationary?")
if(final_adf_result > 0.05):
    print("FALSE")
else:
    print("TRUE")


# if()
# print("")
# if(error_ratio1 < error_ratio2):