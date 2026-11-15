"""Validaciones de los formularios. Cada función agrega un mensaje a 'errores' si algo está mal."""
from datetime import date
from decimal import Decimal, InvalidOperation


def _leer(form, campo):
    return (form.get(campo) or "").strip()


def texto(form, campo, etiqueta, errores, obligatorio=True, max_len=None):
    valor = _leer(form, campo)
    if not valor:
        if obligatorio:
            errores.append(f"{etiqueta} es obligatorio.")
        return None
    if max_len and len(valor) > max_len:
        errores.append(f"{etiqueta} no puede pasar de {max_len} caracteres.")
    return valor


def entero(form, campo, etiqueta, errores, minimo=None):
    valor = _leer(form, campo)
    if not valor:
        errores.append(f"{etiqueta} es obligatorio.")
        return None
    if not valor.lstrip("-").isdigit():
        errores.append(f"{etiqueta} debe ser un número entero.")
        return None
    numero = int(valor)
    if minimo is not None and numero < minimo:
        errores.append(f"{etiqueta} debe ser al menos {minimo}.")
    return numero


def decimal(form, campo, etiqueta, errores, mayor_que=None):
    valor = _leer(form, campo).replace(",", ".")
    if not valor:
        errores.append(f"{etiqueta} es obligatorio.")
        return None
    try:
        numero = Decimal(valor)
    except InvalidOperation:
        errores.append(f"{etiqueta} debe ser un número.")
        return None
    if mayor_que is not None and numero <= mayor_que:
        errores.append(f"{etiqueta} debe ser mayor que {mayor_que}.")
    return numero


def fecha(form, campo, etiqueta, errores):
    valor = _leer(form, campo)
    if not valor:
        errores.append(f"{etiqueta} es obligatoria.")
        return None
    try:
        return date.fromisoformat(valor)
    except ValueError:
        errores.append(f"{etiqueta} no es una fecha válida.")
        return None


def email(form, campo, etiqueta, errores, obligatorio=False):
    valor = _leer(form, campo)
    if not valor:
        if obligatorio:
            errores.append(f"{etiqueta} es obligatorio.")
        return None
    if "@" not in valor or "." not in valor.split("@")[-1]:
        errores.append(f"{etiqueta} no tiene un formato válido.")
    return valor