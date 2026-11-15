"""Conexión a PostgreSQL y funciones para ejecutar consultas."""
import psycopg2
import psycopg2.extras
from flask import current_app

DatabaseError = psycopg2.Error


def conectar():
    cfg = current_app.config
    return psycopg2.connect(
        host=cfg["DB_HOST"],
        port=cfg["DB_PORT"],
        dbname=cfg["DB_NAME"],
        user=cfg["DB_USER"],
        password=cfg["DB_PASSWORD"],
    )


def query(sql, params=None, one=False):
    """SELECT: devuelve una lista de diccionarios (o uno solo si one=True)."""
    conn = conectar()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(sql, params)
            filas = cur.fetchall()
    finally:
        conn.close()
    if one:
        return filas[0] if filas else None
    return filas



def execute(sql, params=None):
    """INSERT, UPDATE o DELETE: guarda los cambios y devuelve las filas afectadas."""
    conn = conectar()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            afectadas = cur.rowcount
        conn.commit()
        return afectadas
    except psycopg2.Error:
        conn.rollback()  # si algo falla, se deshace todo
        raise
    finally:
        conn.close()


def error_message(exc):
    """Convierte el error de PostgreSQL en un mensaje claro para el usuario."""
    codigo = getattr(exc, "pgcode", None)
    if codigo in ("23503", "23001"):
        return ("No se puede eliminar o modificar: el registro tiene datos "
                "relacionados (miembros, clases o inscripciones).")
    if codigo == "23505":
        return "Ya existe un registro con ese valor. No se permiten duplicados."
    if codigo == "23514":
        return "Un valor no cumple las reglas de la base de datos."
    if codigo == "23502":
        return "Falta un campo obligatorio."
    return "Ocurrió un error en la base de datos."