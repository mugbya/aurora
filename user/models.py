from user.db import Model, StringField, BooleanField, FloatField, TextField, IntegerField


class User(Model):
    __table__ = 'users'

    id = IntegerField(primary_key=True,)
    email = StringField(ddl='varchar(50)')
    password = StringField(ddl='varchar(50)')
    username = StringField(ddl='varchar(50)')
    nickname = StringField(ddl='varchar(50)')
