# Plan de pruebas: Iron Paradise (módulo Planes)

**Integrantes:** John Sebastian Meza y Jose Daniel Cerquera

## 1. Alcance

Se prueba el CRUD de planes (crear, listar, editar, eliminar) y la validación de sus datos. Aplicación en Flask con PostgreSQL.

## 2. Estrategia y entorno

- **Pruebas automatizadas** con `pytest` contra la base real. Cada prueba crea registros con el prefijo `ZZ_TEST_` y se borran al terminar.
- **Entorno:** Python _[versión]_, Flask _[versión]_, PostgreSQL _[versión]_.
- **Ejecución:** `python -m pytest -v` (archivo `tests/test_crud.py`).

## 3. Casos de prueba

| ID | Caso | Entrada | Resultado esperado | Estado |
|---|---|---|---|---|
| CP-01 | Páginas principales cargan | `GET /`, `/planes/`, `/planes/nuevo` | Código 200 | Pendiente |
| CP-02 | Plan inexistente | `GET /planes/999999/editar` | Código 404 | Pendiente |
| CP-03 | Crear plan válido | Nombre, 30 días, precio 66000 | "Plan creado correctamente"; +1 registro | Pendiente |
| CP-04 | Editar plan | 90 días, precio 150000 | "Plan actualizado correctamente"; datos nuevos en la base | Pendiente |
| CP-05 | Eliminar plan | `POST /planes/{id}/eliminar` | "Plan eliminado"; -1 registro | Pendiente |
| CP-06 | Eliminar plan inexistente | `POST /planes/999999/eliminar` | "El plan no existe" | Pendiente |
| CP-07 | Datos inválidos | Nombre vacío, duración 0, precio negativo o no numérico | Se muestra el formulario; no se guarda nada | Pendiente |

## 4. Evidencias

Capturas en `docs/evidencias/`:

- `pytest_resultado.png`: terminal con `pytest -v`.
- `cobertura.png`: `pytest --cov=. --cov-report=term-missing`.
- `formulario_error.png`: formulario con datos inválidos.

## 5. Resultados y conclusiones
En evidencias/
