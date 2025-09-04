import telebot
from datetime import date
from telebot import types
from telebot.types import ReplyKeyboardMarkup, ReplyKeyboardRemove
import os
import json

bot = telebot.TeleBot('8212668348:AAGE8zi0XtoX5mnKGj5g3n2-32qBODImugA')

class training:
    def __init__(self):
        self.training_date = str(date.today())
        self.training_time = ''
        self.training_type = ''
        self.training_players = []    
    

cur_training = training()

class States:
    MAIN_MENU = 0
    WAITING_FULL_NAME_FOR_ADD = 1
    WAITING_FULL_NAME_FOR_EDIT = 2
    WAITING_PLAYER_ID_FOR_EDIT = 3
    WAITING_PLAYER_ID_FOR_DELETE = 4
    WAITING_TRAINING_TIME = 5
    WAITING_TRAINING_TYPE = 6
    WAITING_TRAINING_PLAYERS_LIST = 7

def get_lines_count(path):
    count = 0
    with open(path, 'r') as file:
        for line in file:
            count += 1
    return count

def get_arr_from_file(path):
    players = []
    with open(path, 'r') as file:
        for line in file:
            players.append(line)
    return players

def save_team_file(array, path):
    with open(path, 'w', encoding='utf-8') as file:
        for el in array:
            file.write(el)

def get_str_from_arr(array):
    res = ''
    count = 0
    for el in array:
        res += str(count + 1) + '. ' + el 
        count += 1
    return res

#tconv = lambda x: time.strftime("%H:%M:%S %d.%m.%Y", time.localtime(x))

def make_main_menu():
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Состав', callback_data='team')
    markup.row(btn1)
    btn2 = types.InlineKeyboardButton('Тренировка', callback_data='training')
    markup.row(btn2)
    return markup

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
team_list = get_arr_from_file('team.txt')  
temp_data = {}  

@bot.message_handler(commands=['start'])
def start(message):

    user_states[message.chat.id] = States.MAIN_MENU
    bot.send_message(message.chat.id, 'Привет!', reply_markup=make_main_menu())

@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):

    if callback.data == 'team':
        bot.send_message(callback.message.chat.id, get_str_from_arr(team_list), reply_markup=make_team_menu())
    elif callback.data == 'add_player':
        bot.send_message(callback.message.chat.id, 'Введите фамилию и имя игрока')
        user_states[callback.message.chat.id] = States.WAITING_FULL_NAME_FOR_ADD
    elif callback.data == 'edit_player':
        bot.send_message(callback.message.chat.id, get_str_from_arr(team_list) + '\n\n' + 'Введите порядковый номер игрока')
        user_states[callback.message.chat.id] = States.WAITING_PLAYER_ID_FOR_EDIT
    elif callback.data == 'delete_player':
        bot.send_message(callback.message.chat.id, get_str_from_arr(team_list) + '\n\n' + 'Введите порядковый номер игрока')
        user_states[callback.message.chat.id] = States.WAITING_PLAYER_ID_FOR_DELETE
    elif callback.data == 'back_from_team_settings':
        user_states[callback.message.chat.id] = States.MAIN_MENU
        save_team_file(team_list, 'team.txt')
        bot.send_message(callback.message.chat.id, 'Изменения сохранены успешно')
        bot.send_message(callback.message.chat.id, 'Основное меню', reply_markup=make_main_menu())
    elif callback.data == 'training':
        bot.send_message(callback.message.chat.id, 'Введите время тренировки в формате ЧЧ:ММ - ЧЧ:ММ')
        user_states[callback.message.chat.id] = States.WAITING_TRAINING_TIME




@bot.message_handler(content_types=['text'])
def handle_text(message):
    
    global temp_data

    if user_states.get(message.chat.id) == States.WAITING_FULL_NAME_FOR_ADD:
        team_list.append(message.text + '\n')
        bot.send_message(message.chat.id, 'Игрок успешно добавлен')
        bot.send_message(message.chat.id, get_str_from_arr(team_list), reply_markup=make_team_menu())
    elif user_states.get(message.chat.id) == States.WAITING_PLAYER_ID_FOR_EDIT:
        temp_data[message.chat.id] = {'player_id': int(message.text)}
        user_states[message.chat.id] = States.WAITING_FULL_NAME_FOR_EDIT
        bot.send_message(message.chat.id, 'Введите фамилию и имя игрока')
    elif user_states.get(message.chat.id) == States.WAITING_FULL_NAME_FOR_EDIT:
        team_list[temp_data[message.chat.id]['player_id'] - 1] = message.text + '\n'
        bot.send_message(message.chat.id, 'Запись исправлена успешно')
        bot.send_message(message.chat.id, get_str_from_arr(team_list), reply_markup=make_team_menu())
    elif user_states.get(message.chat.id) == States.WAITING_PLAYER_ID_FOR_DELETE:
        team_list.pop(int(message.text) - 1)
        bot.send_message(message.chat.id, 'Игрок удален успешно')
        bot.send_message(message.chat.id, get_str_from_arr(team_list), reply_markup=make_team_menu())
    elif user_states.get(message.chat.id) == States.WAITING_TRAINING_TIME:
        temp_data[message.chat.id] = {'training_time': message.text}
        cur_training.training_time = message.text
        user_states[message.chat.id] = States.WAITING_TRAINING_TYPE
        bot.send_message(message.chat.id, 'Введите тип тренировки\n1. Беговая\n2. Отработка паса\n3. Отработка ударов')
    elif user_states.get(message.chat.id) == States.WAITING_TRAINING_TYPE:
        training_time = temp_data[message.chat.id]['training_time']
        temp_data = {'training_time': training_time, 'training_type': int(message.text)}
        cur_training.training_type = int(message.text)
        user_states[message.chat.id] = States.WAITING_TRAINING_PLAYERS_LIST
        bot.send_message(message.chat.id, 'Отметьте присутствующих игроков в опросе')
        if len(team_list) > 12:
            opt = team_list[:12]
        else:
            opt = team_list
        bot.send_poll(
            chat_id=message.chat.id,
            question="✅ Отметьте того, кто был на тренировке:",
            options=opt,
            is_anonymous=False,
            allows_multiple_answers=True,  
            type='regular'
        )
        user_states[message.chat.id] = States.MAIN_MENU    

@bot.poll_answer_handler()
def handle_poll_answer(poll_answer):
    bot.send_message(poll_answer.user.id, 'Ваш ответ записан')
    option_ids = poll_answer.option_ids  
    players_on_training = []
    for el in option_ids:
        players_on_training.append(team_list[el][:-1])
    cur_training.training_players = players_on_training
    cur_training_dict = cur_training.__dict__
    with open("training_settings.json", "w", encoding='utf-8') as f:
        json.dump(cur_training_dict, f, ensure_ascii=False,)
    bot.send_message(poll_answer.user.id, 'Информация о тренировке успешно записана', reply_markup=make_main_menu())
    with open('training_settings.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

bot.polling(none_stop=True)
