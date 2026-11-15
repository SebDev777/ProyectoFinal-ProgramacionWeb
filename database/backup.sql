--
-- PostgreSQL database dump
--

\restrict cw4Oys5yBhLMnbpjADlZXllOPP6SmPGqebFr0ih0hO69W8skmJt8fym4qDe40t6

-- Dumped from database version 18.1
-- Dumped by pg_dump version 18.1

-- Started on 2026-11-15 14:36:31

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 226 (class 1259 OID 24629)
-- Name: clases; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.clases (
    id_clase integer NOT NULL,
    nombre_clase character varying(80) NOT NULL,
    id_entrenador integer NOT NULL,
    dia_semana character varying(10) NOT NULL,
    hora_inicio time without time zone NOT NULL,
    duracion_min integer NOT NULL,
    cupo_maximo integer NOT NULL,
    CONSTRAINT clases_cupo_maximo_check CHECK ((cupo_maximo > 0)),
    CONSTRAINT clases_dia_semana_check CHECK (((dia_semana)::text = ANY ((ARRAY['Lunes'::character varying, 'Martes'::character varying, 'Miércoles'::character varying, 'Jueves'::character varying, 'Viernes'::character varying, 'Sábado'::character varying, 'Domingo'::character varying])::text[]))),
    CONSTRAINT clases_duracion_min_check CHECK ((duracion_min > 0))
);


ALTER TABLE public.clases OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 24628)
-- Name: clases_id_clase_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.clases_id_clase_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.clases_id_clase_seq OWNER TO postgres;

--
-- TOC entry 5080 (class 0 OID 0)
-- Dependencies: 225
-- Name: clases_id_clase_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.clases_id_clase_seq OWNED BY public.clases.id_clase;


--
-- TOC entry 222 (class 1259 OID 24593)
-- Name: entrenadores; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.entrenadores (
    id_entrenador integer NOT NULL,
    nombre_entrenador character varying(100) NOT NULL,
    especialidad character varying(60) NOT NULL,
    email character varying(120) NOT NULL,
    telefono character varying(15)
);


ALTER TABLE public.entrenadores OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 24592)
-- Name: entrenadores_id_entrenador_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.entrenadores_id_entrenador_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.entrenadores_id_entrenador_seq OWNER TO postgres;

--
-- TOC entry 5081 (class 0 OID 0)
-- Dependencies: 221
-- Name: entrenadores_id_entrenador_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.entrenadores_id_entrenador_seq OWNED BY public.entrenadores.id_entrenador;


--
-- TOC entry 228 (class 1259 OID 24651)
-- Name: inscripciones; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.inscripciones (
    id_inscripcion integer NOT NULL,
    id_miembro integer NOT NULL,
    id_clase integer NOT NULL,
    fecha_inscripcion date DEFAULT CURRENT_DATE NOT NULL,
    estado character varying(15) DEFAULT 'Activa'::character varying NOT NULL,
    CONSTRAINT inscripciones_estado_check CHECK (((estado)::text = ANY ((ARRAY['Activa'::character varying, 'Cancelada'::character varying])::text[])))
);


ALTER TABLE public.inscripciones OWNER TO postgres;

--
-- TOC entry 227 (class 1259 OID 24650)
-- Name: inscripciones_id_inscripcion_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.inscripciones_id_inscripcion_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.inscripciones_id_inscripcion_seq OWNER TO postgres;

--
-- TOC entry 5082 (class 0 OID 0)
-- Dependencies: 227
-- Name: inscripciones_id_inscripcion_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.inscripciones_id_inscripcion_seq OWNED BY public.inscripciones.id_inscripcion;


--
-- TOC entry 224 (class 1259 OID 24606)
-- Name: miembros; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.miembros (
    id_miembro integer NOT NULL,
    nombre_miembro character varying(100) NOT NULL,
    documento character varying(15) NOT NULL,
    email character varying(120),
    telefono character varying(15),
    fecha_nacimiento date NOT NULL,
    id_plan integer NOT NULL,
    fecha_inicio_plan date NOT NULL,
    CONSTRAINT miembros_fecha_nacimiento_check CHECK ((fecha_nacimiento < CURRENT_DATE))
);


ALTER TABLE public.miembros OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 24605)
-- Name: miembros_id_miembro_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.miembros_id_miembro_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.miembros_id_miembro_seq OWNER TO postgres;

