import grift
import schematics.types as sch_types

class AppConfig(grift.BaseConfig):
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


loaders = [grift.EnvLoader()]
settings = AppConfig(loaders)
