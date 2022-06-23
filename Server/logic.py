import sys
import os
sys.path.insert(0, '/home/mark/Practice/DataBase')
import alchemy



userlvl = {
    0: 'user',
    1: 'writer',
    2: 'moder',
    3: 'admin'
}

postlvl = {
    0: 'note',
    1: 'moderating',
    2: 'published',
    3: 'denied'
}

def CheckReg(username): # Проверка на оригинальность никнейма.
    s = alchemy.selUsers.where(
        alchemy.users.c.username == username
    )
    r = alchemy.conn.execute(s)

    if not r.fetchall():
        return True
    else: 
        return False


def CheckCreateRights(id): # Проверка уровня доступа пользователя
    s = alchemy.selUsers.where(
        (alchemy.users.c.id == id) &
        (alchemy.users.c.lvl > 0)
    )
    r = alchemy.conn.execute(s)

    if r.fetchall():
        return True
    else: 
        return False


def SaveContent(str, id):
    os.mkdir(f'Posts/{id}')
    file = open(f'Posts/{id}/{id}.html', 'x')
    file.write(str)
    file.close()
    