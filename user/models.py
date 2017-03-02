import time, uuid

from db import Model, StringField, BooleanField, FloatField, TextField, IntegerField


def next_id():
    return '%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex)


class User(Model):
    __table__ = 'users'

    # id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    id = IntegerField(primary_key=True,)
    email = StringField(ddl='varchar(50)')
    password = StringField(ddl='varchar(50)')
    username = StringField(ddl='varchar(50)')
    nickname = StringField(ddl='varchar(50)')
