# -*- coding: utf-8 -*-
"""
Created on Thu Mar  8 13:44:13 2018

@author: Varun
"""

import NSEpy_Download as nd
from datetime import date ,timedelta
import pandas as pd
import matplotlib.pyplot as plt

class get_stock_futures_continous():
    def __init__(self,stock,start,end):
        self.stock=stock
        self.start=start
        self.end=end
    def get_data(self):
        df=pd.DataFrame()
        df1=pd.DataFrame()
        months=self.end.month-self.start.month
        years=self.end.year-self.start.year
        total_months=months+12*years
        for i in range(total_months):
            if i==0:
              
                df=df.append(nd.get_nsepy_data(self.stock,self.start,self.end)\
                          .get_stock_futures(self.start.year,self.start.month))
                df1=df1.append(nd.get_nsepy_data(self.stock,self.start,self.end)\
                          .get_stock_futures(self.start.year,self.start.month + 1))
            else:
                if (self.start.month+(i-1)%12)%12 !=0:
                    start_month=(self.start.month+(i-1)%12)%12
                    start_year= self.start.year+int((self.start.month+i-1)/12)

                else:
                    start_month=12
                    start_year= self.start.year+int((self.start.month+i-1)/12)-1

                if (self.start.month+(i)%12)%12 !=0:
                    end_month=(self.start.month+(i)%12)%12
                    end_year=self.start.year+int((self.start.month+i)/12)

                else:
                    end_month=12
                    end_year=self.start.year+int((self.start.month+i)/12)-1

                df=df.append(nd.get_nsepy_data(self.stock,nd.get_expiry_date\
                                            (start_year,start_month)+timedelta(1),nd.get_expiry_date\
                                             (end_year,end_month)).\
                                             get_stock_futures(end_year,end_month))
        df=df.append(nd.get_nsepy_data(self.stock,nd.get_expiry_date\
                                            (end_year,end_month)+timedelta(1),self.end).\
                                             get_stock_futures(self.end.year,self.end.month))


        return df


class get_stock_options_continous():
    def __init__(self,stock,start,end,strike,option_type='PE'):
        self.stock=stock
        self.start=start
        self.end=end
        self.strike=strike
        self.option_type=option_type

    def get_data(self):
        df=pd.DataFrame()
        months=self.end.month-self.start.month
        years=self.end.year-self.start.year
        total_months=months+12*years
        
        if self.option_type=='PE':
            for i in range(total_months):
                if i==0:
                  
                    df=df.append(nd.get_nsepy_data(self.stock,self.start,self.end)\
                              .get_stock_put(self.start.year,self.start.month,self.strike))
                else:
                    if (self.start.month+(i-1)%12)%12 !=0:
                        start_month=(self.start.month+(i-1)%12)%12
                        start_year= self.start.year+int((self.start.month+i-1)/12)
    
                    else:
                        start_month=12
                        start_year= self.start.year+int((self.start.month+i-1)/12)-1
    
                    if (self.start.month+(i)%12)%12 !=0:
                        end_month=(self.start.month+(i)%12)%12
                        end_year=self.start.year+int((self.start.month+i)/12)
    
                    else:
                        end_month=12
                        end_year=self.start.year+int((self.start.month+i)/12)-1
    
                    df=df.append(nd.get_nsepy_data(self.stock,nd.get_expiry_date\
                                                (start_year,start_month)+timedelta(1),nd.get_expiry_date\
                                                 (end_year,end_month)).\
                                                 get_stock_put(end_year,end_month,self.strike))
            df=df.append(nd.get_nsepy_data(self.stock,nd.get_expiry_date\
                                (end_year,end_month)+timedelta(1),self.end).\
                                 get_stock_put(self.end.year,self.end.month,self.strike))


        else:
            for i in range(total_months):
                if i==0:
                  
                    df=df.append(nd.get_nsepy_data(self.stock,self.start,self.end)\
                              .get_stock_call(self.start.year,self.start.month,self.strike))
                else:
                    if (self.start.month+(i-1)%12)%12 !=0:
                        start_month=(self.start.month+(i-1)%12)%12
                        start_year= self.start.year+int((self.start.month+i-1)/12)
    
                    else:
                        start_month=12
                        start_year= self.start.year+int((self.start.month+i-1)/12)-1
    
                    if (self.start.month+(i)%12)%12 !=0:
                        end_month=(self.start.month+(i)%12)%12
                        end_year=self.start.year+int((self.start.month+i)/12)

    
                    else:
                        end_month=12
                        end_year=self.start.year+int((self.start.month+i)/12)-1
    
                    df=df.append(nd.get_nsepy_data(self.stock,nd.get_expiry_date\
                                                (start_year,start_month)+timedelta(1),self.end).\
                                                 get_stock_call(end_year,end_month,self.strike))
            print("i == "+str(end_year))
            print("totalmonths == " + str(total_months))

            df=df.append(nd.get_nsepy_data(self.stock,nd.get_expiry_date\
                    (end_year,end_month)+timedelta(1),self.end).\
                     get_stock_call(self.end.year,self.end.month,self.strike))
 
        return df


