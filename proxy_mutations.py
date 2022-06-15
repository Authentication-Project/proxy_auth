#!/usr/bin/env python3

import graphene
import requests

# 1. Import Config

__version__ = "2.0.0"

# 0. Global
pg_conn = None
response_body = ""

# 0.1 PgSql

# 1. Models

# 1.2 Input Models
# De la Mutacion


class UsuarioInputx(graphene.InputObjectType):
    
    id_usuario = graphene.String(required=True)
    nombre1 = graphene.String(required=True)
    nombre2 = graphene.String(required=True)
    apellido1 = graphene.String(required=True)
    apellido2 = graphene.String(required=True)
    fecha_nacimiento = graphene.String(required=True)
    id_genero = graphene.String(required=True)
    telefono = graphene.String(required=True)
    correo = graphene.String(required=True)
    fecha_registro = graphene.String(required=True)
    estado = graphene.String(required=True)
    contrasena = graphene.String(required=True)
    tipo_acceso = graphene.String(required=True)

class ResetInput(graphene.InputObjectType):
    token = graphene.String(required=True)
    contrasena = graphene.String(required=True)





# 1.3 Rta Models

class UsuariosX(graphene.ObjectType):
    message = graphene.String()    
    id_usuario = graphene.String()
    nombre1 = graphene.String()
    nombre2 = graphene.String()
    apellido1 = graphene.String()
    apellido2 = graphene.String()
    fecha_nacimiento = graphene.String()
    id_genero = graphene.String()
    telefono = graphene.String()
    correo = graphene.String()
    fecha_registro = graphene.String()
    estado = graphene.String()
    contrasena = graphene.String()
    tipo_acceso = graphene.String()

class PasswordReset(graphene.ObjectType):
    message = graphene.String()

# 1.5 Llamada De Mutation Principal
class ModifyUserNewx(graphene.Mutation):
    class Arguments:
        userdata = UsuarioInputx(required=True)

    ok = graphene.Boolean()
    user_new = graphene.Field(lambda: UsuariosX)

    def mutate(self, info, userdata):
        user_new = set_usuario_sis( userdata.id_usuario, userdata.nombre1, userdata.nombre2, userdata.apellido1, userdata.apellido2, userdata.fecha_nacimiento, userdata.id_genero, userdata.telefono, userdata.correo, userdata.fecha_registro, userdata.estado, userdata.contrasena, userdata.tipo_acceso)

        #raise Exception("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"+ f'{user_new[0].message}') PRINTF
        if user_new[0].message == "User added":
            ok = True
        else:
            ok = False

        return ModifyUserNewx(user_new=user_new[0], ok=ok)


class ResetPassword(graphene.Mutation):
    class Arguments:
        user_data = ResetInput(required=True)

    ok = graphene.Boolean()
    user_new = graphene.Field(lambda: PasswordReset)

    def mutate(self, info, user_data):
        user_new = set_password(user_data.contrasena, user_data.token)

        if user_new:
            ok = True
        else:
            ok = False

        return ResetPassword(user_new=user_new[0], ok=ok)

# 1.6 Funcion De Ejecucion De La Mutacion
def set_usuario_sis(id_usuario, nombre1, nombre2 , apellido1, apellido2, fecha_nacimiento, id_genero, telefono, correo, fecha_registro, estado, contrasena, tipo_acceso):
    pg_connect()
    global pg_conn, response_body

    gql = []

    try:
        
        datosuser = {
            "nombres": [
                nombre1, nombre2
            ],
            "apellidos": [
                apellido1, apellido2
            ],
            "fecha_nacimiento": fecha_nacimiento,
            "id_genero": id_genero,
            "telefono": telefono,
            "fecha_registro": fecha_registro,
            "estado": estado,
            "correo": correo,
            "tipo_acceso": tipo_acceso,
            "contraseña": contrasena,
            "id_usuario": id_usuario
        }
        response = requests.post('http://172.30.0.37:4555/auth/register/', data=datosuser)

        gql.append(UsuariosX(message=response.json().get('Message'), id_usuario=id_usuario, nombre1=nombre1, nombre2=nombre2, apellido1=apellido1, apellido2=apellido2, fecha_nacimiento=fecha_nacimiento, id_genero=id_genero, telefono=telefono, correo=correo, estado=estado, fecha_registro=fecha_registro, tipo_acceso=tipo_acceso, contrasena=contrasena ))
        #gql.append(UsuariosX(Message = response.json().get("Message")))

        
    except (Exception, psycopg2.DatabaseError) as error:
        response_body = "Notice: check set"
    return gql

def set_password(contrasena, token):
    pg_connect()
    global pg_conn, response_body
    url = 'http://172.30.0.37:4555/auth/reset-password?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZF91c3VhcmlvIjoxMDAwLCJub21icmVzIjpbIkp1YW4iXSwiaWF0IjoxNjU0ODc0NzE3LCJleHAiOjE2NTQ5NjExMTd9.mgDaxiCcD_n_dbc8q1ZsTqP00SPWfDgVB0S0v27SowQ'

    gql = []

    try:
        
        datosuser = {
            "contraseña": contrasena,
        }

        response = requests.put('http://172.30.0.37:4555/auth/reset-password', data=datosuser, params={"token":f'{token}'})
        #response = requests.post(url=url, data=datosuser)


        gql.append(PasswordReset(message = response.json().get("Message")))

        
    except (Exception, psycopg2.DatabaseError) as error:
        response_body = "Notice: check set"
    return gql

