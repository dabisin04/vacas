from flask import Blueprint, request, jsonify
from app.config.db import db
from app.models.usuario_finca import UsuarioFinca, UsuarioFincaSchema
import traceback

ruta_usuario_finca = Blueprint("route_usuario_finca", __name__)

rel_schema = UsuarioFincaSchema()
rels_schema = UsuarioFincaSchema(many=True)

# 🔹 Asignar usuario a finca
@ruta_usuario_finca.route("/asignarUsuarioAFinca", methods=["POST"])
def asignar_usuario_a_finca():
    try:
        data = request.json
        nueva_relacion = UsuarioFinca.from_dict(data)
        db.session.add(nueva_relacion)
        db.session.commit()
        return jsonify({"message": "Relación asignada", "id": nueva_relacion.id})
    except Exception as e:
        print("❌ Error en asignarUsuarioAFinca:", e)
        print(traceback.format_exc())
        return jsonify({"error": "Error al asignar relación"}), 500

# 🔹 Obtener fincas por usuario
@ruta_usuario_finca.route("/fincasPorUsuario/<string:user_id>", methods=["GET"])
def get_fincas_por_usuario(user_id):
    result = UsuarioFinca.query.filter_by(user_id=user_id).all()
    return jsonify([r.farm_id for r in result])

# 🔹 Obtener usuarios por finca
@ruta_usuario_finca.route("/usuariosPorFinca/<string:farm_id>", methods=["GET"])
def get_usuarios_por_finca(farm_id):
    result = UsuarioFinca.query.filter_by(farm_id=farm_id).all()
    return jsonify([r.user_id for r in result])

# 🔹 Eliminar relación por ID
@ruta_usuario_finca.route("/eliminarRelacion/<string:rel_id>", methods=["DELETE"])
def eliminar_relacion(rel_id):
    relacion = UsuarioFinca.query.get(rel_id)
    if not relacion:
        return jsonify({"error": "Relación no encontrada"}), 404
    db.session.delete(relacion)
    db.session.commit()
    return jsonify({"message": "Relación eliminada"})
