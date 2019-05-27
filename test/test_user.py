import logging
import unittest

import grpc
import jwt

import e2e_base
import protos.user.user_pb2 as user_pb2
import protos.user.user_pb2_grpc as user_pb2_grpc
from settings import settings

logger = logging.getLogger(__name__)

class UserServiceEnd2EndTest(e2e_base.End2EndTestBase):
  def setUp(self):
    super().setUp()
    self.stub = user_pb2_grpc.UserStub(self.channel)

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
