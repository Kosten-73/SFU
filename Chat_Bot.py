import telebot
from random import randint
from telebot.types import Message
import time
import datetime
from telebot import types
import threading
import sqlite3

dict_id = dict()
token = '1335509834:AAGQgd-fHs3YEyu5zcDiI3V1rQ9PLLxTUHk'
bot = telebot.TeleBot(token)
list_admins = [321354512, 914239664]  # Список id администраторов
current_guests = []
# conn = sqlite3.connect("schedule_database.ds")
# cursor = conn.cursor()
# #cursor.execute("DROP TABLE schedule")
# cursor.execute("CREATE TABLE IF NOT EXISTS Schedule ("
#                "CabinetNum int NOT NULL,"
#                "QueryNum int NOT NULL,"
#                "GuestNum int NOT NULL)")
# conn.commit()
schedule = []
# Состояния пользователей, привязанные к id
# work - ждёт какой-то команды
# wait_schedule - ждёт от администратора размеров таблицы расписания
users_states = dict()


# Очищение таблицы с расписанием
def clean_schedule():
    global schedule
    schedule = []


# Вынес часть кода наружу, просто чтобы было меньше кода в одной функции
def admin_notification(message: Message, bot_text="---"):
    to_logs(message, bot_text)
    for admin_id in list_admins:
        bot.send_message(admin_id, f'{message.from_user.id} @{message.from_user.username} '
                                   f'{message.from_user.first_name} {message.from_user.last_name} {message.text} \n')


#В логи
def to_logs(message: Message, bot_text: str):
    f = open("logs.txt", "a")
    f.write(f'{datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")} '
            f'ID: {message.from_user.id} @{message.from_user.username} '
            f'{message.from_user.first_name} {message.from_user.last_name} {message.text} \n'
            f'bot answer: {bot_text} \n')
    f.close()


# То же самое
@bot.message_handler(commands=['help'])
def show_help(message: Message):
    # button_hi = types.InlineKeyboardMarkup()
    btn_my_site = types.InlineKeyboardButton(text='/help')
    # button_hi.add(btn_my_site)
    button_hi2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_hi2.add(btn_my_site)
    if message.from_user.id in list_admins:
        answer = 'Команды администратора канала: \n \n' \
                 '/make_schedule - Задать размер таблицы расписания в формате "(количество кабинетов), (количество посетителей)" \n \n' \
                 '/show_schedule - Просмотреть расписание \n \n' \
                 '/clean_schedule - Удалить текущую сетку расписания'
        admin_notification(message, answer)
    else:
        answer = '/price - Цены на услуги Атлант \n \n' \
                 '/team - Наша команда \n \n' \
                 '/dnevnik_kachka_73 - Все о проекте Дневник Качка \n \n' \
                 '/doc - узнай кто состоит в этом боте \n \n' \
                 '/contacts - Контактная информация \n \n' \
                 '/Developer - Разработчик \n \n'
        admin_notification(message, answer)
    bot.send_message(message.from_user.id, answer, reply_markup=button_hi2)


# То же самое
@bot.message_handler(commands=['start', 'go'])
def start_work(message: Message):
    btn_my_site2 = types.InlineKeyboardButton(text='/start')
    btn_my_site1 = types.InlineKeyboardButton(text='/help')
    button_hi3 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_hi3.add(btn_my_site2, btn_my_site1)
    # button_hi3.add(btn_my_site1)
    global users_states

    if message.from_user.id not in users_states:
        users_states[int(message.from_user.id)] = "work"
    if message.from_user.last_name == None:
        message.from_user.last_name = ''
    if message.from_user.id not in dict_id:
        dict_id[int(message.from_user.id)] = len(dict_id) + 1
        with open('id.txt', 'a') as f:
            f.write(str(message.from_user.id))
            f.write(': ')
            f.write(str(len(dict_id)))
            f.write('\n')
    answer = f'Приветствую {message.from_user.last_name} ' \
             f'{message.from_user.first_name} клиент электронной очереди! \n' \
             'Я бот созданный студентами юфу! \n' \
             f'Вы вступили под № {dict_id[message.from_user.id]} \n' \
             f'Всего нас {len(dict_id)} \n \n' \
             'Для начала работы нажмите - /help'
    admin_notification(message)
    bot.send_message(message.from_user.id, answer, reply_markup=button_hi3)


