from contextlib import contextmanager
import socket

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

from settings import settings

class DbSession():
  __engine = None
  __session = None

  @staticmethod
  def init_db_session():
    db_ip = socket.gethostbyname(settings.MYSQL_HOST)
    db_url = "mysql+mysqlconnector://{user}:{password}@{host}:{port}/{dbname}".format(
      user=settings.MYSQL_USER,
      password=settings.MYSQL_PASSWORD,
      host=db_ip,
      port=settings.MYSQL_PORT,
      dbname=settings.MYSQL_DATABASE)
    DbSession.__engine = create_engine(db_url)
    if not database_exists(DbSession.__engine.url):
      create_database(DbSession.__engine.url)
    session_factory = sessionmaker(bind=DbSession.__engine)
    DbSession.__session = scoped_session(session_factory)

  @staticmethod
  @contextmanager
  def session_scope():
    session = DbSession.get_session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

  @staticmethod
  def get_engine():
    return DbSession.__engine

  @staticmethod
  def get_session():
    return DbSession.__session()
