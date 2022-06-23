from sqlalchemy import MetaData, Table, String, Integer, Column, Text, DateTime, Boolean, create_engine, ForeignKey, insert, select

engine = create_engine("postgresql+psycopg2://mark:1234@localhost/practice")
conn = engine.connect()

print(engine)

metadata = MetaData(engine)

users = Table('users', metadata, 
    Column('id', Integer(), primary_key=True),
    Column('username', String(20), nullable=False),
    Column('password', String(90),  nullable=False),
    Column('lvl', Integer(), nullable=False),
    Column('posts', ForeignKey('posts.id')) #подразумевается только авторство, помощники отдельная таблица.
)

helpers = Table('helpers', metadata, 
    Column('id', ForeignKey('users.id')),
    Column('posts', ForeignKey('posts.id')) 
)

posts = Table('posts', metadata, 
    Column('id', Integer(), primary_key=True),
    Column('name', String(100), nullable=False),
    Column('author', ForeignKey('users.id')),
    Column('lvl', Integer(), nullable=False),
)

insUsers = insert(users)
selUsers = select([users])
insHelpers = insert(helpers)
selHelpers = select([helpers])
insPosts = insert(posts)
selPosts = select([posts])
metadata.create_all()
