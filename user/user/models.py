import uuid

from sqlalchemy import Column, String
from sqlalchemy_utils import UUIDType
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates
from validate_email import validate_email

Base = declarative_base()

class User(Base):
  __tablename__ = "Users"
  __id = Column("id", UUIDType(binary=False), primary_key=True,
    unique=True, nullable=False, default=uuid.uuid4)
  username = Column(String(100), nullable=False)
  password = Column(String(128), nullable=False)
  __salt = Column("salt", UUIDType(binary=False), unique=True, nullable=False)
  email = Column(String(100), unique=True, nullable=False)

  @validates("email")
  def validate_email(self, key, address):
    if not validate_email(address):
      raise EmailUserValidationError()
    return address

  @hybrid_property
  def id(self):
    return str(self.__id)

  @property
  def salt(self):
    return str(self.__salt)

  @salt.setter
  def salt(self, salt):
    self.__salt = salt


class UserValidationError(Exception):
  def __init__(self, message):
    super().__init__(message)

class EmailUserValidationError(UserValidationError):
  def __init__(self):
    super().__init__("Email is incorrect.")
