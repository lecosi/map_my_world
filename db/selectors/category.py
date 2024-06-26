from typing import Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from db.connection import get_database_session
from db.models import Category


def get_category_by_name(
    *,
    name: str,
    session_db: Session
) -> Optional[Category]:
    query = select(Category).where(Category.name == name)
    return session_db.execute(query).first()


def get_category_by_id(
    *,
    id: int,
    session_db: Session
) -> Optional[Category]:
    query = select(Category).where(id == id)
    return session_db.execute(query).first()
