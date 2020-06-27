#required packages
import telebot
import requests
import os
import json
from time import sleep

#Config vars
with open('config.json') as f:
  token = json.load(f)

#initialise  bot
bot = telebot.TeleBot(token['telegramToken'])
x = bot.get_me()
print(x)

#handling /commands
@bot.message_handler(commands=['motivate'])
def send_welc(message):
        quote = requests.request(url='https://api.quotable.io/random',method='get')
        bot.send_message(message.chat.id, quote.json()['content'])

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
  bot.send_message(message.chat.id, "Welcome user")

#pool~start the bot
bot.polling()
