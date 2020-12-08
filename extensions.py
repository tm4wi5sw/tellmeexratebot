import requests # импортируем наш знакомый модуль
import json
from config import keys, api_key_in_cryptocompare


class ConvertionException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str): #message: telebot.types.Message
        if quote == base:
                raise ConvertionException(f'Невозможно перевести одинаковые валюты {base}!') # хотя правильный ответ здесь равен amount-у, в одном рубле - один рубль

        try:
                quote_ticker = keys[quote]
        except KeyError:
                raise ConvertionException(f'Не удалось обработать валюту "{quote}"')

        try:
                base_ticker = keys[base]
        except KeyError:
                raise ConvertionException(f'Не удалось обработать валюту "{base}"')

        try:
                amount = float(amount)
        except ValueError:
                raise ConvertionException(f'Не удалось обработать колличество "{amount}"')

        url = "https://min-api.cryptocompare.com/data/price"

        payload = {
        "api_key": api_key_in_cryptocompare,
        "fsym": quote_ticker,
        "tsyms": base_ticker
        }

        result = requests.get(url, params=payload).json()

        total_base = result[keys[base]] * amount

        return total_base