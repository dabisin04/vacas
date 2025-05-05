from app.config.db import db, ma
import uuid

class UsuarioFinca(db.Model):
    __tablename__ = 'usuario_finca'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), nullable=False)
    farm_id = db.Column(db.String(36), nullable=False)

    def __init__(self, user_id, farm_id, id=None):
        self.id = id or str(uuid.uuid4())
        self.user_id = user_id
        self.farm_id = farm_id

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'farm_id': self.farm_id,
        }

    @staticmethod
    def from_dict(data):
        return UsuarioFinca(
            id=data.get('id'),
            user_id=data['user_id'],
            farm_id=data['farm_id'],
        )

class UsuarioFincaSchema(ma.Schema):
    class Meta:
        fields = ('id', 'user_id', 'farm_id')
