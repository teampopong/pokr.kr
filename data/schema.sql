--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


--
-- Name: hstore; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS hstore WITH SCHEMA public;


--
-- Name: EXTENSION hstore; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION hstore IS 'data type for storing sets of (key, value) pairs';


SET search_path = public, pg_catalog;

--
-- Name: enum_gender; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE enum_gender AS ENUM (
    'm',
    'f'
);


ALTER TYPE public.enum_gender OWNER TO postgres;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- Name: assembly; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE assembly (
    id integer NOT NULL,
    session_id integer NOT NULL
);


ALTER TABLE public.assembly OWNER TO postgres;

--
-- Name: bill; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE bill (
    created_at timestamp without time zone,
    modified_at timestamp without time zone,
    modified_by text,
    id text NOT NULL,
    link_id text,
    assembly_id integer NOT NULL,
    name text NOT NULL,
    summary text,
    document_url text,
    proposed_date date,
    decision_date date,
    is_processed boolean,
    extra_vars hstore NOT NULL
);


ALTER TABLE public.bill OWNER TO postgres;

--
-- Name: bill_keyword; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE bill_keyword (
    created_at timestamp without time zone,
    modified_at timestamp without time zone,
    modified_by text,
    id integer NOT NULL,
    bill_id text NOT NULL,
    keyword_id integer NOT NULL,
    weight double precision NOT NULL
);


ALTER TABLE public.bill_keyword OWNER TO postgres;

--
-- Name: bill_keyword_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE bill_keyword_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.bill_keyword_id_seq OWNER TO postgres;

--
-- Name: bill_keyword_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE bill_keyword_id_seq OWNED BY bill_keyword.id;


--
-- Name: bill_process; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE bill_process (
    created_at timestamp without time zone,
    modified_at timestamp without time zone,
    modified_by text,
    id integer NOT NULL,
    bill_id text NOT NULL,
    status_id integer NOT NULL,
    "order" integer,
    start_date date,
    end_date date,
    extra_vars hstore NOT NULL
);


ALTER TABLE public.bill_process OWNER TO postgres;

--
-- Name: bill_process_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE bill_process_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.bill_process_id_seq OWNER TO postgres;

--
-- Name: bill_process_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE bill_process_id_seq OWNED BY bill_process.id;


--
-- Name: bill_status; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE bill_status (
    created_at timestamp without time zone,
    modified_at timestamp without time zone,
    modified_by text,
    id integer NOT NULL,
    name text NOT NULL,
    description text
);


ALTER TABLE public.bill_status OWNER TO postgres;

--
-- Name: bill_status_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE bill_status_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.bill_status_id_seq OWNER TO postgres;

--
-- Name: bill_status_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE bill_status_id_seq OWNED BY bill_status.id;


--
-- Name: candidacy; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE candidacy (
    created_at timestamp without time zone,
    modified_at timestamp without time zone,
    modified_by text,
    id integer NOT NULL,
    election_id integer NOT NULL,
    party_affiliation_id integer NOT NULL,
    named_region_id integer,
    is_elected boolean,
    cand_no integer,
    vote_score integer,
    vote_share double precision
);


ALTER TABLE public.candidacy OWNER TO postgres;

--
-- Name: candidacy_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE candidacy_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.candidacy_id_seq OWNER TO postgres;

--
-- Name: candidacy_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE candidacy_id_seq OWNED BY candidacy.id;


--
-- Name: committee; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE committee (
    created_at timestamp without time zone,
    modified_at timestamp without time zone,
    modified_by text,
    id integer NOT NULL,
    name text NOT NULL
);


ALTER TABLE public.committee OWNER TO postgres;

--
-- Name: committee_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE committee_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.committee_id_seq OWNER TO postgres;

--
-- Name: committee_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE committee_id_seq OWNED BY committee.id;


--
-- Name: cosponsorship; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE cosponsorship (
    created_at timestamp without time zone,
    modified_at timestamp without time zone,
    modified_by text,
    id integer NOT NULL,
    bill_id text NOT NULL,
    name text NOT NULL,
    committee_id integer,
    party_affiliation_id integer,
    is_proposer boolean NOT NULL,
    is_agreement boolean NOT NULL,
    is_withdrawn boolean NOT NULL
);


ALTER TABLE public.cosponsorship OWNER TO postgres;

--
-- Name: cosponsorship_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE cosponsorship_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.cosponsorship_id_seq OWNER TO postgres;

