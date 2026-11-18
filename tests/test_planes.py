from decimal import Decimal

from db import DatabaseError

FORM_VALIDO = {
    "nombre_plan": "Mensual",
    "duracion_dias": "30",
    "precio": "66000",
    "incluye_clases": "on",
    "descripcion": "Acceso total",
}


def _plan(**extra):
    base = {
        "id_plan": 1,
        "nombre_plan": "Mensual",
        "duracion_dias": 30,
        "precio": Decimal("66000.00"),
        "incluye_clases": True,
        "descripcion": "Acceso total",
        "num_miembros": 3,
    }
    return {**base, **extra}


# ---------- Listar ----------

def test_listar_muestra_planes(client, fake_db):
    fake_db.rows = [_plan(), _plan(id_plan=2, nombre_plan="Semana",
                                   precio=Decimal("30000.00"), incluye_clases=False)]
    resp = client.get("/planes/")
    html = resp.get_data(as_text=True)

    assert resp.status_code == 200
    assert "Mensual" in html and "Semana" in html
    assert "$66.000" in html          # precio con formato COP
    assert "Iron Paradise" in html    # marca en la plantilla base


def test_listar_vacio_muestra_mensaje(client, fake_db):
    fake_db.rows = []
    resp = client.get("/planes/")
    assert resp.status_code == 200
    assert "Todavía no hay planes" in resp.get_data(as_text=True)


# ---------- Crear ----------

def test_crear_get_muestra_formulario(client, fake_db):
    resp = client.get("/planes/nuevo")
    assert resp.status_code == 200
    assert 'name="nombre_plan"' in resp.get_data(as_text=True)


def test_crear_valido_inserta_y_redirige(client, fake_db):
    resp = client.post("/planes/nuevo", data=FORM_VALIDO)

    assert resp.status_code == 302
    assert resp.headers["Location"].endswith("/planes/")
    assert len(fake_db.executed) == 1
    _, params = fake_db.executed[0]
    assert params["nombre_plan"] == "Mensual"
    assert params["duracion_dias"] == 30
    assert params["precio"] == 66000
    assert params["incluye_clases"] is True


def test_crear_checkbox_desmarcado_guarda_false(client, fake_db):
    datos = {k: v for k, v in FORM_VALIDO.items() if k != "incluye_clases"}
    client.post("/planes/nuevo", data=datos)
    _, params = fake_db.executed[0]
    assert params["incluye_clases"] is False


def test_crear_invalido_no_inserta_y_muestra_errores(client, fake_db):
    datos = {**FORM_VALIDO, "nombre_plan": "", "duracion_dias": "0", "precio": "-5"}
    resp = client.post("/planes/nuevo", data=datos)

    assert resp.status_code == 200
    assert fake_db.executed == []
    assert "alert-danger" in resp.get_data(as_text=True)


def test_crear_conserva_lo_escrito_si_hay_error(client, fake_db):
    datos = {**FORM_VALIDO, "nombre_plan": "Trimestral", "precio": "0"}
    resp = client.post("/planes/nuevo", data=datos)
    assert 'value="Trimestral"' in resp.get_data(as_text=True)


def test_crear_error_de_base_de_datos_se_muestra(client, fake_db, monkeypatch):
    fake_db.execute_error = DatabaseError("falló")
    monkeypatch.setattr("routes.planes.error_message", lambda exc: "Error de prueba en BD")

    resp = client.post("/planes/nuevo", data=FORM_VALIDO)
    html = resp.get_data(as_text=True)

    assert resp.status_code == 200
    assert "Error de prueba en BD" in html


# ---------- Editar ----------

def test_editar_inexistente_devuelve_404(client, fake_db):
    fake_db.row = None
    assert client.get("/planes/999/editar").status_code == 404


def test_editar_get_precarga_datos(client, fake_db):
    fake_db.row = _plan()
    resp = client.get("/planes/1/editar")
    html = resp.get_data(as_text=True)

    assert resp.status_code == 200
    assert 'value="Mensual"' in html
    assert "checked" in html


def test_editar_valido_actualiza_con_id(client, fake_db):
    fake_db.row = _plan()
    resp = client.post("/planes/1/editar", data={**FORM_VALIDO, "nombre_plan": "Mensual Plus"})

    assert resp.status_code == 302
    _, params = fake_db.executed[0]
    assert params["id"] == 1
    assert params["nombre_plan"] == "Mensual Plus"


def test_editar_invalido_no_actualiza(client, fake_db):
    fake_db.row = _plan()
    resp = client.post("/planes/1/editar", data={**FORM_VALIDO, "precio": "abc"})

    assert resp.status_code == 200
    assert fake_db.executed == []


# ---------- Eliminar ----------

def test_eliminar_existente(client, fake_db):
    fake_db.execute_result = 1
    resp = client.post("/planes/1/eliminar", follow_redirects=True)
    assert resp.status_code == 200
    assert "Plan eliminado." in resp.get_data(as_text=True)


def test_eliminar_inexistente_avisa(client, fake_db):
    fake_db.execute_result = 0
    resp = client.post("/planes/99/eliminar", follow_redirects=True)
    assert "El plan no existe." in resp.get_data(as_text=True)


def test_eliminar_con_error_de_bd(client, fake_db, monkeypatch):
    fake_db.execute_error = DatabaseError("tiene miembros")
    monkeypatch.setattr("routes.planes.error_message",
                        lambda exc: "No se puede eliminar un plan con miembros.")
    resp = client.post("/planes/1/eliminar", follow_redirects=True)
    assert "No se puede eliminar un plan con miembros." in resp.get_data(as_text=True)


def test_eliminar_no_acepta_get(client, fake_db):
    assert client.get("/planes/1/eliminar").status_code == 405
