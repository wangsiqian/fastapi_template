"""sqlalchemy_utils 方法暂不支持 sqlalchemy 2.0 async
"""
from copy import copy

import sqlalchemy as sa
from sqlalchemy.engine.interfaces import Dialect
from sqlalchemy.engine.url import make_url
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import object_session
from sqlalchemy.orm.exc import UnmappedInstanceError


def _set_url_database(url: sa.engine.url.URL, database):
    """Set the database of an engine URL.

    :param url: A SQLAlchemy engine URL.
    :param database: New database to set.

    """
    if hasattr(url, '_replace'):
        # Cannot use URL.set() as database may need to be set to None.
        ret = url._replace(database=database)
    else:  # SQLAlchemy <1.4
        url = copy(url)
        url.database = database
        ret = url
    assert ret.database == database, ret
    return ret


def get_bind(obj):
    """
    Return the bind for given SQLAlchemy Engine / Connection / declarative
    model object.

    :param obj: SQLAlchemy Engine / Connection / declarative model object

    ::

        from sqlalchemy_utils import get_bind


        get_bind(session)  # Connection object

        get_bind(user)

    """
    if hasattr(obj, 'bind'):
        conn = obj.bind
    else:
        try:
            conn = object_session(obj).bind
        except UnmappedInstanceError:
            conn = obj

    return conn


def quote(mixed, ident):
    """
    Conditionally quote an identifier.
    ::


        from sqlalchemy_utils import quote


        engine = create_engine('sqlite:///:memory:')

        quote(engine, 'order')
        # '"order"'

        quote(engine, 'some_other_identifier')
        # 'some_other_identifier'


    :param mixed: SQLAlchemy Session / Connection / Engine / Dialect object.
    :param ident: identifier to conditionally quote
    """
    if isinstance(mixed, Dialect):
        dialect = mixed
    else:
        dialect = get_bind(mixed).dialect
    return dialect.preparer(dialect).quote(ident)


async def _get_scalar_result(engine, sql):
    async with engine.begin() as conn:
        return await conn.scalar(sql)


async def database_exists(url):
    """Check if a database exists.

    :param url: A SQLAlchemy engine URL.

    Performs backend-specific testing to quickly determine if a database
    exists on the server. ::

        database_exists('postgresql://postgres@localhost/name')  #=> False
        create_database('postgresql://postgres@localhost/name')
        database_exists('postgresql://postgres@localhost/name')  #=> True

    Supports checking against a constructed URL as well. ::

        engine = create_engine('postgresql://postgres@localhost/name')
        database_exists(engine.url)  #=> False
        create_database(engine.url)
        database_exists(engine.url)  #=> True

    """

    url = make_url(url)
    database = url.database
    text = f"SHOW DATABASES LIKE {database}"
    url = _set_url_database(url, database=database)
    engine = create_async_engine(url)
    try:
        return bool(await _get_scalar_result(engine, sa.text(text)))
    except Exception as error:
        if str(error).startswith('(pymysql.err.OperationalError) (2003'):
            return False
        else:
            if engine:
                await engine.dispose()

    return True


async def create_database(url):
    """Issue the appropriate CREATE DATABASE statement.

    :param url: A SQLAlchemy engine URL.
    :param encoding: The encoding to create the database as.
    :param template:
        The name of the template from which to create the new database. At the
        moment only supported by PostgreSQL driver.

    To create a database, you can pass a simple URL that would have
    been passed to ``create_engine``. ::

        create_database('postgresql://postgres@localhost/name')

    You may also pass the url from an existing engine. ::

        create_database(engine.url)

    Has full support for mysql, postgres, and sqlite. In theory,
    other database engines should be supported.
    """

    url = make_url(url)
    database = url.database
    url = _set_url_database(url, database="mysql")
    engine = create_async_engine(url, isolation_level='AUTOCOMMIT')

    text = "CREATE DATABASE {}".format(quote(engine, database))

    async with engine.begin() as connection:
        await connection.execute(sa.text(text))

    await engine.dispose()


class WhereClauseWrapper:

    def __init__(self):
        self.conditions = []

    def in_(self, field, expected, condition=True):
        if condition is False:
            return self

        self.conditions.append(field.in_(expected))
        return self

    def eq(self, field, expected, condition=True):
        """等于
        """
        if condition is False:
            return self

        self.conditions.append(field == expected)
        return self

    def ge(self, field, expected, condition=True):
        """大于等于
        """
        if condition is False:
            return self

        self.conditions.append(field >= expected)
        return self

    def le(self, field, expected, condition=True):
        """小于等于
        """
        if condition is False:
            return self

        self.conditions.append(field <= expected)
        return self

    def like_right(self, field, expected, condition=True):
        """右匹配
        """
        if condition is False:
            return self

        self.conditions.append(field.like(f'{expected}%'))
        return self

    def like(self, field, expected, condition=True):
        """匹配
        """
        if condition is False:
            return self

        self.conditions.append(field.like(f'%{expected}%'))
        return self

    def to_where_clause(self) -> list:
        return self.conditions
