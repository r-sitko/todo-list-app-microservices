import logging
import unittest

import grpc

from settings import settings

logger = logging.getLogger(__name__)

class End2EndTestBase(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.DEBUG, format=log_fmt)

  @classmethod
  def tearDownClass(cls):
    pass

  def setUp(self):
    credentials = grpc.ssl_channel_credentials(root_certificates=settings.SERVER_CERT)
    self.channel = grpc.secure_channel("{service}:{port}"
      .format(service=settings.SERVICE_NAME, port=settings.SERVICE_PORT), credentials)
    grpc.channel_ready_future(self.channel).result()

  def tearDown(self):
    self.channel.close()
