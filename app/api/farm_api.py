from flask import Blueprint, request, jsonify
from app.config.db import db
from app.models.farm import Farm, FarmSchema
from datetime import datetime
import traceback

ruta_farm = Blueprint("route_farm", __name__)

farm_schema = FarmSchema()
farms_schema = FarmSchema(many=True)

# 🔹 Crear finca
@ruta_farm.route("/addFarm", methods=["POST"])
def add_farm():
    try:
        data = request.json
        nueva = Farm.from_dict(data)
        db.session.add(nueva)
        db.session.commit()
        return jsonify({"message": "Finca creada", "id": nueva.id})
    except Exception as e:
        print(f"❌ Error al crear finca: {e}")
        print(traceback.format_exc())
        return jsonify({"error": "No se pudo guardar"}), 500

# 🔹 Obtener finca por ID
@ruta_farm.route("/farm/<string:farm_id>", methods=["GET"])
def get_farm_by_id(farm_id):
    try:
        farm = Farm.query.get(farm_id)
        return jsonify(farm_schema.dump(farm)) if farm else jsonify({"message": "No encontrada"}), 404
    except Exception as e:
        print(f"❌ Error al obtener finca: {e}")
        return jsonify({"error": "Error interno"}), 500

# 🔹 Obtener fincas por usuario
@ruta_farm.route("/farmsByUser/<string:user_id>", methods=["GET"])
def get_farms_by_user(user_id):
    try:
        result = db.session.execute(
            '''
            SELECT f.* FROM farms f
            JOIN usuario_finca uf ON f.id = uf.farm_id
            WHERE uf.user_id = :user_id
            ''',
            {"user_id": user_id}
        )
        farms = [dict(r._mapping) for r in result]
        return jsonify(farms)
    except Exception as e:
        print(f"❌ Error al obtener fincas por usuario: {e}")
        return jsonify({"error": "Error interno"}), 500

# 🔹 Actualizar finca
@ruta_farm.route("/updateFarm/<string:farm_id>", methods=["PUT"])
def update_farm(farm_id):
    try:
        data = request.json
        db.session.query(Farm).filter_by(id=farm_id).update(data)
        db.session.commit()
        return jsonify({"message": "Finca actualizada"})
    except Exception as e:
        print(f"❌ Error al actualizar finca: {e}")
        return jsonify({"error": "No se pudo actualizar"}), 500

# 🔹 Eliminar finca
@ruta_farm.route("/deleteFarm/<string:farm_id>", methods=["DELETE"])
def delete_farm(farm_id):
    try:
        db.session.execute("DELETE FROM usuario_finca WHERE farm_id = :id", {"id": farm_id})
        db.session.query(Farm).filter_by(id=farm_id).delete()
        db.session.commit()
        return jsonify({"message": "Finca eliminada"})
    except Exception as e:
        print(f"❌ Error al eliminar finca: {e}")
        return jsonify({"error": "Error interno"}), 500
