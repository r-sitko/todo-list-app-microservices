import logging
import os
import socket
import sys
import time
import unittest

import grift
import grpc
import jwt
import schematics.types as sch_types
import sqlalchemy

import protos.user.user_pb2 as user_pb2
import protos.user.user_pb2_grpc as user_pb2_grpc

logger = logging.getLogger(__name__)

class TestConfig(grift.BaseConfig):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    with open(self.CERT_FOLDER + "/" + self.JWT_PUBLIC_KEY_FILE, "rb") as fh:
       self.JWT_PUBLIC_KEY = fh.read()

  SERVICE_NAME = grift.ConfigProperty(
    property_type=sch_types.StringType(),
    exclude_from_varz=True)
  SERVICE_PORT = grift.ConfigProperty(
    property_type=sch_types.IntType(),
    exclude_from_varz=True)
  MYSQL_HOST = grift.ConfigProperty(
    property_type=sch_types.StringType(),
    exclude_from_varz=True)
  MYSQL_PORT = grift.ConfigProperty(
    property_type=sch_types.IntType(),
    exclude_from_varz=True)
  MYSQL_ROOT_PASSWORD = grift.ConfigProperty(
    property_type=sch_types.StringType(),
    exclude_from_varz=True)
  MYSQL_DATABASE = grift.ConfigProperty(
    property_type=sch_types.StringType(),
    exclude_from_varz=True)
  CERT_FOLDER = grift.ConfigProperty(
    property_type=sch_types.StringType(),
    exclude_from_varz=True)
  JWT_PUBLIC_KEY_FILE = grift.ConfigProperty(
    property_type=sch_types.StringType(),
    exclude_from_varz=True)


loaders = [grift.EnvLoader()]
settings = TestConfig(loaders)

class TestUserService(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.DEBUG, format=log_fmt)

  @classmethod
  def tearDownClass(cls):
    pass

  def setUp(self):
    self.channel = grpc.insecure_channel("{service}:{port}"
      .format(service=settings.SERVICE_NAME, port=settings.SERVICE_PORT))
    grpc.channel_ready_future(self.channel).result()
    self.stub = user_pb2_grpc.UserStub(self.channel)

  def tearDown(self):
    self.channel.close()
    self._drop_all_service_tables()

  def _drop_all_service_tables(self):
    db_ip = socket.gethostbyname(settings.MYSQL_HOST)
    db_url = "mysql+mysqlconnector://{user}:{password}@{host}:{port}/{dbname}".format(
      user="root",
      password=settings.MYSQL_ROOT_PASSWORD,
      host=db_ip,
      port=settings.MYSQL_PORT,
      dbname=settings.MYSQL_DATABASE)
    engine = sqlalchemy.create_engine(db_url)
    meta_data = sqlalchemy.MetaData()
    meta_data.reflect(bind=engine)
    for table in reversed(meta_data.sorted_tables):
      engine.execute(table.delete())

  def test_register_user_and_login(self):
    response = self.stub.Register(user_pb2.RegisterReq(
      username="me", password="pass", email="example@example.com"))
    response = self.stub.Login(user_pb2.LoginReq(
      username="me", password="pass"))
    decoded_payload = jwt.decode(
      response.jwt_token,
      settings.JWT_PUBLIC_KEY,
      algorithms=["RS256"])
    assert "sub" in decoded_payload
    assert "exp" in decoded_payload

  def test_login_not_registered_user(self):
    with self.assertRaises(grpc.RpcError) as cm:
      self.stub.Login(user_pb2.LoginReq(username="you", password="pass"))
    self.assertEqual(cm.exception.code(), grpc.StatusCode.UNAUTHENTICATED)

  def test_register_user_wrong_email(self):
    with self.assertRaises(grpc.RpcError) as cm:
      self.stub.Register(user_pb2.RegisterReq(
        username="John", password="pass", email="wrong_email"))
    self.assertEqual(cm.exception.code(), grpc.StatusCode.INVALID_ARGUMENT)
