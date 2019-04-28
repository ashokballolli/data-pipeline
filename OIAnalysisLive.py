from nsepy import get_history
from nsepy import get_quote
from datetime import date
import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

stock = "ZEEL"
expiry=date(2019, 4, 25)



# def get_quote(symbol, series='EQ', instrument=None, expiry=None, option_type=None, strike=None):
data_stock = get_quote(symbol=stock,
                          series='EQ',
                          expiry=date(2019, 4, 25)
                          )
print("DEBUG: Option Price")
print(data_stock)

#  Call to get the live option price
data_option1 = get_quote(symbol=stock,
                          series='EQ',
                          instrument='OPTSTK',
                          option_type='CE',
                          strike=450,
                          expiry=date(2019, 4, 25)
                          )

print("DEBUG: Option Price")
print(data_option1)


