from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

import validators as v
from db import DatabaseError, error_message, execute, query

bp = Blueprint("entrenadores", __name__, url_prefix="/entrenadores")


def _leer_formulario(form):
    """Valida el formulario en el servidor. Devuelve (datos, errores)."""
    errores = []
    datos = {
        "nombre_entrenador": v.texto(form, "nombre_entrenador", "El nombre", errores, max_len=100),
        "especialidad": v.texto(form, "especialidad", "La especialidad", errores, max_len=60),
        "email": v.email(form, "email", "El correo", errores, obligatorio=True),
        "telefono": v.texto(form, "telefono", "El teléfono", errores,
                            obligatorio=False, max_len=15),
    }
    return datos, errores


@bp.route("/")
def listar():
    items = query("""
        SELECT e.*, COUNT(c.id_clase) AS num_clases
          FROM entrenadores e
          LEFT JOIN clases c ON c.id_entrenador = e.id_entrenador
         GROUP BY e.id_entrenador
         ORDER BY e.id_entrenador
    """)
    return render_template("entrenadores/list.html", items=items)


@bp.route("/nuevo", methods=["GET", "POST"])
def crear():
    item = {}
    if request.method == "POST":
        item = request.form.to_dict()
        datos, errores = _leer_formulario(request.form)
        if not errores:
            try:
                execute("""INSERT INTO entrenadores
                               (nombre_entrenador, especialidad, email, telefono)
                           VALUES (%(nombre_entrenador)s, %(especialidad)s,
                                   %(email)s, %(telefono)s)""",
                        datos)
                flash("Entrenador creado correctamente.", "success")
                return redirect(url_for("entrenadores.listar"))
            except DatabaseError as exc:
                errores.append(error_message(exc))
        for e in errores:
            flash(e, "danger")
    return render_template("entrenadores/form.html", item=item, titulo="Nuevo entrenador")


@bp.route("/<int:id>/editar", methods=["GET", "POST"])
def editar(id):
    item = query("SELECT * FROM entrenadores WHERE id_entrenador = %s", (id,), one=True)
    if item is None:
        abort(404)
    if request.method == "POST":
        item = {**item, **request.form.to_dict()}
        datos, errores = _leer_formulario(request.form)
        if not errores:
            try:
                execute("""UPDATE entrenadores
                              SET nombre_entrenador = %(nombre_entrenador)s,
                                  especialidad = %(especialidad)s,
                                  email = %(email)s,
                                  telefono = %(telefono)s
                            WHERE id_entrenador = %(id)s""",
                        {**datos, "id": id})
                flash("Entrenador actualizado correctamente.", "success")
                return redirect(url_for("entrenadores.listar"))
            except DatabaseError as exc:
                errores.append(error_message(exc))
        for e in errores:
            flash(e, "danger")
    return render_template("entrenadores/form.html", item=item, titulo="Editar entrenador")


@bp.route("/<int:id>/eliminar", methods=["POST"])
def eliminar(id):
    try:
        if execute("DELETE FROM entrenadores WHERE id_entrenador = %s", (id,)):
            flash("Entrenador eliminado.", "success")
        else:
            flash("El entrenador no existe.", "warning")
    except DatabaseError as exc:
        flash(error_message(exc), "danger")
    return redirect(url_for("entrenadores.listar"))