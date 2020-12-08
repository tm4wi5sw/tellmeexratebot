# tellmeexratebot
# python 3.8.1
import telebot
import requests
import time
from extensions import ConvertionException, CryptoConverter
from config import TOKEN, helplist, keys


bot = telebot.TeleBot(TOKEN)

# Обрабатываются все сообщения содержащие команды '/start' or '/help'.
@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    for s in helplist:
        bot.send_message(message.chat.id, s)
 
# Обрабатываются все сообщения содержащие команды '/values'.
@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
            text = '\n'.join((text, key, ))
    bot.reply_to(message, text)
 
# Обрабатывается все текстовые сообщения
@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
                raise ConvertionException('Неправильное колличество параметров!')

        quote, base, amount = values

        total_base = CryptoConverter.get_price(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать комманду\n{e}')
    else:
        text = f'цена {amount} {quote} в {base}: {total_base}'
        bot.send_message(message.chat.id, text)

try:
    bot.polling()
except requests.exceptions.ReadTimeout:
    time.sleep(3)
