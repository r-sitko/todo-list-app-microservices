from concurrent import futures
import logging
import os
import time

import grpc
import mysql.connector

import protos.user.user_pb2_grpc as user_pb2_grpc
from user_servicer import UserServicer
from settings import settings
import models
import session

logger = logging.getLogger(__name__)

def database_not_ready_yet(error, checking_interval_seconds):
  print(
    "Database is not ready yet. \
    Retrying after {} second(s). \
    Returned database error: {}."
    .format(checking_interval_seconds,
      repr(error)))
  time.sleep(checking_interval_seconds)

def wait_for_db_ready(host, port, db, user, password, checking_interval_seconds):
  logger.info("Waiting for database.")
  database_ready = False
  while not database_ready:
    db_connection = None
    try:
      db_connection = mysql.connector.connect(
        host=host,
        port=port,
        db=db,
        user=user,
        password=password,
        connect_timeout=5)
      db_connection.ping()
      logger.info("Database ping successful.")
      database_ready = True
      logger.info("Database is ready.")
    except mysql.connector.InterfaceError as err:
      database_not_ready_yet(err, checking_interval_seconds)
    except Exception as err:
      database_not_ready_yet(err, checking_interval_seconds)
    else:
      db_connection.close()

class App():
  __ONE_DAY_IN_SECONDS = 60 * 60 * 24

  def __enter__(self):
    log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    logger.info("{} is starting".format(settings.SERVICE_NAME))

    wait_for_db_ready(
      settings.MYSQL_HOST,
      int(settings.MYSQL_PORT),
      settings.MYSQL_DATABASE,
      settings.MYSQL_USER,
      settings.MYSQL_PASSWORD,
      1)

    session.DbSession.init_db_session()
    models.Base.metadata.create_all(session.DbSession.get_engine())

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    user_pb2_grpc.add_UserServicer_to_server(UserServicer(), server)
    server.add_insecure_port("{service}:{port}"
      .format(service=settings.SERVICE_NAME, port=settings.SERVICE_PORT))
    server.start()

    try:
      while True:
        time.sleep(App.__ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
      server.stop(0)

  def __exit__(self, exc_type, exc_value, traceback):
    logger.info("{} is going down".format(settings.SERVICE_NAME))
