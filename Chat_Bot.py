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
import SingleClasses
import re
import sys
reload(sys)
# sys.setdefaultencoding('utf-8')

dict_id = dict()
token = '1335509834:AAGQgd-fHs3YEyu5zcDiI3V1rQ9PLLxTUHk'
bot = telebot.TeleBot(token)
# list_admins = [321354512, 914239664]  # Список id администраторов
#
# # Список гостей
# current_guests = []
user_key_to_give = 141400000000
worker_key_to_give = 1500000000
# # Кабинеты
# cabinets = []
# conn = sqlite3.connect("schedule_database.ds")
# cursor = conn.cursor()
# #cursor.execute("DROP TABLE schedule")
# cursor.execute("CREATE TABLE IF NOT EXISTS Schedule ("
#                "CabinetNum int NOT NULL,"
#                "QueryNum int NOT NULL,"
#                "GuestNum int NOT NULL)")
# conn.commit()
schedule = SingleClasses.Schedule()
# Состояния пользователей, привязанные к id
# work - ждёт какой-то команды
# wait_schedule - ждёт от администратора размеров таблицы расписания
users_states = dict()


def clean_schedule():
    """
    Очистка таблицы с расписанием
    :return:
    """
    global schedule
    schedule = SingleClasses.Schedule()


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


@bot.message_handler(commands=['help'])
def show_help(message: Message):
    """
    Вывод помощи
    :param message:
    :return:
    """
    global schedule

    # button_hi = types.InlineKeyboardMarkup()
    btn_my_site = types.InlineKeyboardButton(text='/help')
    # button_hi.add(btn_my_site)
    button_hi2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_hi2.add(btn_my_site)
    permission = schedule.get_permission(message.from_user.id)
    if permission == 1:
        answer = 'Команды администратора канала: \n \n' \
                 '/new_guest - Добавить гостя \n \n' \
                 '/new_cabinet - Добавить кабинет \n \n' \
                 '/show_schedule - Просмотреть расписание \n \n' \
                 '/clean_schedule - Удалить текущую сетку расписания'
    elif permission == 2:
        answer = '/change_name - Сменить имя \n \n' \
                 '/next_guest - Следующий посетитель \n \n'
    elif permission == 3:
        answer = "Вы в очереди"
    else:
        answer = '/log_as_guest - Войти в качестве посетителя\n' \
                 '/log_as_worker - Войти в качестве работника'

    admin_notification(message, answer)
    bot.send_message(message.from_user.id, answer, reply_markup=button_hi2)


@bot.message_handler(commands=['start'])
def start_work(message: Message):
    """
    Начало работы
    :param message:
    :return:
    """
    btn_my_site2 = types.InlineKeyboardButton(text='/start')
    btn_my_site1 = types.InlineKeyboardButton(text='/help')
    button_hi3 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_hi3.add(btn_my_site2, btn_my_site1)
    # button_hi3.add(btn_my_site1)
    global users_states

    if message.from_user.id not in users_states:
        users_states[int(message.from_user.id)] = "work"
    # if message.from_user.last_name == None:
    #     message.from_user.last_name = ''
    # if message.from_user.id not in dict_id:
    #     dict_id[int(message.from_user.id)] = len(dict_id) + 1
    #     with open('id.txt', 'a') as f:
    #         f.write(str(message.from_user.id))
    #         f.write(': ')
    #         f.write(str(len(dict_id)))
    #         f.write('\n')
    answer = f'Приветствую {message.from_user.last_name} ' \
             f'{message.from_user.first_name} клиент электронной очереди! \n' \
             'Для начала работы нажмите - /help'
    admin_notification(message)
    bot.send_message(message.from_user.id, answer, reply_markup=button_hi3)


