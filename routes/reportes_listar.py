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


s3 = boto3.resource(
    os.getenv("RESOURCE_TYPE"),
    endpoint_url=os.getenv("HOST_BUCKET"),
    aws_access_key_id=os.getenv("ACCESS_KEY"),
    aws_secret_access_key=os.getenv("SECRET_KEY"),
    aws_session_token=None,
    config=boto3.session.Config(signature_version=os.getenv("SIGNATURE_VERSION")),
    verify=False,
)




reportes_listar_backup_bp = Blueprint("reportes_listar", __name__)
@reportes_listar_backup_bp.route("/reportes-listar", methods=["GET"])
def reportes_listar_file():
    bucket = s3.Bucket(os.getenv("REPORTES_MINIO_BUCKET_NAME"))
    try:
        objects_list=[]
        objects = bucket.objects.all()
        for item in objects:
            objects_list.append(item.key)
        if(len(objects_list))<1:
            return jsonify({"message": "Empty bucket", "data": []})
        return jsonify({"mensaje":"exitosa operacion", "data":objects_list },200)
    except NoCredentialsError:
        return jsonify({"error": "MINIO credentials not available"}, 500)