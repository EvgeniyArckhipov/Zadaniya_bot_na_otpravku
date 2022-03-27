import telebot
import configure
import requests
import json

TOKEN = str(configure.config['token'])
bot = telebot.TeleBot(TOKEN)
TOKEN_API = str(configure.config['token_api'])

def dobavlenie(message):
    f = open('users.txt', 'a')
    f.write(message.chat.username+'\n'+str(message.chat.id)+'\n')
    f.close()

@bot.message_handler(commands=['start', 'help'])
def comm(message):
    a = message.chat.username
    bot.send_message(message.chat.id, f"Приветствую, {a}!\nЯ умею конвертировать валюту.\n"
                                      f"Для этого Вам необходимо ввести данные следующим образом:\n <название валюты, цену которой хотите узнать>"
                                      f"<имя валюты, в которой надо узнать цену первой валюты> <количество первой валюты>.\n"
                                      f"Для того, чтобы узнать список доступных валют введите команду: /values")
    dobavlenie(message)

@bot.message_handler(commands=['values'])
def val(message):
    nal = requests.get(f'http://api.exchangeratesapi.io/v1/latest?access_key={TOKEN_API}&base=EUR&symbols=USD,AUD,CAD,PLN,MXN')
    slovar_values = list(json.loads(nal.content)["rates"].keys())
    known_currency = ['USD', 'AUD', 'CAD', 'PLN', 'MXN']
    w = len(slovar_values)
    kol = 0
    for key in range(w):
        if slovar_values[key] in known_currency:
            if slovar_values[key] == 'USD':
                slovar_values[key]+=' : доллар'
            elif slovar_values[key] == 'AUD':
                slovar_values[key]+=' : австралийский доллар'
            elif slovar_values[key] == 'CAD':
                slovar_values[key]+=' : канадский доллар'
            elif slovar_values[key] == 'PLN':
                slovar_values[key]+=' : польские золотые'
            elif slovar_values[key] == 'PLN':
                slovar_values[key]+=' : польсие золотые'
            elif slovar_values[key] == 'MXN':
                slovar_values[key]+=' : мексиканские песо'
        else:
            kol+=1

    otvet = '\n'.join(slovar_values)
    if kol:
        bot.send_message(message.chat.id,
                         f"Доступные валюты:\n{otvet}\nКоличество позиций,которые будут добавлены: {kol}")
        bot.send_message(message.chat.id, f"Доступные валюты:\n{otvet}")
    else:
        bot.send_message(message.chat.id, f"Доступные валюты:\n{otvet}")


@bot.message_handler(content_types = ['text'])
def otvet(message):
    base, quote, amount = message.text.split()
    if base == 'EUR':
        r = requests.get(f'http://api.exchangeratesapi.io/v1/latest?access_key={TOKEN_API}&base=EUR&symbols=USD,AUD,CAD,PLN,MXN')
        otvet_api = json.loads(r.content)['rates'][quote]*float(amount)
        itog = f'Цена {amount} {base} в {quote}={otvet_api}'
        bot.send_message(message.chat.id, itog)
    else:
        bot.send_message(message.chat.id, 'В данный момент возможно узнать только цену ЕВРО '
                                          '(API не дает менять базовую валюту при запросе, дает ответ только по ЕВРО)')



#@bot.message_handler(content_types = ['text']) #.message_handler - обработчик поступающих сообщщений
#def function_name(message):
#    if message.text.lower() in ['привет','приветик']:
#        bot.send_message(message.chat.id, "Привет, "+message.chat.username+"!")
 #   else:
#        bot.send_message(message.chat.id, "Нужно поздороваться")
    #dobavlenie(message)

#@bot.message_handler(content_types = ['photo'])#.message_handler - обработчик поступающих сообщщений
#def function_name(message):
#            bot.send_message(message.chat.id, "Это фото!)")



bot.polling(none_stop=True)  # запуск постоянной работы


