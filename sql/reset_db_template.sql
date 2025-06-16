-- End active connections to the datebase, if there are any
DO
$$
BEGIN
   IF EXISTS (SELECT FROM pg_database WHERE datname = '$DB_NAME') THEN
      PERFORM pg_terminate_backend(pid)
      FROM pg_stat_activity
      WHERE datname = '$DB_NAME' AND pid <> pg_backend_pid();
   END IF;
END
$$;

-- Drop the database and user if they exist
DROP DATABASE IF EXISTS $DB_NAME;

DO
$$
BEGIN
   IF EXISTS (SELECT FROM pg_roles WHERE rolname = '$DB_USER') THEN
      DROP ROLE $DB_USER;
   END IF;
END
$$;

-- Create a new user and database
CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';
CREATE DATABASE $DB_NAME OWNER $DB_USER;
GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;
