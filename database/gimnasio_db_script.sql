-- =========================================================
-- Base de datos: gimnasio_db  (PostgreSQL)
-- Script de creación de tablas y carga de 10 registros por tabla
-- =========================================================

-- CREATE DATABASE gimnasio_db;
-- \c gimnasio_db

DROP TABLE IF EXISTS inscripciones;
DROP TABLE IF EXISTS clases;
DROP TABLE IF EXISTS miembros;
DROP TABLE IF EXISTS entrenadores;
DROP TABLE IF EXISTS planes;

-- ---------------------------------------------------------
-- Tablas
-- ---------------------------------------------------------
CREATE TABLE planes (
    id_plan       SERIAL PRIMARY KEY,
    nombre_plan   VARCHAR(60)   NOT NULL UNIQUE,
    duracion_dias INTEGER       NOT NULL CHECK (duracion_dias > 0),
    precio        NUMERIC(12,2) NOT NULL CHECK (precio > 0),
    descripcion   VARCHAR(200)
);

CREATE TABLE entrenadores (
    id_entrenador     SERIAL PRIMARY KEY,
    nombre_entrenador VARCHAR(100) NOT NULL,
    especialidad      VARCHAR(60)  NOT NULL,
    email             VARCHAR(120) NOT NULL UNIQUE,
    telefono          VARCHAR(15)
);

