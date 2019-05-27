import datetime

import jwt

from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy_utils import UUIDType
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property

Base = declarative_base()

class ToDoEntry(Base):
  __tablename__ = "ToDos"
  id = Column("id", Integer, primary_key=True, autoincrement=True)
  __user_id = Column("user_id", UUIDType(binary=False), nullable=False)
  title = Column(String(200), nullable=False)
  text = Column(String(2000), nullable=False)
  created_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
  updated_at = Column(DateTime)

  @hybrid_property
  def user_id(self):
    return self.__user_id

  @user_id.setter
  def user_id(self, user_id):
    self.__user_id = user_id
