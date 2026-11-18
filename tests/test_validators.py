"""Pruebas de validators.py.

Solo asumen lo que se ve en planes.py: cada función recibe
(form, campo, etiqueta, errores, **opciones), devuelve el valor limpio
y agrega un mensaje a `errores` cuando algo está mal.
Si alguna falla por el tipo de retorno exacto, ajusta el assert.
"""
import validators as v


# ---------- texto ----------

def test_texto_valido():
    errores = []
    assert v.texto({"n": "  Mensual "}, "n", "El nombre", errores, max_len=60) == "Mensual"
    assert errores == []


def test_texto_obligatorio_vacio():
    errores = []
    v.texto({"n": "   "}, "n", "El nombre", errores, max_len=60)
    assert len(errores) == 1


def test_texto_demasiado_largo():
    errores = []
    v.texto({"n": "x" * 61}, "n", "El nombre", errores, max_len=60)
    assert len(errores) == 1


def test_texto_opcional_vacio_no_da_error():
    errores = []
    v.texto({}, "d", "La descripción", errores, obligatorio=False, max_len=200)
    assert errores == []


# ---------- entero ----------

def test_entero_valido():
    errores = []
    assert v.entero({"d": "30"}, "d", "La duración", errores, minimo=1) == 30
    assert errores == []


def test_entero_menor_al_minimo():
    errores = []
    v.entero({"d": "0"}, "d", "La duración", errores, minimo=1)
    assert len(errores) == 1


def test_entero_no_numerico():
    errores = []
    v.entero({"d": "abc"}, "d", "La duración", errores, minimo=1)
    assert len(errores) == 1


def test_entero_vacio():
    errores = []
    v.entero({"d": ""}, "d", "La duración", errores, minimo=1)
    assert len(errores) == 1


def test_entero_decimal_no_es_valido():
    errores = []
    v.entero({"d": "3.5"}, "d", "La duración", errores, minimo=1)
    assert len(errores) == 1


# ---------- decimal ----------

def test_decimal_valido():
    errores = []
    assert v.decimal({"p": "66000.50"}, "p", "El precio", errores, mayor_que=0) == 66000.50
    assert errores == []


def test_decimal_cero_no_es_mayor_que_cero():
    errores = []
    v.decimal({"p": "0"}, "p", "El precio", errores, mayor_que=0)
    assert len(errores) == 1


def test_decimal_negativo():
    errores = []
    v.decimal({"p": "-10"}, "p", "El precio", errores, mayor_que=0)
    assert len(errores) == 1


def test_decimal_no_numerico():
    errores = []
    v.decimal({"p": "mucho"}, "p", "El precio", errores, mayor_que=0)
    assert len(errores) == 1
