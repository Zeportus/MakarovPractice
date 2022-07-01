import sys
import os
import webbrowser
sys.path.insert(0, '/home/mark/Practice/DataBase')
from alchemy import s, User, Post, Author

    
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
    if s.query(User.username).filter(User.username == username).all():
        return False
    return True

def CheckCreateRights(id): # Проверка уровня доступа пользователя
    if s.query(User.lvl).filter(User.id == id).one()[0] > 0:
        return True
    return False


def SaveContent(str, id):
    os.mkdir(f'Posts/{id}')
    file = open(f'Posts/{id}/{id}.html', 'x')
    file.write(str)
    file.close()
    
def ShowContent(id):
    url = f'Posts/{id}/{id}.html'
    webbrowser.open(url, new=2)