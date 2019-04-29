from pairTrade.pairDataAnalysis import PairDataAnalysis
from datetime import date
import csv
import datetime
from utils.TelegramInteraction import sendMessage
import os

start_date = date(2018,6,16)
# end_date = date(2019,4,21) # A day lesser than today -- previous day -- today's data will be updated by the LTP function
current_date_time = datetime.datetime.now()
end_date = current_date_time.date()

is_stock01_index = False
is_stock02_index = False
path_local = '../data/master_list.csv'
path_heroku = '/app/data/master_list.csv'

master_list_file = path_local if os.path.isfile(path_local) else path_heroku

# master_list_file = '../data/selected_pairs_true.csv'

with open(master_list_file, mode='r', encoding='utf-8-sig') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        stock01 = row[0].replace('"', '').replace(',', '').strip()
        stock02 = row[1].replace('"', '').replace(',', '').strip()
        PairDataAnalysis.download_stock_data_for_analysis(stock01=stock01, stock02=stock02, start_date=start_date, end_date=end_date, is_stock01_index=is_stock01_index, is_stock02_index=is_stock02_index)
        res, message = PairDataAnalysis.analyseMethod01(stock01=stock01, stock02=stock02)
        if (res == True):
            # bot_message="*bold* _italic_ `fixed width font` [link](http://google.com)."
            sendMessage("*---------- PAIR TRADING ----------*\n"+ str(current_date_time) + '\n' + message + '\n')
        # PairDataAnalysis.analyseMethod02(stock01=stock01, stock02=stock02)



# PairDataAnalysis.getStockSymbols("")