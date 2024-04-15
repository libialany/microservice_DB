from dotenv import load_dotenv

load_dotenv()
import boto3
from botocore.client import Config
from botocore.exceptions import NoCredentialsError, ClientError
from flask import Blueprint, request, jsonify
from routes.utils import ejecutar
from routes.vars import Vars
import os
import logging
from datetime import datetime
from botocore.exceptions import ClientError

reportes_download_backup_bp = Blueprint("reportes_download", __name__)

s3 = boto3.resource(
    os.getenv("RESOURCE_TYPE"),
    endpoint_url=os.getenv("HOST_BUCKET"),
    aws_access_key_id=os.getenv("ACCESS_KEY"),
    aws_secret_access_key=os.getenv("SECRET_KEY"),
    aws_session_token=None,
    config=boto3.session.Config(signature_version=os.getenv("SIGNATURE_VERSION")),
    verify=False,
)

@reportes_download_backup_bp.route("/reportes-download", methods=["POST"])
def download_backup(expiration=3600):
    datos=request.get_json()
    nombre_backup=datos['nombre_backup']
    if not nombre_backup:
        return jsonify({'error': f"error no se tiene el nombre del backup"}, 400)
    bucket_name=os.getenv("REPORTES_MINIO_BUCKET_NAME")
    bucket = s3.Bucket(bucket_name)
    try:
        bucket.download_file(nombre_backup, f"{os.getenv('REPORTES_PATH')}/{nombre_backup}")
    except ClientError as e:
        logging.error(e)
        return  jsonify({'error': f"error no se recupero el reporte"}, 400)
    return jsonify({'mensaje': 'operacion exitosa', "data":f"{os.getenv('REPORTES_PATH')}/{nombre_backup}"},200) 
