import telebot
from telebot import types

token = '2138237247:AAGOfmz-0-_luhmENRbxDDx5v6HFaLnfIrU'

pizza_size = ''
payment = ''
#age = 0

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Вас приветствует бот-ассистент. Я помогу Вам выбрать и заказать пиццу! Чтобы начать делать заказ введи команду /order")

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    if message.text == 'Привет':
        bot.reply_to(message, 'Привет дорогой любитель пиццы!')
    elif message.text == 'hi':
        bot.reply_to(message, 'Hello dear pizza lover!')
    elif message.text == '/order':
        bot.send_message(message.from_user.id, "Какую Вы хотите пиццу? Большую или маленькую?")
        bot.register_next_step_handler(message, reg_pizza_size)

def reg_pizza_size(message):
    global pizza_size
    pizza_size = message.text
    bot.send_message(message.from_user.id, "Как Вы будите платить? Наличкой или картой?")
    bot.register_next_step_handler(message, reg_payment)

def reg_payment(message):
    global payment
    payment = message.text

    keyboard = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
    keyboard.add(key_yes)
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
    keyboard.add(key_no)
    question = 'Вы хотите ' + pizza_size + ' пиццу, оплата - ' + payment + '?'
    bot.send_message(message.from_user.id, text = question, reply_markup=keyboard)
    
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes":
        bot.send_message(call.message.chat.id, "Заказ принят. Ожидайте подтверждения.")
    elif call.data == "no":
        bot.send_message(call.message.chat.id, "Давайте попробуем еще раз!")
        bot.send_message(call.message.chat.id, "Какую Вы хотите пиццу? Большую или маленькую?")
        bot.register_next_step_handler(call.message, reg_pizza_size)

bot.polling()