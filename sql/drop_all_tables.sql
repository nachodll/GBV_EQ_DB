DO $$
DECLARE
    rec record;
BEGIN
    FOR rec IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP
        EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(rec.tablename) || ' CASCADE';
    END LOOP;
END $$;