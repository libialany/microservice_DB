from flask import Blueprint, request
from routes.utils import eliminar
import os

eliminar_bp = Blueprint("eliminar", __name__)


@eliminar_bp.route("/eliminar", methods=["POST"])
def execute_create():
    datos = request.get_json()
    nombre = datos["nombre"]
    usuario = datos["usuario"]
    password = datos["password"]
    datos_coneccion = {
        "db_host": os.getenv("DB_HOST"),
        "db_port": os.getenv("DB_PORT"),
        "db_user": os.getenv("DB_USUARIO"),
        "db_password": os.getenv("DB_PASSWORD"),
        "db_nombre": os.getenv("DB_NOMBRE"),
    }
    return eliminar(
        nombre,
        usuario,
        password,
        datos_coneccion
    )
