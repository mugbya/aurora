import asyncpg
from config import settings

import logging

logger = logging.getLogger()

'''
asyncpg 封装 + orm
'''


def log(sql, args=()):
    logging.info('SQL: %s' % sql)


async def setup_connection(app, loop):
    '''
    创建数据库连接池

    监听数据库连接数变化
    select * from pg_stat_activity;

    :param app:
    :param loop:
    :return:
    '''
    global _pool
    logger.info('create database connection pool...')
    _pool = await asyncpg.create_pool(**settings.DB_CONFIG)
    return _pool


async def close_connection(app, loop):
    '''
    :param app:
    :param loop:
    :return:
    '''
    await _pool.close()
    logger.info('database pool died ')


async def select(sql, *args, size=None):
    log(sql, args)
    async with _pool.acquire() as con:
        # async with con.transaction():
            # cur = await con.fetch(sql.replace('?', '%s'), args or ())
        rs = await con.fetch(sql, *args)
        logging.info('rows returned: %s' % len(rs))
        return rs


async def execute(sql, *args, autocommit=True):
    log(sql)
    async with _pool.acquire() as con:
        rs = await con.execute(sql, *args)
        return rs
    # with (yield from __pool) as conn:
    #     if not autocommit:
    #         yield from conn.begin()
    #     try:
    #         cur = yield from conn.cursor()
    #         yield from cur.execute(sql.replace('?', '%s'), args)
    #         affected = cur.rowcount
    #         yield from cur.close()
    #         if not autocommit:
    #             yield from conn.commit()
    #     except BaseException as e:
    #         if not autocommit:
    #             yield from conn.rollback()
    #         raise
    #     return affected

def create_args_string(num):
    L = []
    for n in range(num):
        L.append('$' + str(n+1))
    return ', '.join(L)


class Field(object):
    def __init__(self, name, column_type, primary_key, default):
        self.name = name
        self.column_type = column_type
        self.primary_key = primary_key
        self.default = default

    def __str__(self):
        return '<%s, %s:%s>' % (self.__class__.__name__, self.column_type, self.name)


class StringField(Field):
    def __init__(self, name=None, primary_key=False, default=None, ddl='varchar(100)'):
        super().__init__(name, ddl, primary_key, default)


class BooleanField(Field):
    def __init__(self, name=None, default=False):
        super().__init__(name, 'boolean', False, default)


class IntegerField(Field):
    def __init__(self, name=None, primary_key=False, default=0):
        super().__init__(name, 'bigint', primary_key, default)


class FloatField(Field):
    def __init__(self, name=None, primary_key=False, default=0.0):
        super().__init__(name, 'real', primary_key, default)


class TextField(Field):
    def __init__(self, name=None, default=None):
        super().__init__(name, 'text', False, default)


class ModelMetaclass(type):
    def __new__(cls, name, bases, attrs):
        if name == 'Model':
            return type.__new__(cls, name, bases, attrs)
        tableName = attrs.get('__table__', None) or name
        logging.info('found model: %s (table: %s)' % (name, tableName))
        mappings = dict()
        fields = []
        primaryKey = None
        for k, v in attrs.items():
            if isinstance(v, Field):
                logging.info('  found mapping: %s ==> %s' % (k, v))
                mappings[k] = v
                if v.primary_key:
                    # 找到主键:
                    if primaryKey:
                        raise Exception('Duplicate primary key for field: %s' % k)
                    primaryKey = k
                else:
                    fields.append(k)
        if not primaryKey:
            raise Exception('Primary key not found.')
        for k in mappings.keys():
            attrs.pop(k)
        escaped_fields = list(map(lambda f: '%s' % f, fields))
        attrs['__mappings__'] = mappings  # 保存属性和列的映射关系
        attrs['__table__'] = tableName
        attrs['__primary_key__'] = primaryKey  # 主键属性名
        attrs['__fields__'] = fields  # 除主键外的属性名
        attrs['__select__'] = 'select %s, %s from %s' % (primaryKey, ', '.join(escaped_fields), tableName)
        # attrs['__insert__'] = 'insert into %s (%s, %s) values (%s)' % (tableName, ', '.join(escaped_fields), primaryKey, create_args_string(len(escaped_fields) + 1))
        attrs['__insert__'] = 'insert into %s (%s) values (%s)' % (tableName, ', '.join(escaped_fields), create_args_string(len(escaped_fields)))
        # attrs['__update__'] = 'update %s set %s where %s=?' % (tableName, ', '.join(map(lambda f: '%s=?' % (mappings.get(f).name or f), fields)), primaryKey)
        attrs['__update__'] = 'update %s set ' % (tableName, )
        attrs['__delete__'] = 'delete from %s where %s=$1' % (tableName, primaryKey)
        return type.__new__(cls, name, bases, attrs)


