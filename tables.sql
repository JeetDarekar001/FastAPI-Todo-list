-- If database if sqlite3 then create todos.db and trigger the below query.
-- Uncomment the lines 6 to 11 in database.py to connect to todos.db
CREATE TABLE users (
        id INTEGER NOT NULL, 
        email VARCHAR, 
        username VARCHAR, 
        firstname VARCHAR, 
        lastname VARCHAR, 
        hashedpassword VARCHAR, 
        is_active BOOLEAN, 
        PRIMARY KEY (id)
);
CREATE INDEX ix_users_id ON users (id);
CREATE UNIQUE INDEX ix_users_username ON users (username);
CREATE UNIQUE INDEX ix_users_email ON users (email);
CREATE TABLE todos (
        id INTEGER NOT NULL, 
        title VARCHAR, 
        description VARCHAR, 
        priority INTEGER, 
        complete BOOLEAN, 
        owner_id INTEGER, 
        PRIMARY KEY (id), 
        FOREIGN KEY(owner_id) REFERENCES users (id)
);
CREATE INDEX ix_todos_id ON todos (id);

-- Below lines should be used when connecting to PostgreSQL.
-- 

CREATE TABLE IF NOT EXISTS public.todos
(
    id integer NOT NULL DEFAULT nextval('todos_id_seq'::regclass),
    title character varying(200) COLLATE pg_catalog."default" DEFAULT NULL::character varying,
    description character varying(200) COLLATE pg_catalog."default" DEFAULT NULL::character varying,
    priority integer,
    complete boolean,
    owner_id integer,
    CONSTRAINT todos_pkey PRIMARY KEY (id),
    CONSTRAINT todos_owner_id_fkey FOREIGN KEY (owner_id)
        REFERENCES public.users (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)


-- DROP TABLE IF EXISTS public.users;

CREATE TABLE IF NOT EXISTS public.users
(
    id integer NOT NULL DEFAULT nextval('users_id_seq'::regclass),
    email character varying(200) COLLATE pg_catalog."default" DEFAULT NULL::character varying,
    username character varying(45) COLLATE pg_catalog."default" DEFAULT NULL::character varying,
    firstname character varying(45) COLLATE pg_catalog."default" DEFAULT NULL::character varying,
    lastname character varying(45) COLLATE pg_catalog."default" DEFAULT NULL::character varying,
    hashedpassword character varying(200) COLLATE pg_catalog."default" DEFAULT NULL::character varying,
    is_active boolean,
    CONSTRAINT users_pkey PRIMARY KEY (id)
)