# Вроде теперь следующие две не нужны
# @bot.message_handler(commands=['make_schedule'])
# def make_schedule(message: Message):
#     """
#     Размер таблицы расписания. 1 строка - один кабинет,
#     ячейки - отрезок времени в на человека (изначально все одинаковой длины)
#     :param message:
#     :return:
#     """
#     # admin_notification(message)
#     global users_states, schedule
#
#     if schedule.get_permission(message.from_user.id) == 1:
#         users_states[int(message.from_user.id)] = "wait_schedule"
#         answer = "Введите через запятую количество кабинетов и интервалов для приёма \n" \
#                  "/cancel для выхода из этого меню \n" \
#                  "Это очистит текущее расписание"
#         admin_notification(message)
#         bot.send_message(message.from_user.id, answer)
#     else:
#         # TODO: Дописать
#         pass
#
#
# @bot.message_handler(regexp=r"\d+,\d+")
# def set_schedule(message: Message):
#     """
#     Меняю размер таблицы расписания
#     :param message:
#     :return:
#     """
#     # admin_notification(message)
#     params = message.text.split(',')
#     global users_states, schedule
#
#     if schedule.get_permission(message.from_user.id) == 1:
#         if users_states[int(message.from_user.id)] == "wait_schedule":
#             if (int(params[0]) > 0) and (int(params[1]) > 0):
#                 cab = ['Не занято'] * int(params[1])
#                 schedule = [cab] * int(params[0])
#                 users_states[int(message.from_user.id)] = "work"
#                 result = list()
#                 print(result)
#                 for i in range(0, int(params[0])):
#                     row = list()
#                     for j in range(0, int(params[1])):
#                         row.append(f'({i + 1},{j + 1},0)')
#                     result.append(','.join(row))
#                 print(result)
#                 # with sqlite3.connect("schedule_database.ds") as conn:
#                 #     cursor = conn.cursor()
#                 #     query = f'INSERT INTO Schedule VALUES {",".join(result)};'
#                 #     print(query)
#                 #     cursor.execute(query)
#                 #     conn.commit()
#                 answer = f'Расписание имеет размеры {len(schedule)}x{len(schedule[0])}'
#             else:
#                 users_states[int(message.from_user.id)] = "work"
#                 answer = f"Расписание не может иметь размеры {params[0]}x{params[1]}\n" \
#                          f"Изменения не применены"
#         else:
#             answer = "Некорректная команда"
#     else:
#         answer = "Некорректная команда"
#     send_message(message, answer)


@bot.message_handler(commands=['show_schedule'])
def show_schedule(message: Message):
    """
    Вывод таблицы расписания
    :param message:
    :return:
    """
    # admin_notification(message)
    global schedule

    if schedule.get_permission(message.from_user.id) == 1:
        answer = str(schedule)
    else:
        answer = "Эта команда вам недоступна"
    if len(answer) == 0:
        answer = "Empty"
    print(answer)
    admin_notification(message, answer)
    bot.send_message(message.from_user.id, answer)


@bot.message_handler(commands=['clean_schedule'])
def clean_validation(message: Message):
    """
    Подтверждение удаления
    :param message:
    :return:
    """
    global users_states

    users_states[int(message.from_user.id)] = "wait_clean"
    answer = "/clean - Подтвердить удаление\n" \
             "/cancel - Отменить операцию"
    send_message(message, answer)


@bot.message_handler(commands=['next_guest'])
def next_guest(message: Message):
    global schedule

    admin_notification(message, "Так чекни")
    print(schedule.workers)
    print(schedule.workers[0])
    print(message.from_user.id)
    print(schedule.get_permission(message.from_user.id))
    if schedule.get_permission(message.from_user.id) == 2:
        ids = dict()
        schedule.next_guest(message.from_user.id, ids)
        if 'prev' in ids.keys():
            if schedule.get_tg_guest(ids['prev']) != -1:
                send_message_by_id(schedule.get_tg_guest(ids['prev']).tg_id, "Выходите из кабинета")
        if 'next' in ids.keys():
            if schedule.get_tg_guest(ids['next']) != -1:
                send_message_by_id(schedule.get_tg_guest(ids['next']).tg_id, "Заходите в кабинет")
        send_message(message, "Должен зайти следующий")


@bot.message_handler(commands=['clean'])
def clean_schedule_manual(message: Message):
    """
    Очистка таблицы
    :param message:
    :return:
    """
    clean_schedule()
    global users_states
    users_states[int(message.from_user.id)] = "work"
    answer = "Сетка расписания сброшена"
    send_message(message, answer)


@bot.message_handler(commands=['cancel'])
def cancel_operation(message: Message):
    """
    Отмена операции (В разных случаях на разную операцию)
    :param message:
    :return:
    """
    # Операции с изменением расписания
    if (users_states[int(message.from_user.id)] == "wait_schedule") or (
            users_states[int(message.from_user.id)] == "wait_clean"):
        answer = "Операция отменена\n" \
                 "/help - Список команд"
        admin_notification(message, answer)
        bot.send_message(message.from_user.id, answer)
        users_states[int(message.from_user.id)] = "work"
    #     Когда никакой операции для отмены нет
    else:
        answer = "Отменять нечего\n" \
                 "/help - Список команд"
        admin_notification(message, answer)
        bot.send_message(message.from_user.id, answer)


@bot.message_handler(commands=['new_guest'])
def new_guest_notify(message: Message):
    """
    Создание нового пользователя, вводное сообщение
    :param message:
    :return:
    """
    global schedule

    if schedule.get_permission(message.from_user.id) == 1:
        answer = "Введите через пробел номера кабинетов, в которые идёт посетитель\n" \
                 "Следующим номерам соответствуют следующие кабинеты:\n" \
                 "(Спросите у администратора)"
        bot.register_next_step_handler(message, register_new_guest)
    else:
        answer = "Команда недоступна"
    send_message(message, answer)


