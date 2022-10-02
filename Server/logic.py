import sys
sys.path.insert(0, '/home/mark/Practice/DataBase')
import dbFace

#    Уровни пользователей
#    0: 'user',
#    1: 'writer',
#    2: 'moder',
#    3: 'admin'


#    Уровени постов
#    0: 'note',
#    1: 'moderating',
#    2: 'published',
#    3: 'denied'

# Словарь для получения пользователей (нужен, чтобы не передавать поле password из класса)
user_dict = {
    'id': None,
    'username': None,
    'lvls': None,
    'posts': None,
    'active': None
}

def CheckReg(userreg): # Проверка на оригинальность никнейма.
    if 3 in userreg.lvl:
        userreg.lvl = [0, 1, 2, 3]

    if dbFace.checkUsername(userreg.username):
        dbFace.addUser(userreg)
        return True
    return False


def CheckCreateRights(id): # Проверка уровня доступа пользователя на создание статьи
    if 1 in dbFace.getLvls(id):
        return True
    return False


def AddPost(postreg):
    dbFace.addPost(postreg)
    return True


def CheckActive(id): # Тут проверяется вошел ли данный пользователь в аккаунт
    if dbFace.getUser(id).active:
        return True
    return False


def AddComment(commreg): # Добавление комментария
    if dbFace.getPost(commreg.post_id).lvl == 2:
        dbFace.addComment(commreg)
        return True
    return False


def CheckLogin(username, password): # Проверка зарегистрированности пользователя
    try: 
        user = dbFace.checkLogin(username, password)
        user_lvls = dbFace.getLvls(user.id)
        
        if 4 in user_lvls:
            return False
        user.active = True
        dbFace.insert(user)
        return True
    except:
        return False


def LogOut(id): # Выход из аккаунта
    user = dbFace.getUser(id)
    user.active = False
    dbFace.insert(user)
    return True


def ModeratePost(post_id, user_id, option, comment): # option отвечает за решение модератора. Ожидается строка accept или denied
    user_lvls = dbFace.getLvls(user_id)
    post = dbFace.getPost(post_id)

    if 2 in user_lvls and post.lvl == 1 and option == 'accept':
        post.lvl = 2
        dbFace.insert(post)
        return True

    elif 2 in user_lvls and post.lvl == 1 and option == 'denied':
        post.lvl = 3
        post.content += '\nModerator comment: ' + comment
        dbFace.insert(post)
        return True
    
    return False


def PubDepubPost(post_id, user_id): # Убрать пост в черновик, если он опубликован или отклонен, либо отправить на модерацию
    post = dbFace.getPost(post_id)

    if post.lvl == 0 and post.lead_author == user_id:
        post.lvl = 1
        dbFace.insert(post)
        return True

    elif (post.lvl == 2 or post.lvl == 3) and post.lead_author == user_id:
        post.lvl = 0
        dbFace.insert(post)
        return True
    
    return False    


def EditPost(post_id, user_id, editedContent): # Изменение контента поста
    post = dbFace.getPost(post_id)
    authors_id = dbFace.getAuthorsId(post_id)

    if post.lvl == 0 and user_id in authors_id:
        post.content = editedContent
        dbFace.insert(post)
        return True
    return False
        

def ChangeAuthors(post_id, user_id, act_id): # Изменение авторов поста
    authors_id = dbFace.getAuthorsId(post_id)
    act_user_lvls = dbFace.getLvls(act_id)
    post = dbFace.getPost(post_id)

    if user_id == post.lead_author:
        if user_id == act_id:
            return 'You can not act with yourself, when you are lead author', False
        elif act_id in authors_id:
            dbFace.delAuthor(act_id, post_id)
            return 'User has deleted from authors', False
        elif 1 in act_user_lvls:
            dbFace.addAuthor(act_id, post_id)
            return 'User has added to authors', True
        else:
            return 'User is not a writer', False
    return 'You are not the lead author', False


def ChangeUserLvl(user_id, act_id, option, lvl): # Изменение уровня пользователя
    act_user = dbFace.getUser(act_id)
    user_lvls = dbFace.getLvls(user_id)
    act_lvls = dbFace.getLvls(act_id)

    if 3 in user_lvls and lvl in [0, 1, 2, 3, 4]:
        if option == 'add' and lvl not in act_lvls:
            if lvl == 4 and 3 in act_lvls:
                return False
            elif lvl == 4:
                act_user.active = False
                dbFace.insert(act_user)

            if lvl == 3:
                for i in range(3):
                    ChangeUserLvl(user_id, act_id, 'add', i)

            dbFace.addLvl(act_id, lvl)
            return True
        elif option == 'remove' and  3 not in act_lvls and lvl in act_lvls:
            dbFace.delLvl(act_id, lvl)
            return True

        return False

    return False


def DelComment(user_id, comment_id):
    user_lvls = dbFace.getLvls(user_id)
    if 2 in user_lvls:
        dbFace.delComment(comment_id)
        return True
    return False


def GetPosts(user_id): # Получаем список объектов постов, выбираем подходящие для пользователя объекты в результирующий список, добавляя необходимые поля.
    posts = dbFace.getPosts()
    user_lvls = dbFace.getLvls(user_id)
    res_posts = []
    
    for i in posts:
        i.comments = dbFace.getComments(i.id)
        i.authors = dbFace.getAuthorsId(i.id)
        if (i.lvl == 2 and (0 in user_lvls or 2 in user_lvls)) or (i.lead_author == user_id) or (user_id in i.authors) or (i.lvl == 1 and 2 in user_lvls):
            res_posts.append(i)      
    return res_posts


def GetUsers(): # Получаем объекты пользователей, используя словарь, добавляем нужные значения, убираем ненужные, выводим 
    users = dbFace.getUsers() 
    res_users = []

    for i in users:
        lvls = dbFace.getLvls(i.id)
        posts = dbFace.getPostsId(i.id)

        user_dict['id'] = i.id
        user_dict['username'] = i.username
        user_dict['lvls'] = lvls
        user_dict['posts'] = posts
        user_dict['active'] = i.active

        res_users.append(user_dict.copy())

    return res_users

