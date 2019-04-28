from datetime import date
from nsepy import get_history
from nsepy import get_quote
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as seabornInstance
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics
# %matplotlib inline
import statsmodels.formula.api as smf
from statsmodels.tsa.stattools import adfuller
from datetime import datetime
import dateutil.relativedelta
from pairTrade.StationarityTests import StationarityTests
import sys


plt.style.use('fivethirtyeight')

stock01 = "ICICIBank"
stock02 = "HDFCBank"
start_date = date(2019,4,1)
end_date = date(2019,4,15)
#
# history_stock01 = get_history(symbol=stock01, start=start_date, end=end_date)
# history_stock02 = get_history(symbol=stock02, start=start_date, end=end_date)
# size_history_stock01 = history_stock01.size
# size_history_stock02 = history_stock02.size
# quote_stock01 = get_quote(symbol=stock01)
# quote_stock02 = get_quote(symbol=stock02)
# ltp_stock01 = quote_stock01['lastPrice']
# ltp_stock02 = quote_stock02['lastPrice']
# #
# print("history_stock01 ==> " + str(size_history_stock01))
# print("history_stock02 ==> " + str(size_history_stock02))
# if history_stock01.size != history_stock02.size:
#     print(" ******************** Data size is not same: So exiting the program  ******************** ")
#     sys.exit()
#
# close_price_history_stock01 = history_stock01[['Close']]
# close_price_history_stock02 = history_stock02[['Close']]
#
# print(history_stock01.tail(5))
# print(history_stock02.tail(5))
# print("LTP of "+stock01+" == "+str(ltp_stock01))
# print("LTP of "+stock02+" == "+str(ltp_stock02))

stock_data = pd.read_csv('/Users/ashok/king/Study/T/system/new_data_pipeline/data-pipeline/pairTrade/stockData.csv', low_memory=False)
# print(stock_data.head())

# # ICICIBank vs HDFCBank
# model = smf.ols('HDFCBank ~ ICICIBank', data=stock_data)
# model = model.fit()
# print("model.params ==> ")
# print(model.params)

# HDFCBank vs ICICIBank
print("********************* HDFCBank vs ICICIBank *********************")

model_1vs2 = smf.ols(stock01+' ~ '+stock02, data=stock_data)
results_1vs2 = model_1vs2.fit()
model_2vs1 = smf.ols(stock02+' ~ '+stock01, data=stock_data)
results_2vs1 = model_2vs1.fit()
print("DEBUG : results_1vs2.params")
print(results_1vs2.params)
print("DEBUG : results_1vs2.summary")
print(results_1vs2.summary())
print(results_2vs1.summary())
print("DEBUG : results_1vs2.bse")
print(results_1vs2.bse)

# Residual Output Section
# print(results_1vs2.fittedvalues)   # Predicted Values
residuals_1vs2 = results_1vs2.resid
residuals_2vs1 = results_2vs1.resid

# print(residuals)  # Residuals
standard_error_1vs2 = np.std(residuals_1vs2)
standard_error_2vs1 = np.std(residuals_2vs1)



print("DEBUG : standard_error")
print(standard_error_1vs2)  # standard_error
print(standard_error_2vs1)  # standard_error


print(results_1vs2.bse)
# print(results_1vs2.params) # gived the coefficients column values
bse_1vs2 = results_1vs2.bse
bse_2vs1 = results_2vs1.bse

# Standard Error of Intercept
print("DEBUG : beta standard_error")
std_error_bse_1vs2 = bse_1vs2['Intercept']
std_error_bse_2vs1 = bse_2vs1['Intercept']
print(std_error_bse_1vs2)
print(std_error_bse_2vs1)

# Error Ratio = Standard Error of Intercept / Standard Error
error_ratio_1vs2 = std_error_bse_1vs2 / standard_error_1vs2
error_ratio_2vs1 = std_error_bse_2vs1 / standard_error_2vs1
print("DEBUG : Error Ratio") # HDFC as X and ICICI as y = 0.227, ICICI as X and HDFC as y = 0.401
print(error_ratio_1vs2)
print(error_ratio_2vs1)
# stk12 = 'ICICIBank ~ HDFCBank'

if error_ratio_1vs2 > error_ratio_2vs1:
    print("Use model_2vs1 HDFCBank ~ ICICIBank ==> HDFCBank is dependent and ICICIBank is independent")
    print("Use "+stock01+" as X and "+stock02+"as Y")
    eligible_residuals = residuals_2vs1
else:
    print("Use model_1vs2 ICICIBank ~ HDFCBank ==> ICICIBank is dependent and HDFCBank is independent")
    print("Use "+stock02+" as X and "+stock01+"as Y")
    eligible_residuals = residuals_1vs2

# ADF Test
print("DEBUG : ADF Test")
# print(residuals_1vs2)

result = adfuller(eligible_residuals)
print(result)
print('ADF Statistic: %f' % result[0])
print('p-value: %f' % result[1])
print('Critical Values:')
for key, value in result[4].items():
	print('\t%s: %.3f' % (key, value))

print("EXP 02")
sTest = StationarityTests()
sTest.ADF_Stationarity_Test(eligible_residuals, printResults = True)
print("Is the time series stationary? {0}".format(sTest.isStationary))
