from flask import Blueprint, request, jsonify
from app.config.db import db
from app.models.peso import Peso, PesoSchema
from datetime import datetime
import traceback

ruta_peso = Blueprint("route_peso", __name__)

peso_schema = PesoSchema()
pesos_schema = PesoSchema(many=True)

# 🔹 Agregar registro de peso
@ruta_peso.route("/addPeso", methods=["POST"])
def add_peso():
    try:
        data = request.json
        nuevo = Peso.from_dict(data)
        db.session.add(nuevo)
        db.session.commit()
        return jsonify({"message": "Peso registrado", "id": nuevo.id})
    except Exception as e:
        print("❌ Error al agregar peso:", e)
        print(traceback.format_exc())
        return jsonify({"error": "No se pudo guardar"}), 500

# 🔹 Obtener pesos por animal
@ruta_peso.route("/pesosByAnimal/<string:animal_id>", methods=["GET"])
def get_pesos_by_animal(animal_id):
    try:
        pesos = Peso.query.filter_by(animal_id=animal_id).all()
        return jsonify(pesos_schema.dump(pesos))
    except Exception as e:
        print("❌ Error al obtener pesos:", e)
        return jsonify({"error": "Error interno"}), 500

# 🔹 Actualizar peso
@ruta_peso.route("/updatePeso/<string:peso_id>", methods=["PUT"])
def update_peso(peso_id):
    try:
        data = request.json
        db.session.query(Peso).filter_by(id=peso_id).update(data)
        db.session.commit()
        return jsonify({"message": "Peso actualizado"})
    except Exception as e:
        print("❌ Error al actualizar peso:", e)
        return jsonify({"error": "No se pudo actualizar"}), 500

# 🔹 Eliminar peso
@ruta_peso.route("/deletePeso/<string:peso_id>", methods=["DELETE"])
def delete_peso(peso_id):
    try:
        db.session.query(Peso).filter_by(id=peso_id).delete()
        db.session.commit()
        return jsonify({"message": "Peso eliminado"})
    except Exception as e:
        print("❌ Error al eliminar peso:", e)
        return jsonify({"error": "Error interno"}), 500
