CREATE TYPE fields_e AS ENUM (
    'elec',
    'video',
    'audio',
    'gps',
    'board',
    'internet',
    'connect'
);

CREATE TABLE dico (
    id      bigserial NOT NULL,
    fields  fields_e[] NOT NULL,
    name    varchar(64) NOT NULL,
    def     text NOT NULL,
    url     varchar(256)
);
