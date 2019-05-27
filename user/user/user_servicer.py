import binascii
import datetime
import hashlib
import logging
import uuid

import grpc
import jwt
import sqlalchemy.orm.exc
import sqlalchemy.exc

import models
import protos.user.user_pb2 as user_pb2
import protos.user.user_pb2_grpc as user_pb2_grpc
from settings import settings
from session import DbSession

_TOKEN_EXPIRATION_HOURS = 24

logger = logging.getLogger(__name__)

def hash_password(password, salt, hash_name="sha512", iterations=100000):
  dk = hashlib.pbkdf2_hmac(
    hash_name,
    password.encode("utf-8"),
    salt.encode("utf-8"),
    iterations)
  return binascii.hexlify(dk).decode("ascii")

def get_expiration_time():
  return datetime.datetime.utcnow() \
    + datetime.timedelta(hours=_TOKEN_EXPIRATION_HOURS)

def generate_token(user, expiration_time):
  return jwt.encode(
    {"sub": user.id, "exp": expiration_time},
    settings.JWT_PRIVATE_KEY,
    algorithm="RS256")

class UserServicer(user_pb2_grpc.UserServicer):
  def Register(self, request, context):
    username = request.username
    password = request.password
    email = request.email
    salt = uuid.uuid4()
    hashed_password = hash_password(password, str(salt))

    try:
      with DbSession.session_scope() as session:
        new_user = models.User(
          username=username,
          password=hashed_password,
          email=email,
          salt=salt)
        session.add(new_user)
        session.commit()
    except models.EmailUserValidationError as err:
      logger.error("EmailUserValidationError {}".format(str(err)))
      context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
      context.set_details(str(err))
    except sqlalchemy.exc.SQLAlchemyError as err:
      logger.error("SQLAlchemyError {}".format(str(err)))
      context.set_code(grpc.StatusCode.UNKNOWN)

    return user_pb2.RegisterRsp()

  def Login(self, request, context):
    response = user_pb2.LoginRsp()
    username = request.username
    password = request.password

    try:
      with DbSession.session_scope() as session:
        user = session.query(models.User).filter_by(username=username).one()
        hashed_password = hash_password(password, user.salt)
        if user.password == hashed_password:
          expiration_time = get_expiration_time()
          token = generate_token(user, expiration_time)
          response.jwt_token = token
          response.expiration = str(expiration_time)
    except sqlalchemy.orm.exc.NoResultFound as err:
      logger.error("NoResultFound {}".format(str(err)))
      context.set_code(grpc.StatusCode.UNAUTHENTICATED)
      context.set_details("Invalid username or password")
    except sqlalchemy.exc.SQLAlchemyError as err:
      logger.error("SQLAlchemyError {}".format(str(err)))
      context.set_code(grpc.StatusCode.UNKNOWN)

    return response
