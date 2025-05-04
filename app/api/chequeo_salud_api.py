from flask import Blueprint, request, jsonify
from config.db import db
from models.chequeos_salud import ChequeoSalud, ChequeoSaludSchema
from datetime import datetime
import traceback

ruta_chequeo = Blueprint("route_chequeo_salud", __name__)

chequeo_schema = ChequeoSaludSchema()
chequeos_schema = ChequeoSaludSchema(many=True)

@ruta_chequeo.route("/chequeos/<string:animal_id>", methods=["GET"])
def get_chequeos_by_animal(animal_id):
    try:
        chequeos = ChequeoSalud.query.filter_by(animal_id=animal_id).all()
        return jsonify(chequeos_schema.dump(chequeos))
    except Exception as e:
        print(f"❌ Error al obtener chequeos: {e}")
        print(traceback.format_exc())
        return jsonify({"error": "Error interno"}), 500

@ruta_chequeo.route("/addChequeo", methods=["POST"])
def add_chequeo():
    try:
        data = request.json
        nuevo = ChequeoSalud.from_dict(data)
        db.session.add(nuevo)
        db.session.commit()
        return jsonify({"message": "Chequeo guardado", "id": nuevo.id})
    except Exception as e:
        print(f"❌ Error al guardar chequeo: {e}")
        print(traceback.format_exc())
        return jsonify({"error": "No se pudo guardar"}), 500

@ruta_chequeo.route("/updateChequeo/<string:chequeo_id>", methods=["PUT"])
def update_chequeo(chequeo_id):
    try:
        data = request.json
        db.session.query(ChequeoSalud).filter_by(id=chequeo_id).update(data)
        db.session.commit()
        return jsonify({"message": "Chequeo actualizado"})
    except Exception as e:
        print(f"❌ Error al actualizar chequeo: {e}")
        print(traceback.format_exc())
        return jsonify({"error": "No se pudo actualizar"}), 500

@ruta_chequeo.route("/deleteChequeo/<string:chequeo_id>", methods=["DELETE"])
def delete_chequeo(chequeo_id):
    try:
        chequeo = ChequeoSalud.query.get(chequeo_id)
        if not chequeo:
            return jsonify({"error": "No encontrado"}), 404
        db.session.delete(chequeo)
        db.session.commit()
        return jsonify({"message": "Chequeo eliminado"})
    except Exception as e:
        print(f"❌ Error al eliminar chequeo: {e}")
        print(traceback.format_exc())
        return jsonify({"error": "Error interno"}), 500
