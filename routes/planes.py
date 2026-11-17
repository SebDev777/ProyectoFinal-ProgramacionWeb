from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

import validators as v
from db import DatabaseError, error_message, execute, query

bp = Blueprint("planes", __name__, url_prefix="/planes")


def _leer_formulario(form):
    """Valida el formulario en el servidor. Devuelve (datos, errores)."""
    errores = []
    datos = {
        "nombre_plan": v.texto(form, "nombre_plan", "El nombre del plan", errores, max_len=60),
        "duracion_dias": v.entero(form, "duracion_dias", "La duración", errores, minimo=1),
        "precio": v.decimal(form, "precio", "El precio", errores, mayor_que=0),
        "descripcion": v.texto(form, "descripcion", "La descripción", errores,
                               obligatorio=False, max_len=200),
    }
    return datos, errores


@bp.route("/")
def listar():
    items = query("""
        SELECT p.*, COUNT(m.id_miembro) AS num_miembros
          FROM planes p
          LEFT JOIN miembros m ON m.id_plan = p.id_plan
         GROUP BY p.id_plan
         ORDER BY p.id_plan
    """)
    return render_template("planes/list.html", items=items)


@bp.route("/nuevo", methods=["GET", "POST"])
def crear():
    item = {}
    if request.method == "POST":
        item = request.form.to_dict()
        datos, errores = _leer_formulario(request.form)
        if not errores:
            try:
                execute("""INSERT INTO planes (nombre_plan, duracion_dias, precio, descripcion)
                           VALUES (%(nombre_plan)s, %(duracion_dias)s, %(precio)s, %(descripcion)s)""",
                        datos)
                flash("Plan creado correctamente.", "success")
                return redirect(url_for("planes.listar"))
            except DatabaseError as exc:
                errores.append(error_message(exc))
        for e in errores:
            flash(e, "danger")
    return render_template("planes/form.html", item=item, titulo="Nuevo plan")


@bp.route("/<int:id>/editar", methods=["GET", "POST"])
def editar(id):
    item = query("SELECT * FROM planes WHERE id_plan = %s", (id,), one=True)
    if item is None:
        abort(404)
    if request.method == "POST":
        item = {**item, **request.form.to_dict()}
        datos, errores = _leer_formulario(request.form)
        if not errores:
            try:
                execute("""UPDATE planes
                              SET nombre_plan = %(nombre_plan)s,
                                  duracion_dias = %(duracion_dias)s,
                                  precio = %(precio)s,
                                  descripcion = %(descripcion)s
                            WHERE id_plan = %(id)s""",
                        {**datos, "id": id})
                flash("Plan actualizado correctamente.", "success")
                return redirect(url_for("planes.listar"))
            except DatabaseError as exc:
                errores.append(error_message(exc))
        for e in errores:
            flash(e, "danger")
    return render_template("planes/form.html", item=item, titulo="Editar plan")


@bp.route("/<int:id>/eliminar", methods=["POST"])
def eliminar(id):
    try:
        if execute("DELETE FROM planes WHERE id_plan = %s", (id,)):
            flash("Plan eliminado.", "success")
        else:
            flash("El plan no existe.", "warning")
    except DatabaseError as exc:
        flash(error_message(exc), "danger")
    return redirect(url_for("planes.listar"))