--
-- Name: cosponsorship_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE cosponsorship_id_seq OWNED BY cosponsorship.id;


--
-- Name: education; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE education (
    created_at timestamp without time zone,
    modified_at timestamp without time zone,
    modified_by text,
    id integer NOT NULL,
    person_id integer NOT NULL,
    school_id integer,
    description text,
    "order" integer
);


ALTER TABLE public.education OWNER TO postgres;

--
-- Name: education_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE education_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.education_id_seq OWNER TO postgres;

--
-- Name: education_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE education_id_seq OWNED BY education.id;


--
-- Name: election; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE election (
    created_at timestamp without time zone,
    modified_at timestamp without time zone,
    modified_by text,
    id integer NOT NULL,
    organization_id integer,
    date date
);


ALTER TABLE public.election OWNER TO postgres;

--
-- Name: election_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE election_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.election_id_seq OWNER TO postgres;

--
-- Name: election_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE election_id_seq OWNED BY election.id;


--
-- Name: keyword; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE keyword (
    created_at timestamp without time zone,
    modified_at timestamp without time zone,
    modified_by text,
    id integer NOT NULL,
    name text NOT NULL
);


ALTER TABLE public.keyword OWNER TO postgres;

--
-- Name: keyword_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE keyword_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.keyword_id_seq OWNER TO postgres;

--
-- Name: keyword_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE keyword_id_seq OWNED BY keyword.id;


--
-- Name: named_region; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE named_region (
    created_at timestamp without time zone,
    modified_at timestamp without time zone,
    modified_by text,
    id integer NOT NULL,
    name text NOT NULL,
    region_id text
);


ALTER TABLE public.named_region OWNER TO postgres;

--
-- Name: named_region_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE named_region_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.named_region_id_seq OWNER TO postgres;

--
-- Name: named_region_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE named_region_id_seq OWNED BY named_region.id;


--
-- Name: organization; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE organization (
    created_at timestamp without time zone,
    modified_at timestamp without time zone,
    modified_by text,
    id integer NOT NULL,
    type_id integer NOT NULL,
    name text NOT NULL,
    start_date date,
    end_date date
);


ALTER TABLE public.organization OWNER TO postgres;

--
-- Name: organization_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE organization_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.organization_id_seq OWNER TO postgres;

--
-- Name: organization_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE organization_id_seq OWNED BY organization.id;


--
-- Name: organization_type; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE organization_type (
    created_at timestamp without time zone,
    modified_at timestamp without time zone,
    modified_by text,
    id integer NOT NULL,
    name text
);


ALTER TABLE public.organization_type OWNER TO postgres;

--
-- Name: organization_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE organization_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.organization_type_id_seq OWNER TO postgres;

--
-- Name: organization_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE organization_type_id_seq OWNED BY organization_type.id;


--
-- Name: party; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE party (
    created_at timestamp without time zone,
    modified_at timestamp without time zone,
    modified_by text,
    id integer NOT NULL,
    name text NOT NULL,
    start_date date,
    end_date date,
    logo text,
    color character(6),
    homepage text
);


ALTER TABLE public.party OWNER TO postgres;

--
-- Name: party_affiliation; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE party_affiliation (
    created_at timestamp without time zone,
    modified_at timestamp without time zone,
    modified_by text,
    id integer NOT NULL,
    person_id integer NOT NULL,
    party_id integer,
    start_date date,
    end_date date
);


ALTER TABLE public.party_affiliation OWNER TO postgres;

--
-- Name: party_affiliation_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE party_affiliation_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.party_affiliation_id_seq OWNER TO postgres;

--
-- Name: party_affiliation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE party_affiliation_id_seq OWNED BY party_affiliation.id;


--
-- Name: party_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE party_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.party_id_seq OWNER TO postgres;

--
-- Name: party_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE party_id_seq OWNED BY party.id;


--
-- Name: person; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE person (
    created_at timestamp without time zone,
    modified_at timestamp without time zone,
    modified_by text,
    id integer NOT NULL,
    name text NOT NULL,
    name_en text,
    name_cn text,
    gender enum_gender,
    birthday date,
    sites hstore NOT NULL
);


ALTER TABLE public.person OWNER TO postgres;

--
-- Name: person_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE person_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.person_id_seq OWNER TO postgres;

--
-- Name: person_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE person_id_seq OWNED BY person.id;


