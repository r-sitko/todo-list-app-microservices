import datetime
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

import protos.todo.todo_pb2 as todo_pb2
import protos.todo.todo_pb2_grpc as todo_pb2_grpc

logger = logging.getLogger(__name__)

class TestConfig(grift.BaseConfig):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    with open(self.CERT_FOLDER + "/" + self.JWT_PRIVATE_KEY_FILE, "rb") as fh:
       self.JWT_PRIVATE_KEY = fh.read()
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
  JWT_PRIVATE_KEY_FILE = grift.ConfigProperty(
    property_type=sch_types.StringType(),
    exclude_from_varz=True)
  JWT_PUBLIC_KEY_FILE = grift.ConfigProperty(
    property_type=sch_types.StringType(),
    exclude_from_varz=True)


loaders = [grift.EnvLoader()]
settings = TestConfig(loaders)


def get_token_expiration_time():
  return datetime.datetime.utcnow() \
    + datetime.timedelta(hours=10)

def generate_token(user_id, expiration_time):
  return jwt.encode(
    {"sub": user_id, "exp": expiration_time},
    settings.JWT_PRIVATE_KEY,
    algorithm="RS256")

class TestToDoService(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.DEBUG, format=log_fmt)

  @classmethod
  def tearDownClass(cls):
    pass

  @property
  def test_metadata(self):
    test_user_id = "12345678123456781234567812345678"
    test_token_expiration_time = get_token_expiration_time()
    return [("user-token", generate_token(test_user_id, test_token_expiration_time))]

  def setUp(self):
    self.channel = grpc.insecure_channel("{service}:{port}"
      .format(service=settings.SERVICE_NAME, port=settings.SERVICE_PORT))
    grpc.channel_ready_future(self.channel).result()
    self.stub = todo_pb2_grpc.ToDoStub(self.channel)

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

  def test_create_get_update_list_delete_todos(self):
    test_todo_entry_1 = todo_pb2.ToDoEntry(
      title="Title 1",
      text="Text 1"
    )
    test_todo_entry_2 = todo_pb2.ToDoEntry(
      title="Title 2",
      text="Text 2"
    )

    # Create two todos
    response = self.stub.CreateToDo(
      todo_pb2.CreateToDoReq(item=test_todo_entry_1),
      metadata=self.test_metadata)
    test_todo_entry_1.id = response.id
    response = self.stub.CreateToDo(
      todo_pb2.CreateToDoReq(item=test_todo_entry_2),
      metadata=self.test_metadata)
    test_todo_entry_2.id = response.id

    # Modify first todo
    test_todo_entry_1.title = "New Title 1"
    test_todo_entry_1.text = "New Text 1"
    self.stub.UpdateToDo(
      todo_pb2.UpdateToDoReq(item=test_todo_entry_1),
      metadata=self.test_metadata)

    # Try modify nonexisting todo (should response with error)
    with self.assertRaises(grpc.RpcError) as cm:
      self.stub.UpdateToDo(
        todo_pb2.UpdateToDoReq(item=todo_pb2.ToDoEntry(
          id=10000,
          title="Fake todo",
          text="Fake todo"
        )),
        metadata=self.test_metadata)
    self.assertEqual(cm.exception.code(), grpc.StatusCode.NOT_FOUND)

    # List todos (should be two todos)
    response = self.stub.ListToDo(
      todo_pb2.ListToDoReq(limit=10),
      metadata=self.test_metadata)
    self.assertEqual(len(response.items), 2)
    self.assertEqual(response.items[0], test_todo_entry_1)
    self.assertEqual(response.items[1], test_todo_entry_2)

    # Get second todo
    response = self.stub.GetToDo(
      todo_pb2.GetToDoReq(id=test_todo_entry_2.id),
      metadata=self.test_metadata)
    self.assertEqual(response.item, test_todo_entry_2)

    # Delete first todo
    self.stub.DeleteToDo(
      request=todo_pb2.DeleteToDoReq(id=test_todo_entry_1.id),
      metadata=self.test_metadata)

    # List todos (should be one todo)
    response = self.stub.ListToDo(
      todo_pb2.ListToDoReq(limit=10),
      metadata=self.test_metadata)
    self.assertEqual(len(response.items), 1)
    self.assertEqual(response.items[0], test_todo_entry_2)

    # Try to get deleted todo (should response with error)
    with self.assertRaises(grpc.RpcError) as cm:
      self.stub.GetToDo(
        todo_pb2.GetToDoReq(id=test_todo_entry_1.id),
        metadata=self.test_metadata)
    self.assertEqual(cm.exception.code(), grpc.StatusCode.NOT_FOUND)

    # Delete second todo
    self.stub.DeleteToDo(
      request=todo_pb2.DeleteToDoReq(id=test_todo_entry_2.id),
      metadata=self.test_metadata)

    # Try to delete nonexisting todo (should response with error)
    with self.assertRaises(grpc.RpcError) as cm:
      self.stub.DeleteToDo(
        request=todo_pb2.DeleteToDoReq(id=test_todo_entry_2.id),
        metadata=self.test_metadata)
    self.assertEqual(cm.exception.code(), grpc.StatusCode.NOT_FOUND)

    # List todos (should be zero todo)
    response = self.stub.ListToDo(
      todo_pb2.ListToDoReq(limit=10),
      metadata=self.test_metadata)
    self.assertEqual(len(response.items), 0)
