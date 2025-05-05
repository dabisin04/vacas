from flask import Blueprint, request, jsonify
from app.config.db import db
from app.models.vacuna import Vacuna, VacunaSchema
import traceback

ruta_vacuna = Blueprint("route_vacuna", __name__)

vacuna_schema = VacunaSchema()
vacunas_schema = VacunaSchema(many=True)

# 🔹 Obtener todas las vacunas de un animal
@ruta_vacuna.route("/vacunas/<string:animal_id>", methods=["GET"])
def get_vacunas_by_animal(animal_id):
    try:
        vacunas = Vacuna.query.filter_by(animal_id=animal_id).all()
        return jsonify(vacunas_schema.dump(vacunas))
    except Exception as e:
        print("❌ Error en get_vacunas_by_animal:", e)
        print(traceback.format_exc())
        return jsonify({"error": "No se pudieron obtener las vacunas"}), 500

# 🔹 Agregar vacuna
@ruta_vacuna.route("/addVacuna", methods=["POST"])
def add_vacuna():
    try:
        data = request.json
        nueva = Vacuna.from_dict(data)
        db.session.add(nueva)
        db.session.commit()
        return jsonify({"message": "Vacuna agregada correctamente", "id": nueva.id})
    except Exception as e:
        print("❌ Error en add_vacuna:", e)
        print(traceback.format_exc())
        return jsonify({"error": "Error al guardar la vacuna"}), 500

# 🔹 Actualizar vacuna
@ruta_vacuna.route("/updateVacuna/<string:vacuna_id>", methods=["PUT"])
def update_vacuna(vacuna_id):
    try:
        data = request.json
        db.session.query(Vacuna).filter_by(id=vacuna_id).update(data)
        db.session.commit()
        return jsonify({"message": "Vacuna actualizada"})
    except Exception as e:
        print("❌ Error en update_vacuna:", e)
        print(traceback.format_exc())
        return jsonify({"error": "No se pudo actualizar"}), 500

# 🔹 Eliminar vacuna
@ruta_vacuna.route("/deleteVacuna/<string:vacuna_id>", methods=["DELETE"])
def delete_vacuna(vacuna_id):
    vacuna = Vacuna.query.get(vacuna_id)
    if not vacuna:
        return jsonify({"error": "Vacuna no encontrada"}), 404
    db.session.delete(vacuna)
    db.session.commit()
    return jsonify({"message": "Vacuna eliminada"})
