"""Pruebas simples con pytest (valor agregado).

Cada prueba hace una petición a la app y consulta PostgreSQL para comprobar
el resultado. Los planes de prueba llevan el prefijo ZZ_TEST_ y se borran
después de cada prueba.

Ejecutar con:  pytest -v
"""
import psycopg2
import pytest

from app import create_app
from config import Config

NOMBRE = "ZZ_TEST_Plan"
DATOS = {"nombre_plan": NOMBRE, "duracion_dias": "30", "precio": "66000",
         "incluye_clases": "on", "descripcion": "prueba"}


@pytest.fixture()
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def sql(consulta, params=()):
    """Ejecuta una consulta en PostgreSQL y devuelve la primera fila (o None)."""
    conn = psycopg2.connect(host=Config.DB_HOST, port=Config.DB_PORT, dbname=Config.DB_NAME,
                            user=Config.DB_USER, password=Config.DB_PASSWORD)
    with conn, conn.cursor() as cur:
        cur.execute(consulta, params)
        fila = cur.fetchone() if cur.description else None
    conn.close()
    return fila


def contar_plan():
    """Cuántos planes de prueba hay en la base."""
    fila = sql("SELECT COUNT(*) FROM planes WHERE nombre_plan = %s", (NOMBRE,))
    return fila[0] if fila else 0


@pytest.fixture(autouse=True)
def limpiar():
    """Borra el plan de prueba antes y después de cada prueba."""
    sql("DELETE FROM planes WHERE nombre_plan = %s", (NOMBRE,))
    yield
    sql("DELETE FROM planes WHERE nombre_plan = %s", (NOMBRE,))


# ---------------------------------------------------------------- páginas

@pytest.mark.parametrize("ruta", [
    "/", "/planes/", "/entrenadores/", "/miembros/", "/clases/", "/inscripciones/",
])
def test_paginas_cargan(client, ruta):
    assert client.get(ruta).status_code == 200


# ---------------------------------------------------------------- planes

def test_crear_plan(client):
    client.post("/planes/nuevo", data=DATOS)
    assert contar_plan() == 1


def test_editar_plan(client):
    client.post("/planes/nuevo", data=DATOS)
    fila = sql("SELECT id_plan FROM planes WHERE nombre_plan = %s", (NOMBRE,))
    assert fila is not None
    client.post(f"/planes/{fila[0]}/editar", data={**DATOS, "duracion_dias": "90"})

    dias = sql("SELECT duracion_dias FROM planes WHERE id_plan = %s", (fila[0],))
    assert dias is not None and dias[0] == 90


def test_eliminar_plan(client):
    client.post("/planes/nuevo", data=DATOS)
    fila = sql("SELECT id_plan FROM planes WHERE nombre_plan = %s", (NOMBRE,))
    assert fila is not None
    client.post(f"/planes/{fila[0]}/eliminar")
    assert contar_plan() == 0


def test_plan_con_precio_negativo_no_se_guarda(client):
    client.post("/planes/nuevo", data={**DATOS, "precio": "-5"})
    assert contar_plan() == 0
