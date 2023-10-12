import os
from dotenv import load_dotenv
from flask import Flask
from flasgger import Swagger
from routes.vars import SwaggerVars
from routes.create_record import create_database_bp
app = Flask(__name__)

load_dotenv()

swagger = Swagger(
  app, 
  template_file=SwaggerVars.FILE.value, 
  config={
    "url_prefix": f"{os.getenv('PATH_SUBDOMAIN')}",
    "specs_route": SwaggerVars.ROUTE.value,
    "basePath": f"{os.getenv('PATH_SUBDOMAIN')}",
  },
  merge=True
)

blueprints = [
  create_database_bp
]

def register_blueprints(app, blueprints, prefix):
  for blueprint in blueprints:
    app.register_blueprint(blueprint, url_prefix=f"{prefix}")

register_blueprints(app, blueprints, os.getenv('PATH_SUBDOMAIN'))

if __name__ == '__main__':
    app.run(debug=True)
