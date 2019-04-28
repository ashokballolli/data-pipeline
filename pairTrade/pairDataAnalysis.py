# %matplotlib inline
import csv
import sys
from datetime import datetime

import numpy as np
import pandas as pd
import statsmodels.api as sm
# %matplotlib inline
import statsmodels.formula.api as smf
import statsmodels.tsa.stattools as ts
from nsepy import get_history
from nsepy import get_quote
from nsetools import Nse
from numpy import array
from prettytable import PrettyTable
from sklearn import linear_model

from pairTrade.StationarityTests import StationarityTests
from utils.File import write


class PairDataAnalysis:
    def __init__(self, significance=.05):
        self.SignificanceLevel = significance
        self.pValue = None
        self.isStationary = None

    def analyseMethod01(stock01, stock02):
        stock01 = stock01.replace(" ", "")
        stock02 = stock02.replace(" ", "")
        file = '../data/pairTradeData/' + stock01+ '_' + stock02 + '.csv'
        PairDataAnalysis.replaceFirstLine(file)
        stock_data = pd.read_csv(file, low_memory=False)

        # Decide which one to be used as X and which one as Y
        model_1vs2 = smf.ols(stock01 + ' ~ ' + stock02, data=stock_data)
        results_1vs2 = model_1vs2.fit()
        model_2vs1 = smf.ols(stock02 + ' ~ ' + stock01, data=stock_data)
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
            x = stock01
            y = stock02
            final_result = results_2vs1
            final_standard_error_of_residuals = standard_error_2vs1
            eligible_residuals = residuals_2vs1
        else:
            x = stock02
            y = stock01
            final_result = results_1vs2
            final_standard_error_of_residuals = standard_error_1vs2
            eligible_residuals = residuals_1vs2

        # ADF Test
        sTest = StationarityTests()
        sTest.ADF_Stationarity_Test(eligible_residuals, printResults=False)

        # Get today's residual
        todays_residual = eligible_residuals.tail(1).iat[0]
        std_error_decision_maker = float(str(round(todays_residual / final_standard_error_of_residuals, 4)))

        # print(eligible_residuals.tail(5))

        beta = float(str(round(final_result.params[x], 4)))
        t = PrettyTable(
            ['Y-Stock', 'X-Stock', "Intercept", "Slope/Beta", "p-Value", "Today's residual", "Sigma/Std Err of Residuals", "Std Err-DecisionMaker",
             "Is the time series stationary?"])

        t.add_row(
            [y, x, float(str(round(final_result.params['Intercept'], 4))), beta,
             str(round(sTest.pValue, 4)), float(str(round(todays_residual, 4))), float(str(round(final_standard_error_of_residuals, 4))), std_error_decision_maker,
             sTest.isStationary])

        print(t)
        if(float(str(round(final_result.params[x], 4))) < 0):
            print("Beta is NEGATIVE, you can't trade this, atleast not always")

        if(std_error_decision_maker <= -2.5):
            print("Long position with SL: -3.0, Target: -1")
            print("Buy "+ y +" and Sell "+ x)
            print("1 "+x+" == "+str(beta)+" * "+y)

        if(std_error_decision_maker >= 2.5):
            print("Short position with SL: +3.0, Target: +1")
            print("Sell " + y + " and Buy " + x)
            print("1 "+x+" == "+str(beta)+" * "+y)

    def analyseMethod02(stock01, stock02):
        stock01 = stock01.replace(" ", "")
        stock02 = stock02.replace(" ", "")
        file = '../data/pairTradeData/' + stock01+ '_' + stock02 + '.csv'

        PairDataAnalysis.replaceFirstLine(file)
        A = list()  # Stock1
        B = list()  # Stock2

        # with open('/Users/ashok/king/Study/T/system/new_data_pipeline/data-pipeline/data/'+stock01+'_'+stock02+'.csv', mode='r', encoding='utf-8-sig') as csvfile:
        with open(file, mode='r', encoding='utf-8-sig') as csvfile:
            next(csvfile)
            readCSV = csv.reader(csvfile, delimiter=',')
            for row in readCSV:
                A.append(float(row[1].replace('"', '').replace(',', '').strip()))
                B.append(float(row[2].replace('"', '').replace(',', '').strip()))

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
        if (error_ratio1 < error_ratio2):
            final_adf_result = round(adf_result1, 4)
            t.add_row(["   Y", " X", float(str(round(intercept1[0], 4))), float(str(round(slope1[0][0], 4))),
                       float(str(round(error_ratio1, 4))), str(round(adf_result1, 4))])
        else:
            final_adf_result = round(adf_result2, 4)
            t.add_row(["   X", " Y", float(str(round(intercept2[0], 4))), float(str(round(slope2[0][0], 4))),
                       float(str(round(error_ratio2, 4))), str(round(adf_result2, 4))])

        print(t)
        print("Is the time series stationary?")
        if (final_adf_result > 0.05):
            print("FALSE")
        else:
            print("TRUE")



    def get_ltp(stock):
        ltp = get_quote(symbol=stock)['lastPrice']
        return ltp

    def download_stock_data_for_analysis(stock01, stock02, start_date, end_date, is_stock01_index, is_stock02_index):
        nse = Nse()
        file = '../data/pairTradeData/' + stock01.replace(" ", "")+ '_' + stock02.replace(" ", "") + '.csv'

        history_stock01 = get_history(symbol=stock01, start=start_date, end=end_date, index=is_stock01_index)
        history_stock02 = get_history(symbol=stock02, start=start_date, end=end_date, index=is_stock02_index)
        if len(history_stock01.index) != len(history_stock02.index):
            print("Size " + stock01 + " = " + str(len(history_stock01.index)))
            print("Size " + stock02 + " = " + str(len(history_stock02.index)))
            print(" ******************** Data size(No Of Rows) is not same: So exiting the program  ******************** ")
            sys.exit()

        close_price_history_stock01 = history_stock01[['Close']]
        close_price_history_stock02 = history_stock02[['Close']]

        merged_data = pd.concat([close_price_history_stock01, close_price_history_stock02], axis=1)
        merged_data.to_csv(file, index = True , header = [stock01,stock02] )

        if(is_stock01_index == False):
            ltp_stock01 = PairDataAnalysis.get_ltp(stock01)
        else:
            quote_01 = nse.get_index_quote(stock01)
            ltp_stock01 = quote_01['lastPrice']

        if(is_stock02_index == False):
            ltp_stock02 = PairDataAnalysis.get_ltp(stock02)
        else:
            quote_02 = nse.get_index_quote(stock02)
            ltp_stock02 = quote_02['lastPrice']

        ltp_content_to_write = datetime.today().strftime('%Y-%m-%d') +","+str(ltp_stock01)+","+str(ltp_stock02)
        write(file,ltp_content_to_write)

    def getStockSymbols(all):
        nse = Nse()
        all_stock_codes = nse.get_stock_codes()
        print(all_stock_codes)

    def replaceFirstLine(file):
        import shutil

        from_file = open(file)
        line = from_file.readline().replace(" ", "")

        # make any changes to line here

        to_file = open(file, mode="w")
        to_file.write(line)
        shutil.copyfileobj(from_file, to_file)