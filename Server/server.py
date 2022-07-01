from cgitb import html
from distutils import file_util
from html.entities import html5
from fastapi import FastAPI, File
from pydantic import BaseModel, FilePath
import sys
sys.path.insert(0, '/home/mark/Practice/DataBase')
from alchemy import s, User, Post, Author
import logic
from typing import List

app = FastAPI()

class UserReg(BaseModel):
  username: str
  password: str
  lvl: int

class PostReg(BaseModel):
    name: str
    lead_author: int
    lvl: int
    authors: List[int] # Тут будут id помощников
    content: str


@app.get('/')
def HealthCheck():
    return 'ok'


@app.post('/registration')
def Registration(userreg: UserReg):
    if logic.CheckReg(userreg.username):  
        new_user = User(username = userreg.username, password = userreg.password, lvl = userreg.lvl)
        s.add(new_user)
        s.commit()
        return 'Registration successful'
    return 'Username already exists'


@app.post('/createpost')
def CreatePost(postreg: PostReg):
    for i in postreg.authors:
        if not logic.CheckCreateRights(i):
            return 'Check your authors lvls. One or more of them is low'

    if logic.CheckCreateRights(postreg.lead_author):
        new_post = Post(name = postreg.name, lead_author = postreg.lead_author, lvl = postreg.lvl)
        s.add(new_post)
        s.commit()
        post_id = s.query(Post.id).order_by(Post.id.desc()).first()[0]

        new_authors = []
        for i in postreg.authors:
            new_authors.append(Author(user_id = i, post_id = post_id))
        s.add_all(new_authors)
        s.commit()

        logic.SaveContent(postreg.content, post_id)
        return 'Post has been created'
    return 'Post has not been created. Your lvl is low'


@app.get('/post/content/{id}')
def ShowPost(id: int):
    logic.ShowContent(id)
    return 'Content has been opened'
