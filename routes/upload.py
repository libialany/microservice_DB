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

upload_backup_bp = Blueprint("upload", __name__)

s3 = boto3.resource(
    os.getenv("RESOURCE_TYPE"),
    endpoint_url=os.getenv("HOST_BUCKET"),
    aws_access_key_id=os.getenv("ACCESS_KEY"),
    aws_secret_access_key=os.getenv("SECRET_KEY"),
    aws_session_token=None,
    config=boto3.session.Config(signature_version=os.getenv("SIGNATURE_VERSION")),
    verify=False,
)

@upload_backup_bp.route("/upload-backup", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part"})
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"})
    try:
        bucket = s3.Bucket(os.getenv("DB_MINIO_BUCKET_NAME"))
        bucket.upload_fileobj(file, file.filename)
        return {'msg': f'creacion backup exitosa, la url es {file.filename}'},200 
    except NoCredentialsError:
        return jsonify({"message": "MINIO credentials not available"})
