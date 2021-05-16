# - *- coding: utf- 8 - *-
from importlib import reload

import telebot
from random import randint
from telebot.types import Message
import time
import datetime
from telebot import types
import threading
import sqlite3
# import SingleClasses
import re
import sys
import json
import requests

reload(sys)
# sys.setdefaultencoding('utf-8')

url_to_api = 'http://localhost:8000/api/smartquerest/'

dict_id_user1 = dict()
dict_id_user2 = dict()

dict_id_worker1 = dict()
dict_id_worker2 = dict()

fl = '1335509834:AAGrGBrUn8l9NTm8IfN5X2AvrgVQ-whkf98'
token = '1335509834:AAGrGBrUn8l9NTm8IfN5X2AvrgVQ-whkf98'
bot = telebot.TeleBot(token)
# list_admins = [321354512, 914239664]  # Список id администраторов
#
# # Список гостей
# current_guests = []
user_key_to_give = 141400000000
worker_key_to_give = 1500000000




def admin_notification(message: Message, bot_text="---"):
    """
    Отправка уведомлений администратору
    :param message:
    :param bot_text:
    :return:
    """
    to_logs(message, bot_text)
    # for admin_id in list_admins:
    #     bot.send_message(admin_id, f'{message.from_user.id} @{message.from_user.username} '
    #                                f'{message.from_user.first_name} {message.from_user.last_name} {message.text} \n')


def to_logs(message: Message, bot_text: str):
    """
    В логи
    :param message:
    :param bot_text:
    :return:
    """
    f = open("logs.txt", "a")
    f.write(f'{datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")} '
            f'ID: {message.from_user.id} @{message.from_user.username} '
            f'{message.from_user.first_name} {message.from_user.last_name} {message.text} \n'
            f'bot answer: {bot_text} \n')
    f.close()


def to_logs_text(text: str):
    f = open("logs.txt", "a")
    f.write("Вылетело, except в working_bot\n")
    f.close()


def incorrect_message(message: Message):
    """
    Неккоректное сообщение
    :param message:
    :return:
    """
    admin_notification(message, "Некорректная команда")
    bot.send_message(message.from_user.id, "Некорректная команда")


def send_message_by_id(tg_id: int, message_text: str):
    """
    Отправка сообщений (для укорачивания кода на месте)
    :param message:
    :param message_text:
    :param to_admins:
    :return:
    """
    # if to_admins:
    #     admin_notification(message, message_text)
    bot.send_message(tg_id, message_text)


def send_message(message: Message, message_text: str, to_admins=True):
    """
    Отправка сообщений (для укорачивания кода на месте)
    :param message:
    :param message_text:
    :param to_admins:
    :return:
    """
    if to_admins:
        admin_notification(message, message_text)
    send_message_by_id(message.from_user.id, message_text)


@bot.message_handler(commands=['test'])
def lol(message: Message):
    response = requests.get("http://178.154.213.228:8000/api/smartquerest/cabinets_by_name/")
    checkboxes = json.loads(response.json())['cabs']
    bot.send_message(message.from_user.id, str(checkboxes))


@bot.message_handler(commands=['help', 'start'])
def show_help(message: Message):
    """
    Вывод помощи
    :param message:
    :return:
    """
    global dict_id_user1, dict_id_worker1
    # btn_my_site2 = types.InlineKeyboardButton(text='/start')
    if (message.from_user.id not in dict_id_user1) and (message.from_user.id not in dict_id_worker1):
        btn_my_site1 = types.InlineKeyboardButton(text='зарегистрироваться в качестве посетителя')
        btn_my_site2 = types.InlineKeyboardButton(text='зарегистрироваться в качестве работника')
        button_hi3 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_hi3.add(btn_my_site1)
        button_hi3.add(btn_my_site2)
        answer = f'Приветствую {message.from_user.last_name} ' \
                 f'{message.from_user.first_name} клиент электронной очереди! \n'
        # admin_notification(message)
        bot.send_message(message.from_user.id, answer, reply_markup=button_hi3)
    else:
        if message.from_user.id in dict_id_user1:
            bot.register_next_step_handler(message, reg_user)
            # btn_my_site12 = types.InlineKeyboardButton(text='положение в очереди')
            # button_hi30 = types.ReplyKeyboardMarkup(resize_keyboard=True)
            # button_hi30.add(btn_my_site12)
            # answer = f'{message.from_user.last_name} ' \
            #          f'{message.from_user.first_name} уже зарегистрирован в качестве посетителя \n'
            # bot.send_message(message.from_user.id, answer, reply_markup=button_hi30)
        if message.from_user.id in dict_id_worker1:
            bot.register_next_step_handler(message, reg_worker)
            # btn_my_site122 = types.InlineKeyboardButton(text='следующий гость')
            # button_hi303 = types.ReplyKeyboardMarkup(resize_keyboard=True)
            # button_hi303.add(btn_my_site122)
            # answer = f'{message.from_user.last_name} ' \
            #          f'{message.from_user.first_name} уже зарегистрирован в качестве работника \n'
            # bot.send_message(message.from_user.id, answer, reply_markup=button_hi303)


