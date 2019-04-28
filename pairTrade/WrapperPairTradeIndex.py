from pairTrade.pairDataAnalysis import PairDataAnalysis
from datetime import date
from nsetools import Nse
from nsepy import get_quote
import csv
import json

start_date = date(2018, 6, 17)
end_date = date(2019, 4, 17)
index = True
index_01 = "NIFTY 50"
index_02 = "NIFTY BANK"
# master_list_file = '../data/master_list.csv'

PairDataAnalysis.download_stock_data_for_analysis(stock01=index_01, stock02=index_02, start_date=start_date,
                                                  end_date=end_date, index=index)
# PairDataAnalysis.analyseMethod01(stock01=stock_01, stock02=stock_02)
PairDataAnalysis.analyseMethod02(stock01=index_01, stock02=index_02)


