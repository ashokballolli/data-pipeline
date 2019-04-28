from apscheduler.schedulers.blocking import BlockingScheduler
import datetime
from datetime import date

from calendarSpreads.calendarSpread import result
from calendarSpreads.downloadData import get_futures_data_continous
from calendarSpreads.downloadData import writeLTPFutureToDataFile
from utils.TelegramInteraction import sendMessage


sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=1)
def timed_job():
    print('This job is run every three minutes.')
    start_date = date(2018, 6, 20)
    # end_date = date(2019, 4, 21)
    end_date = datetime.datetime.now().date()
    symbols = ['ADANIPORTS', 'ASHOKLEY']
    # Start monitoring for the following stocks
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
            message_to_telgramgroup = message_to_telgramgroup + "*" + sym + "*" + '\n'
            message_to_telgramgroup = message_to_telgramgroup + telegram_message + '\n'
            print(message_to_telgramgroup)
            sendMessage(message_to_telgramgroup)
        print('DEBUG : END ==> ' + str(sym))
        print('\n')

    print("************************************ FINAL RESULT ************************************")
    print(tradable_symbols)
    print(tradable_symbols_message)

@sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
def scheduled_job():
    print('This job is run every weekday at 5pm.')

sched.start()
