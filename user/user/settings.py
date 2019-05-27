import grift
import schematics.types as sch_types

class AppConfig(grift.BaseConfig):
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
  MYSQL_USER = grift.ConfigProperty(
    property_type=sch_types.StringType(),
    exclude_from_varz=True)
  MYSQL_PASSWORD = grift.ConfigProperty(
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
settings = AppConfig(loaders)
