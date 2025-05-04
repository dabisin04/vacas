from config.db import db, ma
from datetime import datetime
import uuid

class Animal(db.Model):
    __tablename__ = 'animals'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    farm_id = db.Column(db.String(36), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    raza = db.Column(db.String(100), nullable=False)
    proposito = db.Column(db.String(100), nullable=False)
    ganaderia = db.Column(db.String(100), nullable=False)
    corral = db.Column(db.String(100), nullable=False)
    num_animal = db.Column(db.String(50), nullable=False)
    codigo_referencia = db.Column(db.String(100), nullable=False)
    fecha_nacimiento = db.Column(db.DateTime, nullable=False)
    peso_nacimiento = db.Column(db.Float, nullable=False)
    padre_id = db.Column(db.String(36), nullable=True)
    madre_id = db.Column(db.String(36), nullable=True)
    created_by = db.Column(db.String(36), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, id, farm_id, nombre, tipo, raza, proposito, ganaderia, corral, num_animal, codigo_referencia,
                 fecha_nacimiento, peso_nacimiento, padre_id, madre_id, created_by, created_at, updated_at):
        self.id = id or str(uuid.uuid4())
        self.farm_id = farm_id
        self.nombre = nombre
        self.tipo = tipo
        self.raza = raza
        self.proposito = proposito
        self.ganaderia = ganaderia
        self.corral = corral
        self.num_animal = num_animal
        self.codigo_referencia = codigo_referencia
        self.fecha_nacimiento = fecha_nacimiento
        self.peso_nacimiento = peso_nacimiento
        self.padre_id = padre_id
        self.madre_id = madre_id
        self.created_by = created_by
        self.created_at = created_at
        self.updated_at = updated_at

    def to_dict(self):
        return {
            'id': self.id,
            'farm_id': self.farm_id,
            'nombre': self.nombre,
            'tipo': self.tipo,
            'raza': self.raza,
            'proposito': self.proposito,
            'ganaderia': self.ganaderia,
            'corral': self.corral,
            'num_animal': self.num_animal,
            'codigo_referencia': self.codigo_referencia,
            'fecha_nacimiento': self.fecha_nacimiento.isoformat(),
            'peso_nacimiento': self.peso_nacimiento,
            'padre_id': self.padre_id,
            'madre_id': self.madre_id,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    @staticmethod
    def from_dict(data):
        return Animal(
            id=data.get('id', str(uuid.uuid4())),
            farm_id=data['farm_id'],
            nombre=data['nombre'],
            tipo=data['tipo'],
            raza=data['raza'],
            proposito=data['proposito'],
            ganaderia=data['ganaderia'],
            corral=data['corral'],
            num_animal=data['num_animal'],
            codigo_referencia=data['codigo_referencia'],
            fecha_nacimiento=datetime.fromisoformat(data['fecha_nacimiento']),
            peso_nacimiento=float(data.get('peso_nacimiento', 0)),
            padre_id=data.get('padre_id'),
            madre_id=data.get('madre_id'),
            created_by=data['created_by'],
            created_at=datetime.fromisoformat(data['created_at']),
            updated_at=datetime.fromisoformat(data['updated_at']),
        )

class AnimalSchema(ma.Schema):
    class Meta:
        fields = (
            'id', 'farm_id', 'nombre', 'tipo', 'raza', 'proposito', 'ganaderia',
            'corral', 'num_animal', 'codigo_referencia', 'fecha_nacimiento',
            'peso_nacimiento', 'padre_id', 'madre_id', 'created_by',
            'created_at', 'updated_at'
        )