class Model(dict, metaclass=ModelMetaclass):
    def __init__(self, **kw):
        super(Model, self).__init__(**kw)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

    def get_primary_key(self, primary_val=None):
        '''
        获取主键值，并处理
        :return:
        '''
        if not primary_val:
            primary_val = self.getValue(self.__primary_key__)

        # 处理主键类型 asyncpg 区分类型
        if isinstance(self.__mappings__.get(self.__primary_key__), IntegerField):
            return int(primary_val)
        else:
            return primary_val

    def getValue(self, key):
        '''
        获取属性值
        :param key:
        :return:
        '''
        return getattr(self, key, None)

    def getValueOrDefault(self, key):
        value = getattr(self, key, None)
        if value is None:
            field = self.__mappings__[key]
            if field.default is not None:
                value = field.default() if callable(field.default) else field.default
                logging.debug('using default value for %s: %s' % (key, str(value)))
                setattr(self, key, value)
        return value

    @classmethod
    async def all(cls):
        '''
        find all objects
        :return:
        '''
        sql = [cls.__select__]
        rs = await select(' '.join(sql))
        return [cls(**r) for r in rs]

    @classmethod
    async def filter(cls, *args, **kw):
        '''
        find objects by where clause
        :param args:
        :param kw: Query parameters
        :return:
        '''
        sql = [cls.__select__]
        if kw:
            sql.append('where')
        if not args:
            args = []

        # 用占位符构造查询条件
        for index, key in enumerate(kw.keys()):
            index += 1
            sql.append(key + '=$' + str(index))
            args.append(kw.get(key))

        rs = await select(' '.join(sql), *args)
        return [cls(**r) for r in rs]

    @classmethod
    async def get(cls, *args, **kw):
        '''
        返回对象
        :param args:
        :param kw:
        :return:
        '''
        sql = [cls.__select__]
        if kw:
            sql.append('where')
        if not args:
            args = []

        # 用占位符构造查询条件
        for index, key in enumerate(kw.keys()):
            index += 1
            sql.append(key + '=$' + str(index))
            args.append(kw.get(key))

        res = await select(' '.join(sql), *args)
        return [type(cls.__name__, (Model, ), cls(**r)) for r in res]

    @classmethod
    async def findAll(cls, where=None, *args, **kw):
        ' find objects by where clause. '
        sql = [cls.__select__]
        if where:
            sql.append('where')
            sql.append(where)
        if args is None:
            args = []
        orderBy = kw.get('orderBy', None)
        if orderBy:
            sql.append('order by')
            sql.append(orderBy)
        limit = kw.get('limit', None)
        if limit is not None:
            sql.append('limit')
            if isinstance(limit, int):
                sql.append('?')
                args.append(limit)
            elif isinstance(limit, tuple) and len(limit) == 2:
                sql.append('?, ?')
                args.extend(limit)
            else:
                raise ValueError('Invalid limit value: %s' % str(limit))
        rs = await select(' '.join(sql), *args)
        return [cls(**r) for r in rs]

    @classmethod
    async def findNumber(cls, selectField, where=None, args=None):
        ' find number by select and where. '
        sql = ['select %s _num_ from `%s`' % (selectField, cls.__table__)]
        if where:
            sql.append('where')
            sql.append(where)
        rs = await select(' '.join(sql), args, 1)
        if len(rs) == 0:
            return None
        return rs[0]['_num_']

    @classmethod
    async def find(cls, pk):
        ' find object by primary key. '
        rs = await select('%s where `%s`=?' % (cls.__select__, cls.__primary_key__), [pk], 1)
        if len(rs) == 0:
            return None
        return cls(**rs[0])

    async def save(self):
        args = list(map(self.getValueOrDefault, self.__fields__))

        rows = await execute(self.__insert__, *args)
        if not rows:
            logging.warn('failed to insert record: affected rows: %s' % rows)
            return False
        else:
            return True

    async def update(self):
        try:
            primary_val = self.pop(self.__primary_key__)

            args = list(map(self.getValue, self.keys()))
            args.append(self.get_primary_key(primary_val=primary_val))

            sql = self.__update__
            index = 0
            for index, key in enumerate(self.keys()):
                index += 1
                sql += key + '=$' + str(index) + ', '
            sql = sql[0:-2] + ' where id=$' + str(index+1)
            rows = await execute(sql, *args)

            if rows == 'UPDATE 0':
                raise Exception('record not exits')
            elif rows == 'UPDATE 1':
                return True
            return False
        except Exception as e:
            raise Exception(e)

    async def delete(self):
        args = [self.get_primary_key()]
        rows = await execute(self.__delete__, *args)
        if rows == 'DELETE 0':
            raise Exception('record not exits')
        elif rows == 'DELETE 1':
            return True
        return False


