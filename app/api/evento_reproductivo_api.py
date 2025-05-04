from flask import Blueprint, request, jsonify
from config.db import db
from models.evento_reproductivo import EventoReproductivo, EventoReproductivoSchema
from datetime import datetime
import traceback

ruta_evento = Blueprint("route_evento_reproductivo", __name__)

evento_schema = EventoReproductivoSchema()
eventos_schema = EventoReproductivoSchema(many=True)

# 🔹 Obtener eventos por animal
@ruta_evento.route("/eventos/animal/<string:animal_id>", methods=["GET"])
def get_eventos_by_animal(animal_id):
    try:
        eventos = EventoReproductivo.query.filter_by(animal_id=animal_id).all()
        return jsonify(eventos_schema.dump(eventos))
    except Exception as e:
        print(f"❌ Error al obtener eventos por animal: {e}")
        print(traceback.format_exc())
        return jsonify({"error": "Error interno"}), 500

# 🔹 Obtener eventos por finca
@ruta_evento.route("/eventos/farm/<string:farm_id>", methods=["GET"])
def get_eventos_by_farm(farm_id):
    try:
        eventos = EventoReproductivo.query.filter_by(farm_id=farm_id).all()
        return jsonify(eventos_schema.dump(eventos))
    except Exception as e:
        print(f"❌ Error al obtener eventos por finca: {e}")
        print(traceback.format_exc())
        return jsonify({"error": "Error interno"}), 500

# 🔹 Obtener todos los eventos
@ruta_evento.route("/eventos", methods=["GET"])
def get_all_eventos():
    try:
        eventos = EventoReproductivo.query.all()
        return jsonify(eventos_schema.dump(eventos))
    except Exception as e:
        print(f"❌ Error al obtener todos los eventos: {e}")
        print(traceback.format_exc())
        return jsonify({"error": "Error interno"}), 500

# 🔹 Agregar evento
@ruta_evento.route("/addEvento", methods=["POST"])
def add_evento():
    try:
        data = request.json
        nuevo = EventoReproductivo.from_dict(data)
        db.session.add(nuevo)
        db.session.commit()
        return jsonify({"message": "Evento guardado", "id": nuevo.id})
    except Exception as e:
        print(f"❌ Error al guardar evento: {e}")
        print(traceback.format_exc())
        return jsonify({"error": "No se pudo guardar"}), 500

# 🔹 Actualizar evento
@ruta_evento.route("/updateEvento/<string:evento_id>", methods=["PUT"])
def update_evento(evento_id):
    try:
        data = request.json
        db.session.query(EventoReproductivo).filter_by(id=evento_id).update(data)
        db.session.commit()
        return jsonify({"message": "Evento actualizado"})
    except Exception as e:
        print(f"❌ Error al actualizar evento: {e}")
        print(traceback.format_exc())
        return jsonify({"error": "No se pudo actualizar"}), 500

# 🔹 Eliminar evento
@ruta_evento.route("/deleteEvento/<string:evento_id>", methods=["DELETE"])
def delete_evento(evento_id):
    try:
        evento = EventoReproductivo.query.get(evento_id)
        if not evento:
            return jsonify({"error": "No encontrado"}), 404
        db.session.delete(evento)
        db.session.commit()
        return jsonify({"message": "Evento eliminado"})
    except Exception as e:
        print(f"❌ Error al eliminar evento: {e}")
        print(traceback.format_exc())
        return jsonify({"error": "Error interno"}), 500
