CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS stats (
    num_apikeys INTEGER NOT NULL DEFAULT 0,
    num_models INTEGER NOT NULL DEFAULT 0,
    num_actions INTEGER NOT NULL DEFAULT 0,
    num_collections INTEGER NOT NULL DEFAULT 0,
    num_records INTEGER NOT NULL DEFAULT 0,
    num_chunks INTEGER NOT NULL DEFAULT 0,
    created_timestamp BIGINT NOT NULL DEFAULT (EXTRACT(EPOCH FROM NOW()) * 1000)::BIGINT
);


CREATE TABLE IF NOT EXISTS app_admin (
    admin_id CHAR(16) PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    salt TEXT NOT NULL,
    password_hash TEXT NOT NULL ,
    token TEXT,
    created_timestamp BIGINT NOT NULL DEFAULT (EXTRACT(EPOCH FROM NOW()) * 1000)::BIGINT,
    updated_timestamp BIGINT NOT NULL DEFAULT (EXTRACT(EPOCH FROM NOW()) * 1000)::BIGINT
);


CREATE TABLE IF NOT EXISTS apikey (
    apikey_id CHAR(8) PRIMARY KEY,
    apikey TEXT NOT NULL UNIQUE, -- todo: secret apikey
    name TEXT NOT NULL,
    created_timestamp BIGINT NOT NULL DEFAULT (EXTRACT(EPOCH FROM NOW()) * 1000)::BIGINT,
    updated_timestamp BIGINT NOT NULL DEFAULT (EXTRACT(EPOCH FROM NOW()) * 1000)::BIGINT
);


CREATE TABLE IF NOT EXISTS model (
    model_id CHAR(8) NOT NULL PRIMARY KEY,
    model_schema_id TEXT NOT NULL,
    provider_id TEXT NOT NULL,
    provider_model_id TEXT NOT NULL,
    name TEXT NOT NULL,
    encrypted_credentials JSONB NOT NULL,
    display_credentials JSONB NOT NULL,
    -- todo: add metadata
    created_timestamp BIGINT NOT NULL DEFAULT (EXTRACT(EPOCH FROM NOW()) * 1000)::BIGINT,
    updated_timestamp BIGINT NOT NULL DEFAULT (EXTRACT(EPOCH FROM NOW()) * 1000)::BIGINT
);


CREATE TABLE IF NOT EXISTS action (
    action_id CHAR(24) NOT NULL PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    openapi_schema JSONB NOT NULL,
    authentication JSONB NOT NULL DEFAULT '{}',
    -- todo: add metadata
    created_timestamp BIGINT NOT NULL DEFAULT (EXTRACT(EPOCH FROM NOW()) * 1000)::BIGINT,
    updated_timestamp BIGINT NOT NULL DEFAULT (EXTRACT(EPOCH FROM NOW()) * 1000)::BIGINT
);


CREATE TABLE IF NOT EXISTS collection (
    collection_id CHAR(24) PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    num_chunks INTEGER NOT NULL DEFAULT 0,
    num_records INTEGER NOT NULL DEFAULT 0,
    capacity INTEGER NOT NULL,
    embedding_model_id CHAR(8) NOT NULL REFERENCES model (model_id) ON DELETE CASCADE,
    embedding_size INTEGER NOT NULL,
    text_splitter JSONB NOT NULL,
    status TEXT NOT NULL,
    metadata JSONB NOT NULL DEFAULT '{}',
    created_timestamp BIGINT NOT NULL DEFAULT (EXTRACT(EPOCH FROM NOW()) * 1000)::BIGINT,
    updated_timestamp BIGINT NOT NULL DEFAULT (EXTRACT(EPOCH FROM NOW()) * 1000)::BIGINT
);


CREATE TABLE IF NOT EXISTS record (
    collection_id CHAR(24) NOT NULL REFERENCES collection (collection_id) ON DELETE CASCADE,
    record_id CHAR(24) NOT NULL ,
    num_chunks INTEGER NOT NULL DEFAULT 0,
    title TEXT NOT NULL,
    type TEXT NOT NULL,
    content TEXT NOT NULL,
    status TEXT NOT NULL,
    metadata JSONB NOT NULL DEFAULT '{}',
    created_timestamp BIGINT NOT NULL DEFAULT (EXTRACT(EPOCH FROM NOW()) * 1000)::BIGINT,
    updated_timestamp BIGINT NOT NULL DEFAULT (EXTRACT(EPOCH FROM NOW()) * 1000)::BIGINT,
    PRIMARY KEY (collection_id, record_id)
);


--todo: index on created_timestamp and name for each table