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

download_backup_bp = Blueprint("download", __name__)

s3 = boto3.resource(
    os.getenv("RESOURCE_TYPE"),
    endpoint_url=os.getenv("HOST_BUCKET"),
    aws_access_key_id=os.getenv("ACCESS_KEY"),
    aws_secret_access_key=os.getenv("SECRET_KEY"),
    aws_session_token=None,
    config=boto3.session.Config(signature_version=os.getenv("SIGNATURE_VERSION")),
    verify=False,
)

@download_backup_bp.route("/download-backup", methods=["POST"])
def create_presigned_url(expiration=3600):
    datos=request.get_json()
    nombre_backup=datos['nombre_backup']
    if not nombre_backup:
        return {'error': f"error no se tiene el nombre del backup"}, 400
    bucket_name=os.getenv("DB_MINIO_BUCKET_NAME")
    try:
        response = s3.meta.client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket_name, "Key": nombre_backup},
            ExpiresIn=expiration,
        )
    except ClientError as e:
        logging.error(e)
        return None
    return response
