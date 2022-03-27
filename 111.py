import telebot
import configure
import requests
import json

TOKEN = str(configure.config['token'])
bot = telebot.TeleBot(TOKEN)
TOKEN_API = str(configure.config['token_api'])

base = 'USD'
quote = 'MXN'

nal = requests.get(
    f'http://api.exchangeratesapi.io/v1/latest?access_key={TOKEN_API}&base=EUR&symbols=USD,AUD,CAD,PLN,MXN')
slovar_values = json.loads(nal.content)
print(slovar_values)
#w = slovar_values.copy()
#n = len(w)
#for i in range(n):
#    if slovar_values[i] in w:
#        slovar_values[i]+='жопа'
#print(slovar_values)