# Размер таблицы расписания. 1 строка - один кабинет, ячейки - отрезок времени в на человека (изначально все одинаковой длины)
@bot.message_handler(commands=['make_schedule'])
def make_schedule(message: Message):
    #admin_notification(message)
    global users_states

    users_states[int(message.from_user.id)] = "wait_schedule"
    answer = "Введите через запятую количество кабинетов и интервалов для приёма \n" \
             "/cancel для выхода из этого меню \n" \
             "Это очистит текущее расписание"
    admin_notification(message)
    bot.send_message(message.from_user.id, answer)


# Меняю размер таблицы расписания
@bot.message_handler(regexp="\d+,\d+")
def set_schedule(message: Message):
    #admin_notification(message)
    params = message.text.split(',')
    global users_states

    if int(message.from_user.id) in users_states:
        if (users_states[int(message.from_user.id)] == "wait_schedule"):
            if ((int(params[0]) > 0) and (int(params[1]) > 0)) :
                cab = ['Не занято'] * int(params[1])
                global schedule
                schedule = [cab] * int(params[0])
                users_states[int(message.from_user.id)] = "work"
                result = list()
                print(result)
                for i in range(0, int(params[0])):
                    row = list()
                    for j in range(0, int(params[1])):
                        row.append(f'({i + 1},{j + 1},0)')
                    result.append(','.join(row))
                print(result)
                # with sqlite3.connect("schedule_database.ds") as conn:
                #     cursor = conn.cursor()
                #     query = f'INSERT INTO Schedule VALUES {",".join(result)};'
                #     print(query)
                #     cursor.execute(query)
                #     conn.commit()
                answer = f'Расписание имеет размеры {len(schedule)}x{len(schedule[0])}'
            else:
                users_states[int(message.from_user.id)] = "work"
                answer = f"Расписание не может иметь размеры {params[0]}x{params[1]}\n" \
                         f"Изменения не применены"
        else:
            answer = "Некорректная команда"
    else:
        answer = "Некорректная команда"
    admin_notification(message, answer)
    bot.send_message(message.from_user.id, answer)


# Вывод таблицы расписания
@bot.message_handler(commands=['show_schedule'])
def show_schedule(message: Message):
    #admin_notification(message)
    str_schedule = []
    for i in range(0, len(schedule)):
        cabinet_name = f'Кабинет номер {i + 1}: '
        str_schedule.append(cabinet_name + ", ".join(schedule[i]))
    if (len(schedule) == 0):
        answer = "Таблица расписания ещё не составлена"
    else:
        answer = "\n".join(str_schedule)
    print(answer)
    admin_notification(message, answer)
    bot.send_message(message.from_user.id, answer)


@bot.message_handler(commands=['clean_schedule'])
def clean_validation(message: Message):
    global users_states

    users_states[int(message.from_user.id)] = "wait_clean"
    answer = "/clean - Подтвердить удаление\n" \
             "/cancel - Отменить операцию"
    admin_notification(message, answer)
    bot.send_message(message.from_user.id, answer)


@bot.message_handler(commands=['clean'])
def clean_schedule_manual(message: Message):
    clean_schedule()
    global users_states

    users_states[int(message.from_user.id)] = "work"
    answer = "Сетка расписания сброшена"
    admin_notification(message, answer)
    bot.send_message(message.from_user.id, answer)


@bot.message_handler(commands=['cancel'])
def cancel_operation(message: Message):
    if (users_states[int(message.from_user.id)] == "wait_schedule") or (users_states[int(message.from_user.id)] == "wait_clean"):
        answer = "Операция отменена\n" \
                 "/help - Список команд"
        admin_notification(message, answer)
        bot.send_message(message.from_user.id, answer)
        users_states[int(message.from_user.id)] = "work"
    else:
        answer = "Отменять нечего\n" \
                 "/help - Список команд"
        admin_notification(message, answer)
        bot.send_message(message.from_user.id, answer)


@bot.message_handler(commands=['price', 'contacts', 'team', 'doc', 'gym', 'aerobic_room',
                               'individual_sessions', 'Developer'])
def get_commands_message(message: Message):
    admin_notification(message)

#Здесь объявляю для того, чтобы цикличного импорта не было
import cleaner

threading.Thread(target=cleaner.delete).start()

bot.polling()
