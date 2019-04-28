import time
import schedule
import requests


def sendMessage(bot_message):
    bot_token = '821213282:AAFb6RRiSYQVzIQ7fsokm0rwz7FcaG0Slw8'
    bot_chatID = '287780369'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()

def report():
    my_balance = 10  ## Replace this number with an API call to fetch your account balance
    my_message = "Current balance is: {}".format(my_balance)  ## Customize your message
    sendMessage(my_message)


schedule.every().day.at("12:00").do(report)
# schedule.every().second.do(report)

while True:
    schedule.run_pending()
    time.sleep(1)