--
-- Name: person_image; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE person_image (
    created_at timestamp without time zone,
    modified_at timestamp without time zone,
    modified_by text,
    id integer NOT NULL,
    person_id integer,
    url text
);


ALTER TABLE public.person_image OWNER TO postgres;

--
-- Name: person_image_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE person_image_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.person_image_id_seq OWNER TO postgres;

--
-- Name: person_image_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE person_image_id_seq OWNED BY person_image.id;


--
-- Name: pledge; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE pledge (
    created_at timestamp without time zone,
    modified_at timestamp without time zone,
    modified_by text,
    id integer NOT NULL,
    candidacy_id integer NOT NULL,
    no integer NOT NULL,
    title text,
    description text
);


ALTER TABLE public.pledge OWNER TO postgres;

--
-- Name: pledge_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE pledge_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.pledge_id_seq OWNER TO postgres;

--
-- Name: pledge_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE pledge_id_seq OWNED BY pledge.id;


--
-- Name: region; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE region (
    created_at timestamp without time zone,
    modified_at timestamp without time zone,
    modified_by text,
    id text NOT NULL,
    parent_id text,
    name text NOT NULL,
    name_en text,
    name_cn text,
    fullname text,
    fullname_en text
);


ALTER TABLE public.region OWNER TO postgres;

--
-- Name: residence; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE residence (
    created_at timestamp without time zone,
    modified_at timestamp without time zone,
    modified_by text,
    id integer NOT NULL,
    person_id integer NOT NULL,
    named_region_id integer NOT NULL
);


ALTER TABLE public.residence OWNER TO postgres;

--
-- Name: residence_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE residence_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.residence_id_seq OWNER TO postgres;

--
-- Name: residence_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE residence_id_seq OWNED BY residence.id;


--
-- Name: school; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE school (
    created_at timestamp without time zone,
    modified_at timestamp without time zone,
    modified_by text,
    id integer NOT NULL,
    name text NOT NULL
);


ALTER TABLE public.school OWNER TO postgres;

--
-- Name: school_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE school_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.school_id_seq OWNER TO postgres;

