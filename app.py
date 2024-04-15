import os
from dotenv import load_dotenv
from flask import Flask
from flasgger import Swagger
from routes.vars import SwaggerVars
from routes.backup import backup_bp
from routes.status import estado_database_bp
from routes.upload import upload_backup_bp
from flask_cors import CORS
from routes.download import download_backup_bp
from routes.create_database import create_database_bp
from routes.editar import editar_bp
from routes.eliminar import eliminar_bp
from routes.reportes_download import reportes_download_backup_bp
from routes.reportes_listar import reportes_listar_backup_bp
from routes.reportes_upload import reportes_upload_backup_bp

app = Flask(__name__)
cors = CORS(app)
import os

load_dotenv()

swagger = Swagger(
    app,
    template_file=SwaggerVars.FILE.value,
    config={
        "url_prefix": f"{os.getenv('PATH_SUBDOMAIN')}",
        "specs_route": SwaggerVars.ROUTE.value,
        "basePath": f"{os.getenv('PATH_SUBDOMAIN')}",
    },
    merge=True,
)

blueprints = [
    create_database_bp,
    backup_bp,
    estado_database_bp,
    upload_backup_bp,
    download_backup_bp,
    reportes_download_backup_bp,
    reportes_listar_backup_bp,
    reportes_upload_backup_bp,
    editar_bp,
    eliminar_bp,
]


def register_blueprints(app, blueprints, prefix):
    for blueprint in blueprints:
        app.register_blueprint(blueprint, url_prefix=f"{prefix}")


register_blueprints(app, blueprints, os.getenv("PATH_SUBDOMAIN"))


def create_log_file():
    file_path = os.getenv("PATH_LOG")
    print("creating log folder...")
    if not os.path.exists(file_path):
        with open(file_path, "w") as file:
            file.write("\n")


def create_ssh_log_file(folder_name):
    try:
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
            print(f"Folder '{folder_name}' created successfully.")
        else:
            print(f"Folder '{folder_name}' already exists.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    create_log_file()
    create_ssh_log_file(os.getenv("HOSTS_ARCHIVO"))
    app.run(debug=True)
