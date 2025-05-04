from config.db import db, ma
from datetime import datetime
import uuid

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    nombre = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    rol = db.Column(db.String(50), nullable=False, default='asistente')  # Enum como string
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, id, nombre, email, rol, created_at, updated_at):
        self.id = id or str(uuid.uuid4())
        self.nombre = nombre
        self.email = email
        self.rol = rol  # Se espera un string: "administrador", "veterinario", o "asistente"
        self.created_at = created_at
        self.updated_at = updated_at

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'email': self.email,
            'rol': self.rol,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }

    @staticmethod
    def from_dict(data):
        return Usuario(
            id=data.get('id', str(uuid.uuid4())),
            nombre=data['nombre'],
            email=data['email'],
            rol=data.get('rol', 'asistente'),  # valor por defecto
            created_at=datetime.fromisoformat(data['created_at']),
            updated_at=datetime.fromisoformat(data['updated_at']),
        )

class UsuarioSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nombre', 'email', 'rol', 'created_at', 'updated_at')