--
-- Name: school_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE school_id_seq OWNED BY school.id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY bill_keyword ALTER COLUMN id SET DEFAULT nextval('bill_keyword_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY bill_process ALTER COLUMN id SET DEFAULT nextval('bill_process_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY bill_status ALTER COLUMN id SET DEFAULT nextval('bill_status_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY candidacy ALTER COLUMN id SET DEFAULT nextval('candidacy_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY committee ALTER COLUMN id SET DEFAULT nextval('committee_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY cosponsorship ALTER COLUMN id SET DEFAULT nextval('cosponsorship_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY education ALTER COLUMN id SET DEFAULT nextval('education_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY election ALTER COLUMN id SET DEFAULT nextval('election_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY keyword ALTER COLUMN id SET DEFAULT nextval('keyword_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY named_region ALTER COLUMN id SET DEFAULT nextval('named_region_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY organization ALTER COLUMN id SET DEFAULT nextval('organization_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY organization_type ALTER COLUMN id SET DEFAULT nextval('organization_type_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY party ALTER COLUMN id SET DEFAULT nextval('party_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY party_affiliation ALTER COLUMN id SET DEFAULT nextval('party_affiliation_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY person ALTER COLUMN id SET DEFAULT nextval('person_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY person_image ALTER COLUMN id SET DEFAULT nextval('person_image_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY pledge ALTER COLUMN id SET DEFAULT nextval('pledge_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY residence ALTER COLUMN id SET DEFAULT nextval('residence_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY school ALTER COLUMN id SET DEFAULT nextval('school_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY alembic_version (version_num) FROM stdin;
\.


--
-- Data for Name: assembly; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY assembly (id, session_id) FROM stdin;
\.


--
-- Data for Name: bill; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY bill (created_at, modified_at, modified_by, id, link_id, assembly_id, name, summary, document_url, proposed_date, decision_date, is_processed, extra_vars) FROM stdin;
\.


--
-- Data for Name: bill_keyword; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY bill_keyword (created_at, modified_at, modified_by, id, bill_id, keyword_id, weight) FROM stdin;
\.


--
-- Name: bill_keyword_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('bill_keyword_id_seq', 1, false);


--
-- Data for Name: bill_process; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY bill_process (created_at, modified_at, modified_by, id, bill_id, status_id, "order", start_date, end_date, extra_vars) FROM stdin;
\.


--
-- Name: bill_process_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('bill_process_id_seq', 1, false);


--
-- Data for Name: bill_status; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY bill_status (created_at, modified_at, modified_by, id, name, description) FROM stdin;
\.


--
-- Name: bill_status_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('bill_status_id_seq', 1, false);


--
-- Data for Name: candidacy; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY candidacy (created_at, modified_at, modified_by, id, election_id, party_affiliation_id, named_region_id, is_elected, cand_no, vote_score, vote_share) FROM stdin;
\.


--
-- Name: candidacy_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('candidacy_id_seq', 1, false);


--
-- Data for Name: committee; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY committee (created_at, modified_at, modified_by, id, name) FROM stdin;
\.


--
-- Name: committee_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('committee_id_seq', 1, false);


--
-- Data for Name: cosponsorship; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY cosponsorship (created_at, modified_at, modified_by, id, bill_id, name, committee_id, party_affiliation_id, is_proposer, is_agreement, is_withdrawn) FROM stdin;
\.


--
-- Name: cosponsorship_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('cosponsorship_id_seq', 1, false);


--
-- Data for Name: education; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY education (created_at, modified_at, modified_by, id, person_id, school_id, description, "order") FROM stdin;
\.


--
-- Name: education_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('education_id_seq', 1, false);


--
-- Data for Name: election; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY election (created_at, modified_at, modified_by, id, organization_id, date) FROM stdin;
\.


--
-- Name: election_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('election_id_seq', 1, false);


--
-- Data for Name: keyword; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY keyword (created_at, modified_at, modified_by, id, name) FROM stdin;
\.


--
-- Name: keyword_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('keyword_id_seq', 1, false);


--
-- Data for Name: named_region; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY named_region (created_at, modified_at, modified_by, id, name, region_id) FROM stdin;
\.


--
-- Name: named_region_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('named_region_id_seq', 1, false);


--
-- Data for Name: organization; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY organization (created_at, modified_at, modified_by, id, type_id, name, start_date, end_date) FROM stdin;
\.


--
-- Name: organization_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('organization_id_seq', 1, false);


--
-- Data for Name: organization_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY organization_type (created_at, modified_at, modified_by, id, name) FROM stdin;
\.


--
-- Name: organization_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('organization_type_id_seq', 1, false);


--
-- Data for Name: party; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY party (created_at, modified_at, modified_by, id, name, start_date, end_date, logo, color, homepage) FROM stdin;
\.


--
-- Data for Name: party_affiliation; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY party_affiliation (created_at, modified_at, modified_by, id, person_id, party_id, start_date, end_date) FROM stdin;
\.


--
-- Name: party_affiliation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('party_affiliation_id_seq', 1, false);


--
-- Name: party_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('party_id_seq', 1, false);


--
-- Data for Name: person; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY person (created_at, modified_at, modified_by, id, name, name_en, name_cn, gender, birthday, sites) FROM stdin;
\.


--
-- Name: person_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('person_id_seq', 1, false);


--
-- Data for Name: person_image; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY person_image (created_at, modified_at, modified_by, id, person_id, url) FROM stdin;
\.


--
-- Name: person_image_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('person_image_id_seq', 1, false);


--
-- Data for Name: pledge; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY pledge (created_at, modified_at, modified_by, id, candidacy_id, no, title, description) FROM stdin;
\.


--
-- Name: pledge_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('pledge_id_seq', 1, false);


--
-- Data for Name: region; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY region (created_at, modified_at, modified_by, id, parent_id, name, name_en, name_cn, fullname, fullname_en) FROM stdin;
\.


--
-- Data for Name: residence; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY residence (created_at, modified_at, modified_by, id, person_id, named_region_id) FROM stdin;
\.


--
-- Name: residence_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('residence_id_seq', 1, false);


--
-- Data for Name: school; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY school (created_at, modified_at, modified_by, id, name) FROM stdin;
\.


--
-- Name: school_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('school_id_seq', 1, false);


--
-- Name: assembly_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY assembly
    ADD CONSTRAINT assembly_pkey PRIMARY KEY (id);


--
-- Name: bill_keyword_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY bill_keyword
    ADD CONSTRAINT bill_keyword_pkey PRIMARY KEY (id);


--
-- Name: bill_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY bill
    ADD CONSTRAINT bill_pkey PRIMARY KEY (id);


--
-- Name: bill_process_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY bill_process
    ADD CONSTRAINT bill_process_pkey PRIMARY KEY (id);


--
-- Name: bill_status_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY bill_status
    ADD CONSTRAINT bill_status_pkey PRIMARY KEY (id);


--
-- Name: candidacy_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY candidacy
    ADD CONSTRAINT candidacy_pkey PRIMARY KEY (id);


--
-- Name: committee_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY committee
    ADD CONSTRAINT committee_pkey PRIMARY KEY (id);


--
-- Name: cosponsorship_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY cosponsorship
    ADD CONSTRAINT cosponsorship_pkey PRIMARY KEY (id);


--
-- Name: education_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY education
    ADD CONSTRAINT education_pkey PRIMARY KEY (id);


--
-- Name: election_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY election
    ADD CONSTRAINT election_pkey PRIMARY KEY (id);


--
-- Name: keyword_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY keyword
    ADD CONSTRAINT keyword_pkey PRIMARY KEY (id);


--
-- Name: named_region_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY named_region
    ADD CONSTRAINT named_region_pkey PRIMARY KEY (id);


--
-- Name: organization_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY organization
    ADD CONSTRAINT organization_pkey PRIMARY KEY (id);


--
-- Name: organization_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY organization_type
    ADD CONSTRAINT organization_type_pkey PRIMARY KEY (id);


--
-- Name: party_affiliation_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY party_affiliation
    ADD CONSTRAINT party_affiliation_pkey PRIMARY KEY (id);


--
-- Name: party_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY party
    ADD CONSTRAINT party_pkey PRIMARY KEY (id);


--
-- Name: person_image_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY person_image
    ADD CONSTRAINT person_image_pkey PRIMARY KEY (id);


--
-- Name: person_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY person
    ADD CONSTRAINT person_pkey PRIMARY KEY (id);


--
-- Name: pledge_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY pledge
    ADD CONSTRAINT pledge_pkey PRIMARY KEY (id);


--
-- Name: region_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY region
    ADD CONSTRAINT region_pkey PRIMARY KEY (id);


--
-- Name: residence_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY residence
    ADD CONSTRAINT residence_pkey PRIMARY KEY (id);


--
-- Name: school_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY school
    ADD CONSTRAINT school_pkey PRIMARY KEY (id);


--
-- Name: ix_assembly_session_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_assembly_session_id ON assembly USING btree (session_id);


--
-- Name: ix_bill_assembly_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_bill_assembly_id ON bill USING btree (assembly_id);


--
-- Name: ix_bill_created_at; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_bill_created_at ON bill USING btree (created_at);


--
-- Name: ix_bill_decision_date; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_bill_decision_date ON bill USING btree (decision_date);


--
-- Name: ix_bill_is_processed; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_bill_is_processed ON bill USING btree (is_processed);


--
-- Name: ix_bill_keyword_bill_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE UNIQUE INDEX ix_bill_keyword_bill_id ON bill_keyword USING btree (bill_id);


--
-- Name: ix_bill_keyword_created_at; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_bill_keyword_created_at ON bill_keyword USING btree (created_at);


--
-- Name: ix_bill_keyword_keyword_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE UNIQUE INDEX ix_bill_keyword_keyword_id ON bill_keyword USING btree (keyword_id);


--
-- Name: ix_bill_keyword_modified_at; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_bill_keyword_modified_at ON bill_keyword USING btree (modified_at);


--
-- Name: ix_bill_keyword_weight; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_bill_keyword_weight ON bill_keyword USING btree (weight);


--
-- Name: ix_bill_link_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_bill_link_id ON bill USING btree (link_id);


--
-- Name: ix_bill_modified_at; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_bill_modified_at ON bill USING btree (modified_at);


--
-- Name: ix_bill_name; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_bill_name ON bill USING btree (name);


--
-- Name: ix_bill_process_bill_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE UNIQUE INDEX ix_bill_process_bill_id ON bill_process USING btree (bill_id);


--
-- Name: ix_bill_process_created_at; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_bill_process_created_at ON bill_process USING btree (created_at);


--
-- Name: ix_bill_process_end_date; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_bill_process_end_date ON bill_process USING btree (end_date);


--
-- Name: ix_bill_process_modified_at; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_bill_process_modified_at ON bill_process USING btree (modified_at);


--
-- Name: ix_bill_process_order; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_bill_process_order ON bill_process USING btree ("order");


--
-- Name: ix_bill_process_start_date; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_bill_process_start_date ON bill_process USING btree (start_date);


--
-- Name: ix_bill_process_status_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE UNIQUE INDEX ix_bill_process_status_id ON bill_process USING btree (status_id);


--
-- Name: ix_bill_proposed_date; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_bill_proposed_date ON bill USING btree (proposed_date);


--
-- Name: ix_bill_status_created_at; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_bill_status_created_at ON bill_status USING btree (created_at);


--
-- Name: ix_bill_status_modified_at; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_bill_status_modified_at ON bill_status USING btree (modified_at);


--
-- Name: ix_bill_status_name; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_bill_status_name ON bill_status USING btree (name);


--
-- Name: ix_candidacy_created_at; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_candidacy_created_at ON candidacy USING btree (created_at);


--
-- Name: ix_candidacy_election_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE UNIQUE INDEX ix_candidacy_election_id ON candidacy USING btree (election_id);


--
-- Name: ix_candidacy_is_elected; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_candidacy_is_elected ON candidacy USING btree (is_elected);


--
-- Name: ix_candidacy_modified_at; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_candidacy_modified_at ON candidacy USING btree (modified_at);


--
-- Name: ix_candidacy_named_region_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_candidacy_named_region_id ON candidacy USING btree (named_region_id);


--
-- Name: ix_candidacy_party_affiliation_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE UNIQUE INDEX ix_candidacy_party_affiliation_id ON candidacy USING btree (party_affiliation_id);


--
-- Name: ix_committee_created_at; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_committee_created_at ON committee USING btree (created_at);


--
-- Name: ix_committee_modified_at; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_committee_modified_at ON committee USING btree (modified_at);


--
-- Name: ix_committee_name; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_committee_name ON committee USING btree (name);


--
-- Name: ix_cosponsorship_bill_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_cosponsorship_bill_id ON cosponsorship USING btree (bill_id);


--
-- Name: ix_cosponsorship_committee_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_cosponsorship_committee_id ON cosponsorship USING btree (committee_id);


--
-- Name: ix_cosponsorship_created_at; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_cosponsorship_created_at ON cosponsorship USING btree (created_at);


--
-- Name: ix_cosponsorship_is_agreement; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_cosponsorship_is_agreement ON cosponsorship USING btree (is_agreement);


--
-- Name: ix_cosponsorship_is_proposer; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_cosponsorship_is_proposer ON cosponsorship USING btree (is_proposer);


--
-- Name: ix_cosponsorship_is_withdrawn; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_cosponsorship_is_withdrawn ON cosponsorship USING btree (is_withdrawn);


--
-- Name: ix_cosponsorship_modified_at; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_cosponsorship_modified_at ON cosponsorship USING btree (modified_at);


--
-- Name: ix_cosponsorship_name; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_cosponsorship_name ON cosponsorship USING btree (name);


--
-- Name: ix_cosponsorship_party_affiliation_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_cosponsorship_party_affiliation_id ON cosponsorship USING btree (party_affiliation_id);


--
-- Name: ix_education_created_at; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_education_created_at ON education USING btree (created_at);


--
-- Name: ix_education_modified_at; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_education_modified_at ON education USING btree (modified_at);


--
-- Name: ix_education_order; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_education_order ON education USING btree ("order");


--
-- Name: ix_education_person_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_education_person_id ON education USING btree (person_id);


--
-- Name: ix_education_school_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_education_school_id ON education USING btree (school_id);


--
-- Name: ix_election_created_at; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_election_created_at ON election USING btree (created_at);


--
-- Name: ix_election_date; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_election_date ON election USING btree (date);


--
-- Name: ix_election_modified_at; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_election_modified_at ON election USING btree (modified_at);


--
-- Name: ix_election_organization_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_election_organization_id ON election USING btree (organization_id);


--
-- Name: ix_keyword_created_at; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_keyword_created_at ON keyword USING btree (created_at);


--
-- Name: ix_keyword_modified_at; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_keyword_modified_at ON keyword USING btree (modified_at);


--
-- Name: ix_keyword_name; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE UNIQUE INDEX ix_keyword_name ON keyword USING btree (name);


--
-- Name: ix_named_region_created_at; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_named_region_created_at ON named_region USING btree (created_at);


--
-- Name: ix_named_region_modified_at; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_named_region_modified_at ON named_region USING btree (modified_at);


--
-- Name: ix_named_region_name; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_named_region_name ON named_region USING btree (name);


--
-- Name: ix_named_region_region_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_named_region_region_id ON named_region USING btree (region_id);


--
-- Name: ix_organization_created_at; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_organization_created_at ON organization USING btree (created_at);


--
-- Name: ix_organization_end_date; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_organization_end_date ON organization USING btree (end_date);


--
-- Name: ix_organization_modified_at; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_organization_modified_at ON organization USING btree (modified_at);


--
-- Name: ix_organization_name; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_organization_name ON organization USING btree (name);


--
-- Name: ix_organization_start_date; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_organization_start_date ON organization USING btree (start_date);


--
-- Name: ix_organization_type_created_at; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_organization_type_created_at ON organization_type USING btree (created_at);


--
-- Name: ix_organization_type_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_organization_type_id ON organization USING btree (type_id);


--
-- Name: ix_organization_type_modified_at; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_organization_type_modified_at ON organization_type USING btree (modified_at);


--
-- Name: ix_organization_type_name; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_organization_type_name ON organization_type USING btree (name);


--
-- Name: ix_party_affiliation_created_at; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_party_affiliation_created_at ON party_affiliation USING btree (created_at);


--
-- Name: ix_party_affiliation_end_date; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_party_affiliation_end_date ON party_affiliation USING btree (end_date);


--
-- Name: ix_party_affiliation_modified_at; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_party_affiliation_modified_at ON party_affiliation USING btree (modified_at);


--
-- Name: ix_party_affiliation_party_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_party_affiliation_party_id ON party_affiliation USING btree (party_id);


--
-- Name: ix_party_affiliation_person_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_party_affiliation_person_id ON party_affiliation USING btree (person_id);


--
-- Name: ix_party_affiliation_start_date; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_party_affiliation_start_date ON party_affiliation USING btree (start_date);


--
-- Name: ix_party_created_at; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_party_created_at ON party USING btree (created_at);


--
-- Name: ix_party_end_date; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_party_end_date ON party USING btree (end_date);


--
-- Name: ix_party_modified_at; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_party_modified_at ON party USING btree (modified_at);


--
-- Name: ix_party_name; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_party_name ON party USING btree (name);


--
-- Name: ix_party_start_date; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_party_start_date ON party USING btree (start_date);


--
-- Name: ix_person_birthday; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_person_birthday ON person USING btree (birthday);


--
-- Name: ix_person_created_at; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_person_created_at ON person USING btree (created_at);


--
-- Name: ix_person_gender; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_person_gender ON person USING btree (gender);


--
-- Name: ix_person_image_created_at; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_person_image_created_at ON person_image USING btree (created_at);


--
-- Name: ix_person_image_modified_at; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_person_image_modified_at ON person_image USING btree (modified_at);


--
-- Name: ix_person_image_person_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_person_image_person_id ON person_image USING btree (person_id);


--
-- Name: ix_person_modified_at; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_person_modified_at ON person USING btree (modified_at);


--
-- Name: ix_person_name; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_person_name ON person USING btree (name);


--
-- Name: ix_person_name_en; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_person_name_en ON person USING btree (name_en);


--
-- Name: ix_pledge_candidacy_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_pledge_candidacy_id ON pledge USING btree (candidacy_id);


--
-- Name: ix_pledge_created_at; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_pledge_created_at ON pledge USING btree (created_at);


--
-- Name: ix_pledge_modified_at; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_pledge_modified_at ON pledge USING btree (modified_at);


--
-- Name: ix_pledge_no; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_pledge_no ON pledge USING btree (no);


--
-- Name: ix_region_created_at; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_region_created_at ON region USING btree (created_at);


--
-- Name: ix_region_fullname; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_region_fullname ON region USING btree (fullname);


--
-- Name: ix_region_modified_at; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_region_modified_at ON region USING btree (modified_at);


--
-- Name: ix_region_name; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_region_name ON region USING btree (name);


--
-- Name: ix_region_parent_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_region_parent_id ON region USING btree (parent_id);


--
-- Name: ix_residence_created_at; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_residence_created_at ON residence USING btree (created_at);


--
-- Name: ix_residence_modified_at; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_residence_modified_at ON residence USING btree (modified_at);


--
-- Name: ix_residence_named_region_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_residence_named_region_id ON residence USING btree (named_region_id);


--
-- Name: ix_residence_person_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_residence_person_id ON residence USING btree (person_id);


--
-- Name: ix_school_created_at; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_school_created_at ON school USING btree (created_at);


--
-- Name: ix_school_modified_at; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_school_modified_at ON school USING btree (modified_at);


--
-- Name: ix_school_name; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX ix_school_name ON school USING btree (name);


--
-- Name: assembly_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY assembly
    ADD CONSTRAINT assembly_id_fkey FOREIGN KEY (id) REFERENCES organization(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: bill_assembly_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY bill
    ADD CONSTRAINT bill_assembly_id_fkey FOREIGN KEY (assembly_id) REFERENCES assembly(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: bill_keyword_bill_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY bill_keyword
    ADD CONSTRAINT bill_keyword_bill_id_fkey FOREIGN KEY (bill_id) REFERENCES bill(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: bill_keyword_keyword_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY bill_keyword
    ADD CONSTRAINT bill_keyword_keyword_id_fkey FOREIGN KEY (keyword_id) REFERENCES keyword(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: bill_process_bill_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY bill_process
    ADD CONSTRAINT bill_process_bill_id_fkey FOREIGN KEY (bill_id) REFERENCES bill(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: bill_process_status_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY bill_process
    ADD CONSTRAINT bill_process_status_id_fkey FOREIGN KEY (status_id) REFERENCES bill_status(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: candidacy_election_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY candidacy
    ADD CONSTRAINT candidacy_election_id_fkey FOREIGN KEY (election_id) REFERENCES election(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: candidacy_named_region_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY candidacy
    ADD CONSTRAINT candidacy_named_region_id_fkey FOREIGN KEY (named_region_id) REFERENCES named_region(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: candidacy_party_affiliation_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY candidacy
    ADD CONSTRAINT candidacy_party_affiliation_id_fkey FOREIGN KEY (party_affiliation_id) REFERENCES party_affiliation(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: cosponsorship_bill_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY cosponsorship
    ADD CONSTRAINT cosponsorship_bill_id_fkey FOREIGN KEY (bill_id) REFERENCES bill(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: cosponsorship_committee_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY cosponsorship
    ADD CONSTRAINT cosponsorship_committee_id_fkey FOREIGN KEY (committee_id) REFERENCES committee(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: cosponsorship_party_affiliation_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY cosponsorship
    ADD CONSTRAINT cosponsorship_party_affiliation_id_fkey FOREIGN KEY (party_affiliation_id) REFERENCES party_affiliation(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: education_person_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY education
    ADD CONSTRAINT education_person_id_fkey FOREIGN KEY (person_id) REFERENCES person(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: education_school_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY education
    ADD CONSTRAINT education_school_id_fkey FOREIGN KEY (school_id) REFERENCES school(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: election_organization_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY election
    ADD CONSTRAINT election_organization_id_fkey FOREIGN KEY (organization_id) REFERENCES organization(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: named_region_region_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY named_region
    ADD CONSTRAINT named_region_region_id_fkey FOREIGN KEY (region_id) REFERENCES region(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: organization_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY organization
    ADD CONSTRAINT organization_type_id_fkey FOREIGN KEY (type_id) REFERENCES organization_type(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: party_affiliation_party_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY party_affiliation
    ADD CONSTRAINT party_affiliation_party_id_fkey FOREIGN KEY (party_id) REFERENCES party(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: party_affiliation_person_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY party_affiliation
    ADD CONSTRAINT party_affiliation_person_id_fkey FOREIGN KEY (person_id) REFERENCES person(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: person_image_person_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY person_image
    ADD CONSTRAINT person_image_person_id_fkey FOREIGN KEY (person_id) REFERENCES person(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: pledge_candidacy_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY pledge
    ADD CONSTRAINT pledge_candidacy_id_fkey FOREIGN KEY (candidacy_id) REFERENCES candidacy(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: region_parent_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY region
    ADD CONSTRAINT region_parent_id_fkey FOREIGN KEY (parent_id) REFERENCES region(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: residence_named_region_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY residence
    ADD CONSTRAINT residence_named_region_id_fkey FOREIGN KEY (named_region_id) REFERENCES named_region(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: residence_person_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY residence
    ADD CONSTRAINT residence_person_id_fkey FOREIGN KEY (person_id) REFERENCES person(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

