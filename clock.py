from apscheduler.schedulers.blocking import BlockingScheduler
import datetime
from datetime import date
from pairTrade.pairDataAnalysis import PairDataAnalysis
from calendarSpreads.calendarSpread import result
from calendarSpreads.downloadData import get_futures_data_continous
from calendarSpreads.downloadData import writeLTPFutureToDataFile
from utils.TelegramInteraction import sendMessage
import csv
import os

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=1)
def timed_job():
    print('This job is run every 15 minutes.')
    start_date = date(2018, 6, 20)
    # end_date = date(2019, 4, 21)
    end_date = datetime.datetime.now().date()
    symbols = ['ACC', 'ADANIENT', 'ADANIPORTS', 'ADANIPOWER', 'AJANTPHARM', 'ALBK', 'AMARAJABAT', 'AMBUJACEM', 'APOLLOHOSP',
               'APOLLOTYRE', 'ARVIND', 'ASHOKLEY', 'ASIANPAINT', 'AUROPHARMA', 'AXISBANK', 'BAJAJ-AUTO', 'BAJAJFINSV',
               'BAJFINANCE', 'BALKRISIND', 'BANKBARODA', 'BANKINDIA', 'BATAINDIA', 'BEL', 'BEML', 'BERGEPAINT', 'BHARATFIN',
               'BHARATFORG', 'BHARTIARTL', 'BHEL', 'BIOCON', 'BOSCHLTD', 'BPCL', 'BRITANNIA', 'BSOFT', 'CADILAHC', 'CANBK',
               'CANFINHOME', 'CASTROLIND', 'CEATLTD', 'CENTURYTEX', 'CESC', 'CGPOWER', 'CHENNPETRO', 'CHOLAFIN', 'CIPLA',
               'COALINDIA', 'COLPAL', 'CONCOR', 'CUMMINSIND', 'DABUR', 'DCBBANK', 'DHFL', 'DISHTV', 'DIVISLAB', 'DLF',
               'DRREDDY', 'EICHERMOT', 'ENGINERSIN', 'EQUITAS', 'ESCORTS', 'EXIDEIND', 'FEDERALBNK', 'GAIL', 'GLENMARK',
               'GMRINFRA', 'GODFRYPHLP', 'GODREJCP', 'GODREJIND', 'GRASIM', 'GSFC', 'HAVELLS', 'HCLTECH', 'HDFC',
               'HDFCBANK', 'HEROMOTOCO', 'HEXAWARE', 'HINDALCO', 'HINDPETRO', 'HINDUNILVR', 'HINDZINC', 'IBULHSGFIN',
               'ICICIBANK', 'ICICIPRULI', 'IDBI', 'IDEA', 'IDFC', 'IDFCFIRSTB', 'IFCI', 'IGL', 'INDIACEM', 'INDIANB',
               'INDIGO', 'INDUSINDBK', 'INFIBEAM', 'INFRATEL', 'INFY', 'IOC', 'IRB', 'ITC', 'JETAIRWAYS', 'JINDALSTEL',
               'JISLJALEQS', 'JSWSTEEL', 'JUBLFOOD', 'JUSTDIAL', 'KAJARIACER', 'KOTAKBANK', 'KSCL', 'KTKBANK', 'LICHSGFIN',
               'LT', 'LUPIN', 'MANAPPURAM', 'MARICO', 'MARUTI', 'MCDOWELL-N', 'MCX', 'MFSL', 'MGL', 'MINDTREE',
               'MOTHERSUMI', 'MRF', 'MRPL', 'MUTHOOTFIN', 'NATIONALUM', 'NBCC', 'NCC', 'NESTLEIND', 'NHPC', 'NIITTECH',
               'NMDC', 'NTPC', 'OFSS', 'OIL', 'ONGC', 'ORIENTBANK', 'PAGEIND', 'PCJEWELLER', 'PEL', 'PETRONET', 'PFC',
               'PIDILITIND', 'PNB', 'POWERGRID', 'PVR', 'RAMCOCEM', 'RAYMOND', 'RBLBANK', 'RECLTD', 'RELCAPITAL',
               'RELIANCE', 'RELINFRA', 'REPCOHOME', 'RPOWER', 'SAIL', 'SBIN', 'SHREECEM', 'SIEMENS', 'SOUTHBANK', 'SRF',
               'SRTRANSFIN', 'STAR', 'SUNPHARMA', 'SUNTV', 'SUZLON', 'SYNDIBANK', 'TATACHEM', 'TATACOMM', 'TATAELXSI',
               'TATAGLOBAL', 'TATAMOTORS', 'TATAMTRDVR', 'TATAPOWER', 'TATASTEEL', 'TCS', 'TECHM', 'TITAN', 'TORNTPHARM',
               'TORNTPOWER', 'TV18BRDCST', 'TVSMOTOR', 'UBL', 'UJJIVAN', 'ULTRACEMCO', 'UNIONBANK', 'UPL', 'VEDL', 'VGUARD',
               'VOLTAS', 'WIPRO', 'WOCKPHARMA', 'YESBANK']
    symbols = ['ACC']

    #  Start monitoring for the following stocks
    # JINDALSTEL  GMRINFRA  POWERGRID   VEDL

    tradable_symbols = []
    tradable_symbols_message = []

    for sym in symbols:
        print('DEBUG : START ==> ' + str(sym))
        # get_futures_data_continous(symbol=sym, start_date=start_date, end_date=end_date)
        writeLTPFutureToDataFile(symbol=sym)
        res, message, telegram_message = result(symbol=sym)
        if (res == True):
            # bot_message="*bold* _italic_ `fixed width font` [link](http://google.com)."
            message_to_telgramgroup = ""
            tradable_symbols.append(sym)
            tradable_symbols_message.append(message)
            message_to_telgramgroup = message_to_telgramgroup + "*---------- CALENDAR SPREAD ----------*\n"
            message_to_telgramgroup = message_to_telgramgroup + "*" + sym + "*" + '\n'
            message_to_telgramgroup = message_to_telgramgroup + telegram_message + '\n'
            print(message_to_telgramgroup)
            sendMessage(message_to_telgramgroup)
        print('DEBUG : END ==> ' + str(sym))
        print('\n')

    print("************************************ FINAL RESULT ************************************")
    print(tradable_symbols)
    print(tradable_symbols_message)

