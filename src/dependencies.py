from typing import Optional

from fastapi import Query
from sqlalchemy.orm import Session

from database import SessionLocalLive
from pagination import PaginationParams


def get_live_db_session() -> Session:
    """
    It is used as a FastAPI dependency. Creates a new connection to the database.
    """
    session = SessionLocalLive(expire_on_commit=True)
    try:
        yield session
    finally:
        session.close()


def get_pagination_params(
        skip: Optional[int] = Query(0, ge=0),
        limit: Optional[int] = Query(10, ge=1, le=100)
) -> PaginationParams:
    return PaginationParams(skip=skip, limit=limit)
