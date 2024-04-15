from flask import Blueprint, request
from routes.utils import editar
import os

editar_bp = Blueprint("editar", __name__)


@editar_bp.route("/editar", methods=["POST"])
def execute_create():
    datos = request.get_json()
    nombre = datos["nombre"]
    usuario = datos["usuario"]
    password = datos["password"]
    esquemas = datos["esquemas"]
    datos_coneccion = {
        "db_host": os.getenv("DB_HOST"),
        "db_port": os.getenv("DB_PORT"),
        "db_user": os.getenv("DB_USUARIO"),
        "db_password": os.getenv("DB_PASSWORD"),
        "db_nombre": os.getenv("DB_NOMBRE"),
    }
    return editar(
        nombre,
        usuario,
        password,
        esquemas,
        datos_coneccion
    )
