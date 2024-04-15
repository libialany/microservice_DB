from enum import Enum
from dotenv import load_dotenv
load_dotenv()
import os
class SwaggerVars(Enum):
  FILE = "./routes/doc/swagger.yml"
  ROUTE = "/doc"

class Errores(Enum):
  UNREACHABLE = "runner_on_unreachable"
  FAILED =  "runner_on_failed"
  ITEMFAILED = "runner_item_on_failed"

class Vars(Enum):
  BACKUPS = "%s@config_backup.yml" % os.getenv("PATH_FOLDER_VARIABLES")

class ArchivosCluster(Enum):
  MAIN = 'main.yml'
  INVENTORY = "%s/inventory.ini" % os.getenv("PATH_FOLDER_NFS")
  RUTA = './logs'

class LogsVars(Enum):
  FILE = os.getenv("PATH_LOG")
  LIMITE = 10000
  FILE_ERROR = os.getenv("PATH_LOG")