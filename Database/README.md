# SENTINEL PostgreSQL Database

This folder contains the production-oriented PostgreSQL schema for the SENTINEL cybersecurity intelligence platform. It is intentionally aligned to the existing backend concepts already used by the repository, while preserving the SENTINEL-specific intelligence architecture described in the specification.

## Database and schema

- Database: `sentinel_db`
- Schema: `sentinel`

## Execution order

1. `01_create_database.sql`
2. `02_create_schema.sql`
3. `03_create_enums.sql`
4. `04_create_tables.sql`
5. `05_create_indexes.sql`
6. `06_create_constraints.sql`
7. `07_seed_demo_data.sql`

## Initialize

Connect as a PostgreSQL superuser or a role with database creation rights and run the files in order:

```bash
psql -U postgres -f 01_create_database.sql
psql -U postgres -d sentinel_db -f 02_create_schema.sql
psql -U postgres -d sentinel_db -f 03_create_enums.sql
psql -U postgres -d sentinel_db -f 04_create_tables.sql
psql -U postgres -d sentinel_db -f 05_create_indexes.sql
psql -U postgres -d sentinel_db -f 06_create_constraints.sql
psql -U postgres -d sentinel_db -f 07_seed_demo_data.sql
```

## Notes

- All timestamps use `TIMESTAMPTZ` and UTC-aware values.
- Score values are normalized to a 0-100 range for consistency.
- The design avoids generic over-modeling and stays focused on the SENTINEL intelligence and response flow.
- The schema is intentionally compatible with the repository’s existing backend concepts for devices, security events, behavioral baselines, assumptions, and attack flow analysis.

## Compatibility note

The current backend models in the repository are a simplified subset of a broader security system. This SQL design preserves the relevant field naming and intelligence concepts without duplicating unrelated application tables. The schema intentionally does not invent a second generic user or auth model in the `sentinel` schema.
