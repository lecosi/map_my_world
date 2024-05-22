
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

from sqlalchemy.orm import Session

from db.models import Location
from db.selectors.location import get_location_by_params
from schemas.location_schema import CreateLocationModel


class LocationBase(ABC):
    @abstractmethod
    def create(self, data: Dict[str, Any]):
        pass


class LocationCrudController(LocationBase):
    def __init__(self, session: Session):
        self._db_connection = session

    def validate_and_create(
        self,
        location_data: CreateLocationModel,
    ) -> Optional[Location]:

        location_qs = get_location_by_params(
            name=location_data.name,
            latitude=location_data.latitude,
            longitude=location_data.longitude,
            session_db=self._db_connection
        )
        if location_qs:
            return

        return self.create(data=location_data)

    def create(
        self,
        data: CreateLocationModel
    ) -> Optional[Location]:
        try:
            new_location = Location(
                name=data.name,
                latitude=data.latitude,
                longitude=data.longitude,
                category_id=data.category_id
            )
            self._db_connection.add(new_location)
            self._db_connection.commit()
            self._db_connection.refresh(new_location)
            return new_location

        except Exception:
            raise ValueError('category does not exists')
