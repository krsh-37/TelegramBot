#required packages
import telebot
import requests
import os
import json, youtube_dl

#Config vars
token = os.environ['TELEGRAM_TOKEN']
#Intitialize YouTube downloader
ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s%(ext)s'})

#initialise  bot
bot = telebot.TeleBot(token)
x = bot.get_me()
print(x)

#   handling /commands  #

# works when /start is given
@bot.message_handler(commands=['start'])
def send_welcome(message):
  bot.send_message(message.chat.id, "Welcome user")

# works when /motivate is given
@bot.message_handler(commands=['motivate'])
def send_quotes(message):
        quote = requests.request(url='https://api.quotable.io/random',method='get')
        bot.send_message(message.chat.id, quote.json()['content'])

# works when /ytdl <link> is given
@bot.message_handler(commands=['ytdl'])
def down(msg):
    args = msg.text.split()[1]
    try:
        with ydl:
            result = ydl.extract_info(
                args,
                download=False  # We just want to extract the info
            )

        if 'entries' in result:
            # Can be a playlist or a list of videos
            video = result['entries'][0]
        else:
            # Just a video
            video = result
        
        for i in video['formats']:
            link = '<a href=\"' + i['url'] + '\">' + 'link' + '</a>'

            if i.get('format_note'):
                bot.reply_to(msg, 'Quality- ' + i['format_note'] + ': ' + link, parse_mode='HTML')
            else:
                bot.reply_to(msg, link, parse_mode='HTML', disable_notification=True)
    except:
        bot.reply_to(msg, 'This can\'t be downloaded by me')

#pool~start the bot
bot.polling()
