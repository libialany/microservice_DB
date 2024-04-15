from dotenv import load_dotenv
load_dotenv()
import boto3
from botocore.client import Config
from botocore.exceptions import NoCredentialsError,ClientError
from flask import Blueprint, request, jsonify
from routes.utils import ejecutar
from routes.vars import Vars
import os
import logging
from datetime import datetime
from botocore.exceptions import ClientError
backup_bp = Blueprint('backup', __name__)
s3=boto3.resource(os.getenv("RESOURCE_TYPE"), 
    endpoint_url=os.getenv("HOST_BUCKET"),
    aws_access_key_id=os.getenv("ACCESS_KEY"),
    aws_secret_access_key=os.getenv("SECRET_KEY"),
    aws_session_token=None,
    config=boto3.session.Config(signature_version=os.getenv("SIGNATURE_VERSION")),
    verify=False)
def create_presigned_url(object_name, expiration=3600):
    s3 = boto3.resource(
        os.getenv("RESOURCE_TYPE"),
        endpoint_url=os.getenv("HOST_BUCKET"),
        aws_access_key_id=os.getenv("ACCESS_KEY"),
        aws_secret_access_key=os.getenv("SECRET_KEY"),
        aws_session_token=None,
        config=boto3.session.Config(signature_version=os.getenv("SIGNATURE_VERSION")),
        verify=False,
    )
    bucket_name = os.getenv("DB_MINIO_BUCKET_NAME")
    try:
        response = s3.meta.client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket_name, "Key": object_name},
            ExpiresIn=expiration,
        )
    except ClientError as e:
        logging.error(e)
        return None
    return response
@backup_bp.route('/backup', methods=['POST'])
def execute_backup():
  datos = request.get_json()
  actual_datetime = datetime.now()
  formato_datetime = actual_datetime.strftime('%Y-%m-%d')
  nombre_backup=f'{datos["db_name"]}-bck-{formato_datetime}'
  agregarVars(datos,nombre_backup)
  if not ejecutar('backup', Vars.BACKUPS.value):
    return (jsonify({"error": f"No se ejecuto el playbook, error en las credenciales"}), 404)
  return {'mensaje': f'creacion backup exitosa', 'data': nombre_backup },200 
def agregarVars(datos, nombre_backup):
  data = '''archivo_salida: {archivo_salida}
db_name: {db_name}
db_username: {db_username}
db_password: {db_password}
db_host: {db_host}
db_port: {db_port}
use_docker: {use_docker}
nombre_contenedor: {nombre_contenedor}
ruta_salida: {ruta_salida}
url_db: {url_db}
'''
  data = data.format(
    archivo_salida=nombre_backup,
    db_name=datos['db_name'],
    db_host=datos['db_host'],
    db_port=datos['db_port'],
    db_username=datos['db_username'],
    db_password=datos['db_password'],
    use_docker=False if datos['use_docker']=="" else True,
    nombre_contenedor=os.getenv('NOMBRE_CONTAINER'),
    ruta_salida='',
    url_db=os.getenv('URL_MICROSERVICIO_DB')
  )
  with open(Vars.BACKUPS.value, 'w') as file:
    file.write(data)