import datetime
import logging
import uuid

import grpc
import jwt
from google.protobuf.timestamp_pb2 import Timestamp
import sqlalchemy.orm.exc

import models
import protos.todo.todo_pb2 as todo_pb2
import protos.todo.todo_pb2_grpc as todo_pb2_grpc
from session import DbSession

logger = logging.getLogger(__name__)

class ToDoEntryMapper():
  @staticmethod
  def to_protobuf(todo):
    updated_at = None
    if todo.updated_at is not None:
      updated_at = Timestamp().FromDatetime(todo.updated_at)

    return todo_pb2.ToDoEntry(
      id = todo.id,
      title = todo.title,
      text = todo.text,
      created_at = Timestamp().FromDatetime(todo.created_at),
      updated_at = updated_at)


class ToDoServicer(todo_pb2_grpc.ToDoServicer):
  def CreateToDo(self, request, context):
    response = todo_pb2.CreateToDoRsp()
    user_id = self.__get_user_id_from_token(context)
    todo_item = request.item

    try:
      with DbSession.session_scope() as session:
        new_todo_item = models.ToDoEntry(
          user_id=user_id,
          title=todo_item.title,
          text=todo_item.text)
        session.add(new_todo_item)
        session.commit()
        response.id = new_todo_item.id
    except sqlalchemy.exc.SQLAlchemyError as err:
      logger.error("SQLAlchemyError {}".format(str(err)))
      context.set_code(grpc.StatusCode.UNKNOWN)

    return response

  def GetToDo(self, request, context):
    response = todo_pb2.GetToDoRsp()
    user_id = self.__get_user_id_from_token(context)
    todo_id = request.id

    try:
      with DbSession.session_scope() as session:
        todo_item = session.query(models.ToDoEntry) \
          .filter_by(id=todo_id, user_id=user_id).one()
        response.item.CopyFrom(ToDoEntryMapper.to_protobuf(todo_item))
    except sqlalchemy.orm.exc.NoResultFound as err:
      logger.error("NoResultFound {}".format(str(err)))
      context.set_code(grpc.StatusCode.NOT_FOUND)
      context.set_details("ToDoEntry not found")
    except sqlalchemy.exc.SQLAlchemyError as err:
      logger.error("SQLAlchemyError {}".format(str(err)))
      context.set_code(grpc.StatusCode.UNKNOWN)

    return response

  def DeleteToDo(self, request, context):
    user_id = self.__get_user_id_from_token(context)
    todo_id = request.id

    try:
      with DbSession.session_scope() as session:
        number = session.query(models.ToDoEntry) \
          .filter_by(id=todo_id, user_id=user_id) \
          .delete(synchronize_session="fetch")
        session.commit()
        if number == 0:
          context.set_code(grpc.StatusCode.NOT_FOUND)
          context.set_details("ToDoEntry not found")
    except sqlalchemy.exc.SQLAlchemyError as err:
      logger.error("SQLAlchemyError {}".format(str(err)))
      context.set_code(grpc.StatusCode.UNKNOWN)

    return todo_pb2.DeleteToDoRsp()

  def UpdateToDo(self, request, context):
    user_id = self.__get_user_id_from_token(context)
    todo_item = request.item
    todo_id = todo_item.id

    try:
      with DbSession.session_scope() as session:
        number = session.query(models.ToDoEntry) \
          .filter_by(id=todo_id, user_id=user_id) \
          .update(
            {models.ToDoEntry.title: todo_item.title,
            models.ToDoEntry.text: todo_item.text,
            models.ToDoEntry.updated_at: datetime.datetime.utcnow()},
            synchronize_session="fetch")
        if number == 0:
          context.set_code(grpc.StatusCode.NOT_FOUND)
          context.set_details("ToDoEntry not found")
    except sqlalchemy.exc.SQLAlchemyError as err:
      logger.error("SQLAlchemyError {}".format(str(err)))
      context.set_code(grpc.StatusCode.UNKNOWN)

    return todo_pb2.UpdateToDoRsp()

  def ListToDo(self, request, context):
    response = todo_pb2.ListToDoRsp()
    user_id = self.__get_user_id_from_token(context)
    limit = request.limit

    try:
      with DbSession.session_scope() as session:
        todo_items_db = session.query(models.ToDoEntry) \
          .filter_by(user_id=user_id) \
          .limit(limit)
        for todo_item_db in todo_items_db:
          response.items.append(ToDoEntryMapper.to_protobuf(todo_item_db))
    except sqlalchemy.exc.SQLAlchemyError as err:
      logger.error("SQLAlchemyError {}".format(str(err)))
      context.set_code(grpc.StatusCode.UNKNOWN)

    return response

  def __get_user_id_from_token(self, context):
    metadata = dict(context.invocation_metadata())
    decoded_payload = jwt.decode(metadata["user-token"], verify=False)
    return decoded_payload["sub"]
