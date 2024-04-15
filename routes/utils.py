from dotenv import load_dotenv

load_dotenv()
import os
import re
import subprocess
from flask import jsonify
import ansible_runner
from routes.vars import Errores, Vars, ArchivosCluster, LogsVars
import psycopg2

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USUARIO")
DB_PASS = os.getenv("DB_PASSWORD")
DB_NOMBRE = os.getenv("DB_NOMBRE")
playbook_path = "./playbook.yml"


def estado_database(datos):
    db_nombre = datos["db_nombre"]
    db_user = datos["db_user"]
    db_pass = datos["db_password"]
    db_host = datos["db_host"]
    db_port = datos["db_port"]
    conn = psycopg2.connect(
        database=db_nombre, user=db_user, password=db_pass, host=db_host, port=db_port
    )
    conn.autocommit = True
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT 1;")
    except psycopg2.Error as e:
        print(e)
        return False
    return True


def ejecutar(tag, var=None):
    argumentos = {
        "private_data_dir": ".",
        "playbook": playbook_path,
        "tags": tag,
        "rotate_artifacts": 1,
        "suppress_env_files": True,
        "inventory": "%s/inventory.ini" % os.getenv("PATH_FOLDER_NFS"),
    }
    if var:
        argumentos["extravars"] = var
    conexiones()
    r = ansible_runner.run(**argumentos)
    logsErrores()
    for event in r.events:
        if event["event"] == Errores.UNREACHABLE.value:
            return False
        if (
            event["event"] == Errores.FAILED.value
            or event["event"] == Errores.ITEMFAILED.value
        ):
            return False
    if r.status == "successful":
        return True
    return False


def logsErrores():
    lineasErrores = []
    with open(LogsVars.FILE.value, "r") as file:
        lineas = file.readlines()
        copiar = False
        for i in range(len(lineas)):
            linea = lineas[i]
            if ("fatal" in linea) or ("failed" in linea and "failed=" not in linea):
                lineasErrores.append(lineas[i - 1])
                lineasErrores.append(linea)
                copiar = True
            elif copiar and "...ignoring" in linea:
                lineasErrores.append(linea)
                copiar = False
        with open(LogsVars.FILE_ERROR.value, "w") as file:
            for linea in lineasErrores:
                file.write(linea)


def conexiones():
    with open(ArchivosCluster.INVENTORY.value, "r") as file:
        config_data = file.read()
    host_pattern = r"ansible_host=(\S+)"
    user_pattern = r"ansible_user=(\S+)"
    pass_pattern = r"ansible_become_pass=(\S+)"
    hosts = re.findall(host_pattern, config_data)
    users = re.findall(user_pattern, config_data)
    passwords = re.findall(pass_pattern, config_data)
    if len(hosts) == len(users) == len(passwords):
        for host, user, passw in zip(hosts, users, passwords):
            print(user, passw, host)
            copiarPublicKey(user, passw, host)
    else:
        return (jsonify({"error": f"No se encontraron valores suficientes."}), 404)


def copiarPublicKey(user, passw, ip, folder="/home/adas/.ssh"):
    if not os.path.exists(folder):
        os.makedirs(folder)
        print("Added folder .ssh ....")
    user_home = os.path.expanduser("~")
    path_key = os.path.join(user_home, ".ssh/id_rsa.pub")
    path_ssh = os.path.join(user_home, ".ssh/known_hosts")
    keyScan = ["ssh-keyscan", ip]
    if os.path.exists(path_ssh):
        with open(path_ssh, "r") as file:
            lineas = file.read()
            if ip in lineas:
                return True
    with open(path_ssh, "a") as file:
        subprocess.run(keyScan, stdout=file, text=True)
    copyId = ["sshpass", "-p", passw, "ssh-copy-id", "-i", path_key, f"{user}@{ip}"]
    subprocess.run(copyId)


def crear_database(nombre, usuario, password, esquemas, datos_coneccion):
    db_nombre = datos_coneccion["db_nombre"]
    db_user = datos_coneccion["db_user"]
    db_pass = datos_coneccion["db_password"]
    db_host = datos_coneccion["db_host"]
    db_port = datos_coneccion["db_port"]
    conn = psycopg2.connect(
        database=db_nombre, user=db_user, password=db_pass, host=db_host, port=db_port
    )
    conn.autocommit = True
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                f"SELECT datname FROM pg_database WHERE datname = '{nombre}';"
            )
            if len(cursor.fetchall()) != 0:
                return {"error": f"error nombre de base de datos existente"}, 400
            if existe_usuario(usuario, datos_coneccion):
                return {"error": f"error usuario de base de datos existente"}, 400
            cursor.execute(f"CREATE DATABASE {nombre};")
            crear_user(usuario, password, datos_coneccion)
            asignar_user(nombre, usuario, datos_coneccion)
            datos = {
                "db_nombre": nombre,
                "db_user": usuario,
                "db_password": password,
                "db_host": datos_coneccion["db_host"],
                "db_port":   nn ["db_port"],
                "esquemas": esquemas,
            }
            if not estado_database(datos):
                eliminar(nombre, usuario, password, datos_coneccion)
                return {"error": f"error en la creacion de esquemas"}, 400
            crear_esquemas(nombre, usuario, password, esquemas, datos_coneccion)
            return {"mensaje": f"creacion base de datos exitosa", "data": datos}, 201
    except psycopg2.Error as e:
        print(e)
        return {"error": f"error creacion base de datos"}, 400
    finally:
        if conn is not None:
            conn.close()


