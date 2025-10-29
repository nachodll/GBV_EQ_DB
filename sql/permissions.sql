------------------------------------------------------------------------------------
-- Grant permissions to readonly user over all schemas
------------------------------------------------------------------------------------
DO $$
DECLARE
    schema_rec RECORD;
BEGIN
    FOR schema_rec IN
        SELECT schema_name
        FROM information_schema.schemata
        WHERE schema_name NOT IN ('pg_catalog', 'information_schema')
    LOOP
        EXECUTE format('GRANT USAGE ON SCHEMA %I TO gbv_db_user_readonly;', schema_rec.schema_name);
        EXECUTE format('GRANT SELECT ON ALL TABLES IN SCHEMA %I TO gbv_db_user_readonly;', schema_rec.schema_name);
        EXECUTE format('GRANT SELECT ON ALL SEQUENCES IN SCHEMA %I TO gbv_db_user_readonly;', schema_rec.schema_name);
        EXECUTE format('ALTER DEFAULT PRIVILEGES IN SCHEMA %I GRANT SELECT ON TABLES TO gbv_db_user_readonly;', schema_rec.schema_name);
    END LOOP;
END
$$;