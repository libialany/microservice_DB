# **Acerca del Repositorio**

El microservicio que crea la base de datos el esquema de base de datos.

## **Requisitos**

Para utilizarlo debes asegurarte de tener los siguientes requisitos:

- Conocer bases de Ansible.
- Una base de datos local de Postgresql.
- Python con psycopg2-binary=2.9.9 instalado.

## **Configuración**

Sigue estos pasos para configurar Nsupdate:

1. Copia las variables de entorno

   ```shell
   cp .env.sample .env
   cp inventory.ini.example inventory.ini
   ```
2. Configura los datos del microservicio

   ```shell
   PORT=
   PATH_SUBDOMAIN=
   DB_PORT=
   DB_HOST=
   DB_PASSWORD=
   DB_USUARIO=
   DB_NOMBRE=
   USER_GENERAR=
   PASS_GENERAR=
   HOSTS_ARCHIVO=
   ```

   Ejemplo:


   ```bash
   PORT=5000
   PATH_SUBDOMAIN=/api
   DB_PORT=5432
   DB_HOST='10.10.10.1'
   DB_PASSWORD=postgres
   DB_USUARIO=postgres
   DB_NOMBRE=postgres
   USER_GENERAR=usr
   PASS_GENERAR=pas
   HOSTS_ARCHIVO=/ssh/keys/id_rsa
   ```

3. Creación de un entorno virtual

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

### Instalación 

   ```shell
   source venv/bin/activate
   python3 app.py
   ```
### Instalación usando docker 

   ```bash
   docker build -t img-ms-db:<VERSION> .
   docker run -p 5000:5000 --name ms-db img-ms-db:<VERSION>
   ```
Recuerda reemplazar _<VERSION>_ con la versión actual.

### Uso

**Gunicorn: El Motor de Ejecución de Tu Aplicación**

Gunicorn, abreviatura de "Green Unicorn," es la pieza clave que hace que nuestra aplicación cobre vida. Funciona como el motor de ejecución, tomando las riendas de nuestra aplicación web y permitiéndole funcionar de manera eficiente.

Para poner en marcha nuestra aplicación, simplemente ejecutamos el siguiente comando:

```bash
gunicorn --config gunicorn.config.py app:app
```

Este comando inicia la aplicación en el puerto y la ubicación definida en las variables de entorno, lo que significa que tu aplicación estará en funcionamiento y lista para atender solicitudes en un instante.

**Swagger**

Una vez que la aplicación está en ejecución, puedes explorar la documentación de tu API utilizando Swagger. Esto te proporciona una visión detallada de los puntos finales y las operaciones disponibles en tu API.

Simplemente visita la siguiente URL en tu navegador:

```bash
localhost:5000/api/doc
```