def eliminar(nombre, usuario, password, datos_coneccion):
    db_nombre = datos_coneccion["db_nombre"]
    db_user = datos_coneccion["db_user"]
    db_pass = datos_coneccion["db_password"]
    db_host = datos_coneccion["db_host"]
    db_port = datos_coneccion["db_port"]
    conn = psycopg2.connect(
        database=db_nombre, user=db_user, password=db_pass, host=db_host, port=db_port
    )
    conn.autocommit = True
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                f"SELECT datname FROM pg_database WHERE datname = '{nombre}';"
            )
            if len(cursor.fetchall()) == 0:
                return {"error": f"error nombre de base de datos no existente"}, 400
            if not existe_usuario(usuario, datos_coneccion):
                return {"error": f"error usuario de base de datos no existente"}, 400
            cursor.execute(f"DROP DATABASE {nombre};")
            cursor.execute(f"DROP USER {usuario};")
            datos = {
                "nombre": nombre,
                "usuario": usuario,
                "password": password,
            }
            return {"mensaje": f"eliminacion base de datos exitosa", "data": datos}, 201
    except psycopg2.Error as e:
        print(e)
        return {"error": f"error creacion base de datos"}, 400
    finally:
        if conn is not None:
            conn.close()


def editar(nombre, usuario, password, esquemas, datos_coneccion):
    db_nombre = datos_coneccion["db_nombre"]
    db_user = datos_coneccion["db_user"]
    db_pass = datos_coneccion["db_password"]
    db_host = datos_coneccion["db_host"]
    db_port = datos_coneccion["db_port"]
    conn = psycopg2.connect(
        database=db_nombre, user=db_user, password=db_pass, host=db_host, port=db_port
    )
    conn.autocommit = True
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                f"SELECT datname FROM pg_database WHERE datname = '{nombre}';"
            )
            if len(cursor.fetchall()) == 0:
                return {"error": f"error nombre de base de datos no existe"}, 400
            if not existe_usuario(usuario, datos_coneccion):
                return {"error": f"error usuario de base de datos no existe"}, 400
            crear_esquemas(nombre, usuario, password, esquemas, datos_coneccion)
            datos = {
                "nombre": nombre,
                "usuario": usuario,
                "password": password,
                "esquemas": esquemas,
            }
            return {"mensaje": f"creacion base de datos exitosa", "data": datos}, 201
    except psycopg2.Error as e:
        print(e)
        return {"error": f"error creacion base de datos"}, 400
    finally:
        if conn is not None:
            conn.close()


def existe_usuario(usuario, datos_coneccion):
    conn = psycopg2.connect(
        database=datos_coneccion["db_nombre"],
        user=datos_coneccion["db_user"],
        password=datos_coneccion["db_password"],
        host=datos_coneccion["db_host"],
        port=datos_coneccion["db_port"],
    )
    conn.autocommit = True
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                f"select * from pg_roles where pg_roles.rolname='{usuario}';"
            )
            if len(cursor.fetchall()) == 0:
                return False
            return True
    except psycopg2.Error as e:
        print(e)
        return False
    finally:
        if conn is not None:
            conn.close()


def crear_user(usuario, password, datos_coneccion):
    conn = psycopg2.connect(
        database=datos_coneccion["db_nombre"],
        user=datos_coneccion["db_user"],
        password=datos_coneccion["db_password"],
        host=datos_coneccion["db_host"],
        port=datos_coneccion["db_port"],
    )
    conn.autocommit = True
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"CREATE USER {usuario} WITH PASSWORD '{password}';")
            cursor.execute(f"ALTER ROLE {usuario} SUPERUSER CREATEDB;")
    except psycopg2.Error as e:
        print(e)
    finally:
        if conn is not None:
            conn.close()


def asignar_user(nombre, usuario, datos_coneccion):
    conn = psycopg2.connect(
        database=datos_coneccion["db_nombre"],
        user=datos_coneccion["db_user"],
        password=datos_coneccion["db_password"],
        host=datos_coneccion["db_host"],
        port=datos_coneccion["db_port"],
    )
    conn.autocommit = True
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"ALTER DATABASE {nombre} OWNER TO {usuario};")
            cursor.execute(f"GRANT ALL PRIVILEGES ON DATABASE {nombre} TO {usuario};")
    except psycopg2.Error as e:
        print(e)
    finally:
        if conn is not None:
            conn.close()


def crear_esquemas(nombre, usuario, password, esquemas, datos_coneccion):
    conn = psycopg2.connect(
        database=nombre,
        user=usuario,
        password=password,
        host=datos_coneccion["db_host"],
        port=datos_coneccion["db_port"],
    )
    conn.autocommit = True
    try:
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
