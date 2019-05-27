import datetime
import logging
import unittest

import grpc
import jwt

import e2e_base
import protos.todo.todo_pb2 as todo_pb2
import protos.todo.todo_pb2_grpc as todo_pb2_grpc
import protos.user.user_pb2 as user_pb2
import protos.user.user_pb2_grpc as user_pb2_grpc
from settings import settings

logger = logging.getLogger(__name__)

class ToDoServiceEnd2EndTest(e2e_base.End2EndTestBase):
  def setUp(self):
    super().setUp()
    self.user_stub = user_pb2_grpc.UserStub(self.channel)
    self.todo_stub = todo_pb2_grpc.ToDoStub(self.channel)

  def test_create_get_update_list_delete_todos(self):
    response = self.user_stub.Register(user_pb2.RegisterReq(
      username="todo_user", password="todo_pass", email="todo_test@todo_test.com"))
    response = self.user_stub.Login(user_pb2.LoginReq(
      username="todo_user", password="todo_pass"))

    jwt_token = (("authorization", response.jwt_token),)

    test_todo_entry_1 = todo_pb2.ToDoEntry(
      title="Title 1",
      text="Text 1"
    )
    test_todo_entry_2 = todo_pb2.ToDoEntry(
      title="Title 2",
      text="Text 2"
    )

    # Create two todos
    response = self.todo_stub.CreateToDo(
      todo_pb2.CreateToDoReq(item=test_todo_entry_1),
      metadata=jwt_token)
    test_todo_entry_1.id = response.id
    response = self.todo_stub.CreateToDo(
      todo_pb2.CreateToDoReq(item=test_todo_entry_2),
      metadata=jwt_token)
    test_todo_entry_2.id = response.id

    # Modify first todo
    test_todo_entry_1.title = "New Title 1"
    test_todo_entry_1.text = "New Text 1"
    self.todo_stub.UpdateToDo(
      todo_pb2.UpdateToDoReq(item=test_todo_entry_1),
      metadata=jwt_token)

    # Try modify nonexisting todo (should response with error)
    with self.assertRaises(grpc.RpcError) as cm:
      self.todo_stub.UpdateToDo(
        todo_pb2.UpdateToDoReq(item=todo_pb2.ToDoEntry(
          id=10000,
          title="Fake todo",
          text="Fake todo"
        )),
        metadata=jwt_token)
    self.assertEqual(cm.exception.code(), grpc.StatusCode.NOT_FOUND)

    # List todos (should be two todos)
    response = self.todo_stub.ListToDo(
      todo_pb2.ListToDoReq(limit=10),
      metadata=jwt_token)
    self.assertEqual(len(response.items), 2)
    self.assertEqual(response.items[0], test_todo_entry_1)
    self.assertEqual(response.items[1], test_todo_entry_2)

    # Get second todo
    response = self.todo_stub.GetToDo(
      todo_pb2.GetToDoReq(id=test_todo_entry_2.id),
      metadata=jwt_token)
    self.assertEqual(response.item, test_todo_entry_2)

    # Delete first todo
    self.todo_stub.DeleteToDo(
      request=todo_pb2.DeleteToDoReq(id=test_todo_entry_1.id),
      metadata=jwt_token)

    # List todos (should be one todo)
    response = self.todo_stub.ListToDo(
      todo_pb2.ListToDoReq(limit=10),
      metadata=jwt_token)
    self.assertEqual(len(response.items), 1)
    self.assertEqual(response.items[0], test_todo_entry_2)

    # Try to get deleted todo (should response with error)
    with self.assertRaises(grpc.RpcError) as cm:
      self.todo_stub.GetToDo(
        todo_pb2.GetToDoReq(id=test_todo_entry_1.id),
        metadata=jwt_token)
    self.assertEqual(cm.exception.code(), grpc.StatusCode.NOT_FOUND)

    # Delete second todo
    self.todo_stub.DeleteToDo(
      request=todo_pb2.DeleteToDoReq(id=test_todo_entry_2.id),
      metadata=jwt_token)

    # Try to delete nonexisting todo (should response with error)
    with self.assertRaises(grpc.RpcError) as cm:
      self.todo_stub.DeleteToDo(
        request=todo_pb2.DeleteToDoReq(id=test_todo_entry_2.id),
        metadata=jwt_token)
    self.assertEqual(cm.exception.code(), grpc.StatusCode.NOT_FOUND)

    # List todos (should be zero todo)
    response = self.todo_stub.ListToDo(
      todo_pb2.ListToDoReq(limit=10),
      metadata=jwt_token)
    self.assertEqual(len(response.items), 0)

  def test_error_when_wrong_token(self):
    test_metadata = (("authorization", "wrong_token"),)

    with self.assertRaises(grpc.RpcError) as cm:
      self.todo_stub.CreateToDo(
        todo_pb2.CreateToDoReq(
          item=todo_pb2.ToDoEntry(
            title="Title 2",
            text="Text 2")
          ),
          metadata=test_metadata)
    self.assertEqual(cm.exception.code(), grpc.StatusCode.UNAUTHENTICATED)

    with self.assertRaises(grpc.RpcError) as cm:
      self.todo_stub.GetToDo(
        todo_pb2.GetToDoReq(id=1),
        metadata=test_metadata)
    self.assertEqual(cm.exception.code(), grpc.StatusCode.UNAUTHENTICATED)

    with self.assertRaises(grpc.RpcError) as cm:
      self.todo_stub.DeleteToDo(
        request=todo_pb2.DeleteToDoReq(id=1),
        metadata=test_metadata)
    self.assertEqual(cm.exception.code(), grpc.StatusCode.UNAUTHENTICATED)

    with self.assertRaises(grpc.RpcError) as cm:
      self.todo_stub.UpdateToDo(
        todo_pb2.UpdateToDoReq(item=todo_pb2.ToDoEntry(
          id=1,
          title="title",
          text="text"
        )),
        metadata=test_metadata)
    self.assertEqual(cm.exception.code(), grpc.StatusCode.UNAUTHENTICATED)

    with self.assertRaises(grpc.RpcError) as cm:
      self.todo_stub.ListToDo(
        todo_pb2.ListToDoReq(limit=10),
        metadata=test_metadata)
    self.assertEqual(cm.exception.code(), grpc.StatusCode.UNAUTHENTICATED)
