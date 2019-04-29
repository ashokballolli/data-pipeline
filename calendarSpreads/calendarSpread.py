import numpy as np
import pandas as pd
import datetime
import os

def result(symbol):
    path_local = '../data/data_calendarSpreads/' + symbol + '.xlsx'
    path_heroku = '/app/data/data_calendarSpreads/' + symbol + '.xlsx'

    file = path_local if os.path.isfile(path_local) else path_heroku

    stock_data_df = pd.read_excel(file, sheet_name=symbol).tail(201)
    stock_data_df['Diff'] = stock_data_df['Next Close'] - stock_data_df['Curr Close']
    diff_mean = stock_data_df['Diff'].mean()
    diff_mean = float(str(round(diff_mean, 4)))
    diff_stdevp = np.std(stock_data_df['Diff'])
    diff_stdevp = float(str(round(diff_stdevp, 4)))
    print('diff_mean == '+str(diff_mean))
    print('diff_stdevp == '+str(diff_stdevp))

    upper_range = diff_mean + diff_stdevp
    lower_range = diff_mean - diff_stdevp
    new_upper_range = upper_range + 1.0*upper_range
    new_lower_range = lower_range - 1.0*lower_range
    print("upper range = "+str(upper_range))
    print("lower range = "+str(lower_range))
    print("New upper range = "+str(new_upper_range))
    print("New lower range = "+str(new_lower_range))

    # IMP: change this to what range you want to consider
    upper_range_considered = upper_range
    lower_range_considered = lower_range
    # upper_range_considered = new_upper_range
    # lower_range_considered = new_lower_range
    # sell_spread
    count=0
    current_date = datetime.datetime.now().date()
    print_message = ""
    telegram_message = ""
    for index, row in stock_data_df.iterrows():
        if(row['Diff'] > upper_range_considered):
            print_message = print_message + str(row['Date'])+", "+ str(row['Curr Close'])+", "+ str(row['Next Close'])+", "+ str(row['Diff']) + '\n'
            count = count+1
            if(row['Date'].to_pydatetime().date() == current_date):
                telegram_message=telegram_message + str(row['Date']) + '\n'
                telegram_message=telegram_message + "Buy Current Month @ " +str(row['Curr Close']) + '\n'
                telegram_message=telegram_message + "Sell Next Month @ " +  str(row['Next Close']) + '\n'
                telegram_message = telegram_message + "Diff = " + str(row['Diff']) + '\n'
                telegram_message=telegram_message + "Profit Potential = " + str(round((row['Diff'] - diff_mean), 4)) + '\n'
                print(telegram_message)
                print("*********************** Sell Spread Occurances ***********************")
                print("Number of Sell Spread Occurances= " + str(count))
                print(print_message)
                from_intitial_range=str(float(str(round(((row['Diff'] - upper_range)/upper_range)*100, 2))))+"% > Original upper range (" + str(round(upper_range, 2)) + ')\n'
                from_updated_range=str(float(str(round(((row['Diff'] - upper_range_considered)/upper_range_considered)*100, 2))))+"% > New upper range (" + str(round(upper_range_considered, 2)) + ')\n'
                print(from_intitial_range)
                print(from_updated_range)
                telegram_message = telegram_message + from_intitial_range
                telegram_message = telegram_message + from_updated_range
                print('\n')
                return True, print_message, telegram_message

    return False, print_message, telegram_message

    # count=0
    # print_message = ""
    # for index, row in stock_data_df.iterrows():
    #     if(row['Diff'] < new_lower_range):
    #         print_message = print_message + str(row['Date'])+", "+ str(row['Curr Close'])+", "+ str(row['Next Close'])+", "+ str(row['Diff']) + '\n'
    #         count = count+1
    #         if(row['Date'].to_pydatetime().date() == current_date):
    #             print("*********************** Buy Spread Occurances ***********************")
    #             print("Number of Buy Spread Occurances= " + str(count))
    #             print(print_message)
    #             print('\n')
    #             return True

    return False, "Nothing"

def analyse_existing_positions(symbol):

    path_local = '../data/data_calendarSpreads/' + symbol + '.xlsx'
    path_heroku = '/app/data/data_calendarSpreads/' + symbol + '.xlsx'

    file = path_local if os.path.isfile(path_local) else path_heroku


    stock_data_df = pd.read_excel(file, sheet_name=symbol).tail(201)
    stock_data_df['Diff'] = stock_data_df['Next Close'] - stock_data_df['Curr Close']
    diff_mean = stock_data_df['Diff'].mean()
    diff_mean = float(str(round(diff_mean, 4)))
    diff_stdevp = np.std(stock_data_df['Diff'])
    diff_stdevp = float(str(round(diff_stdevp, 4)))
    print('mean(diff) == '+str(diff_mean))
    print('stdevp(diff) == '+str(diff_stdevp))

    upper_range = diff_mean + diff_stdevp
    lower_range = diff_mean - diff_stdevp
    print("upper range = "+str(upper_range))
    print("lower range = "+str(lower_range))
    # sell_spread
    exit_upper_range = diff_mean + abs(0.2*diff_mean)
    print("exit_upper_range = "+str(exit_upper_range))
    current_date = datetime.datetime.now().date()
    for index, row in stock_data_df.iterrows():
        if(row['Date'].to_pydatetime().date() == current_date):
            print("Current DIFF = " + str(row['Diff']))
            if (row['Diff'] < exit_upper_range):
                print("@@@@@@@@@@@@@@@@@@@  PLAN FOR EXIT @@@@@@@@@@@@@@@@@@")
