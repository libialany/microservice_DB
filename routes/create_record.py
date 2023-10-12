from flask import Blueprint, request
from routes.utils import crear_database,crear_esquemas


create_database_bp = Blueprint('crear_database', __name__)

@create_database_bp.route('/crear_database', methods=['POST'])
def execute_create():
  datos=request.get_json()
  nombre=datos['nombre']
  usuario=datos['usuario']
  password=datos['password']
  esquemas=datos['esquemas']
  if not crear_database(nombre,usuario,password,esquemas):
    return {'error': f"error creacion base de datos"}, 400
  return {'msg': 'creacion exitosa'},200 
