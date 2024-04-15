from flask import Blueprint, request
from routes.utils import estado_database
import os
estado_database_bp = Blueprint('estado', __name__)
@estado_database_bp.route('/estado', methods=['GET'])
def verificar_estado(datos):
  datos = request.get_json()
  datos_coneccion = {
        "db_host": os.getenv("DB_HOST"),
        "db_port": os.getenv("DB_PORT"),
        "db_user": os.getenv("DB_USUARIO"),
        "db_password": os.getenv("DB_PASSWORD"),
        "db_nombre": os.getenv("DB_NOMBRE"),
    }
  if not estado_database(datos_coneccion):
    return {'error': f"error coneccion con la base de datos"}, 400
  return {'msg': 'coneccion exitosa'},200 