def register_new_guest(message: Message):
    try:
        global users_states, schedule

        answer = "Добавлен посетитель с ключом: "
        new_cabinets = message.text.split(' ')
        for i in range(0, len(new_cabinets)):
            new_cabinets[i] = int(new_cabinets[i])
        set_cabinets = set(new_cabinets)
        current_key = user_key_to_give + randint(10000000, 100000000)
        this_guest = SingleClasses.Guest(schedule.id_guest(), current_key, set_cabinets)
        schedule.add_guest(this_guest)
        answer += str(current_key)
        send_message(message, answer)
    except Exception as e:
        send_message(message, f"Что-то не так: {repr(e)}")


@bot.message_handler(commands="log_as_guest")
def log_as_guest(message: Message):
    global schedule

    if schedule.get_permission(message.from_user.id) == 0:
        answer = "Введите код, который получили от администратора"
        bot.register_next_step_handler(message, reg_user)
    else:
        answer = "Вам эта команда недоступна"
    send_message(message, answer)


def reg_user(message: Message):
    global schedule, users_states

    try:
        res = schedule.set_guest_id(int(message.text), message.from_user.id)
        if res:
            users_states[message.from_user.id] = "user"
            answer = schedule.count_time_guest(message.from_user.id)
            if answer == "Empty":
                answer = "Вы прошли все кабинеты"
            else:
                answer = f'Ваш следующий приём примерно через {int(answer) // 60} минут'
        else:
            answer = "Неправильный код"
        send_message(message, answer)
    except Exception as e:
        send_message(message, f"Что-то не так: {repr(e)}")


@bot.message_handler(commands="log_as_worker")
def log_as_worker(message: Message):
    global schedule

    if schedule.get_permission(message.from_user.id) == 0:
        answer = "Введите код, который получили от администратора"
        bot.register_next_step_handler(message, reg_worker)
    else:
        answer = "Вам эта команда недоступна"
    send_message(message, answer)


def reg_worker(message: Message):
    global schedule
    try:
        res = schedule.set_worker_id(int(message.text), message.from_user.id)
        if res:
            users_states[message.from_user.id] = "worker"
            answer = f'Вы зарегистрированы'
            show_help(message)
        else:
            answer = "Неправильный код"
        send_message(message, answer)
    except Exception as e:
        send_message(message, f"Что-то не так: {repr(e)}")


@bot.message_handler(commands=['change_name'])
def change_worker_name_first(message: Message):
    global schedule

    if schedule.get_permission(message.from_user.id) == 2:
        answer = "Введите ваше имя, без пробелов или других знаков препинания"
        bot.register_next_step_handler(message, change_name_now)
    else:
        answer = "Некорректная команда"
    send_message(message, answer)


def change_name_now(message: Message):
    try:
        global schedule

        admin_notification(message, "Изменение имени")
        schedule.change_worker_name(message.from_user.id, message.text)
        send_message(message, "Ваше имя изменено")
    except Exception as e:
        send_message(message, f"Что-то не так: {repr(e)}")
        admin_notification(message, f"Что-то не так: {repr(e)}")


@bot.message_handler(commands=['new_cabinet'])
def new_cabinet_first(message: Message):
    """
    Создание нового кабинета, вводное сообщение
    :param message:
    :return:
    """
    global users_states, schedule

    if schedule.get_permission(message.from_user.id) == 1:
        answer = "Введите название кабинета:"
        users_states[message.from_user.id] = "wait_new_cabinet"
        send_message(message, answer)
        bot.register_next_step_handler(message, new_cabinet_save)


def new_cabinet_save(message: Message):
    try:
        print("I'm here1")
        global schedule, worker_key_to_give

        m = re.match(r"[\w\s\d]+", message.text)
        if m.start() != 0 or m.end() != len(message.text):
            raise Exception("Имя не соответствует шаблону")

        print("I'm here2")
        answer = ""
        current_key = worker_key_to_give + randint(10000000, 100000000)
        new_cab_id = schedule.id_cabinet()
        new_cab = SingleClasses.Cabinet(new_cab_id, message.text, 300)
        schedule.add_cabinet(new_cab)
        new_worker = SingleClasses.Worker(current_key, new_cab_id)
        schedule.add_worker(new_worker)
        answer = f"Создан кабинет {message.text} с id = {new_cab_id} и ключом доступа работника {current_key}, время приёма установлено на 300 секунд."
        send_message(message, answer)
    except Exception as e:
        send_message(message, f"Что-то не так: {repr(e)}")


# @bot.message_handler(commands=['price', 'contacts', 'team', 'doc', 'gym', 'aerobic_room',
#                                'individual_sessions', 'Developer'])
# def get_commands_message(message: Message):
#     """
#     Можно и удалить, думаю. Или заходить сюда на все некорректные команды, которые неизвестно как обрабатывать
#     :param message:
#     :return:
#     """
#     send_message(message, "Wrong command")
#

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
