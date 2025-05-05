import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate

# Crear instancia de Flask
app = Flask(__name__)

# Obtener URL completa desde Railway y ajustarla para SQLAlchemy
raw_url = os.getenv('DATABASE_URL', '')
db_url = raw_url.replace('mysql://', 'mysql+pymysql://', 1)

# Configuración SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Clave secreta personalizada (la defines tú)
app.secret_key = os.getenv('SECRET_KEY')

# Inicializar extensiones
db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)
