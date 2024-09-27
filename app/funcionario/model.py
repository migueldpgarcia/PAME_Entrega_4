from enum import unique
from app.extensions import db
from sqlalchemy.orm import backref


class Funcionario (db.Model):
    __tablename__ = 'funcionario'
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(20), nullable = False)
    email = db.Column(db.String(20), nullable = False, unique = True)
    cpf = db.Column(db.String(40), nullable = False)
    idade = db.Column(db.Integer, nullable = False)
    senha_hash = db.Column (db.String(400), nullable = False)
    
    presenca = db.relationship ('Presenca', backref = 'funcionario')

    def json(self):
        return {'nome': self.nome,
        'email':self.email,
        'cpf': self.cpf,
        'idade':self.idade
        }
 


 