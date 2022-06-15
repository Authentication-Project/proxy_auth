#!/usr/bin/env python3

from graphene import ObjectType, ID, String, Boolean
from requests import post, get
from os import environ

# 1. Import Config
# import sis_t_config

# 19042022
__version__ = "1.0"

# 0. Global
pg_conn = None
response_body = ""
auth_uri = environ.get('APP_URL_BACKEND')


# 0.1 PgSql

# 1. Models

# 1.2 Input


# class TotalUsuarios(graphene.ObjectType):
#    total = graphene.String()
class UsuariosFiltro(ObjectType):
    id_usuario = ID()
    nombres = String()
    # nombresp = graphene.String()
    apellidos = String()
    # apellido_primer = graphene.String()
    # apellido_segundo = graphene.String()
    fecha_nacimiento = String()
    id_genero = String()
    telefono = String()
    correo = String()
    fecha_registro = String()
    estado = String()
    fecha_registro = String()
    id_tipo_acceso = String()
    contrasena = String()
    # grupos_id = graphene.String()
    # grupos_nombre = graphene.String()

class LoginFiltro(ObjectType):
   message = String()
   token = String()
   valid = Boolean()
   nombres = String()
   apellidos = String()
   id_genero = ID()
   id_usuario = ID()
   correo = String()
   tipo_acceso = String()

   """
   class LoginUser(graphene.ObjectType):
   nombres = graphene.String()
   apellidos = graphene.String()
   id_genero = graphene.String()
   correo = graphene.String()
   id_tipo_acceso = graphene.String()
   """


class RecuperarFiltro(ObjectType):
   message = String()

class TotalUsuarios(ObjectType):
    total = String()

# 2. Data

def get_login(pg_conn, email, contrasena):
    global response_body
    
    gql = []    
    response = post(url=f'{auth_uri}/auth/login/', data={"correo":f'{email}', "contraseña":f'{contrasena}'})
    data = response.json()   
    
    try:        
        data_user = data.get('user')

        datosuser = {
            "nombres": data_user.get('nombres'),
            "apellidos": data_user.get('apellidos'),
            "id_genero": data_user.get('id_genero'),
            "id_usuario": data_user.get('id_usuario'),
            "correo": data_user.get('correo'),
            "tipo_acceso": data_user.get('tipo_acceso')
        }

        gql.append(LoginFiltro(valid=data.get('valid'), message=data.get('Message'), token=data.get('token'), nombres=datosuser.get('nombres'), apellidos=datosuser.get('apellidos'), id_genero= datosuser.get('id_genero'), id_usuario=datosuser.get('id_usuario'), correo=datosuser.get('correo'), tipo_acceso=datosuser.get('tipo_acceso') ))
        
    except Exception as error:
        message = data.get('Message')
        raise Exception(f'{message}')

    return gql


def get_recuperar(pg_conn, email):
    global response_body
    gql = []
    try:
        response = post('http://172.30.0.37:4555/auth/forgot-password/', data={"correo":f'{email}'})
        #response.raise_for_status()
        # if response.status_code >= 200:
        #     raise Exception(f'{response.json()}')
        gql.append(RecuperarFiltro(message=response.json().get('Message')))
        #gql.append(LoginFiltro(message=response.content, token='Holaaa'))


    except (Exception, psycopg2.DatabaseError) as error:
        response_body = "Notice: check gets"
        raise Exception('FALLÉEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE')

    return gql


def get_usuarios(pg_conn, token):
    global response_body

    gql = []

    try:

        response = get('http://172.30.0.37:4555/user-sis/users/', headers={"token":f'{token}'})

        for pg_row in response.json():
            nombres = pg_row.get("nombres")
            
            # print(nombrejson)

            gql.append(UsuariosFiltro(id_usuario=pg_row.get("id_usuario"), nombres=nombres, apellidos=pg_row.get("apellidos"), fecha_nacimiento=pg_row.get("fecha_nacimiento"), id_genero=pg_row.get("id_genero"), telefono=pg_row.get("telefono"), correo=pg_row.get("correo"), estado=pg_row.get("estado"), fecha_registro=pg_row.get("fecha_registro"), id_tipo_acceso=pg_row.get("id_tipo_acceso"), contrasena=pg_row.get("contraseña") ))


    except (Exception, psycopg2.DatabaseError) as error:
        response_body = "Notice: check gets"
        gql = response
    return gql

