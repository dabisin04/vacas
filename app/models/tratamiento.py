from app.config.db import db, ma
from datetime import datetime
import uuid

class Tratamiento(db.Model):
    __tablename__ = 'tratamientos'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    farm_id = db.Column(db.String(36), nullable=False)
    animal_id = db.Column(db.String(36), nullable=False)
    medicamento = db.Column(db.String(255), nullable=False)
    motivo = db.Column(db.Text, nullable=False)
    fecha = db.Column(db.DateTime, nullable=False)
    registrado_por = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, id, farm_id, animal_id, medicamento, motivo, fecha, registrado_por, created_at, updated_at):
        self.id = id or str(uuid.uuid4())
        self.farm_id = farm_id
        self.animal_id = animal_id
        self.medicamento = medicamento
        self.motivo = motivo
        self.fecha = fecha
        self.registrado_por = registrado_por
        self.created_at = created_at
        self.updated_at = updated_at

    def to_dict(self):
        return {
            'id': self.id,
            'farm_id': self.farm_id,
            'animal_id': self.animal_id,
            'medicamento': self.medicamento,
            'motivo': self.motivo,
            'fecha': self.fecha.isoformat(),
            'registrado_por': self.registrado_por,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }

    @staticmethod
    def from_dict(data):
        return Tratamiento(
            id=data.get('id', str(uuid.uuid4())),
            farm_id=data['farm_id'],
            animal_id=data['animal_id'],
            medicamento=data['medicamento'],
            motivo=data['motivo'],
            fecha=datetime.fromisoformat(data['fecha']),
            registrado_por=data['registrado_por'],
            created_at=datetime.fromisoformat(data['created_at']),
            updated_at=datetime.fromisoformat(data['updated_at']),
        )

class TratamientoSchema(ma.Schema):
    class Meta:
        fields = (
            'id', 'farm_id', 'animal_id', 'medicamento',
            'motivo', 'fecha', 'registrado_por', 'created_at', 'updated_at'
        )
