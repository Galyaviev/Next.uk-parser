import sqlite3


def create_db(): # Cоздать базу
    conn = sqlite3.connect('DB.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE if not exists next(id integer primary key AUTOINCREMENT,
                                                      login TEXT,
                                                      password TEXT)''')
    cursor.close()
    conn.close()


def create_all_user(): # Создать юзеров
    data = [('sutyagina@b-f-uk.com','ybyzrf01'),
            ('zkitanova@inbox.ru', 'qwerty1'),
            ('lenext@list.ru','qwerty1'),
            ('zifanext@mail.ru','qwerty1'),
            ('1020mary@mail.ru','ybyzrf01'),
            ('alenanext@list.ru','qwerty1'),
            ('kruglova@b-f-uk.com','qwerty1'),
            ('sutyagina@b-f-uk.com','qwerty1'),
            ('ivannext@list.ru','qwerty1'),
            ('1012next@mail.ru','qwerty1'),
            ('zaynagieva@b-f-uk.com','qwerty1')]

    conn = sqlite3.connect('DB.db')
    cursor = conn.cursor()
    for data_unit in data:
        cursor.execute('''INSERT INTO next(login, password ) VALUES (?, ?)''', data_unit)


    conn.commit()
    cursor.close()
    conn.close()


def create_user(loginPaswword):
    print(loginPaswword)
    conn = sqlite3.connect('DB.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO next(login, password ) VALUES (?, ?)''', loginPaswword)
    conn.commit()
    cursor.close()
    conn.close()


def select_all(): #
    conn = sqlite3.connect('DB.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM next''')
    row = cursor.fetchall()
    log_pass = []
    for i in row:
        log_pass.append({'login':i[1],'password':i[2]})


    cursor.close()
    conn.close()

    return log_pass

def del_log(id):
    print(id)
    conn = sqlite3.connect('DB.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM next WHERE id = '+str(id)+'')

    conn.commit()
    cursor.close()
    conn.close()


def select_id_login(): #
    conn = sqlite3.connect('DB.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM next''')
    row = cursor.fetchall()
    log_pass = []
    for i in row:
        log_pass.append({'id':i[0],'login':i[1]})


    cursor.close()
    conn.close()
    print(log_pass)
    return log_pass
