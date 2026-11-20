"""Fixtures compartidas.

Ajusta la línea `from app import app` si tu app.py usa una función
fábrica (por ejemplo `create_app()`).
"""
import pytest

from app import app as flask_app


@pytest.fixture
def app():
    flask_app.config.update(TESTING=True)
    if not flask_app.config.get("SECRET_KEY"):
        flask_app.config["SECRET_KEY"] = "clave-solo-para-pruebas"
    return flask_app


@pytest.fixture
def client(app):
    return app.test_client()


class FakeDB:
    """Reemplaza query() y execute() de routes.planes sin tocar PostgreSQL."""

    def __init__(self):
        self.rows = []            # lo que devuelve query() cuando one=False
        self.row = None           # lo que devuelve query() cuando one=True
        self.execute_result = 1   # filas afectadas que devuelve execute()
        self.execute_error = None # excepción a lanzar en execute()
        self.executed = []        # (sql, params) de cada execute()

    def query(self, sql, params=None, one=False):
        return self.row if one else self.rows

    def execute(self, sql, params=None):
        if self.execute_error:
            raise self.execute_error
        self.executed.append((sql, params))
        return self.execute_result


@pytest.fixture
def fake_db(monkeypatch):
    db = FakeDB()
    monkeypatch.setattr("routes.planes.query", db.query)
    monkeypatch.setattr("routes.planes.execute", db.execute)
    return db
