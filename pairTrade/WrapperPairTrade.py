from pairTrade.pairDataAnalysis import PairDataAnalysis
from datetime import date
import csv

start_date = date(2018,6,16)
end_date = date(2019,4,21) # A day lesser than today -- previous day -- today's data will be updated by the LTP function
is_stock01_index = False
is_stock02_index = False
master_list_file = '../data/master_list.csv'
# master_list_file = '../data/selected_pairs_true.csv'

with open(master_list_file, mode='r', encoding='utf-8-sig') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        stock01 = row[0].replace('"', '').replace(',', '').strip()
        stock02 = row[1].replace('"', '').replace(',', '').strip()
        PairDataAnalysis.download_stock_data_for_analysis(stock01=stock01, stock02=stock02, start_date=start_date, end_date=end_date, is_stock01_index=is_stock01_index, is_stock02_index=is_stock02_index)
        PairDataAnalysis.analyseMethod01(stock01=stock01, stock02=stock02)
        # PairDataAnalysis.analyseMethod02(stock01=stock01, stock02=stock02)



# PairDataAnalysis.getStockSymbols("")