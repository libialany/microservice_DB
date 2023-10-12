from enum import Enum

class SwaggerVars(Enum):
  FILE = "./routes/doc/swagger.yml"
  ROUTE = "/doc"

class Errores(Enum):
  UNREACHABLE = "runner_on_unreachable"
  FAILED =  "runner_on_failed"
  ITEMFAILED = "runner_item_on_failed"
class record_types(Enum):
  TIPOS=['A']
class ArchivosCluster(Enum):
  MAIN = 'main.yml'
  INVENTORY = 'inventory.ini'
  RUTA = './clusters'

class LogsVars(Enum):
  FILE = './clusters/terraform.log'
  LIMITE = 10000
  FILE_ERROR = './clusters/terraform-errores.log'
