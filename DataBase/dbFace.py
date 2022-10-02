from alchemy import s, User, Post, Author, Comment, Lvl

def createArr(arr): # Принимает query запрос с методом all() и превращает его в удобный массив
    res = []
    for i in arr:
        res.append(i[0])
    return res


def insert(data):
    s.add(data)
    s.commit()


def insertAll(data):
    s.add_all(data)
    s.commit()


def delete(data):
    s.delete(data)
    s.commit()


def addUser(userreg): # Добавление пользователя, добавление его уровней
    new_user = User(username = userreg.username, password = userreg.password)
    insert(new_user)

    user_id = s.query(User.id).order_by(User.id.desc()).first()[0]
    user_lvls = []
    for i in userreg.lvl:
        user_lvls.append(Lvl(user_id = user_id, lvl = i))

    insertAll(user_lvls)


def addPost(postreg): # Добавление поста, добавление авторов поста
    new_post = Post(name = postreg.name, lead_author = postreg.lead_author, lvl = postreg.lvl, content = postreg.content)
    insert(new_post)
    post_id = s.query(Post.id).order_by(Post.id.desc()).first()[0]

    new_authors = []
    for i in postreg.authors:
        new_authors.append(Author(user_id = i, post_id = post_id))

    new_authors.append(Author(user_id = postreg.lead_author, post_id = post_id))
    insertAll(new_authors)


def addComment(commreg):
    new_comment = Comment(content = commreg.content, post_id = commreg.post_id, user_id = commreg.user_id)
    insert(new_comment)


def delComment(comment_id):
    delete(s.query(Comment).filter(Comment.id == comment_id).one())

def getUser(user_id):
    return s.query(User).filter(User.id == user_id).one()


def getUsers():
    return s.query(User).all()

def checkUsername(username): # Проверка на наличие никнейма в базе
    if s.query(User.username).filter(User.username == username).all():
        return False
    return True

def checkLogin(username, password): # Получаем объект пользователя по нику и паролю, то есть авторизация
    return s.query(User).filter(User.username == username, User.password == password).one()


def getPost(post_id):
    return s.query(Post).filter(Post.id == post_id).one()


def getPosts():
    return s.query(Post).all()


def getLvls(user_id): # Получение списка уровней пользователя
    return createArr(s.query(Lvl.lvl).filter(Lvl.user_id == user_id).all())


def getAuthorsId(post_id): # Возвращает список id авторов у постов
    return createArr(s.query(Author.user_id).filter(Author.post_id == post_id).all())


def getPostsId(user_id): # Вовзращает список id постов у пользователя
    return createArr(s.query(Author.post_id).filter(Author.user_id == user_id).all())


def getComments(post_id): # Получаем список кортежей неободимых полей комментария для поста
    return s.query(Comment.user_id, Comment.content, Comment.id).filter(Comment.post_id == post_id).all()


def addAuthor(user_id, post_id): 
    new_author = Author(user_id = user_id, post_id = post_id)
    insert(new_author)

def delAuthor(user_id, post_id):
    author = s.query(Author).filter(Author.user_id == user_id, Author.post_id == post_id).one()
    delete(author)


def addLvl(user_id, lvl):
    insert(Lvl(user_id = user_id, lvl = lvl))


def delLvl(user_id, lvl):
    user_lvl = s.query(Lvl).filter(Lvl.user_id == user_id, Lvl.lvl == lvl).one()
    delete(user_lvl)
