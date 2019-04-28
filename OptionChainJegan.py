import requests
from bs4 import BeautifulSoup

# Get all get possible expiry date details for the given script
def get_expiry_from_option_chain (symbol):

    # Base url page for the symbole with default expiry date
    Base_url = "https://www.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp?symbol=" + symbol + "&date=-"

    # Load the page and sent to HTML parse
    page = requests.get(Base_url)
    soup = BeautifulSoup(page.content, 'html.parser')

    # Locate where expiry date details are available
    locate_expiry_point = soup.find(id="date")
    # Convert as rows based on tag option
    expiry_rows = locate_expiry_point.find_all('option')

    index = 0
    expiry_list = []
    for each_row in expiry_rows:
        # skip first row as it does not have value
        if index <= 0:
            index = index + 1
            continue
        index = index + 1
        # Remove HTML tag and save to list
        expiry_list.append(BeautifulSoup(str(each_row), 'html.parser').get_text())

    print(expiry_list)
    return expiry_list # return list

def get_strike_price_from_option_chain(symbol, expdate):

    Base_url = "https://www.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp?symbol=" + symbol + "&date=" + expdate

    page = requests.get(Base_url)
    soup = BeautifulSoup(page.content, 'html.parser')

    table_cls_2 = soup.find(id="octable")
    req_row = table_cls_2.find_all('tr')

    strike_price_list = []

    for row_number, tr_nos in enumerate(req_row):

        # This ensures that we use only the rows with values
        if row_number <= 1 or row_number == len(req_row) - 1:
            continue

        td_columns = tr_nos.find_all('td')
        strike_price = int(float(BeautifulSoup(str(td_columns[11]), 'html.parser').get_text()))
        strike_price_list.append(strike_price)

    print (strike_price_list)
    return strike_price_list

def get_OI_from_option_chain(symbol, expdate):

    Base_url = "https://www.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp?symbol=" + symbol + "&date=" + expdate

    page = requests.get(Base_url)
    soup = BeautifulSoup(page.content, 'html.parser')

    table_cls_2 = soup.find(id="octable")
    req_row = table_cls_2.find_all('tr')

    strike_price_list = []

    for row_number, tr_nos in enumerate(req_row):

        # This ensures that we use only the rows with values
        if row_number <= 1 or row_number == len(req_row) - 1:
            continue

        td_columns = tr_nos.find_all('td')
        strike_price = int(float(BeautifulSoup(str(td_columns[11]), 'html.parser').get_text()))
        if strike_price == 450:
            oi_ce = BeautifulSoup(str(td_columns[21]), 'html.parser').get_text()
            oi_pe = BeautifulSoup(str(td_columns[1]), 'html.parser').get_text()
            print(oi_ce)
            print(oi_pe)
            strike_price_list.append(strike_price)

    print (strike_price_list)
    return strike_price_list

def get_OI_strike_price(symbol, strikePrice, expdate):

    Base_url = "https://www.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionDates.jsp?symbol=" + symbol + "&instrument=OPTSTK&strike="+ strikePrice

    page = requests.get(Base_url)
    soup = BeautifulSoup(page.content, 'html.parser')

    table_cls_2 = soup.find(id="octable")
    req_row = table_cls_2.find_all('tr')

    strike_price_list = []

    for row_number, tr_nos in enumerate(req_row):

        # This ensures that we use only the rows with values
        if row_number <= 1 or row_number == len(req_row) - 1:
            continue

        td_columns = tr_nos.find_all('td')
        expiry_date = BeautifulSoup(str(td_columns[11]), 'html.parser').get_text()
        print(expiry_date)
        if expiry_date == '25APR2019':
            oi_ce = BeautifulSoup(str(td_columns[21]), 'html.parser').get_text()
            oi_pe = BeautifulSoup(str(td_columns[1]), 'html.parser').get_text()
            change_oi_ce = BeautifulSoup(str(td_columns[20]), 'html.parser').get_text()
            change_oi_pe = BeautifulSoup(str(td_columns[2]), 'html.parser').get_text()

            print("oi_ce = "+oi_ce)
            print("oi_pe = "+oi_pe)
            print("change_oi_ce = "+change_oi_ce)
            print("change_oi_pe = "+change_oi_pe)
            strike_price_list.append(expiry_date)
    print (strike_price_list)
    return strike_price_list

# get_expiry_from_option_chain('ZEEL')

def write_to_excel():
    sd=""

scrip_name='ZEEL'
exp_date='25APR2019'
strikePrice='410'
# get_OI_from_option_chain(scrip_name, exp_date)
get_OI_strike_price(scrip_name, strikePrice, exp_date)