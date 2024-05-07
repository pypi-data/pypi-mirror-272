import pytest
from journeylib.funciones import ins_historico
from fastapi.responses import JSONResponse
import json

"""
def test_ins_historico():
    usr = 'usuario'
    num_chat = 1
    contexto = 'contexto'
    lista_msg = [{"role": "user", "content": "Hola, ¿cómo estás?"},
                 {"role": "assistant", "content": "Hola, soy ia."}]
    tipoIA = 'PASADO'
    cerrado = True
    datos=[usr, num_chat, contexto, lista_msg, tipoIA, cerrado]

    response = ins_historico(usr, num_chat, contexto, lista_msg, tipoIA, cerrado)
    assert response.status_code == 200

    expected_data = {
        'id_usuario': usr,
        'num_chat': num_chat,
        'contexto': contexto,
        'lista_msg': lista_msg,
        'tipoIA': tipoIA,
        'cerrado': cerrado
    }
    # Convierte la respuesta JSON a un diccionario para comparar fácilmente
    response_data = json.loads(response.content)
    assert response_data == expected_data
"""
    
def test_ins_historico_usr_vacio():
    usr = ''
    num_chat = 1
    contexto = 'contexto'
    lista_msg = [{"role": "user", "content": "Hola, ¿cómo estás?"},
                 {"role": "assistant", "content": "Hola, soy ia."}]
    tipoIA = 'PASADO'
    cerrado = True

    status_code = ins_historico(usr, num_chat, contexto, lista_msg, tipoIA, cerrado)
    assert status_code != 200

def test_ins_historico_lista_msg_vacia():
    usr = 'usuario'
    num_chat = 1
    contexto = 'contexto'
    lista_msg = []
    tipoIA = 'PASADO'
    cerrado = True

    status_code = ins_historico(usr, num_chat, contexto, lista_msg, tipoIA, cerrado)
    assert status_code != 200