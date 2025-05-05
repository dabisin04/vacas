from flask import Flask
from app.config.db import app as flask_app, db  # ⬅️ Renombramos el objeto importado

# 📦 Importar Blueprints necesarios
from app.api.user_api import ruta_usuario
from app.api.animal_api import ruta_animal
from app.api.farm_api import ruta_farm
from app.api.chequeo_salud_api import ruta_chequeo
from app.api.evento_reproductivo_api import ruta_evento
from app.api.peso_api import ruta_peso
from app.api.produccion_api import ruta_produccion
from app.api.tratamiento_api import ruta_tratamiento
from app.api.usuario_finca_api import ruta_usuario_finca
from app.api.vacunas_api import ruta_vacuna

# 👇 Asignamos el nombre correcto que gunicorn busca
app = flask_app

# 🧩 Registrar Blueprints con prefijo /api
app.register_blueprint(ruta_usuario, url_prefix="/api")
app.register_blueprint(ruta_animal, url_prefix="/api")
app.register_blueprint(ruta_farm, url_prefix="/api")
app.register_blueprint(ruta_chequeo, url_prefix="/api")
app.register_blueprint(ruta_evento, url_prefix="/api")
app.register_blueprint(ruta_peso, url_prefix="/api")
app.register_blueprint(ruta_produccion, url_prefix="/api")
app.register_blueprint(ruta_tratamiento, url_prefix="/api")
app.register_blueprint(ruta_usuario_finca, url_prefix="/api")
app.register_blueprint(ruta_vacuna, url_prefix="/api")

# 🏠 Ruta principal
@app.route("/")
def index():
    return "✅ API de gestión ganadera funcionando correctamente"
