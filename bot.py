import telebot
from telebot import types
from telebot.types import ReplyKeyboardMarkup, ReplyKeyboardRemove
import os


bot = telebot.TeleBot('8212668348:AAGE8zi0XtoX5mnKGj5g3n2-32qBODImugA')  

class States:
    MAIN_MENU = 0
    WAITING_FULL_NAME_FOR_ADD = 1
    WAITING_FULL_NAME_FOR_EDIT = 2
    WAITING_PLAYER_ID_FOR_EDIT = 3
    WAITING_PLAYER_ID_FOR_DELETE = 4

def get_lines_count(path):
    count = 0
    with open(path, 'r') as file:
        for line in file:
            count += 1
    return count

def get_dict_from_file(path):
    players = {}
    count = 0
    with open(path, 'r') as file:
        for line in file:
            cur_str = line
            for ch in line:
                cur_str = cur_str[1:]
                if ch == ' ':
                    break
            players[count + 1] = cur_str
            count += 1
    return players

def save_team_file(dictionary, path):
    with open(path, 'w', encoding='utf-8') as file:
        for key, value in dictionary.items():
            file.write(f"{key}. {value}")

def get_str_from_dict(dictionary):
    str = ''
    for key, value in dictionary.items():
        str += f"{key}. {value}"
    return str

def make_team_menu():
    team_markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Добавить', callback_data='add_player')
    team_markup.row(btn1)
    btn2 = types.InlineKeyboardButton('Изменить', callback_data='edit_player')
    team_markup.row(btn2)
    btn3 = types.InlineKeyboardButton('Удалить', callback_data='delete_player')
    team_markup.row(btn3)
    btn4 = types.InlineKeyboardButton('Назад', callback_data='back_from_team_settings')
    team_markup.row(btn4)
    return team_markup

user_states = {}
team_list = get_dict_from_file('team.txt')  
temp_data = {}  

@bot.message_handler(commands=['start'])
def start(message):

    user_states[message.chat.id] = States.MAIN_MENU
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Состав', callback_data='team')
    markup.row(btn1)
    btn2 = types.InlineKeyboardButton('Тренировка', callback_data='training')
    markup.row(btn2)

    bot.send_message(message.chat.id, 'Привет!', reply_markup=markup)

@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):

    if callback.data == 'team':
        bot.send_message(callback.message.chat.id, get_str_from_dict(team_list), reply_markup=make_team_menu())
    elif callback.data == 'add_player':
        bot.send_message(callback.message.chat.id, 'Введите фамилию и имя игрока')
        user_states[callback.message.chat.id] = States.WAITING_FULL_NAME_FOR_ADD
    elif callback.data == 'edit_player':
        bot.send_message(callback.message.chat.id, get_str_from_dict(team_list) + '\n\n' + 'Введите порядковый номер игрока')
        user_states[callback.message.chat.id] = States.WAITING_PLAYER_ID_FOR_EDIT
    elif callback.data == 'delete_player':
        bot.send_message(callback.message.chat.id, get_str_from_dict(team_list) + '\n\n' + 'Введите порядковый номер игрока')
        user_states[callback.message.chat.id] = States.WAITING_PLAYER_ID_FOR_DELETE
    elif callback.data == 'back_from_team_settings':
        user_states[callback.message.chat.id] = States.MAIN_MENU
        save_team_file(team_list, 'team.txt')
        bot.send_message(callback.message.chat.id, 'Изменения сохранены успешно')


@bot.message_handler(content_types=['text'])
def handle_text(message):
    if user_states.get(message.chat.id) == States.WAITING_FULL_NAME_FOR_ADD:
        team_list[get_lines_count('team.txt') + 1] = message.text + '\n'
        bot.send_message(message.chat.id, 'Игрок успешно добавлен')
        bot.send_message(message.chat.id, get_str_from_dict(team_list), reply_markup=make_team_menu())
    elif user_states.get(message.chat.id) == States.WAITING_PLAYER_ID_FOR_EDIT:
        temp_data[message.chat.id] = {'player_id': int(message.text)}
        user_states[message.chat.id] = States.WAITING_FULL_NAME_FOR_EDIT
        bot.send_message(message.chat.id, 'Введите фамилию и имя игрока')
    elif user_states.get(message.chat.id) == States.WAITING_FULL_NAME_FOR_EDIT:
        team_list[temp_data[message.chat.id]['player_id']] = message.text + '\n'
        bot.send_message(message.chat.id, 'Запись исправлена успешно')
        bot.send_message(message.chat.id, get_str_from_dict(team_list), reply_markup=make_team_menu())
    elif user_states.get(message.chat.id) == States.WAITING_PLAYER_ID_FOR_DELETE:
        del team_list[int(message.text)]
        bot.send_message(message.chat.id, 'Игрок удален успешно')
        bot.send_message(message.chat.id, get_str_from_dict(team_list), reply_markup=make_team_menu())


bot.polling(none_stop=True)
