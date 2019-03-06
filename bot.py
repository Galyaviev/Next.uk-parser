import subprocess

import sql
import telebot
import conf

bot = telebot.TeleBot(conf.tokken)




log_pass_dict = {}


class Login_password:
    def __init__(self, login):
        self.login = login
        self.password = None


@bot.message_handler(commands=['start'])
def handle_start(message):
    mark_up = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    mark_up.row('Запустить', 'Остановить')
    mark_up.row('Добавить пользователя', 'Удалить пользователя')
    mark_up.row('Список пользователей')
    bot.send_message(message.chat.id, "Привет", reply_markup=mark_up)


@bot.message_handler(content_types=['text'])
def send_message(message):
    try:
        if 'Список пользователей' in message.text:
            bot.send_message(message.chat.id, "Список")
            list = sql.select_all()
            for date in list:
                login = date['login']
                password = date['password']
                bot.send_message(message.chat.id, login+' '+ password)
    except Exception as e:
        with open('error_bot.txt', 'a') as f:
            f.write(str(e) + '\n')
    if 'Запустить' in message.text:
        bot.send_message(message.chat.id, "Запускаю")
        subprocess.check_call(['service', 'zifa', 'start'])
    if 'Остановить' in message.text:
        bot.send_message(message.chat.id, "Останавливаю")
        subprocess.check_call(['service', 'zifa', 'stop'])
    if 'Добавить пользователя' in message.text:
        login = bot.send_message(message.chat.id, "Введите логин")
        bot.register_next_step_handler(login, add_user_in_sql)
    if 'Удалить пользователя' in message.text:
        list = sql.select_id_login()
        for date in list:
            id = date['id']
            login = date['login']
            bot.send_message(message.chat.id, 'ID= '+str(id)+' '+login)
        msg = bot.send_message(message.chat.id, "Введите ID= ")
        bot.register_next_step_handler(msg, del_user)


def del_user(message):
    id = message.text
    sql.del_log(id)
    bot.send_message(message.chat.id, 'Новый список пользователей: ')
    list = sql.select_id_login()
    for date in list:
        id = date['id']
        login = date['login']
        bot.send_message(message.chat.id, 'ID= ' + str(id) + ' ' + login)


def add_user_in_sql(message):
    chat_id = message.chat.id
    login = message.text
    login_password = Login_password(login)
    log_pass_dict[chat_id] = login_password
    msg = bot.reply_to(message, 'Введите пароль')
    bot.register_next_step_handler(msg, add_user_in_sql2)

def add_user_in_sql2(message):
    chat_id = message.chat.id
    password = message.text
    login_password = log_pass_dict[chat_id]
    login_password.password = password
    print(login_password.login, login_password.password)
    loginPaswword = []
    loginPaswword.append(login_password.login)
    loginPaswword.append(login_password.password)
    sql.create_user(loginPaswword)
    bot.send_message(message.chat.id, 'Пользователь с логином '+login_password.login+' и паролем '+ login_password.password+' добавлен')





bot.polling(none_stop=True, interval=0)
