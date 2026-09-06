-- 02_create_schema.sql
-- Creates the sentinel schema used by all SENTINEL tables.

CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE SCHEMA IF NOT EXISTS sentinel;

SET search_path TO sentinel, public;
