from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

from sqlalchemy.orm import Session

from db.models import LocationCategoryReviewed
from schemas.location_review_schema import CreateLocationReviewModel


class LocationReviewBase(ABC):
    @abstractmethod
    def create(self, data: Dict[str, Any]):
        pass


class LocationReviewController(LocationReviewBase):
    def __init__(self, session: Session):
        self._db_connection = session

    def create(
        self,
        data: CreateLocationReviewModel
    ) -> Optional[LocationCategoryReviewed]:

        new_location = LocationCategoryReviewed(

            category_id=data.category_id
        )
        self._db_connection.add(new_location)
        self._db_connection.commit()
        self._db_connection.refresh(new_location)
        return new_location


