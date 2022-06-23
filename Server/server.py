from cgitb import html
from distutils import file_util
from html.entities import html5
from fastapi import FastAPI, File
from pydantic import BaseModel, FilePath
import sys
sys.path.insert(0, '/home/mark/Practice/DataBase')
import alchemy
import logic
from typing import List

app = FastAPI()

class UserReg(BaseModel):
  username: str
  password: str
  lvl: int

class PostReg(BaseModel):
    name: str
    author: int
    lvl: int
    helpers: List[int] # Тут будут id помощников
    content: str
@app.get('/')
def HealthCheck():
    return 'ok'


@app.post('/registration')
def Registration(userreg: UserReg):  
    new_user = userreg.dict()
    if logic.CheckReg(new_user['username']):
        r = alchemy.conn.execute(alchemy.insUsers, 
            username = new_user['username'],
            password = new_user['password'],
            lvl = new_user['lvl']
        )
        return 'User has created'
    return 'Error'


@app.post('/createpost')
def CreatePost(postreg: PostReg):
    new_post = postreg.dict()
    helpers = new_post['helpers']

    if not logic.CheckCreateRights(new_post['author']): # Отправляем id пользователя на проверку
        return 'Error, your level is low.'

    for i in helpers: 
        if not logic.CheckCreateRights(i):  # Делаем то же самое с помощниками
            return 'Error, check your helpers level. 1 or more of them is low.'
    
    r = alchemy.conn.execute(alchemy.insPosts, 
            name = new_post['name'],
            author = new_post['author'],
            lvl = new_post['lvl'])
    
    for i in helpers:
        alchemy.conn.execute(alchemy.insHelpers,
            id = i,
            posts = r.inserted_primary_key[0])

    logic.SaveContent(new_post['content'], r.inserted_primary_key[0])

            
    return 'ok'