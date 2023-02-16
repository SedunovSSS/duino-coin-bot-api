from telebot import TeleBot
import requests

bot = TeleBot("Your Bot Token")
username = ''
password = ''
balance = 0
main_menu = """Main Menu \n \n ######################### \n \n Main Menu: /main_menu \n Price: /price \n Balance: /balance \n Balance in USD : /balance_dollars \n Balance in BTC : /balance_btc \n Login : /login \n \n #########################"""


@bot.message_handler(content_types=['text'])
def start(message):
    global username
    bot.send_message(message.from_user.id, "Hello, Welcome to Duino Coin API Bot")
    if message.text == '/start':
        bot.send_message(message.from_user.id, "Duino Coin username")
        bot.register_next_step_handler(message, get_name)


@bot.message_handler(content_types=['text'])
def get_name(message):
    global username, balance
    username = message.text
    try:
        data_json = requests.get("http://51.15.127.80/balances.json").json()
        balance = data_json[username]
        bot.send_message(message.from_user.id, main_menu)
        bot.register_next_step_handler(message, if_login)
    except Exception as ex:
        print(ex)
        bot.send_message(message.from_user.id, "Try again")
        bot.send_message(message.from_user.id, "Duino Coin username")
        bot.register_next_step_handler(message, get_name)


@bot.message_handler(content_types=['text'])
def if_login(message):
    global username, balance
    data_json_api = requests.get("http://51.15.127.80/api.json").json()
    price = data_json_api['Duco price']
    if message.text == '/balance':
        data_json = requests.get("http://51.15.127.80/balances.json").json()
        balance = data_json[username]
        bot.send_message(message.from_user.id, f"Duino Coin balance: {balance} DUCO")
        bot.register_next_step_handler(message, if_login)
    elif message.text == '/balance_dollars':
        current_balance = balance
        bot.send_message(message.from_user.id, f"Duino Coin balance: {current_balance*price}$")
        bot.register_next_step_handler(message, if_login)
    elif message.text == '/balance_btc':
        data_json = requests.get("http://51.15.127.80/balances.json").json()
        balance = data_json[username]
        current_balance = balance
        key = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
        data = requests.get(key)
        data = data.json()
        btc = float(data['price'])
        bot.send_message(message.from_user.id, f"Duino Coin balance: {current_balance*price/btc} BTC")
        bot.register_next_step_handler(message, if_login)
    elif message.text == '/price':
        bot.send_message(message.from_user.id, f"Duino Coin price: {price}$")
        bot.register_next_step_handler(message, if_login)
    elif message.text == '/main_menu':
        bot.send_message(message.from_user.id, main_menu)
        bot.register_next_step_handler(message, if_login)
    elif message.text == '/login':
        bot.send_message(message.from_user.id, "Duino Coin username")
        bot.register_next_step_handler(message, get_name)
    else:
        bot.send_message(message.from_user.id, "Command not found. Working commands: /main_menu")
        bot.register_next_step_handler(message, if_login)


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
