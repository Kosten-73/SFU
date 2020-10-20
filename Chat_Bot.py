import telebot
from random import randint
from telebot.types import Message

dict_id = dict()
token = '1335509834:AAGQgd-fHs3YEyu5zcDiI3V1rQ9PLLxTUHk'
bot = telebot.TeleBot(token)
@bot.message_handler(commands=['start', 'go', 'help', 'price',
                               'contacts', 'team', , 'doc', 'gym', 'aerobic_room',
                               'individual_sessions', 'Developer'])

def get_commands_message(message: Message):
    if message.from_user.id != 321354512 and message.from_user.id != 914239664:
        bot.send_message(321354512, f'{message.from_user.id} @{message.from_user.username} '
        f'{message.from_user.first_name} {message.from_user.last_name} {message.text} \n')
        bot.send_message(914239664, f'{message.from_user.id} @{message.from_user.username} '
        f'{message.from_user.first_name} {message.from_user.last_name} {message.text} \n')

    if message.text == '/help':
        bot.send_message(message.from_user.id, '/price - Цены на услуги Атлант \n \n'
                                               '/team - Наша команда \n \n'
                                               '/dnevnik_kachka_73 - Все о проекте Дневник Качка \n \n'
                                               '/doc - узнай кто состоит в этом боте \n \n'
                                               '/contacts - Контактная информация \n \n'
                                               '/Developer - Разработчик \n \n')
    elif message.text == '/start' or '/go':
        if message.from_user.last_name == None:
            message.from_user.last_name = ''
        if message.from_user.id not in dict_id:
            dict_id[int(message.from_user.id)] = len(dict_id) + 1
            with open('id.txt', 'a') as f:
                f.write(str(message.from_user.id))
                f.write(': ')
                f.write(str(len(dict_id)))
                f.write('\n')
        bot.send_message(message.from_user.id, f'Приветствую {message.from_user.last_name} '
                                           f'{message.from_user.first_name} клиент электронной очереди! \n'
                                           'Я бот созданный студентами юфу! \n'
                                           f'Вы вступили под № {dict_id[message.from_user.id]} \n'
                                           f'Всего нас {len(dict_id)} \n \n'
                                           'Для начала работы нажмите - /help')
bot.polling()
