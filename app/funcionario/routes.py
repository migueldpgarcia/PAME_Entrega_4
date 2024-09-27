from app.funcionario.controllers import FuncionariosCreate, FuncionariosDetails, FuncionarioLogin
from flask import Blueprint




funcionario_api = Blueprint ('funcionario_api', __name__)

funcionario_api.add_url_rule(

    '/funcionario/create', view_func=FuncionariosCreate.as_view('funcionario_create'), methods = ['GET', 'POST']

)
funcionario_api.add_url_rule(

    '/funcionario/details/<int:id>', view_func=FuncionariosDetails.as_view('funcionario_details'), methods = ['GET', 'PUT', 'PATCH', 'DELETE']

)
funcionario_api.add_url_rule(

    '/funcionario/login', view_func=FuncionarioLogin.as_view('funcionario_login'), methods = ['POST']

)