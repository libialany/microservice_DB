from flask import jsonify
from dotenv import load_dotenv
import os
import psycopg2
import subprocess
pg_dump_command = [
   'pg_dump',
   '-h', 'localhost',
   '-p', '5432',
   '-U', 'e',
   '-d', 'e',
   '--file', 'e_file.sql',
]
load_dotenv()
def crear_esquemas(nombre,usuario,password,esquemas):
   db_database=nombre
   db_user=usuario
   db_password=password
   db_host=os.getenv('DB_HOST')
   db_port=os.getenv('DB_PORT')
   try:
      conn = psycopg2.connect(database=db_database,user=db_user,password=db_password,host=db_host,port=db_port)
      conn.autocommit = True
      with conn.cursor() as cursor:
         for schema in esquemas:
            cursor.execute(f"CREATE SCHEMA {schema};")
            cursor.execute(f"ALTER SCHEMA {schema} OWNER TO {usuario};")
   except psycopg2.Error as e:
      return False
   finally:
      if conn is not None:
         conn.close()
   return True
def crear_database(nombre,usuario,password,esquemas):
   db_database=os.getenv('DB_NOMBRE')
   db_user=os.getenv('DB_USUARIO')
   db_password=os.getenv('DB_PASSWORD')
   db_host=os.getenv('DB_HOST')
   db_port=os.getenv('DB_PORT')
   try:
      conn = psycopg2.connect(database=db_database,user=db_user,password=db_password,host=db_host,port=db_port)
      conn.autocommit = True
      with conn.cursor() as cursor:
         cursor.execute(f"CREATE DATABASE {nombre};")
         print("Database created successfully")
         cursor.execute(f"CREATE USER {usuario} WITH PASSWORD '{password}';")
         print("User created successfully")
         cursor.execute(f"ALTER ROLE {usuario} SUPERUSER CREATEDB;")
         print("User super user granted successfully")         
         cursor.execute(f"ALTER DATABASE {nombre} OWNER TO {usuario};")
         print('Alterado')
         cursor.execute(f"GRANT ALL PRIVILEGES ON DATABASE {nombre} TO {usuario};")
         print("Privileges granted to the user")
   except psycopg2.Error as e:
      print(e)
      return False
   finally:
      if conn is not None:
         conn.close()
   return True