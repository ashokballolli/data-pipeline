from pairTrade.pairDataAnalysis import PairDataAnalysis
from datetime import date
from nsetools import Nse
from nsepy import get_quote
import csv
import json

start_date = date(2018,6,16)
end_date = date(2019,4,16)
stock_01 = "RELIANCE"
stock_02 = "NIFTY 50"
is_stock01_index = False
is_stock02_index = True
# master_list_file = '../data/master_list.csv'

PairDataAnalysis.download_stock_data_for_analysis(stock01=stock_01, stock02=stock_02, start_date=start_date,
                                                  end_date=end_date, is_stock01_index=is_stock01_index, is_stock02_index=is_stock02_index)

PairDataAnalysis.analyseMethod01(stock01=stock_01, stock02=stock_02)
# PairDataAnalysis.analyseMethod02(stock01=stock_01, stock02=stock_02)

# print(stock_02.replace(" ", ""))
