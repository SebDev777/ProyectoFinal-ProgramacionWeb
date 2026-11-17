from datetime import date

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

import validators as v
from db import DatabaseError, error_message, execute, query

bp = Blueprint("miembros", __name__, url_prefix="/miembros")


def _planes():
    """Opciones de la lista desplegable de planes."""
    return query("SELECT id_plan, nombre_plan FROM planes ORDER BY nombre_plan")


def _leer_formulario(form, id_miembro=None):
    """Valida el formulario en el servidor. Devuelve (datos, errores)."""
    errores = []
    datos = {
        "nombre_miembro": v.texto(form, "nombre_miembro", "El nombre", errores, max_len=100),
        "documento": v.texto(form, "documento", "El documento", errores, max_len=15),
        "email": v.email(form, "email", "El correo", errores),
        "telefono": v.texto(form, "telefono", "El teléfono", errores,
                            obligatorio=False, max_len=15),
        "fecha_nacimiento": v.fecha(form, "fecha_nacimiento", "La fecha de nacimiento", errores),
        "id_plan": v.entero(form, "id_plan", "El plan", errores, minimo=1),
        "fecha_inicio_plan": v.fecha(form, "fecha_inicio_plan", "La fecha de inicio del plan", errores),
    }

    if datos["documento"] and not datos["documento"].isdigit():
        errores.append("El documento solo debe tener números.")

    if datos["fecha_nacimiento"] and datos["fecha_nacimiento"] >= date.today():
        errores.append("La fecha de nacimiento debe ser anterior a hoy.")

    # Regla de negocio: no pasar a un plan sin clases si ya tiene inscripciones activas
    if id_miembro and datos["id_plan"]:
        plan = query("SELECT nombre_plan, incluye_clases FROM planes WHERE id_plan = %s",
                     (datos["id_plan"],), one=True)
        activas = query("""SELECT COUNT(*) AS n FROM inscripciones
                            WHERE id_miembro = %s AND estado = 'Activa'""",
                        (id_miembro,), one=True)["n"]
        if plan and not plan["incluye_clases"] and activas > 0:
            errores.append(f"No se puede cambiar al plan «{plan['nombre_plan']}»: no incluye "
                           f"clases y el miembro tiene {activas} inscripción(es) activa(s).")
    return datos, errores


@bp.route("/")
def listar():
    items = query("""
        SELECT m.*, p.nombre_plan, p.incluye_clases,
               m.fecha_inicio_plan + p.duracion_dias AS fecha_vencimiento,
               (SELECT COUNT(*) FROM inscripciones i
                 WHERE i.id_miembro = m.id_miembro) AS num_inscripciones
          FROM miembros m
          JOIN planes p ON p.id_plan = m.id_plan
         ORDER BY m.id_miembro
    """)
    return render_template("miembros/list.html", items=items)


@bp.route("/nuevo", methods=["GET", "POST"])
def crear():
    item = {}
    if request.method == "POST":
        item = request.form.to_dict()
        datos, errores = _leer_formulario(request.form)
        if not errores:
            try:
                execute("""INSERT INTO miembros
                               (nombre_miembro, documento, email, telefono,
                                fecha_nacimiento, id_plan, fecha_inicio_plan)
                           VALUES (%(nombre_miembro)s, %(documento)s, %(email)s, %(telefono)s,
                                   %(fecha_nacimiento)s, %(id_plan)s, %(fecha_inicio_plan)s)""",
                        datos)
                flash("Miembro creado correctamente.", "success")
                return redirect(url_for("miembros.listar"))
            except DatabaseError as exc:
                errores.append(error_message(exc))
        for e in errores:
            flash(e, "danger")
    return render_template("miembros/form.html", item=item, planes=_planes(),
                           titulo="Nuevo miembro")


@bp.route("/<int:id>/editar", methods=["GET", "POST"])
def editar(id):
    item = query("SELECT * FROM miembros WHERE id_miembro = %s", (id,), one=True)
    if item is None:
        abort(404)
    if request.method == "POST":
        item = {**item, **request.form.to_dict()}
        datos, errores = _leer_formulario(request.form, id_miembro=id)
        if not errores:
            try:
                execute("""UPDATE miembros
                              SET nombre_miembro = %(nombre_miembro)s,
                                  documento = %(documento)s,
                                  email = %(email)s,
                                  telefono = %(telefono)s,
                                  fecha_nacimiento = %(fecha_nacimiento)s,
                                  id_plan = %(id_plan)s,
                                  fecha_inicio_plan = %(fecha_inicio_plan)s
                            WHERE id_miembro = %(id)s""",
                        {**datos, "id": id})
                flash("Miembro actualizado correctamente.", "success")
                return redirect(url_for("miembros.listar"))
            except DatabaseError as exc:
                errores.append(error_message(exc))
        for e in errores:
            flash(e, "danger")
    return render_template("miembros/form.html", item=item, planes=_planes(),
                           titulo="Editar miembro")


@bp.route("/<int:id>/eliminar", methods=["POST"])
def eliminar(id):
    try:
        if execute("DELETE FROM miembros WHERE id_miembro = %s", (id,)):
            flash("Miembro eliminado.", "success")
        else:
            flash("El miembro no existe.", "warning")
    except DatabaseError as exc:
        flash(error_message(exc), "danger")
    return redirect(url_for("miembros.listar"))