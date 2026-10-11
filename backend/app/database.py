from sqlalchemy import create_engine, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings


def _sqlite_path(url: str) -> str | None:
    if not url.startswith("sqlite:"):
        return None
    return url.split("///", 1)[-1]


_db_file = _sqlite_path(settings.database_url)
if _db_file:
    from pathlib import Path

    Path(_db_file).parent.mkdir(parents=True, exist_ok=True)

_connect_args = {"check_same_thread": False} if _db_file else {}
engine = create_engine(settings.database_url, pool_pre_ping=not _db_file, connect_args=_connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


def ensure_schema() -> None:
    if engine.dialect.name != "postgresql":
        return
    with engine.begin() as connection:
        connection.execute(text("ALTER TABLE products ADD COLUMN IF NOT EXISTS details TEXT DEFAULT '{}'"))
        connection.execute(text("ALTER TABLE services ADD COLUMN IF NOT EXISTS image_url VARCHAR(500) DEFAULT ''"))
        connection.execute(text("ALTER TABLE services ADD COLUMN IF NOT EXISTS slug VARCHAR(200) DEFAULT ''"))
        connection.execute(text("ALTER TABLE services ADD COLUMN IF NOT EXISTS details TEXT DEFAULT '{}'"))


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
