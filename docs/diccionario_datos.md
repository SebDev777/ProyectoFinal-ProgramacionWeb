# Diccionario de datos y normalización – Iron Paradise Gym

**Integrantes:** Jose Daniel Cerquera Ramírez, John Sebastián Meza Saldaña
**Curso:** Programación Web · Proyecto final
**Tema:** Gestión de un gimnasio · **Base de datos:** `gimnasio_db` (PostgreSQL)

---

## 1. Descripción del modelo

El modelo tiene 5 tablas relacionadas entre sí. Los planes definen la membresía de cada miembro, los entrenadores dictan las clases, y las inscripciones registran qué miembro asiste a qué clase. La tabla `inscripciones` es la que tiene dos llaves foráneas. El diagrama entidad-relación está en el archivo `MER.png`.

Todas las llaves foráneas usan `ON UPDATE CASCADE` y `ON DELETE RESTRICT`: no se puede eliminar un registro que tenga datos relacionados.

### Relaciones entre tablas

| Relación | Cardinalidad | Llave foránea |
|---|---|---|
| `planes` – `miembros` | 1:N (un plan tiene muchos miembros; cada miembro tiene un solo plan) | `miembros.id_plan` → `planes.id_plan` |
| `entrenadores` – `clases` | 1:N (un entrenador dicta muchas clases; cada clase tiene un entrenador) | `clases.id_entrenador` → `entrenadores.id_entrenador` |
| `miembros` – `clases` | N:M, resuelta con la tabla `inscripciones` | `inscripciones.id_miembro` → `miembros.id_miembro` y `inscripciones.id_clase` → `clases.id_clase` |

---

## 2. Diccionario de datos

### 2.1 Tabla `planes`

Tipos de membresía que ofrece el gimnasio.

| Campo | Tipo de dato | Restricciones | Descripción |
|---|---|---|---|
| `id_plan` | SERIAL | PK | Identificador único del plan |
| `nombre_plan` | VARCHAR(60) | NOT NULL, UNIQUE | Nombre del plan |
| `duracion_dias` | INTEGER | NOT NULL, CHECK (> 0) | Días de vigencia del plan |
| `precio` | NUMERIC(12,2) | NOT NULL, CHECK (> 0) | Precio del plan en pesos |
| `incluye_clases` | BOOLEAN | NOT NULL, DEFAULT FALSE | Indica si el plan da acceso a clases grupales |
| `descripcion` | VARCHAR(200) | — | Qué incluye el plan |

### 2.2 Tabla `entrenadores`

Personal que dicta las clases.

| Campo | Tipo de dato | Restricciones | Descripción |
|---|---|---|---|
| `id_entrenador` | SERIAL | PK | Identificador único del entrenador |
| `nombre_entrenador` | VARCHAR(100) | NOT NULL | Nombre completo |
| `especialidad` | VARCHAR(60) | NOT NULL | Área en la que enseña |
| `email` | VARCHAR(120) | NOT NULL, UNIQUE | Correo de contacto |
| `telefono` | VARCHAR(15) | — | Teléfono de contacto |

### 2.3 Tabla `miembros`

Personas afiliadas al gimnasio.

| Campo | Tipo de dato | Restricciones | Descripción |
|---|---|---|---|
| `id_miembro` | SERIAL | PK | Identificador único del miembro |
| `nombre_miembro` | VARCHAR(100) | NOT NULL | Nombre completo |
| `documento` | VARCHAR(15) | NOT NULL, UNIQUE | Número de documento de identidad |
| `email` | VARCHAR(120) | UNIQUE | Correo del miembro |
| `telefono` | VARCHAR(15) | — | Teléfono del miembro |
| `fecha_nacimiento` | DATE | NOT NULL, CHECK (< fecha actual) | Fecha de nacimiento |
| `id_plan` | INTEGER | NOT NULL, FK → `planes(id_plan)` | Plan contratado |
| `fecha_inicio_plan` | DATE | NOT NULL | Fecha en que inicia el plan |

### 2.4 Tabla `clases`

Clases grupales con su horario y cupo.

| Campo | Tipo de dato | Restricciones | Descripción |
|---|---|---|---|
| `id_clase` | SERIAL | PK | Identificador único de la clase |
| `nombre_clase` | VARCHAR(80) | NOT NULL | Nombre de la clase |
| `id_entrenador` | INTEGER | NOT NULL, FK → `entrenadores(id_entrenador)` | Entrenador que la dicta |
| `dia_semana` | VARCHAR(10) | NOT NULL, CHECK (Lunes a Domingo) | Día en que se dicta |
| `hora_inicio` | TIME | NOT NULL | Hora de inicio |
| `duracion_min` | INTEGER | NOT NULL, CHECK (> 0) | Duración en minutos |
| `cupo_maximo` | INTEGER | NOT NULL, CHECK (> 0) | Máximo de asistentes |

