from fastapi import FastAPI
from pydantic import BaseModel
import sys
sys.path.insert(0, '/home/mark/Practice/DataBase')
import logic
from typing import List

app = FastAPI()

class UserReg(BaseModel):
  username: str
  password: str
  lvl: List[int]


class PostReg(BaseModel):
    name: str
    lead_author: int
    lvl: int
    authors: List[int] # Тут будут id помощников
    content: str


class CommReg(BaseModel):
    user_id: int
    post_id: int
    content: str


@app.get('/')
def HealthCheck():
    return 'ok'


@app.post('/registration')
def Registration(userreg: UserReg): 
    if logic.CheckReg(userreg):
        return 'Registration successful'
    return 'Username already exists'
    


@app.post('/authorization')
def Authorization(username: str, password: str): 
    if logic.CheckLogin(username, password):
        return 'Authorization successful'
    return 'Authorization failed'
        

@app.post('/logout')
def LogOut(id: int):
    if logic.LogOut(id):
        return 'Logout successful'
    return 'Logout failed'


@app.post('/createpost')
def CreatePost(postreg: PostReg): # Создание поста, добавление авторов, проверка их прав
    if not logic.CheckActive(postreg.lead_author):
        return 'You are not authorized'

    for i in postreg.authors:
        if not logic.CheckCreateRights(i):
            return 'Check your authors lvls. One or more of them is low'

    if logic.CheckCreateRights(postreg.lead_author):
        logic.AddPost(postreg)
        return 'Post has been created'
    return 'Post has not been created. Your lvl is low'


@app.post('/addComment')
def AddComment(commreg: CommReg): # Добавление комментария
    if logic.CheckActive(commreg.user_id):
        if logic.AddComment(commreg):
            return 'Comment has added'
        return 'Post does not exist'
    return 'You are not authorized'


@app.post('/moderatePost')
def ModeratePost(post_id: int, user_id: int, option: str, comment: str): # option для модерации. accept - опубликовать пост, denied - отклонить.
    if logic.CheckActive(user_id):
        if logic.ModeratePost(post_id, user_id, option, comment):
            return 'Post status has changed(moderated)'
        return 'Post status has not changed, check user or/and post level'
    return 'You are not authorized'


@app.post('/changeAuthors') 
def ChangeAuthors(post_id: int, user_id: int, act_id: int): # act_id - id юзера над которым проводят манипуляции
    if logic.CheckActive(user_id):
        res = logic.ChangeAuthors(post_id, user_id, act_id)
        return res[0]
    return 'You are not authorized'


@app.post('/editPost')
def EditPost(post_id: int, user_id: int, editedContent: str):#  Изменение контента поста
    if logic.CheckActive(user_id): 
        if logic.EditPost(post_id, user_id, editedContent):
            return 'Post has edited'
        return 'You can not edit this post. Check lvl post or/and your permission'
    return 'You are not authorized'


@app.post('/pubDepubPost')
def PubDepubPost(post_id: int, user_id: int): # Выложить пост в модерацию или спрятать его в черновик в зависимости от статуса поста
    if logic.CheckActive(user_id):
        if logic.PubDepubPost(post_id, user_id):
            return 'Your post status has changed'
        return 'You can not change the post status. Check post lvl or/and your permissions'
    return 'You are not authorized'


@app.post('/changeUserLvl')
def ChangeUserLvl(user_id: int, act_id: int, option: str, lvl: int):  # option: add - добавляет lvl к act_id, remove - убирает lvl у act_id
    if logic.CheckActive(user_id):
        if logic.ChangeUserLvl(user_id, act_id, option, lvl):
            return 'User lvls has changed'
        return 'User lvls has not changed. Check user lvls or your permissions'
    return 'You are not authorized'


@app.post('/delComment')
def DelComment(user_id: int, comment_id: int): # Удаление комментария модератором 
    if logic.CheckActive(user_id):
        if logic.DelComment(user_id, comment_id):
            return 'Comment has deleted'
        return 'Comment has not deleted. Check your permission.'
    return 'You are not authorized'


@app.get('/posts')
def GetPosts(user_id: int): # Получение всех постов, которые может видеть пользователь
    if logic.CheckActive(user_id):
        return logic.GetPosts(user_id)
    return 'You are not authorized'


@app.get('/users')
def GetUsers(user_id: int): # Получение информации о всех пользователях 
    if logic.CheckActive(user_id):
        return logic.GetUsers()
    return 'You are not authorized'