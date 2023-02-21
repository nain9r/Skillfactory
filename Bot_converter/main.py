import telebot
from telebot import types
from extensions import Converter, APIException
from config import TOKEN, exchanges

bot = telebot.TeleBot(TOKEN)
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
item1 = types.KeyboardButton('Доллар')
item2 = types.KeyboardButton('Евро')
item3 = types.KeyboardButton('Фунт')
markup.add(item1)
markup.add(item2)
markup.add(item3)


@bot.message_handler(commands=['convert'])
def values(message):
    bot.send_message(message.chat.id, 'Выберите исходную валюту из предложенного меню, '
                                      'либо введите ее название самостоятельно', reply_markup=markup)
    bot.register_next_step_handler(message, base_handler)


def base_handler(message):
    if message.text in exchanges.keys():
        base = message.text
        bot.send_message(message.chat.id, 'Выберите валюту, в которую нужно конвертировать')
        bot.register_next_step_handler(message, sym_handler, base)
    else:
        bot.send_message(message.chat.id, 'Некорректный ввод. Используйте кнопки '
                                          'или введите название валюты правильно (как в меню)')
        bot.register_next_step_handler(message, base_handler)


def sym_handler(message, base):
    if message.text in exchanges.keys():
        sym = message.text
        hide_markup = telebot.types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'Введите количество', reply_markup=hide_markup)
        bot.register_next_step_handler(message, amount_handler, base, sym)
    else:
        bot.send_message(message.chat.id, 'Некорректный ввод. Используйте кнопки или '
                                          'введите название валюты правильно (как в меню)')
        bot.register_next_step_handler(message, sym_handler, base)


def amount_handler(message, base, sym):
    if message.text.isdigit():
        try:
            amount = message.text
            price = Converter.get_price(base, sym, amount)
        except APIException as e:
            bot.send_message(message.chat.id, f"Ошибка: {e}")
        else:
            bot.send_message(message.chat.id, f'Результат конвертации: {price}')
    else:
        bot.send_message(message.chat.id, 'Введите цифру!')
        bot.register_next_step_handler(message, amount_handler, base, sym)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, text='Вас приветствует бот-конвертер! Для конвертации используйте команду '
                                           '/convert \nДля просмотра доступных валют используйте команду /values')


@bot.message_handler(commands=['values'])
def values(message):
    text = 'Доступные валюты:'
    for i in exchanges.keys():
        text = '\n'.join((text, i))
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text'])
def converter(message):
    bot.send_message(message.chat.id, 'Используйте команды /convert или /values')


bot.polling()