--
-- TOC entry 5083 (class 0 OID 0)
-- Dependencies: 223
-- Name: miembros_id_miembro_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.miembros_id_miembro_seq OWNED BY public.miembros.id_miembro;


--
-- TOC entry 220 (class 1259 OID 24578)
-- Name: planes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.planes (
    id_plan integer NOT NULL,
    nombre_plan character varying(60) NOT NULL,
    duracion_dias integer NOT NULL,
    precio numeric(12,2) NOT NULL,
    descripcion character varying(200),
    CONSTRAINT planes_duracion_dias_check CHECK ((duracion_dias > 0)),
    CONSTRAINT planes_precio_check CHECK ((precio > (0)::numeric))
);


ALTER TABLE public.planes OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 24577)
-- Name: planes_id_plan_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.planes_id_plan_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.planes_id_plan_seq OWNER TO postgres;

--
-- TOC entry 5084 (class 0 OID 0)
-- Dependencies: 219
-- Name: planes_id_plan_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.planes_id_plan_seq OWNED BY public.planes.id_plan;


--
-- TOC entry 4879 (class 2604 OID 24632)
-- Name: clases id_clase; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clases ALTER COLUMN id_clase SET DEFAULT nextval('public.clases_id_clase_seq'::regclass);


--
-- TOC entry 4877 (class 2604 OID 24596)
-- Name: entrenadores id_entrenador; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.entrenadores ALTER COLUMN id_entrenador SET DEFAULT nextval('public.entrenadores_id_entrenador_seq'::regclass);


--
-- TOC entry 4880 (class 2604 OID 24654)
-- Name: inscripciones id_inscripcion; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.inscripciones ALTER COLUMN id_inscripcion SET DEFAULT nextval('public.inscripciones_id_inscripcion_seq'::regclass);


--
-- TOC entry 4878 (class 2604 OID 24609)
-- Name: miembros id_miembro; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.miembros ALTER COLUMN id_miembro SET DEFAULT nextval('public.miembros_id_miembro_seq'::regclass);


--
-- TOC entry 4876 (class 2604 OID 24581)
-- Name: planes id_plan; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.planes ALTER COLUMN id_plan SET DEFAULT nextval('public.planes_id_plan_seq'::regclass);


--
-- TOC entry 5072 (class 0 OID 24629)
-- Dependencies: 226
-- Data for Name: clases; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.clases (id_clase, nombre_clase, id_entrenador, dia_semana, hora_inicio, duracion_min, cupo_maximo) FROM stdin;
1	Spinning mañana	1	Lunes	06:00:00	45	20
2	Yoga restaurativo	2	Martes	07:00:00	60	15
3	Crossfit WOD	3	Miércoles	18:00:00	60	12
4	Zumba	4	Jueves	19:00:00	50	25
5	Funcional intensivo	5	Viernes	17:30:00	45	18
6	Pilates mat	6	Lunes	08:00:00	55	14
7	Boxeo recreativo	7	Martes	19:30:00	60	16
8	Pilates avanzado	8	Sábado	09:00:00	55	14
9	Spinning noche	1	Jueves	20:00:00	45	20
10	Yoga dominical	2	Domingo	08:30:00	60	15
\.


--
-- TOC entry 5068 (class 0 OID 24593)
-- Dependencies: 222
-- Data for Name: entrenadores; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.entrenadores (id_entrenador, nombre_entrenador, especialidad, email, telefono) FROM stdin;
1	Carlos Andrés Medina	Spinning	carlos.medina@gym.com	3101112233
2	Laura Catalina Rojas	Yoga	laura.rojas@gym.com	3112223344
3	Juan Pablo Cabrera	Crossfit	juan.cabrera@gym.com	3123334455
4	Daniela Ortiz Vargas	Baile fitness	daniela.ortiz@gym.com	3134445566
5	Mauricio Perdomo	Entrenamiento funcional	mauricio.perdomo@gym.com	3145556677
6	Paola Andrea Charry	Pilates	paola.charry@gym.com	3156667788
7	Sebastián Quintero	Boxeo	sebastian.quintero@gym.com	3167778899
8	Natalia Trujillo	Pilates	natalia.trujillo@gym.com	3178889900
9	Felipe Cuéllar	Musculación	felipe.cuellar@gym.com	3189990011
10	Viviana Polanía	Nutrición deportiva	viviana.polania@gym.com	3190001122
\.


