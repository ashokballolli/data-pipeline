import time
import schedule
import requests

bot_token = '821213282:AAFb6RRiSYQVzIQ7fsokm0rwz7FcaG0Slw8'
bot_chatID = '287780369'

def sendMessage(bot_message):
    # bot_message="*bold* _italic_ `fixed width font` [link](http://google.com)."
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
    response = requests.get(send_text)
    return response.json()

# test = sendMessage("Testing Telegram bot")
# print(test)
# bot.send_message(chat_id=chat_id,
#                  text="*bold* _italic_ `fixed width font` [link](http://google.com).",
#                  parse_mode=telegram.ParseMode.MARKDOWN)
