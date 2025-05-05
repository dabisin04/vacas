from app.config.db import db, ma
from datetime import datetime
import uuid

class ProduccionLeche(db.Model):
    __tablename__ = 'produccion_leche'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    farm_id = db.Column(db.String(36), nullable=False)
    animal_id = db.Column(db.String(36), nullable=False)
    fecha = db.Column(db.DateTime, nullable=False)
    cantidad_litros = db.Column(db.Float, nullable=False)
    registrado_por = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, id, farm_id, animal_id, fecha, cantidad_litros, registrado_por, created_at, updated_at):
        self.id = id or str(uuid.uuid4())
        self.farm_id = farm_id
        self.animal_id = animal_id
        self.fecha = fecha
        self.cantidad_litros = cantidad_litros
        self.registrado_por = registrado_por
        self.created_at = created_at
        self.updated_at = updated_at

    def to_dict(self):
        return {
            'id': self.id,
            'farm_id': self.farm_id,
            'animal_id': self.animal_id,
            'fecha': self.fecha.isoformat(),
            'cantidad_litros': self.cantidad_litros,
            'registrado_por': self.registrado_por,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }

    @staticmethod
    def from_dict(data):
        return ProduccionLeche(
            id=data.get('id', str(uuid.uuid4())),
            farm_id=data['farm_id'],
            animal_id=data['animal_id'],
            fecha=datetime.fromisoformat(data['fecha']),
            cantidad_litros=float(data['cantidad_litros']),
            registrado_por=data['registrado_por'],
            created_at=datetime.fromisoformat(data['created_at']),
            updated_at=datetime.fromisoformat(data['updated_at']),
        )

class ProduccionLecheSchema(ma.Schema):
    class Meta:
        fields = (
            'id', 'farm_id', 'animal_id', 'fecha',
            'cantidad_litros', 'registrado_por', 'created_at', 'updated_at'
        )