def reg_user(message: Message):
    global dict_id_user1, dict_id_worker1, dict_id_user2, dict_id_user2

    try:
        cabs_data = json.dumps(int(message.text))
        second = {'json_s': cabs_data}
        clientnumber = requests.post("http://178.154.213.228:8000/api/smartquerest/check_guest_key/",
                                     data=second)
        temp = json.loads(clientnumber.text)
        if temp == "\"True\"":
            dict_id_user1[message.from_user.id] = int(message.text)
            dict_id_user2[int(message.text)] = message.from_user.id
            answer = "Зарегистрированы"
            btn_my_site123 = types.InlineKeyboardButton(text='сколько посетителей передомной')
            btn_my_site543 = types.InlineKeyboardButton(text='мои кабинеты')
            btn_my_site765 = types.InlineKeyboardButton(text='выход')
            # button_hi.add(btn_my_site)
            button_hi223 = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button_hi223.add(btn_my_site123)
            button_hi223.add(btn_my_site543)
            button_hi223.add(btn_my_site765)
            bot.send_message(message.from_user.id, answer, reply_markup=button_hi223)
        else:
            answer = "Неправильный код"
            btn_my_site8 = types.InlineKeyboardButton(text='Отправить код еще раз')
            btn_my_site9 = types.InlineKeyboardButton(text='Выйти в главное меню')
            button_hi273 = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button_hi273.add(btn_my_site8)
            button_hi273.add(btn_my_site9)
            bot.send_message(message.from_user.id, answer, reply_markup=button_hi273)

    except Exception as e:
        send_message(message, f"Что-то не так: {repr(e)}")

def reg_worker(message: Message):
    try:
        # # res = schedule.set_worker_id(int(message.text), message.from_user.id)
        # cabs_data = json.dumps(int(message.text))
        # second = {'json_s': cabs_data}
        # clientnumber = requests.post("http://178.154.213.228:8000/api/smartquerest/check_cabinet_key/",
        #                              data=second)
        # temp = json.loads(clientnumber.text)
        temp = '\"True\"'
        print("\"True\"")
        if temp == '\"True\"':
            dict_id_worker1[message.from_user.id] = int(message.text)
            dict_id_worker2[int(message.text)] = message.from_user.id
            answer = "Зарегистрированы"
            btn_my_site1 = types.InlineKeyboardButton(text='Следующий посетитель')
            btn_my_site123 = types.InlineKeyboardButton(text='сколько людей в очереди')
            btn_my_site765 = types.InlineKeyboardButton(text='выход')
            button_hi3 = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button_hi3.add(btn_my_site1)
            button_hi3.add(btn_my_site123)
            button_hi3.add(btn_my_site765)
            bot.send_message(message.from_user.id, answer, reply_markup=button_hi3)
        else:
            answer = "Неправильный код"
            btn_my_site8 = types.InlineKeyboardButton(text='Отправить код еще раз')
            btn_my_site9 = types.InlineKeyboardButton(text='Выйти в главное меню')
            button_hi273 = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button_hi273.add(btn_my_site8)
            button_hi273.add(btn_my_site9)
            bot.send_message(message.from_user.id, answer, reply_markup=button_hi273)


    except Exception as e:
        send_message(message, f"Что-то не так: {repr(e)}")

