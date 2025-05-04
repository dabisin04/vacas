from flask import Blueprint, request, jsonify
from config.db import db
from models.user import Usuario, UsuarioSchema
from datetime import datetime
import traceback

ruta_usuario = Blueprint("route_usuario", __name__)

usuario_schema = UsuarioSchema()
usuarios_schema = UsuarioSchema(many=True)

# 🔹 Crear usuario
@ruta_usuario.route("/addUsuario", methods=["POST"])
def add_usuario():
    try:
        data = request.json
        nuevo = Usuario.from_dict(data)
        db.session.add(nuevo)
        db.session.commit()
        return jsonify({"message": "Usuario creado", "id": nuevo.id})
    except Exception as e:
        print("❌ Error en addUsuario:", e)
        print(traceback.format_exc())
        return jsonify({"error": "Error al crear usuario"}), 500

# 🔹 Obtener todos los usuarios
@ruta_usuario.route("/usuarios", methods=["GET"])
def get_all_usuarios():
    usuarios = Usuario.query.all()
    return jsonify(usuarios_schema.dump(usuarios))

# 🔹 Obtener usuario por ID
@ruta_usuario.route("/usuario/<string:user_id>", methods=["GET"])
def get_usuario(user_id):
    usuario = Usuario.query.get(user_id)
    return jsonify(usuario_schema.dump(usuario)) if usuario else jsonify({"message": "No encontrado"}), 404

# 🔹 Obtener usuarios por finca
@ruta_usuario.route("/usuariosPorFinca/<string:farm_id>", methods=["GET"])
def get_usuarios_por_finca(farm_id):
    result = db.session.execute("""
        SELECT u.* FROM usuarios u
        JOIN usuario_finca uf ON u.id = uf.user_id
        WHERE uf.farm_id = :farm_id
    """, {"farm_id": farm_id}).fetchall()
    usuarios = [dict(row._mapping) for row in result]
    return jsonify(usuarios)

# 🔹 Login (solo con email)
@ruta_usuario.route("/login", methods=["POST"])
def login_usuario():
    email = request.json.get("email")
    usuario = Usuario.query.filter_by(email=email).first()
    if usuario:
        return jsonify(usuario_schema.dump(usuario))
    return jsonify({"error": "Usuario no encontrado"}), 404

# 🔹 Actualizar usuario
@ruta_usuario.route("/updateUsuario/<string:user_id>", methods=["PUT"])
def update_usuario(user_id):
    data = request.json
    db.session.query(Usuario).filter_by(id=user_id).update(data)
    db.session.commit()
    return jsonify({"message": "Usuario actualizado"})

# 🔹 Eliminar usuario
@ruta_usuario.route("/deleteUsuario/<string:user_id>", methods=["DELETE"])
def delete_usuario(user_id):
    db.session.query(Usuario).filter_by(id=user_id).delete()
    db.session.query("DELETE FROM usuario_finca WHERE user_id = :uid", {"uid": user_id})
    db.session.commit()
    return jsonify({"message": "Usuario eliminado"})
