from app.funcionario.model import Funcionario
from flask import request, jsonify
from app.extensions import db
from flask.views import MethodView 
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

import bcrypt



class FuncionariosCreate (MethodView): #/funcionario/create
    def get(self):
        funcionario=Funcionario.query.all()
        return jsonify([funcionario.json() for funcionario in funcionario]), 200


    def post(self):
        dados = request.json 
        nome = dados.get('nome')
        cpf = dados.get ('cpf')
        idade = dados.get ('idade')
        email = dados.get ('email')
        senha = dados.get ('senha')

        funcionario = Funcionario.query.filter_by(email = email).first()

        if funcionario:
            return {'error':'email já cadastrado'}, 400

    

        if not isinstance (nome,str) or not isinstance (idade, int):
            return {'error':'tipo invalido'}, 400

        senha_hash = bcrypt.hashpw(senha.encode(), bcrypt.gensalt())


        funcionario = Funcionario(nome=nome, cpf=cpf, idade=idade, email=email, senha_hash=senha_hash)
        db.session.add (funcionario)
        db.session.commit()

        return funcionario.json(), 200

class FuncionariosDetails(MethodView): #/funcionario/details/<int:id>
    decorators = [jwt_required()]
    def get(self, id):
        if (get_jwt_identity() != id):
            return {'error':'Usuario não permitido'}, 400

        funcionario = Funcionario.query.get_or_404(id)
        
        return funcionario.json(), 200

    def put(self, id):
        if (get_jwt_identity() != id):
            return {'error':'Usuario não permitido'}, 400
        funcionario=Funcionario.query.get_or_404(id)
        dados = request.json

        nome = dados.get('nome')
        email = dados.get ('email')
        cpf = dados.get ('cpf')
        idade = dados.get ('idade')
       

        funcionario.nome = nome
        funcionario.email = email
        funcionario.cpf = cpf
        funcionario.idade = idade


        db.session.commit()

        return funcionario.json(), 200

    def patch(self, id):
        if (get_jwt_identity() != id):
            return {'error':'Usuario não permitido'}, 400

        funcionario = Funcionario.query.get_or_404(id)
        funcionario=Funcionario.query.get_or_404(id)
        dados = request.json

        nome = dados.get('nome', funcionario.nome)
        email = dados.get ('email', funcionario.email)
        cpf = dados.get ('cpf', funcionario.cpf)
        idade = dados.get ('idade', funcionario.idade)
        

        funcionario.nome = nome
        funcionario.email = email
        funcionario.cpf = cpf
        funcionario.idade = idade

        db.session.commit()

        return funcionario.json(), 200
    
    def delete(self, id):
        if (get_jwt_identity() != id):
            return {'error':'Usuario não permitido'}, 400
        funcionario=Funcionario.query.get_or_404(id)
        db.session.delete(funcionario)
        db.session.commit()
        return funcionario.json(), 200

class FuncionarioLogin(MethodView):
    def post(self):
        dados = request.json 
        email = dados.get ('email')
        senha = dados.get ('senha')
        
        funcionario = Funcionario.query.filter_by(email = email).first()
        if (not funcionario) or (not bcrypt.checkpw(senha.encode(), funcionario.senha_hash)):
            return {'error':'Email ou senha inválida'}, 400
        
        token = create_access_token(identity = funcionario.id)
        
        return {"token" : token}, 200






