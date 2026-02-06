# Alembic migrations (T006)

Add `sqlalchemy.url` in alembic.ini or set env for DATABASE_URL.
Create first revision: `alembic revision -m "initial"` then add table definitions in upgrade().
