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
import statsmodels.tsa.stattools as ts
from table import Table
from prettytable import PrettyTable

plt.style.use('fivethirtyeight')
stock01 = "BANKBARODA"
stock02 = "RBLBANK"
index = False
# start_date = date(2017,8,23)
# end_date = date(2018,6,12)
#
# # Get History
# history_stock01 = get_history(symbol=stock01, start=start_date, end=end_date, index=index)
# history_stock02 = get_history(symbol=stock02, start=start_date, end=end_date, index=index)
# size_history_stock01 = history_stock01.size
# size_history_stock02 = history_stock02.size
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
#
# merged_data = pd.concat([close_price_history_stock01, close_price_history_stock02], axis=1)
# merged_data.to_csv('/Users/ashok/king/Study/T/system/new_data_pipeline/data-pipeline/data/'+stock01+'_'+stock02+'.csv',index = True , header = [stock01,stock02] )

# stock_data = pd.read_csv('/Users/ashok/king/Study/T/system/new_data_pipeline/data-pipeline/data/'+stock01+'_'+stock02+'.csv', low_memory=False)
stock_data = pd.read_csv('/Users/ashok/king/Study/T/system/new_data_pipeline/data-pipeline/data/BANKBARODA_RBLBANK.csv', low_memory=False)
# Get LTP - Quote
quote_stock01 = get_quote(symbol=stock01)
quote_stock02 = get_quote(symbol=stock02)
ltp_stock01 = quote_stock01['lastPrice']
ltp_stock02 = quote_stock02['lastPrice']
# print("LTP of "+stock01+" == "+str(ltp_stock01))
# print("LTP of "+stock02+" == "+str(ltp_stock02))

# Decide which one to be used as X and which one as Y
model_1vs2 = smf.ols(stock01+' ~ '+stock02, data=stock_data)
results_1vs2 = model_1vs2.fit()
model_2vs1 = smf.ols(stock02+' ~ '+stock01, data=stock_data)
results_2vs1 = model_2vs1.fit()

# Residual Output Section
residuals_1vs2 = results_1vs2.resid
residuals_2vs1 = results_2vs1.resid

# Residuals
standard_error_1vs2 = np.std(residuals_1vs2)
standard_error_2vs1 = np.std(residuals_2vs1)

# gived the coefficients column values
bse_1vs2 = results_1vs2.bse
bse_2vs1 = results_2vs1.bse

# Standard Error of Intercept
std_error_bse_1vs2 = bse_1vs2['Intercept']
std_error_bse_2vs1 = bse_2vs1['Intercept']

# Error Ratio = Standard Error of Intercept / Standard Error
error_ratio_1vs2 = std_error_bse_1vs2 / standard_error_1vs2
error_ratio_2vs1 = std_error_bse_2vs1 / standard_error_2vs1

if error_ratio_1vs2 > error_ratio_2vs1:
    x=stock01
    y=stock02
    final_result=results_2vs1
    final_standard_error_of_residuals=standard_error_2vs1
    eligible_residuals = residuals_2vs1
else:
    x=stock02
    y=stock01
    final_result = results_1vs2
    final_standard_error_of_residuals = standard_error_1vs2
    eligible_residuals = residuals_1vs2

# ADF Test
sTest = StationarityTests()
sTest.ADF_Stationarity_Test(eligible_residuals, printResults = False)


# print(eligible_residuals.head(5))


t = PrettyTable(['yStock', 'xStock', "Intercept", "Slope/Beta", "p-Value", "Std Err", "Sigma/Std Err of Residuals", "Is the time series stationary?"])

t.add_row([y, x, float(str(round(final_result.params['Intercept'], 4))), float(str(round(final_result.params[x], 4))),
       str(round(sTest.pValue, 4)), "PENDING", float(str(round(final_standard_error_of_residuals, 4))), sTest.isStationary])

print(t)

