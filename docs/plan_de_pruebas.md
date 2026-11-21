# Plan de pruebas funcionales: Iron Paradise Gym

**Integrantes:** Jose Daniel Cerquera Ramírez, John Sebastián Meza Saldaña
**Base de datos:** `gimnasio_db` (PostgreSQL)  **Fecha:** _[dd/mm/aaaa]_

## 1. Alcance

Se prueban las 5 tablas del sistema (`planes`, `entrenadores`, `miembros`, `clases`, `inscripciones`). Por cada tabla se registran 4 casos que cubren: **crear y listar, editar, ingreso de datos inválidos, y eliminar** (incluido el intento de eliminar un registro relacionado). Total: **20 casos**, por encima del mínimo de 15.

## 2. Entorno

Python _[versión]_ · Flask _[versión]_ · PostgreSQL _[versión]_ · Navegador _[nombre y versión]_

## 3. Cómo se registra cada caso

Cada caso se ejecuta a mano en el navegador. Se anota el **resultado obtenido** y se guarda una **captura** en `docs/evidencias/` con el ID del caso como nombre (por ejemplo `PL-01.png`). Si un caso necesita dos capturas, se usa el sufijo `a` y `b` (`PL-04a.png`, `PL-04b.png`).

Estado: **OK** si el resultado obtenido coincide con el esperado, **FALLA** si no coincide.

## 4. Casos de prueba

### 4.1 Tabla `planes`

| ID | Tipo | Pasos y datos | Resultado esperado | Resultado obtenido | Evidencia | Estado |
|---|---|---|---|---|---|---|
| PL-01 | Crear y listar | Ir a Planes > Nuevo plan. Nombre "Plan Prueba", 30 días, precio 66000, incluye clases. Guardar | Aviso "Plan creado correctamente"; el plan aparece en el listado | _[ ]_ | `evidencias/PL-01.png` | _[ ]_ |
| PL-02 | Editar | Editar "Plan Prueba": duración 90 días, precio 150000. Guardar | Aviso "Plan actualizado correctamente"; el listado muestra los datos nuevos | _[ ]_ | `evidencias/PL-02.png` | _[ ]_ |
| PL-03 | Datos inválidos | Nuevo plan con nombre vacío; repetir con duración 0 y con precio -5 | Se muestra un error y no se guarda el plan | _[ ]_ | `evidencias/PL-03.png` | _[ ]_ |
| PL-04 | Eliminar | (a) Eliminar "Plan Prueba", que no tiene miembros. (b) Intentar eliminar un plan que sí tiene miembros | (a) "Plan eliminado". (b) Se rechaza con mensaje de registro relacionado y el plan sigue en el listado | _[ ]_ | `evidencias/PL-04a.png`, `PL-04b.png` | _[ ]_ |

### 4.2 Tabla `entrenadores`

| ID | Tipo | Pasos y datos | Resultado esperado | Resultado obtenido | Evidencia | Estado |
|---|---|---|---|---|---|---|
| EN-01 | Crear y listar | Nuevo entrenador: "Entrenador Prueba", especialidad "Yoga", correo `prueba@ejemplo.co` | Aviso de creación; aparece en el listado | _[ ]_ | `evidencias/EN-01.png` | _[ ]_ |
| EN-02 | Editar | Cambiar la especialidad a "Spinning". Guardar | Aviso de actualización; el listado muestra "Spinning" | _[ ]_ | `evidencias/EN-02.png` | _[ ]_ |
| EN-03 | Datos inválidos | Nuevo entrenador sin nombre; repetir sin especialidad y con un correo que ya existe | Se muestra un error y no se guarda | _[ ]_ | `evidencias/EN-03.png` | _[ ]_ |
| EN-04 | Eliminar | (a) Eliminar "Entrenador Prueba", sin clases. (b) Intentar eliminar un entrenador que dicta clases | (a) Se elimina. (b) Se rechaza por registro relacionado | _[ ]_ | `evidencias/EN-04a.png`, `EN-04b.png` | _[ ]_ |

### 4.3 Tabla `miembros`

| ID | Tipo | Pasos y datos | Resultado esperado | Resultado obtenido | Evidencia | Estado |
|---|---|---|---|---|---|---|
| MI-01 | Crear y listar | Nuevo miembro con documento numérico, correo, fecha de nacimiento pasada, un plan y fecha de inicio | Aviso de creación; aparece en el listado con su plan | _[ ]_ | `evidencias/MI-01.png` | _[ ]_ |
| MI-02 | Editar | Cambiar el teléfono del miembro. Guardar | Aviso de actualización; el dato nuevo se ve en el listado | _[ ]_ | `evidencias/MI-02.png` | _[ ]_ |
| MI-03 | Datos inválidos | Documento "abc"; repetir con fecha de nacimiento futura y con un documento ya registrado | Se muestra un error en cada caso y no se guarda | _[ ]_ | `evidencias/MI-03.png` | _[ ]_ |
| MI-04 | Eliminar | (a) Eliminar un miembro sin inscripciones. (b) Intentar eliminar un miembro con inscripciones | (a) Se elimina. (b) Se rechaza por registro relacionado | _[ ]_ | `evidencias/MI-04a.png`, `MI-04b.png` | _[ ]_ |