--
-- TOC entry 5074 (class 0 OID 24651)
-- Dependencies: 228
-- Data for Name: inscripciones; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.inscripciones (id_inscripcion, id_miembro, id_clase, fecha_inscripcion, estado) FROM stdin;
1	1	1	2026-10-06	Activa
2	1	4	2026-10-06	Activa
3	2	3	2026-10-11	Activa
4	3	2	2026-09-02	Cancelada
5	3	6	2026-09-02	Activa
6	4	5	2026-01-16	Activa
7	6	8	2026-06-02	Activa
8	8	7	2026-10-19	Activa
9	9	10	2026-11-03	Activa
10	10	9	2026-10-26	Cancelada
\.


--
-- TOC entry 5070 (class 0 OID 24606)
-- Dependencies: 224
-- Data for Name: miembros; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.miembros (id_miembro, nombre_miembro, documento, email, telefono, fecha_nacimiento, id_plan, fecha_inicio_plan) FROM stdin;
1	Andrea Milena Gómez	1075201001	andrea.gomez@mail.com	3201000001	1998-03-14	4	2026-10-05
2	Brayan Steven Ramírez	1075201002	brayan.ramirez@mail.com	3201000002	2001-07-22	8	2026-10-10
3	Camila Fernanda Soto	1075201003	camila.soto@mail.com	3201000003	1995-11-02	5	2026-09-01
4	Diego Alejandro Peña	1075201004	diego.pena@mail.com	3201000004	1990-01-30	7	2026-01-15
5	Estefanía Lozano	1075201005	estefania.lozano@mail.com	3201000005	2000-05-18	3	2026-10-20
6	Fabián Andrés Muñoz	1075201006	fabian.munoz@mail.com	3201000006	1987-09-09	6	2026-06-01
7	Gloria Inés Tovar	1075201007	gloria.tovar@mail.com	3201000007	1958-12-25	10	2026-10-12
8	Hernán Darío Bahamón	1075201008	hernan.bahamon@mail.com	3201000008	1993-04-07	4	2026-10-18
9	Isabela Cortés	1075201009	isabela.cortes@mail.com	3201000009	2003-08-11	8	2026-11-02
10	Julián David Salazar	1075201010	julian.salazar@mail.com	3201000010	1996-06-27	9	2026-10-25
\.


--
-- TOC entry 5066 (class 0 OID 24578)
-- Dependencies: 220
-- Data for Name: planes; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.planes (id_plan, nombre_plan, duracion_dias, precio, descripcion) FROM stdin;
1	Diario	1	15000.00	Acceso por un día a sala de máquinas
2	Semanal	7	40000.00	Acceso libre durante siete días
3	Mensual Básico	30	90000.00	Sala de máquinas, sin clases grupales
4	Mensual Full	30	130000.00	Sala de máquinas y todas las clases grupales
5	Trimestral	90	330000.00	Tres meses con clases grupales incluidas
6	Semestral	180	600000.00	Seis meses con clases y valoración física
7	Anual	365	1050000.00	Doce meses con clases y plan de entrenamiento
8	Estudiante	30	75000.00	Mensual con descuento para estudiantes
9	Pareja	30	220000.00	Mensual Full para dos personas
10	Senior	30	70000.00	Mensual para mayores de 60 años
\.


--
-- TOC entry 5085 (class 0 OID 0)
-- Dependencies: 225
-- Name: clases_id_clase_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.clases_id_clase_seq', 10, true);


--
-- TOC entry 5086 (class 0 OID 0)
-- Dependencies: 221
-- Name: entrenadores_id_entrenador_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.entrenadores_id_entrenador_seq', 10, true);


--
-- TOC entry 5087 (class 0 OID 0)
-- Dependencies: 227
-- Name: inscripciones_id_inscripcion_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.inscripciones_id_inscripcion_seq', 10, true);


--
-- TOC entry 5088 (class 0 OID 0)
-- Dependencies: 223
-- Name: miembros_id_miembro_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.miembros_id_miembro_seq', 10, true);


