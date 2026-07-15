"""Idempotent database bootstrap for deployable HosPrime runtimes.

This module intentionally does not drop tables or load demo institutional data.
It creates missing schema objects, enables required extensions, and creates the
initial administrator only when that account does not already exist.
"""

import logging

from sqlalchemy.orm import Session

from backend.app.auth import get_password_hash
from backend.app.core.config import settings
from backend.app.db.bootstrap import ensure_database_extensions
from backend.app.db.models import Base, User as DBUser
from backend.app.db.session import SessionLocal, engine


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def ensure_schema() -> None:
    """Create missing schema objects without deleting existing data."""
    ensure_database_extensions()
    Base.metadata.create_all(bind=engine)
    logger.info("Database schema is ready; existing tables and data were preserved.")


def ensure_bootstrap_admin(db: Session) -> bool:
    """Create the configured bootstrap administrator once.

    Existing credentials are never overwritten during container restart. Future
    password rotation must use an explicit administrative workflow.
    """
    username = settings.BOOTSTRAP_ADMIN_USERNAME.strip()
    existing = db.query(DBUser).filter(DBUser.username == username).first()
    if existing:
        logger.info("Bootstrap administrator already exists; credentials unchanged.")
        return False

    db.add(
        DBUser(
            username=username,
            hashed_password=get_password_hash(settings.BOOTSTRAP_ADMIN_PASSWORD),
            role="admin",
            department="IT",
            confidentiality_level="Confidential",
        )
    )
    db.commit()
    logger.info("Bootstrap administrator created from runtime configuration.")
    return True


def bootstrap_runtime() -> None:
    fatal_issues = settings.fatal_configuration_issues()
    if fatal_issues:
        raise RuntimeError(
            "Unsafe runtime configuration: " + "; ".join(fatal_issues)
        )

    ensure_schema()
    db: Session = SessionLocal()
    try:
        ensure_bootstrap_admin(db)
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    bootstrap_runtime()
