import datetime
from datetime import date

from calendarSpreads.calendarSpread import analyse_existing_positions
from calendarSpreads.downloadData import get_futures_data_continous
from calendarSpreads.downloadData import writeLTPFutureToDataFile

start_date = date(2018, 6, 20)
# end_date = date(2019, 4, 21)
end_date = datetime.datetime.now().date()

# Analyse existing positions
symbols = ['INDIGO', 'BAJFINANCE', 'AUROPHARMA']
for sym in symbols:
    print('DEBUG : START ==> ' + str(sym))
    get_futures_data_continous(symbol=sym, start_date=start_date, end_date=end_date)
    writeLTPFutureToDataFile(symbol=sym)
    res = analyse_existing_positions(symbol=sym)
    print('DEBUG : END ==> ' + str(sym))
    print('\n')
