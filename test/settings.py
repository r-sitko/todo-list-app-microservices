import grift
import schematics.types as sch_types

class AppConfig(grift.BaseConfig):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    with open(self.CERT_FOLDER + "/" + self.SERVER_CERT_FILE, "rb") as fh:
       self.SERVER_CERT = fh.read()
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
  CERT_FOLDER = grift.ConfigProperty(
    property_type=sch_types.StringType(),
    exclude_from_varz=True)
  SERVER_CERT_FILE = grift.ConfigProperty(
    property_type=sch_types.StringType(),
    exclude_from_varz=True)
  JWT_PRIVATE_KEY_FILE = grift.ConfigProperty(
    property_type=sch_types.StringType(),
    exclude_from_varz=True)
  JWT_PUBLIC_KEY_FILE = grift.ConfigProperty(
    property_type=sch_types.StringType(),
    exclude_from_varz=True)


loaders = [grift.EnvLoader()]
settings = AppConfig(loaders)
