import telebot
from telebot import types

bot = telebot.TeleBot('8212668348:AAGE8zi0XtoX5mnKGj5g3n2-32qBODImugA')

@bot.message_handler(commands=['start'])
def main(message):
    
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Состав', callback_data='team')
    markup.row(btn1)
    btn2 = types.InlineKeyboardButton('Тренировка', callback_data='training')
    markup.row(btn2)

    bot.send_message(message.chat.id, 'Привет!', reply_markup=markup)

@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'team':
        team_markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('Добавить', callback_data='add_player')
        team_markup.row(btn1)
        btn2 = types.InlineKeyboardButton('Изменить', callback_data='edit_player')
        team_markup.row(btn2)
        btn3 = types.InlineKeyboardButton('Удалить', callback_data='delete_player')
        team_markup.row(btn3)
        btn4 = types.InlineKeyboardButton('Назад', callback_data='back_from_team_settings')
        team_markup.row(btn4)
        with open('team.txt', 'r') as file:
            content = file.read()
            bot.send_message(callback.message.chat.id, content, reply_markup=team_markup)
    if callback.data == 'training':
        bot.send_message(callback.message.chat.id, 'Данные о тренировке')
    if callback.data == 'add_player':
        bot.send_message(callback.message.chat.id, 'Введите имя и фамилию игрока')
        print(callback.message.text)

bot.polling(none_stop=True)
