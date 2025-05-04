from flask import Blueprint, request, jsonify
from config.db import db
from models.tratamiento import Tratamiento, TratamientoSchema
from datetime import datetime
import traceback

ruta_tratamiento = Blueprint("route_tratamiento", __name__)

schema = TratamientoSchema()
schema_many = TratamientoSchema(many=True)

# 🔹 Crear tratamiento
@ruta_tratamiento.route("/addTratamiento", methods=["POST"])
def add_tratamiento():
    try:
        data = request.json
        nuevo = Tratamiento.from_dict(data)
        db.session.add(nuevo)
        db.session.commit()
        return jsonify({"message": "Tratamiento registrado", "id": nuevo.id})
    except Exception as e:
        print("❌ Error al guardar tratamiento:", e)
        print(traceback.format_exc())
        return jsonify({"error": "Error al guardar"}), 500

# 🔹 Obtener tratamientos por animal
@ruta_tratamiento.route("/tratamientosByAnimal/<string:animal_id>", methods=["GET"])
def get_tratamientos_by_animal(animal_id):
    try:
        tratamientos = Tratamiento.query.filter_by(animal_id=animal_id).all()
        return jsonify(schema_many.dump(tratamientos))
    except Exception as e:
        return jsonify({"error": "Error interno"}), 500

# 🔹 Actualizar tratamiento
@ruta_tratamiento.route("/updateTratamiento/<string:tratamiento_id>", methods=["PUT"])
def update_tratamiento(tratamiento_id):
    try:
        data = request.json
        db.session.query(Tratamiento).filter_by(id=tratamiento_id).update(data)
        db.session.commit()
        return jsonify({"message": "Tratamiento actualizado"})
    except Exception as e:
        return jsonify({"error": "Error al actualizar"}), 500

# 🔹 Eliminar tratamiento
@ruta_tratamiento.route("/deleteTratamiento/<string:tratamiento_id>", methods=["DELETE"])
def delete_tratamiento(tratamiento_id):
    try:
        db.session.query(Tratamiento).filter_by(id=tratamiento_id).delete()
        db.session.commit()
        return jsonify({"message": "Tratamiento eliminado"})
    except Exception as e:
        return jsonify({"error": "Error al eliminar"}), 500