### 2.5 Tabla `inscripciones`

Registra qué miembro se inscribe en qué clase.

| Campo | Tipo de dato | Restricciones | Descripción |
|---|---|---|---|
| `id_inscripcion` | SERIAL | PK | Identificador único de la inscripción |
| `id_miembro` | INTEGER | NOT NULL, FK → `miembros(id_miembro)` | Miembro inscrito |
| `id_clase` | INTEGER | NOT NULL, FK → `clases(id_clase)` | Clase a la que se inscribe |
| `fecha_inscripcion` | DATE | NOT NULL, DEFAULT fecha actual | Fecha en que se hizo la inscripción |
| `estado` | VARCHAR(15) | NOT NULL, DEFAULT 'Activa', CHECK ('Activa' o 'Cancelada') | Estado de la inscripción |

Además, la pareja (`id_miembro`, `id_clase`) es `UNIQUE`: un miembro no puede inscribirse dos veces en la misma clase.

---

## 3. Justificación de la normalización

### 3.1 Primera forma normal (1FN)

Todas las tablas cumplen la 1FN porque cada campo guarda un único valor atómico, no hay grupos repetidos ni listas dentro de una columna, y cada fila se identifica con una llave primaria. Por ejemplo, las clases a las que asiste un miembro no se guardan en una columna de `miembros`, sino como filas separadas en `inscripciones`. El teléfono y el correo guardan un solo valor cada uno.

### 3.2 Segunda forma normal (2FN)

Todas las tablas están en 1FN y usan como llave primaria una sola columna (`SERIAL`). Al no existir llaves compuestas, ningún atributo puede depender solo de una parte de la llave, así que todos dependen de la llave completa. En `inscripciones` la pareja (`id_miembro`, `id_clase`) no es la llave primaria sino una restricción `UNIQUE`; sus atributos (`fecha_inscripcion` y `estado`) describen la inscripción en sí, no al miembro ni a la clase por separado.

### 3.3 Tercera forma normal (3FN)

Cumplen la 2FN y no tienen dependencias transitivas: ningún atributo que no es llave depende de otro atributo que no es llave.

| Tabla | Por qué cumple la 3FN |
|---|---|
| `planes` | `duracion_dias`, `precio` e `incluye_clases` dependen solo de `id_plan`. Los datos del plan se guardan una sola vez y no se repiten en cada miembro. |
| `entrenadores` | Nombre, especialidad y contacto dependen solo de `id_entrenador`. Esos datos no se repiten en cada clase. |
| `miembros` | Los datos personales dependen de `id_miembro`. Del plan solo se guarda `id_plan`: el nombre, el precio y la duración se consultan en `planes`. |
| `clases` | Horario y cupo dependen de `id_clase`. Del entrenador solo se guarda `id_entrenador`, no su nombre ni su especialidad. |
| `inscripciones` | `fecha_inscripcion` y `estado` dependen de la inscripción. Los datos del miembro y de la clase se obtienen por las llaves foráneas. |

### 3.4 Decisiones de diseño

- **No se guarda la fecha de vencimiento.** Se calcula como `fecha_inicio_plan + duracion_dias`. Guardarla repetiría un dato derivable y podría quedar inconsistente si cambia el plan.
- **La relación muchos a muchos** entre `miembros` y `clases` se resuelve con la tabla `inscripciones`, que tiene dos llaves foráneas.
- **El campo `incluye_clases`** está en `planes`, y no como texto en la descripción, para poder validar en la aplicación que solo se inscriban a clases los miembros cuyo plan las incluye.

---

## 4. Reglas de integridad

### 4.1 En la base de datos

- **Llaves primarias:** una por tabla, de tipo `SERIAL`.
- **Llaves foráneas con `ON DELETE RESTRICT`:** impiden eliminar un plan con miembros, un entrenador con clases, o un miembro o una clase con inscripciones.
- **`UNIQUE`:** nombre del plan, correo del entrenador, documento y correo del miembro, y la pareja miembro–clase en `inscripciones`.
- **`CHECK`:** precio, duración, duración de la clase y cupo mayores que cero; fecha de nacimiento anterior a hoy; día de la semana válido; estado de la inscripción válido.

### 4.2 En la aplicación (Flask)

Además de las restricciones de la base de datos, el servidor valida estas reglas y muestra un mensaje claro al usuario:

- No se puede inscribir a una clase a un miembro cuyo plan no incluye clases.
- No se puede inscribir a una clase que ya alcanzó su cupo máximo.
- Un miembro no puede inscribirse dos veces en la misma clase.
- Un entrenador no puede tener dos clases que se crucen en el mismo día y horario.
- No se puede cambiar a un miembro a un plan sin clases si tiene inscripciones activas.
- No se puede bajar el cupo de una clase por debajo de sus inscritos activos.
- El documento del miembro solo puede contener números y la fecha de nacimiento debe ser anterior a hoy.
