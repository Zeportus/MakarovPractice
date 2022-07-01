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


def CheckActive(id): # Тут проверяется вошел ли данный пользователь в аккаунт
    if s.query(User.active).filter(User.id == id).one()[0]:
        return True
    return False

def SaveContent(str, id): # Сохранение содержимого контента в виде html файла
    os.mkdir(f'Posts/{id}')
    file = open(f'Posts/{id}/{id}.html', 'x')
    file.write(str)
    file.close()


def AddComment(post_id, comm_id):
    file = open(f'Posts/{post_id}/comm_{comm_id}.html', 'x')
    file.write(str)
    file.close()
    

def ShowContent(post_id, user_id):
    post = s.query(Post).filter(Post.id == post_id).one()
    authors_id = s.query(Author.user_id).filter(Author.post_id == post_id).all()[0]
    if post.lvl == 2 or post.lead_author == user_id or user_id in authors_id:
        url = f'Posts/{post_id}/{post_id}.html'
        webbrowser.open(url, new=2)
        return True
    return False


def CheckLogin(username, password):
    try: 
        user = s.query(User).filter(User.username == username, User.password == password).one()
        user.active = True
        s.add(user)
        s.commit()
        return True
    except:
        return False


def LogOut(id):
    user = s.query(User).filter(User.id == id).one()
    user.active = False
    s.add(user)
    s.commit()
    return True