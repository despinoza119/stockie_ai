-- Description: Bootstrap extensions for the stockie_ai database.
--              Runs automatically on first container start (docker-entrypoint-initdb.d).
--              TimescaleDB must be in shared_preload_libraries — the official image
--              handles this; no manual postgresql.conf edit needed.
-- Last Modified By: bvela
-- Created: 2026-05-22
-- Last Modified:
--     2026-05-22 - File created; enabled timescaledb extension.

CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;
