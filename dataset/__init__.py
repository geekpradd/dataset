import os
# shut up useless SA warning:
import warnings
warnings.filterwarnings(
    'ignore', 'Unicode type received non-unicode bind param value.')

from dataset.persistence.util import sqlite_datetime_fix
from dataset.persistence.database import Database
from dataset.persistence.table import Table
from dataset.freeze.app import freeze
import sqlite3
__all__ = ['Database', 'Table', 'freeze', 'connect']

def createsqlite3(name,sql=None,file=None):
    db=sqlite3.connect(name)
    if sql is None and file is None:
        raise ValueError("Either sql or file paramter must be supplied to create a database")
        return False
    elif sql is None:
        if file.split('.')[-1]!='sql':
            raise TypeError("Only sql extension is supported for creating database from file")
        else:
            with open(file,'r') as f:
                data=f.read()
            db.cursor().execute(data)
    elif file is None:
        db.cursor().execute(sql)
    return True
        db.cursor().execute()
def connect(url=None, schema=None, reflectMetadata=True, engine_kwargs=None):
    """
    Opens a new connection to a database. *url* can be any valid `SQLAlchemy engine URL`_.
    If *url* is not defined it will try to use *DATABASE_URL* from environment variable.
    Returns an instance of :py:class:`Database <dataset.Database>`. Set *reflectMetadata* to False if you
    don't want the entire database schema to be pre-loaded. This significantly speeds up
    connecting to large databases with lots of tables. Additionally, *engine_kwargs* will be directly passed to
    SQLAlchemy, e.g. set *engine_kwargs={'pool_recycle': 3600}* will avoid `DB connection timeout`_.
    ::

        db = dataset.connect('sqlite:///factbook.db')

    .. _SQLAlchemy Engine URL: http://docs.sqlalchemy.org/en/latest/core/engines.html#sqlalchemy.create_engine
    .. _DB connection timeout: http://docs.sqlalchemy.org/en/latest/core/pooling.html#setting-pool-recycle
    """
    if url is None:
        url = os.environ.get('DATABASE_URL', url)

    if url.startswith("sqlite://"):
        sqlite_datetime_fix()

    return Database(url, schema=schema, reflectMetadata=reflectMetadata,
                    engine_kwargs=engine_kwargs)