CREATE TABLE miembros (
    id_miembro        SERIAL PRIMARY KEY,
    nombre_miembro    VARCHAR(100) NOT NULL,
    documento         VARCHAR(15)  NOT NULL UNIQUE,
    email             VARCHAR(120) UNIQUE,
    telefono          VARCHAR(15),
    fecha_nacimiento  DATE         NOT NULL CHECK (fecha_nacimiento < CURRENT_DATE),
    id_plan           INTEGER      NOT NULL,
    fecha_inicio_plan DATE         NOT NULL,
    CONSTRAINT fk_miembros_plan
        FOREIGN KEY (id_plan) REFERENCES planes (id_plan)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE clases (
    id_clase      SERIAL PRIMARY KEY,
    nombre_clase  VARCHAR(80) NOT NULL,
    id_entrenador INTEGER     NOT NULL,
    dia_semana    VARCHAR(10) NOT NULL
        CHECK (dia_semana IN ('Lunes','Martes','Miércoles','Jueves','Viernes','Sábado','Domingo')),
    hora_inicio   TIME        NOT NULL,
    duracion_min  INTEGER     NOT NULL CHECK (duracion_min > 0),
    cupo_maximo   INTEGER     NOT NULL CHECK (cupo_maximo > 0),
    CONSTRAINT fk_clases_entrenador
        FOREIGN KEY (id_entrenador) REFERENCES entrenadores (id_entrenador)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

-- Tabla con dos llaves foráneas (relación muchos a muchos miembros <-> clases)
CREATE TABLE inscripciones (
    id_inscripcion    SERIAL PRIMARY KEY,
    id_miembro        INTEGER     NOT NULL,
    id_clase          INTEGER     NOT NULL,
    fecha_inscripcion DATE        NOT NULL DEFAULT CURRENT_DATE,
    estado            VARCHAR(15) NOT NULL DEFAULT 'Activa'
        CHECK (estado IN ('Activa', 'Cancelada')),
    CONSTRAINT uq_inscripcion UNIQUE (id_miembro, id_clase),
    CONSTRAINT fk_inscripciones_miembro
        FOREIGN KEY (id_miembro) REFERENCES miembros (id_miembro)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_inscripciones_clase
        FOREIGN KEY (id_clase) REFERENCES clases (id_clase)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE INDEX idx_miembros_plan        ON miembros (id_plan);
CREATE INDEX idx_clases_entrenador    ON clases (id_entrenador);
CREATE INDEX idx_inscripciones_miembro ON inscripciones (id_miembro);
CREATE INDEX idx_inscripciones_clase   ON inscripciones (id_clase);

-- ---------------------------------------------------------
-- Datos (10 registros por tabla)
-- ---------------------------------------------------------
INSERT INTO planes (nombre_plan, duracion_dias, precio, descripcion) VALUES
('Diario',            1,    15000.00, 'Acceso por un día a sala de máquinas'),
('Semanal',           7,    40000.00, 'Acceso libre durante siete días'),
('Mensual Básico',   30,    90000.00, 'Sala de máquinas, sin clases grupales'),
('Mensual Full',     30,   130000.00, 'Sala de máquinas y todas las clases grupales'),
('Trimestral',       90,   330000.00, 'Tres meses con clases grupales incluidas'),
('Semestral',       180,   600000.00, 'Seis meses con clases y valoración física'),
('Anual',           365,  1050000.00, 'Doce meses con clases y plan de entrenamiento'),
('Estudiante',       30,    75000.00, 'Mensual con descuento para estudiantes'),
('Pareja',           30,   220000.00, 'Mensual Full para dos personas'),
('Senior',           30,    70000.00, 'Mensual para mayores de 60 años');

INSERT INTO entrenadores (nombre_entrenador, especialidad, email, telefono) VALUES
('Carlos Andrés Medina',   'Spinning',           'carlos.medina@gym.com',   '3101112233'),
('Laura Catalina Rojas',   'Yoga',               'laura.rojas@gym.com',     '3112223344'),
('Juan Pablo Cabrera',     'Crossfit',           'juan.cabrera@gym.com',    '3123334455'),
('Daniela Ortiz Vargas',   'Baile fitness',      'daniela.ortiz@gym.com',   '3134445566'),
('Mauricio Perdomo',       'Entrenamiento funcional', 'mauricio.perdomo@gym.com', '3145556677'),
('Paola Andrea Charry',    'Pilates',            'paola.charry@gym.com',    '3156667788'),
('Sebastián Quintero',     'Boxeo',              'sebastian.quintero@gym.com', '3167778899'),
('Natalia Trujillo',       'Pilates',            'natalia.trujillo@gym.com','3178889900'),
('Felipe Cuéllar',         'Musculación',        'felipe.cuellar@gym.com',  '3189990011'),
('Viviana Polanía',        'Nutrición deportiva','viviana.polania@gym.com', '3190001122');

INSERT INTO miembros (nombre_miembro, documento, email, telefono, fecha_nacimiento, id_plan, fecha_inicio_plan) VALUES
('Andrea Milena Gómez',   '1075201001', 'andrea.gomez@mail.com',   '3201000001', '1998-03-14',  4, '2026-10-05'),
('Brayan Steven Ramírez', '1075201002', 'brayan.ramirez@mail.com', '3201000002', '2001-07-22',  8, '2026-10-10'),
('Camila Fernanda Soto',  '1075201003', 'camila.soto@mail.com',    '3201000003', '1995-11-02',  5, '2026-09-01'),
('Diego Alejandro Peña',  '1075201004', 'diego.pena@mail.com',     '3201000004', '1990-01-30',  7, '2026-01-15'),
('Estefanía Lozano',      '1075201005', 'estefania.lozano@mail.com','3201000005','2000-05-18',  3, '2026-10-20'),
('Fabián Andrés Muñoz',   '1075201006', 'fabian.munoz@mail.com',   '3201000006', '1987-09-09',  6, '2026-06-01'),
('Gloria Inés Tovar',     '1075201007', 'gloria.tovar@mail.com',   '3201000007', '1958-12-25', 10, '2026-10-12'),
('Hernán Darío Bahamón',  '1075201008', 'hernan.bahamon@mail.com', '3201000008', '1993-04-07',  4, '2026-10-18'),
('Isabela Cortés',        '1075201009', 'isabela.cortes@mail.com', '3201000009', '2003-08-11',  8, '2026-11-02'),
('Julián David Salazar',  '1075201010', 'julian.salazar@mail.com', '3201000010', '1996-06-27',  9, '2026-10-25');

INSERT INTO clases (nombre_clase, id_entrenador, dia_semana, hora_inicio, duracion_min, cupo_maximo) VALUES
('Spinning mañana',        1, 'Lunes',     '06:00', 45, 20),
('Yoga restaurativo',      2, 'Martes',    '07:00', 60, 15),
('Crossfit WOD',           3, 'Miércoles', '18:00', 60, 12),
('Zumba',                  4, 'Jueves',    '19:00', 50, 25),
('Funcional intensivo',    5, 'Viernes',   '17:30', 45, 18),
('Pilates mat',            6, 'Lunes',     '08:00', 55, 14),
('Boxeo recreativo',       7, 'Martes',    '19:30', 60, 16),
('Pilates avanzado',       8, 'Sábado',    '09:00', 55, 14),
('Spinning noche',         1, 'Jueves',    '20:00', 45, 20),
('Yoga dominical',         2, 'Domingo',   '08:30', 60, 15);

INSERT INTO inscripciones (id_miembro, id_clase, fecha_inscripcion, estado) VALUES
(1,  1, '2026-10-06', 'Activa'),
(1,  4, '2026-10-06', 'Activa'),
(2,  3, '2026-10-11', 'Activa'),
(3,  2, '2026-09-02', 'Cancelada'),
(3,  6, '2026-09-02', 'Activa'),
(4,  5, '2026-01-16', 'Activa'),
(6,  8, '2026-06-02', 'Activa'),
(8,  7, '2026-10-19', 'Activa'),
(9, 10, '2026-11-03', 'Activa'),
(10, 9, '2026-10-26', 'Cancelada');