### 4.4 Tabla `clases`

| ID | Tipo | Pasos y datos | Resultado esperado | Resultado obtenido | Evidencia | Estado |
|---|---|---|---|---|---|---|
| CL-01 | Crear y listar | Nueva clase: "Clase Prueba", un entrenador, Lunes 18:00, 60 min, cupo 20 | Aviso de creación; aparece en el listado | _[ ]_ | `evidencias/CL-01.png` | _[ ]_ |
| CL-02 | Editar | Cambiar el cupo máximo a 30. Guardar | Aviso de actualización; el listado muestra cupo 30 | _[ ]_ | `evidencias/CL-02.png` | _[ ]_ |
| CL-03 | Datos inválidos | Cupo 0; repetir con duración 0 y con un horario que se cruza con otra clase del mismo entrenador | Se muestra un error en cada caso y no se guarda | _[ ]_ | `evidencias/CL-03.png` | _[ ]_ |
| CL-04 | Eliminar | (a) Eliminar una clase sin inscripciones. (b) Intentar eliminar una clase con inscripciones | (a) Se elimina. (b) Se rechaza por registro relacionado | _[ ]_ | `evidencias/CL-04a.png`, `CL-04b.png` | _[ ]_ |

### 4.5 Tabla `inscripciones`

| ID | Tipo | Pasos y datos | Resultado esperado | Resultado obtenido | Evidencia | Estado |
|---|---|---|---|---|---|---|
| IN-01 | Crear y listar | Inscribir a un miembro con plan que incluye clases en una clase con cupo | Aviso de creación; la inscripción aparece como "Activa" en el listado | _[ ]_ | `evidencias/IN-01.png` | _[ ]_ |
| IN-02 | Datos inválidos (plan) | Inscribir a un miembro cuyo plan no incluye clases | Se rechaza con un mensaje claro; no se crea la inscripción | _[ ]_ | `evidencias/IN-02.png` | _[ ]_ |
| IN-03 | Datos inválidos (duplicada y cupo) | (a) Repetir la inscripción del mismo miembro en la misma clase. (b) Inscribir en una clase que ya llegó a su cupo máximo | Se rechaza en ambos casos con un mensaje claro | _[ ]_ | `evidencias/IN-03a.png`, `IN-03b.png` | _[ ]_ |
| IN-04 | Eliminar | Eliminar la inscripción creada en IN-01 | La inscripción desaparece del listado | _[ ]_ | `evidencias/IN-04.png` | _[ ]_ |

> `inscripciones` no tiene tablas que dependan de ella, por eso no existe el caso de "eliminar un registro relacionado". Esa regla se prueba con las otras cuatro tablas.

## 5. Pruebas automatizadas con pytest (valor agregado)

Archivo: `tests/test_crud.py`. Se ejecutan contra la base real; cada prueba crea sus datos con el prefijo `ZZ_TEST_` y un fixture los borra antes y después, respetando el orden de las llaves foráneas.

```bash
pytest -v
```

Las pruebas automatizadas cubren los casos principales de cada tabla:

| Tabla | Funciones de prueba | Casos que respaldan |
|---|---|---|
| Todas | `test_paginas_cargan` | Carga de las páginas de listado |
| `planes` | `test_crear_plan`, `test_editar_plan`, `test_plan_datos_invalidos`, `test_eliminar_plan_con_miembros_se_rechaza` | PL-01 a PL-04 |
| `entrenadores` | `test_crear_entrenador` | EN-01 |
| `miembros` | `test_crear_miembro` | MI-01 |
| `clases` | `test_crear_clase` | CL-01 |
| `inscripciones` | `test_crear_inscripcion`, `test_inscripcion_plan_sin_clases_se_rechaza` | IN-01, IN-02 |

Los demás casos (EN-02 a EN-04, MI-02 a MI-04, CL-02 a CL-04, IN-03 e IN-04) se verifican solo de forma manual.

**Evidencias de las pruebas automatizadas** (en `docs/evidencias/`):

- `pytest_resultado.png`: terminal con `pytest -v` y todas las pruebas aprobadas.
- `cobertura.png`: salida de `pytest --cov=. --cov-report=term-missing`.

## 6. Resumen de resultados

| Total de casos manuales | OK | FALLA |
|---|---|---|
| 20 | _[ ]_ | _[ ]_ |

**Pruebas automatizadas:** _[N]_ pruebas ejecutadas, _[N]_ aprobadas.

## 7. Defectos encontrados y conclusiones

| ID | Caso | Defecto | Corrección | Estado |
|---|---|---|---|---|
| D-01 | _[ ]_ | _[ ]_ | _[ ]_ | _[ ]_ |

**Conclusión:** _[qué cubren las pruebas, qué errores se corrigieron y qué tan confiable queda el sistema]_
