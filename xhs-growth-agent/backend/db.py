from contextlib import contextmanager
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from .config import DATABASE_URL

class Base(DeclarativeBase):
    pass

def make_engine(url=DATABASE_URL):
    engine = create_engine(url, connect_args={"check_same_thread": False} if url.startswith("sqlite") else {})
    if url.startswith("sqlite"):
        from sqlalchemy import event
        @event.listens_for(engine, "connect")
        def sqlite_setup(connection, _):
            connection.execute("PRAGMA foreign_keys=ON")
            connection.execute("PRAGMA busy_timeout=5000")
            connection.execute("PRAGMA journal_mode=WAL")
    return engine

engine = make_engine()
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

def migrate(target=engine):
    from . import models  # registers all domain entities
    Base.metadata.create_all(target)
    with target.begin() as connection:
        connection.execute(text("CREATE TABLE IF NOT EXISTS schema_version (version INTEGER PRIMARY KEY, applied_at TEXT NOT NULL)"))
        connection.execute(text("INSERT OR IGNORE INTO schema_version VALUES (1, CURRENT_TIMESTAMP)"))
        columns = {column["name"] for column in inspect(connection).get_columns("publish_authorizations")}
        for name in ("account_id", "account_name"):
            if name not in columns:
                connection.execute(text(f"ALTER TABLE publish_authorizations ADD COLUMN {name} VARCHAR NOT NULL DEFAULT ''"))
        # Legacy authorizations have no verified account binding and cannot authorize a write.
        connection.execute(text("UPDATE publish_authorizations SET valid = 0 WHERE account_id = ''"))
        connection.execute(text("INSERT OR IGNORE INTO schema_version VALUES (2, CURRENT_TIMESTAMP)"))
        if "policy" not in columns:
            connection.execute(text("ALTER TABLE publish_authorizations ADD COLUMN policy VARCHAR NOT NULL DEFAULT 'manual'"))
        connection.execute(text("INSERT OR IGNORE INTO schema_version VALUES (3, CURRENT_TIMESTAMP)"))

@contextmanager
def session_scope():
    with SessionLocal() as session:
        yield session

def get_db():
    with SessionLocal() as session:
        yield session
