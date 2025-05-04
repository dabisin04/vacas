from flask import Blueprint, request, jsonify
from config.db import db
from models.produccion_leche import ProduccionLeche, ProduccionLecheSchema
from datetime import datetime
import traceback

ruta_produccion = Blueprint("route_produccion_leche", __name__)

schema = ProduccionLecheSchema()
schema_many = ProduccionLecheSchema(many=True)

# 🔹 Crear producción de leche
@ruta_produccion.route("/addProduccionLeche", methods=["POST"])
def add_produccion_leche():
    try:
        data = request.json
        nueva = ProduccionLeche.from_dict(data)
        db.session.add(nueva)
        db.session.commit()
        return jsonify({"message": "Producción registrada", "id": nueva.id})
    except Exception as e:
        print("❌ Error al guardar producción:", e)
        print(traceback.format_exc())
        return jsonify({"error": "Error al guardar"}), 500

# 🔹 Obtener producción por animal
@ruta_produccion.route("/produccionByAnimal/<string:animal_id>", methods=["GET"])
def get_by_animal(animal_id):
    try:
        registros = ProduccionLeche.query.filter_by(animal_id=animal_id).all()
        return jsonify(schema_many.dump(registros))
    except Exception as e:
        return jsonify({"error": "Error interno"}), 500

# 🔹 Obtener producción por finca
@ruta_produccion.route("/produccionByFarm/<string:farm_id>", methods=["GET"])
def get_by_farm(farm_id):
    try:
        registros = ProduccionLeche.query.filter_by(farm_id=farm_id).all()
        return jsonify(schema_many.dump(registros))
    except Exception as e:
        return jsonify({"error": "Error interno"}), 500

# 🔹 Obtener toda la producción
@ruta_produccion.route("/produccionTotal", methods=["GET"])
def get_all_produccion():
    try:
        registros = ProduccionLeche.query.all()
        return jsonify(schema_many.dump(registros))
    except Exception as e:
        return jsonify({"error": "Error interno"}), 500

# 🔹 Actualizar producción
@ruta_produccion.route("/updateProduccion/<string:produccion_id>", methods=["PUT"])
def update_produccion(produccion_id):
    try:
        data = request.json
        db.session.query(ProduccionLeche).filter_by(id=produccion_id).update(data)
        db.session.commit()
        return jsonify({"message": "Producción actualizada"})
    except Exception as e:
        return jsonify({"error": "Error al actualizar"}), 500

# 🔹 Eliminar producción
@ruta_produccion.route("/deleteProduccion/<string:produccion_id>", methods=["DELETE"])
def delete_produccion(produccion_id):
    try:
        db.session.query(ProduccionLeche).filter_by(id=produccion_id).delete()
        db.session.commit()
        return jsonify({"message": "Producción eliminada"})
    except Exception as e:
        return jsonify({"error": "Error al eliminar"}), 500