class get_index_options_call():
    def __init__(self, stock, start, end, strike):
        self.stock = stock
        self.start = start
        self.end = end
        self.strike = strike
        self.option_type = "CE"

    def get_data(self):
        df = pd.DataFrame()
        months = self.end.month - self.start.month
        years = self.end.year - self.start.year
        total_months = months + 12 * years

        if self.option_type == 'PE':
            for i in range(total_months):
                if i == 0:

                    df = df.append(nd.get_nsepy_data(self.stock, self.start, self.end) \
                                   .get_stock_put(self.start.year, self.start.month, self.strike))

                    df = df.append(nd.get_nsepy_data(self.stock, self.start, self.end) \
                                   .get_index_call())
                else:
                    if (self.start.month + (i - 1) % 12) % 12 != 0:
                        start_month = (self.start.month + (i - 1) % 12) % 12
                        start_year = self.start.year + int((self.start.month + i - 1) / 12)

                    else:
                        start_month = 12
                        start_year = self.start.year + int((self.start.month + i - 1) / 12) - 1

                    if (self.start.month + (i) % 12) % 12 != 0:
                        end_month = (self.start.month + (i) % 12) % 12
                        end_year = self.start.year + int((self.start.month + i) / 12)

                    else:
                        end_month = 12
                        end_year = self.start.year + int((self.start.month + i) / 12) - 1

                    df = df.append(nd.get_nsepy_data(self.stock, nd.get_expiry_date \
                        (start_year, start_month) + timedelta(1), nd.get_expiry_date \
                                                         (end_year, end_month)). \
                                   get_stock_put(end_year, end_month, self.strike))
            df = df.append(nd.get_nsepy_data(self.stock, nd.get_expiry_date \
                (end_year, end_month) + timedelta(1), self.end). \
                           get_stock_put(self.end.year, self.end.month, self.strike))


        else:
            for i in range(total_months):
                if i == 0:

                    df = df.append(nd.get_nsepy_data(self.stock, self.start, self.end) \
                                   .get_stock_call(self.start.year, self.start.month, self.strike))
                else:
                    if (self.start.month + (i - 1) % 12) % 12 != 0:
                        start_month = (self.start.month + (i - 1) % 12) % 12
                        start_year = self.start.year + int((self.start.month + i - 1) / 12)

                    else:
                        start_month = 12
                        start_year = self.start.year + int((self.start.month + i - 1) / 12) - 1

                    if (self.start.month + (i) % 12) % 12 != 0:
                        end_month = (self.start.month + (i) % 12) % 12
                        end_year = self.start.year + int((self.start.month + i) / 12)


                    else:
                        end_month = 12
                        end_year = self.start.year + int((self.start.month + i) / 12) - 1

                    df = df.append(nd.get_nsepy_data(self.stock, nd.get_expiry_date \
                        (start_year, start_month) + timedelta(1), self.end). \
                                   get_stock_call(end_year, end_month, self.strike))
            print("i == " + str(end_year))
            print("totalmonths == " + str(total_months))

            df = df.append(nd.get_nsepy_data(self.stock, nd.get_expiry_date \
                (end_year, end_month) + timedelta(1), self.end). \
                           get_stock_call(self.end.year, self.end.month, self.strike))

        return df


class get_index_futures_continous():
    def __init__(self, stock, start, end):
        self.stock = stock
        self.start = start
        self.end = end

    def get_data(self):
        df = pd.DataFrame()
        months = self.end.month - self.start.month
        years = self.end.year - self.start.year
        total_months = months + 12 * years
        for i in range(total_months):
            if i == 0:

                df = df.append(nd.get_nsepy_data(self.stock, self.start, self.end) \
                               .get_index_futures(self.start.year, self.start.month))
            else:
                if (self.start.month + (i - 1) % 12) % 12 != 0:
                    start_month = (self.start.month + (i - 1) % 12) % 12
                    start_year = self.start.year + int((self.start.month + i - 1) / 12)

                else:
                    start_month = 12
                    start_year = self.start.year + int((self.start.month + i - 1) / 12) - 1

                if (self.start.month + (i) % 12) % 12 != 0:
                    end_month = (self.start.month + (i) % 12) % 12
                    end_year = self.start.year + int((self.start.month + i) / 12)

                else:
                    end_month = 12
                    end_year = self.start.year + int((self.start.month + i) / 12) - 1

                df = df.append(nd.get_nsepy_data(self.stock, nd.get_expiry_date \
                    (start_year, start_month) + timedelta(1), nd.get_expiry_date \
                                                     (end_year, end_month)). \
                               get_index_futures(end_year, end_month))
        df = df.append(nd.get_nsepy_data(self.stock, nd.get_expiry_date \
            (end_year, end_month) + timedelta(1), self.end). \
                       get_index_futures(self.end.year, self.end.month))

        return df




stock='ZEEL'
# index='BANKNIFTY'
start=date(2018,6,27)
end=date(2019,4,17)
#expiry_month=3
#expiry_year=2018
#
# data1=get_stock_futures_continous(stock,start,end).get_data()
# data2=get_stock_options_continous(stock,start,end,450,'CE').get_data()
# data3=get_index_options_call(index,start,end,11600).get_data()
# data4=get_index_futures_continous(index,start,end).get_data()
#
# data4.Close.plot()
#
# # data2.Close.plot()
#
# plt.show()
file='/Users/ashok/king/Study/T/system/new_data_pipeline/data-pipeline/data/data_calendarSpreads/zeel.csv'
data1=get_stock_futures_continous(stock,start,end).get_data()['Close']
data1.to_csv(file)
# print(data1.Close)