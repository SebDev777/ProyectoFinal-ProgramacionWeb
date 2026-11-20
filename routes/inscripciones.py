from datetime import date

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

import validators as v
from db import DatabaseError, error_message, execute, query

bp = Blueprint("inscripciones", __name__, url_prefix="/inscripciones")

ESTADOS = ["Activa", "Cancelada"]


def _miembros():
    """Opciones de la lista desplegable de miembros (con su plan)."""
    return query("""
        SELECT m.id_miembro, m.nombre_miembro, m.documento, p.nombre_plan, p.incluye_clases
          FROM miembros m
          JOIN planes p ON p.id_plan = m.id_plan
         ORDER BY m.nombre_miembro
    """)


def _clases():
    """Opciones de la lista desplegable de clases."""
    return query("""SELECT id_clase, nombre_clase, dia_semana, hora_inicio
                      FROM clases ORDER BY nombre_clase""")


def _leer_formulario(form, id_inscripcion=None):
    """Valida el formulario en el servidor. Devuelve (datos, errores)."""
    errores = []
    datos = {
        "id_miembro": v.entero(form, "id_miembro", "El miembro", errores, minimo=1),
        "id_clase": v.entero(form, "id_clase", "La clase", errores, minimo=1),
        "fecha_inscripcion": v.fecha(form, "fecha_inscripcion", "La fecha de inscripción", errores),
        "estado": v.texto(form, "estado", "El estado", errores),
    }
    if datos["estado"] and datos["estado"] not in ESTADOS:
        errores.append("El estado seleccionado no es válido.")

    # Las reglas de negocio solo se revisan si los datos básicos son válidos
    if errores:
        return datos, errores

    id_ins = id_inscripcion or 0

    # Regla 1: el miembro no puede inscribirse dos veces en la misma clase
    repetida = query("""SELECT 1 FROM inscripciones
                         WHERE id_miembro = %s AND id_clase = %s AND id_inscripcion <> %s""",
                     (datos["id_miembro"], datos["id_clase"], id_ins), one=True)
    if repetida:
        errores.append("El miembro ya está inscrito en esa clase.")

    if datos["estado"] == "Activa":
        # Regla 2: el plan del miembro debe incluir clases
        plan = query("""SELECT p.nombre_plan, p.incluye_clases
                          FROM miembros m
                          JOIN planes p ON p.id_plan = m.id_plan
                         WHERE m.id_miembro = %s""",
                     (datos["id_miembro"],), one=True)
        if plan is None:
            errores.append("El miembro seleccionado no existe.")
        elif not plan["incluye_clases"]:
            errores.append(f"El plan «{plan['nombre_plan']}» de este miembro no incluye clases.")

        # Regla 3: la clase debe tener cupo disponible
        clase = query("""
            SELECT nombre_clase, cupo_maximo,
                   (SELECT COUNT(*) FROM inscripciones
                     WHERE id_clase = %s AND estado = 'Activa'
                       AND id_inscripcion <> %s) AS ocupados
              FROM clases WHERE id_clase = %s
        """, (datos["id_clase"], id_ins, datos["id_clase"]), one=True)
        if clase is None:
            errores.append("La clase seleccionada no existe.")
        elif clase["ocupados"] >= clase["cupo_maximo"]:
            errores.append(f"La clase «{clase['nombre_clase']}» ya está llena "
                           f"({clase['ocupados']} de {clase['cupo_maximo']} cupos).")
    return datos, errores


@bp.route("/")
def listar():
    items = query("""
        SELECT i.*, m.nombre_miembro, c.nombre_clase, c.dia_semana, c.hora_inicio
          FROM inscripciones i
          JOIN miembros m ON m.id_miembro = i.id_miembro
          JOIN clases c ON c.id_clase = i.id_clase
         ORDER BY i.id_inscripcion
    """)
    return render_template("inscripciones/list.html", items=items)


@bp.route("/nuevo", methods=["GET", "POST"])
def crear():
    item = {}
    if request.method == "POST":
        item = request.form.to_dict()
        datos, errores = _leer_formulario(request.form)
        if not errores:
            try:
                execute("""INSERT INTO inscripciones
                               (id_miembro, id_clase, fecha_inscripcion, estado)
                           VALUES (%(id_miembro)s, %(id_clase)s, %(fecha_inscripcion)s, %(estado)s)""",
                        datos)
                flash("Inscripción creada correctamente.", "success")
                return redirect(url_for("inscripciones.listar"))
            except DatabaseError as exc:
                errores.append(error_message(exc))
        for e in errores:
            flash(e, "danger")
    return render_template("inscripciones/form.html", item=item, miembros=_miembros(),
                           clases=_clases(), estados=ESTADOS, hoy=date.today().isoformat(),
                           titulo="Nueva inscripción")


@bp.route("/<int:id>/editar", methods=["GET", "POST"])
def editar(id):
    item = query("SELECT * FROM inscripciones WHERE id_inscripcion = %s", (id,), one=True)
    if item is None:
        abort(404)
    if request.method == "POST":
        item = {**item, **request.form.to_dict()}
        datos, errores = _leer_formulario(request.form, id_inscripcion=id)
        if not errores:
            try:
                execute("""UPDATE inscripciones
                              SET id_miembro = %(id_miembro)s,
                                  id_clase = %(id_clase)s,
                                  fecha_inscripcion = %(fecha_inscripcion)s,
                                  estado = %(estado)s
                            WHERE id_inscripcion = %(id)s""",
                        {**datos, "id": id})
                flash("Inscripción actualizada correctamente.", "success")
                return redirect(url_for("inscripciones.listar"))
            except DatabaseError as exc:
                errores.append(error_message(exc))
        for e in errores:
            flash(e, "danger")
    return render_template("inscripciones/form.html", item=item, miembros=_miembros(),
                           clases=_clases(), estados=ESTADOS, hoy=date.today().isoformat(),
                           titulo="Editar inscripción")


@bp.route("/<int:id>/eliminar", methods=["POST"])
def eliminar(id):
    try:
        if execute("DELETE FROM inscripciones WHERE id_inscripcion = %s", (id,)):
            flash("Inscripción eliminada.", "success")
        else:
            flash("La inscripción no existe.", "warning")
    except DatabaseError as exc:
        flash(error_message(exc), "danger")
    return redirect(url_for("inscripciones.listar"))