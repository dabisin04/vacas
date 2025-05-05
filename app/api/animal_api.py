import traceback
from flask import Blueprint, request, jsonify
from app.config.db import db
from app.models.animal import Animal, AnimalSchema
from datetime import datetime
import uuid

ruta_animal = Blueprint("route_animal", __name__)

animal_schema = AnimalSchema()
animals_schema = AnimalSchema(many=True)

@ruta_animal.route("/animals", methods=["GET"])
def get_all_animals():
    farm_id = request.args.get("farm_id")
    if not farm_id:
        return jsonify({"error": "Parámetro 'farm_id' requerido"}), 400

    animals = Animal.query.filter_by(farm_id=farm_id).all()
    return jsonify(animals_schema.dump(animals))

@ruta_animal.route("/animal/<string:animal_id>", methods=["GET"])
def get_animal_by_id(animal_id):
    animal = Animal.query.get(animal_id)
    return jsonify(animal_schema.dump(animal)) if animal else jsonify({"message": "No encontrado"}), 404

@ruta_animal.route("/addAnimal", methods=["POST"])
def add_animal():
    try:
        data = request.json
        new_animal = Animal.from_dict(data)
        db.session.add(new_animal)
        db.session.commit()
        return jsonify({"message": "Animal guardado correctamente", "id": new_animal.id})
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({"error": "Error al guardar el animal"}), 500

@ruta_animal.route("/updateAnimal/<string:animal_id>", methods=["PUT"])
def update_animal(animal_id):
    try:
        data = request.json
        db.session.query(Animal).filter_by(id=animal_id).update(data)
        db.session.commit()
        return jsonify({"message": "Animal actualizado"})
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({"error": "Error al actualizar el animal"}), 500

@ruta_animal.route("/deleteAnimal/<string:animal_id>", methods=["DELETE"])
def delete_animal(animal_id):
    animal = Animal.query.get(animal_id)
    if not animal:
        return jsonify({"error": "Animal no encontrado"}), 404
    db.session.delete(animal)
    db.session.commit()
    return jsonify({"message": "Animal eliminado"})
