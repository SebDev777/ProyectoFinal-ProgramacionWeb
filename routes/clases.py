from datetime import datetime

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

import validators as v
from db import DatabaseError, error_message, execute, query

bp = Blueprint("clases", __name__, url_prefix="/clases")

DIAS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]


def _entrenadores():
    """Opciones de la lista desplegable de entrenadores."""
    return query("""SELECT id_entrenador, nombre_entrenador, especialidad
                      FROM entrenadores ORDER BY nombre_entrenador""")


def _hora(form, campo, etiqueta, errores):
    """Lee una hora (HH:MM) del formulario. Devuelve un objeto time o None."""
    valor = (form.get(campo) or "").strip()
    if not valor:
        errores.append(f"{etiqueta} es obligatoria.")
        return None
    for formato in ("%H:%M", "%H:%M:%S"):
        try:
            return datetime.strptime(valor, formato).time()
        except ValueError:
            pass
    errores.append(f"{etiqueta} no es una hora válida.")
    return None


def _leer_formulario(form, id_clase=None):
    """Valida el formulario en el servidor. Devuelve (datos, errores)."""
    errores = []
    datos = {
        "nombre_clase": v.texto(form, "nombre_clase", "El nombre de la clase", errores, max_len=80),
        "id_entrenador": v.entero(form, "id_entrenador", "El entrenador", errores, minimo=1),
        "dia_semana": v.texto(form, "dia_semana", "El día", errores),
        "hora_inicio": _hora(form, "hora_inicio", "La hora de inicio", errores),
        "duracion_min": v.entero(form, "duracion_min", "La duración", errores, minimo=1),
        "cupo_maximo": v.entero(form, "cupo_maximo", "El cupo máximo", errores, minimo=1),
    }

    if datos["dia_semana"] and datos["dia_semana"] not in DIAS:
        errores.append("El día seleccionado no es válido.")

    # Regla 1: un entrenador no puede dictar dos clases que se crucen el mismo día
    if (not errores and datos["id_entrenador"] and datos["dia_semana"]
            and datos["hora_inicio"] and datos["duracion_min"]):
        cruce = query("""
            SELECT nombre_clase, hora_inicio
              FROM clases
             WHERE id_entrenador = %(ent)s
               AND dia_semana = %(dia)s
               AND id_clase <> %(id)s
               AND hora_inicio < %(inicio)s::time + make_interval(mins => %(dur)s)
               AND %(inicio)s::time < hora_inicio + make_interval(mins => duracion_min)
        """, {"ent": datos["id_entrenador"], "dia": datos["dia_semana"], "id": id_clase or 0,
              "inicio": datos["hora_inicio"], "dur": datos["duracion_min"]}, one=True)
        if cruce:
            errores.append(f"El entrenador ya dicta «{cruce['nombre_clase']}» a las "
                           f"{cruce['hora_inicio'].strftime('%H:%M')} ese día y se cruza con este horario.")

    # Regla 2: al editar, el cupo no puede ser menor que los inscritos activos
    if id_clase and datos["cupo_maximo"]:
        activos = query("""SELECT COUNT(*) AS n FROM inscripciones
                            WHERE id_clase = %s AND estado = 'Activa'""",
                        (id_clase,), one=True)["n"]
        if datos["cupo_maximo"] < activos:
            errores.append(f"El cupo no puede ser menor que los inscritos activos ({activos}).")
    return datos, errores


@bp.route("/")
def listar():
    items = query("""
        SELECT c.*, e.nombre_entrenador,
               (SELECT COUNT(*) FROM inscripciones i
                 WHERE i.id_clase = c.id_clase AND i.estado = 'Activa') AS inscritos
          FROM clases c
          JOIN entrenadores e ON e.id_entrenador = c.id_entrenador
         ORDER BY c.id_clase
    """)
    return render_template("clases/list.html", items=items)


@bp.route("/nuevo", methods=["GET", "POST"])
def crear():
    item = {}
    if request.method == "POST":
        item = request.form.to_dict()
        datos, errores = _leer_formulario(request.form)
        if not errores:
            try:
                execute("""INSERT INTO clases
                               (nombre_clase, id_entrenador, dia_semana,
                                hora_inicio, duracion_min, cupo_maximo)
                           VALUES (%(nombre_clase)s, %(id_entrenador)s, %(dia_semana)s,
                                   %(hora_inicio)s, %(duracion_min)s, %(cupo_maximo)s)""",
                        datos)
                flash("Clase creada correctamente.", "success")
                return redirect(url_for("clases.listar"))
            except DatabaseError as exc:
                errores.append(error_message(exc))
        for e in errores:
            flash(e, "danger")
    return render_template("clases/form.html", item=item, entrenadores=_entrenadores(),
                           dias=DIAS, titulo="Nueva clase")


@bp.route("/<int:id>/editar", methods=["GET", "POST"])
def editar(id):
    item = query("SELECT * FROM clases WHERE id_clase = %s", (id,), one=True)
    if item is None:
        abort(404)
    if request.method == "POST":
        item = {**item, **request.form.to_dict()}
        datos, errores = _leer_formulario(request.form, id_clase=id)
        if not errores:
            try:
                execute("""UPDATE clases
                              SET nombre_clase = %(nombre_clase)s,
                                  id_entrenador = %(id_entrenador)s,
                                  dia_semana = %(dia_semana)s,
                                  hora_inicio = %(hora_inicio)s,
                                  duracion_min = %(duracion_min)s,
                                  cupo_maximo = %(cupo_maximo)s
                            WHERE id_clase = %(id)s""",
                        {**datos, "id": id})
                flash("Clase actualizada correctamente.", "success")
                return redirect(url_for("clases.listar"))
            except DatabaseError as exc:
                errores.append(error_message(exc))
        for e in errores:
            flash(e, "danger")
    return render_template("clases/form.html", item=item, entrenadores=_entrenadores(),
                           dias=DIAS, titulo="Editar clase")


@bp.route("/<int:id>/eliminar", methods=["POST"])
def eliminar(id):
    try:
        if execute("DELETE FROM clases WHERE id_clase = %s", (id,)):
            flash("Clase eliminada.", "success")
        else:
            flash("La clase no existe.", "warning")
    except DatabaseError as exc:
        flash(error_message(exc), "danger")
    return redirect(url_for("clases.listar"))