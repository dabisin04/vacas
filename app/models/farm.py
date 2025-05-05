from app.config.db import db, ma
from datetime import datetime
import uuid

class Farm(db.Model):
    __tablename__ = 'farms'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    nombre = db.Column(db.String(255), nullable=False)
    ubicacion = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    propietario_id = db.Column(db.String(36), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, id, nombre, ubicacion, descripcion, propietario_id, created_at, updated_at):
        self.id = id or str(uuid.uuid4())
        self.nombre = nombre
        self.ubicacion = ubicacion
        self.descripcion = descripcion
        self.propietario_id = propietario_id
        self.created_at = created_at
        self.updated_at = updated_at

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'ubicacion': self.ubicacion,
            'descripcion': self.descripcion,
            'propietario_id': self.propietario_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }

    @staticmethod
    def from_dict(data):
        return Farm(
            id=data.get('id', str(uuid.uuid4())),
            nombre=data['nombre'],
            ubicacion=data['ubicacion'],
            descripcion=data['descripcion'],
            propietario_id=data['propietario_id'],
            created_at=datetime.fromisoformat(data['created_at']),
            updated_at=datetime.fromisoformat(data['updated_at']),
        )

class FarmSchema(ma.Schema):
    class Meta:
        fields = (
            'id', 'nombre', 'ubicacion', 'descripcion',
            'propietario_id', 'created_at', 'updated_at'
        )
