GRANT CONNECT ON DATABASE sem2025_kosmrma TO javnost;

GRANT USAGE ON SCHEMA public TO javnost;

GRANT ALL ON ALL TABLES IN SCHEMA public TO javnost;


ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO javnost;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO javnost;