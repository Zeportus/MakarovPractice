from email.policy import default
from sqlalchemy import MetaData, Table, String, Integer, Column, Text, DateTime, Boolean, create_engine, ForeignKey, insert, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

engine = create_engine("postgresql+psycopg2://mark:1234@localhost/practice")
session = sessionmaker(bind=engine)
s = session()

Base = declarative_base()
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer(), primary_key=True)
    username = Column(String(20), nullable=False)
    password = Column(String(90),  nullable=False)
    lvl = Column(Integer(), nullable=False)
    active = Column(Boolean(), default=False) # Залогинин или нет
    
class Author(Base):
    __tablename__ = 'authors'
    
    id = Column(Integer(), primary_key=True)
    user_id = Column(ForeignKey('users.id'))
    post_id = Column(ForeignKey('posts.id'))
    user = relationship('User')
    post = relationship('Post')


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer(), primary_key=True)
    post_id = Column(ForeignKey('posts.id'))
    user_id = Column(ForeignKey('users.id'))
    user = relationship('User')
    post = relationship('Post')

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer(), primary_key=True)
    name = Column(String(100), nullable=False)
    lead_author = Column(ForeignKey('users.id'))
    lvl = Column(Integer(), nullable=False)
    comm_count = Column(Integer(), default = 0)
    user = relationship('User')
    

Base.metadata.create_all(engine)
