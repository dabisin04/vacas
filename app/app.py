from flask import Flask
from config.db import app, db  # db importado explícitamente para create_all

# 📦 Importar Blueprints necesarios (sin book-related)
from api.user_api import ruta_usuario
from api.animal_api import ruta_animal
from api.farm_api import ruta_farm
from api.chequeo_salud_api import ruta_chequeo
from api.evento_reproductivo_api import ruta_evento
from api.peso_api import ruta_peso
from api.produccion_api import ruta_produccion
from api.tratamiento_api import ruta_tratamiento
from api.usuario_finca_api import ruta_usuario_finca
from api.vacunas_api import ruta_vacuna

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

# 🚀 Ejecutar servidor
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Crear tablas si no existen
    app.run(debug=True, port=5050, host="0.0.0.0")

