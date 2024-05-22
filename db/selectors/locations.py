
from typing import Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from db.connection import get_database_session
from db.models import Location


def get_location_by_params(
    name: str,
    latitude: float,
    longitude: float,
    session_db: Session = Depends(get_database_session)
) -> Optional[Location]:
    query = select(Location).where(
        Location.name == name,
        Location.latitude == latitude,
        Location.longitude == longitude
    )
    return session_db.execute(query).first()
