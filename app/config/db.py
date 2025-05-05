import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate, upgrade

# Crear instancia de Flask
app = Flask(__name__)

# Obtener y transformar la URL de la base de datos
raw_url = os.getenv('DATABASE_URL', '')
if not raw_url:
    raise RuntimeError("DATABASE_URL no está definida en el entorno. Verifica Railway.")

# Asegurar compatibilidad con SQLAlchemy + PyMySQL
db_url = raw_url.replace("mysql://", "mysql+pymysql://", 1)

# Configuración de SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Clave secreta definida por el usuario en Railway
app.secret_key = os.getenv('SECRET_KEY', 'valor_predeterminado_inseguro')

# Inicializar extensiones
db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)