@bot.message_handler(content_types=['text'])
def text_parse(message: Message):
    """
    Вывод помощи
    :param message:
    :return:
    """


    if message.text == 'Следующий посетитель':
        def slPos(message: Message):
            global dict_id_worker1

            if message.from_user.id in dict_id_worker1:
                key = json.dumps(dict_id_worker1[message.from_user.id])
                second = {'json_s': key}
                clientnumber = requests.post("http://178.154.213.228:8000/api/smartquerest/next_guest/", data=second)
                temp = json.loads(clientnumber.text)

                if temp == "\"True\"":
                    send_message(message, "Должен зайти следующий")
                else:
                    send_message(message, "Ошибка на сервере или никого нет в очереди")
        slPos(message)

    if message.text == 'зарегистрироваться в качестве посетителя' or message.text == 'Отправить код еще раз':
        def log_as_guest(message: Message):
            global dict_id_user1, dict_id_worker1, dict_id_user2, dict_id_user2
            if (message.from_user.id not in dict_id_worker1) and (message.from_user.id not in dict_id_user1):
                send_message(message, "Введите код, который получили от администратора")
                bot.register_next_step_handler(message, reg_user)
            else:
                send_message(message, "Вы уже зарегистрированы")
        log_as_guest(message)

    if message.text == 'Выйти в главное меню':
        def start(message: Message):
            global dict_id_user1, dict_id_worker1
            # btn_my_site2 = types.InlineKeyboardButton(text='/start')
            if (message.from_user.id not in dict_id_user1) and (message.from_user.id not in dict_id_worker1):
                btn_my_site1 = types.InlineKeyboardButton(text='зарегистрироваться в качестве посетителя')
                btn_my_site2 = types.InlineKeyboardButton(text='зарегистрироваться в качестве работника')
                button_hi3 = types.ReplyKeyboardMarkup(resize_keyboard=True)
                button_hi3.add(btn_my_site1)
                button_hi3.add(btn_my_site2)
                bot.send_message(message.from_user.id, ' Вы в главном меню', reply_markup=button_hi3)
        start(message)

    if message.text == 'мои кабинеты':
        def my_cab(message: Message):
            pass
        my_cab(message)

    if message.text == 'сколько людей в очереди':
        def counter(message: Message):
            pass
        counter(message)

    if message.text == 'выход':
        def out(message: Message):
            global dict_id_user1, dict_id_worker1, dict_id_user2, dict_id_user2

            if (message.from_user.id in dict_id_user1):
                del dict_id_user2[dict_id_user1[message.from_user.id]]
                del dict_id_user1[message.from_user.id]

            if (message.from_user.id in dict_id_worker1):
                del dict_id_worker2[dict_id_worker1[message.from_user.id]]
                del dict_id_worker1[message.from_user.id]
            if (message.from_user.id not in dict_id_user1) and (message.from_user.id not in dict_id_worker1):
                btn_my_site1 = types.InlineKeyboardButton(text='зарегистрироваться в качестве посетителя')
                btn_my_site2 = types.InlineKeyboardButton(text='зарегистрироваться в качестве работника')
                button_hi3 = types.ReplyKeyboardMarkup(resize_keyboard=True)
                button_hi3.add(btn_my_site1)
                button_hi3.add(btn_my_site2)
                bot.send_message(message.from_user.id, ' Вы в главном меню', reply_markup=button_hi3)


        out(message)


    if message.text == 'сколько посетителей передомной':
        def count_user(message: Message):
            global dict_id_user1
            if message.from_user.id in dict_id_user1:
                cabs_data = json.dumps(dict_id_user1[message.from_user.id])
                second = {'json_s': cabs_data}
                clientnumber = requests.post("http://178.154.213.228:8000/api/smartquerest/count_people/", data=second)
                temp = json.loads(clientnumber.text)
                send_message(message, f"Перед вами {temp}")
        count_user(message)

    if message.text == 'зарегистрироваться в качестве работника':

        def log_as_worker(message: Message):
            global dict_id_user1, dict_id_worker1, dict_id_user2, dict_id_user2

            if (message.from_user.id not in dict_id_worker1) and (message.from_user.id not in dict_id_user1):
                send_message(message, "Введите код, который получили от администратора")
                bot.register_next_step_handler(message, reg_worker)
            else:
                send_message(message, "Вы уже зарегистрированы")

        log_as_worker(message)


# Здесь объявляю для того, чтобы цикличного импорта не было
import cleaner

threading.Thread(target=cleaner.delete).start()

bot.enable_save_next_step_handlers(delay=2)

bot.load_next_step_handlers()


bot.skip_pending = True

def working_bot():
    global bot
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        working_bot()


if __name__ == '__main__':
    working_bot()
