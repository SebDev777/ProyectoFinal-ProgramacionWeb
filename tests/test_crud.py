"""Pruebas del CRUD de planes contra la base de datos real.

Cada prueba crea registros con el prefijo ZZ_TEST_ y al final se borran.
Ejecutar con:  python -m pytest -v
"""
import psycopg2
import pytest

from app import create_app
from config import Config

PREFIJO = "ZZ_TEST_"

DATOS = {
    "nombre_plan": PREFIJO + "Plan",
    "duracion_dias": "30",
    "precio": "66000",
    "incluye_clases": "on",
    "descripcion": "plan de prueba",
}


@pytest.fixture()
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def conectar():
    return psycopg2.connect(host=Config.DB_HOST, port=Config.DB_PORT, dbname=Config.DB_NAME,
                            user=Config.DB_USER, password=Config.DB_PASSWORD)


def ejecutar(consulta, params=()):
    """Ejecuta INSERT/UPDATE/DELETE directo en PostgreSQL (no devuelve nada)."""
    conn = conectar()
    with conn, conn.cursor() as cur:
        cur.execute(consulta, params)
    conn.close()


def consultar(consulta, params=()):
    """Ejecuta un SELECT y devuelve la primera fila (siempre una tupla)."""
    conn = conectar()
    with conn, conn.cursor() as cur:
        cur.execute(consulta, params)
        fila = cur.fetchone()
    conn.close()
    assert fila is not None, "La consulta no devolvió ninguna fila"
    return fila


@pytest.fixture(autouse=True)
def limpiar():
    """Después de cada prueba, borra los planes que ella haya creado."""
    yield
    ejecutar("DELETE FROM planes WHERE nombre_plan LIKE %s", (PREFIJO + "%",))


def contar():
    return consultar("SELECT COUNT(*) FROM planes")[0]


# ---------------------------------------------------------------- páginas

@pytest.mark.parametrize("ruta", ["/", "/planes/", "/planes/nuevo"])
def test_paginas_cargan(client, ruta):
    assert client.get(ruta).status_code == 200


def test_plan_inexistente_da_404(client):
    assert client.get("/planes/999999/editar").status_code == 404


# ---------------------------------------------------------------- CRUD

def test_crear_plan(client):
    antes = contar()
    r = client.post("/planes/nuevo", data=DATOS, follow_redirects=True)

    assert "Plan creado correctamente" in r.get_data(as_text=True)
    assert contar() == antes + 1


def test_editar_plan(client):
    client.post("/planes/nuevo", data=DATOS)
    id_ = consultar("SELECT id_plan FROM planes WHERE nombre_plan = %s", (DATOS["nombre_plan"],))[0]

    r = client.post(f"/planes/{id_}/editar",
                    data={**DATOS, "duracion_dias": "90", "precio": "150000"},
                    follow_redirects=True)

    assert "Plan actualizado correctamente" in r.get_data(as_text=True)
    dias, precio = consultar("SELECT duracion_dias, precio FROM planes WHERE id_plan = %s", (id_,))
    assert dias == 90
    assert float(precio) == 150000


def test_eliminar_plan(client):
    client.post("/planes/nuevo", data=DATOS)
    id_ = consultar("SELECT id_plan FROM planes WHERE nombre_plan = %s", (DATOS["nombre_plan"],))[0]
    antes = contar()

    r = client.post(f"/planes/{id_}/eliminar", follow_redirects=True)

    assert "Plan eliminado" in r.get_data(as_text=True)
    assert contar() == antes - 1


def test_eliminar_plan_inexistente(client):
    r = client.post("/planes/999999/eliminar", follow_redirects=True)
    assert "El plan no existe" in r.get_data(as_text=True)


# ---------------------------------------------------------------- validaciones

@pytest.mark.parametrize("cambio", [
    {"nombre_plan": ""},        # el nombre es obligatorio
    {"duracion_dias": "0"},     # mínimo 1 día
    {"precio": "-5"},           # el precio debe ser mayor que 0
    {"precio": "mucho"},        # el precio debe ser un número
])
def test_datos_invalidos_no_se_guardan(client, cambio):
    antes = contar()
    r = client.post("/planes/nuevo", data={**DATOS, **cambio})

    assert r.status_code == 200      # vuelve a mostrar el formulario
    assert contar() == antes         # y no se insertó nada
