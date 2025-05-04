from config.db import db, ma
from datetime import datetime
import uuid

class EventoReproductivo(db.Model):
    __tablename__ = 'eventos_reproductivos'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    farm_id = db.Column(db.String(36), nullable=False)
    animal_id = db.Column(db.String(36), nullable=False)
    tipo = db.Column(db.String(100), nullable=False)
    fecha = db.Column(db.DateTime, nullable=False)
    resultado = db.Column(db.Text, nullable=False)
    realizado_por = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, id, farm_id, animal_id, tipo, fecha, resultado, realizado_por, created_at, updated_at):
        self.id = id or str(uuid.uuid4())
        self.farm_id = farm_id
        self.animal_id = animal_id
        self.tipo = tipo
        self.fecha = fecha
        self.resultado = resultado
        self.realizado_por = realizado_por
        self.created_at = created_at
        self.updated_at = updated_at

    def to_dict(self):
        return {
            'id': self.id,
            'farm_id': self.farm_id,
            'animal_id': self.animal_id,
            'tipo': self.tipo,
            'fecha': self.fecha.isoformat(),
            'resultado': self.resultado,
            'realizado_por': self.realizado_por,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }

    @staticmethod
    def from_dict(data):
        return EventoReproductivo(
            id=data.get('id', str(uuid.uuid4())),
            farm_id=data['farm_id'],
            animal_id=data['animal_id'],
            tipo=data['tipo'],
            fecha=datetime.fromisoformat(data['fecha']),
            resultado=data['resultado'],
            realizado_por=data['realizado_por'],
            created_at=datetime.fromisoformat(data['created_at']),
            updated_at=datetime.fromisoformat(data['updated_at']),
        )

class EventoReproductivoSchema(ma.Schema):
    class Meta:
        fields = (
            'id', 'farm_id', 'animal_id', 'tipo', 'fecha', 'resultado',
            'realizado_por', 'created_at', 'updated_at'
        )