# @sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
# def scheduled_job():
#     print('This job is run every weekday at 5pm.')

# @sched.scheduled_job('interval', minutes=5)
# def timed_job():
#     start_date = date(2018, 6, 16)
#     # end_date = date(2019,4,21) # A day lesser than today -- previous day -- today's data will be updated by the LTP function
#     current_date_time = datetime.datetime.now()
#     end_date = current_date_time.date()
#
#     is_stock01_index = False
#     is_stock02_index = False
#     path_local = '../data/master_list.csv'
#     path_heroku = '/app/data/master_list.csv'
#
#     master_list_file = path_local if os.path.isfile(path_local) else path_heroku
#
#     # master_list_file = '../data/selected_pairs_true.csv'
#
#     with open(master_list_file, mode='r', encoding='utf-8-sig') as csvfile:
#         readCSV = csv.reader(csvfile, delimiter=',')
#         for row in readCSV:
#             stock01 = row[0].replace('"', '').replace(',', '').strip()
#             stock02 = row[1].replace('"', '').replace(',', '').strip()
#             PairDataAnalysis.download_stock_data_for_analysis(stock01=stock01, stock02=stock02, start_date=start_date,
#                                                               end_date=end_date, is_stock01_index=is_stock01_index,
#                                                               is_stock02_index=is_stock02_index)
#             res, message = PairDataAnalysis.analyseMethod01(stock01=stock01, stock02=stock02)
#             if (res == True):
#                 # bot_message="*bold* _italic_ `fixed width font` [link](http://google.com)."
#                 sendMessage("*---------- PAIR TRADING ----------*\n" + str(current_date_time) + '\n' + message + '\n')
#             # PairDataAnalysis.analyseMethod02(stock01=stock01, stock02=stock02)


sched.start()