--
-- TOC entry 5089 (class 0 OID 0)
-- Dependencies: 219
-- Name: planes_id_plan_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.planes_id_plan_seq', 10, true);


--
-- TOC entry 4906 (class 2606 OID 24644)
-- Name: clases clases_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clases
    ADD CONSTRAINT clases_pkey PRIMARY KEY (id_clase);


--
-- TOC entry 4895 (class 2606 OID 24604)
-- Name: entrenadores entrenadores_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.entrenadores
    ADD CONSTRAINT entrenadores_email_key UNIQUE (email);


--
-- TOC entry 4897 (class 2606 OID 24602)
-- Name: entrenadores entrenadores_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.entrenadores
    ADD CONSTRAINT entrenadores_pkey PRIMARY KEY (id_entrenador);


--
-- TOC entry 4911 (class 2606 OID 24664)
-- Name: inscripciones inscripciones_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.inscripciones
    ADD CONSTRAINT inscripciones_pkey PRIMARY KEY (id_inscripcion);


--
-- TOC entry 4900 (class 2606 OID 24620)
-- Name: miembros miembros_documento_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.miembros
    ADD CONSTRAINT miembros_documento_key UNIQUE (documento);


--
-- TOC entry 4902 (class 2606 OID 24622)
-- Name: miembros miembros_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.miembros
    ADD CONSTRAINT miembros_email_key UNIQUE (email);


--
-- TOC entry 4904 (class 2606 OID 24618)
-- Name: miembros miembros_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.miembros
    ADD CONSTRAINT miembros_pkey PRIMARY KEY (id_miembro);


--
-- TOC entry 4891 (class 2606 OID 24591)
-- Name: planes planes_nombre_plan_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.planes
    ADD CONSTRAINT planes_nombre_plan_key UNIQUE (nombre_plan);


--
-- TOC entry 4893 (class 2606 OID 24589)
-- Name: planes planes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.planes
    ADD CONSTRAINT planes_pkey PRIMARY KEY (id_plan);


--
-- TOC entry 4913 (class 2606 OID 24666)
-- Name: inscripciones uq_inscripcion; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.inscripciones
    ADD CONSTRAINT uq_inscripcion UNIQUE (id_miembro, id_clase);


--
-- TOC entry 4907 (class 1259 OID 24678)
-- Name: idx_clases_entrenador; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_clases_entrenador ON public.clases USING btree (id_entrenador);


--
-- TOC entry 4908 (class 1259 OID 24680)
-- Name: idx_inscripciones_clase; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_inscripciones_clase ON public.inscripciones USING btree (id_clase);


--
-- TOC entry 4909 (class 1259 OID 24679)
-- Name: idx_inscripciones_miembro; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_inscripciones_miembro ON public.inscripciones USING btree (id_miembro);


--
-- TOC entry 4898 (class 1259 OID 24677)
-- Name: idx_miembros_plan; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_miembros_plan ON public.miembros USING btree (id_plan);


--
-- TOC entry 4915 (class 2606 OID 24645)
-- Name: clases fk_clases_entrenador; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clases
    ADD CONSTRAINT fk_clases_entrenador FOREIGN KEY (id_entrenador) REFERENCES public.entrenadores(id_entrenador) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- TOC entry 4916 (class 2606 OID 24672)
-- Name: inscripciones fk_inscripciones_clase; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.inscripciones
    ADD CONSTRAINT fk_inscripciones_clase FOREIGN KEY (id_clase) REFERENCES public.clases(id_clase) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- TOC entry 4917 (class 2606 OID 24667)
-- Name: inscripciones fk_inscripciones_miembro; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.inscripciones
    ADD CONSTRAINT fk_inscripciones_miembro FOREIGN KEY (id_miembro) REFERENCES public.miembros(id_miembro) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- TOC entry 4914 (class 2606 OID 24623)
-- Name: miembros fk_miembros_plan; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.miembros
    ADD CONSTRAINT fk_miembros_plan FOREIGN KEY (id_plan) REFERENCES public.planes(id_plan) ON UPDATE CASCADE ON DELETE RESTRICT;


-- Completed on 2026-11-15 14:36:31

--
-- PostgreSQL database dump complete
--

\unrestrict cw4Oys5yBhLMnbpjADlZXllOPP6SmPGqebFr0ih0hO69W8skmJt8fym4qDe40t6

