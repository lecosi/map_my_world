from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List

from sqlalchemy.orm import Session

from db.models import LocationCategoryReviewed
from db.selectors.location_review import get_location_review_by_params, \
    get_location_review_list
from schemas.location_review_schema import CreateLocationReviewModel, \
    UpdateLocationReviewModel, GetLocationReviewModel


class LocationReviewBase(ABC):

    @abstractmethod
    def get_data_list(self):
        pass

    @abstractmethod
    def create(self, data: Dict[str, Any]):
        pass

    @abstractmethod
    def update(self, data: Dict[str, Any]):
        pass


class LocationReviewCrudController(LocationReviewBase):
    def __init__(self, session: Session):
        self._db_connection = session

    def validate_and_create(
        self,
        location_review_data: CreateLocationReviewModel,
    ) -> Optional[LocationCategoryReviewed]:
        location_review_qs = get_location_review_by_params(
            location_id=location_review_data.location_id,
            category_id=location_review_data.category_id,
            session_db=self._db_connection
        )
        if location_review_qs:
            return

        return self.create(data=location_review_data)

    def create(
        self,
        data: CreateLocationReviewModel
    ) -> Optional[LocationCategoryReviewed]:

        new_location = LocationCategoryReviewed(
            location_id=data.location_id,
            category_id=data.category_id
        )
        self._db_connection.add(new_location)
        self._db_connection.commit()
        self._db_connection.refresh(new_location)
        return new_location

    def update(self, data: UpdateLocationReviewModel):
        pass

    def get_data_list(self) -> Optional[List[GetLocationReviewModel]]:
        location_review_lst = get_location_review_list(
            session_db=self._db_connection
        )
        result = []
        for location_review in location_review_lst:
            data = GetLocationReviewModel(
                id=location_review[0],
                created_at=location_review[1],
                is_active=location_review[2],
                last_verification_date=location_review[3],
                category_name=location_review[4],
                latitude=location_review[5],
                longitude=location_review[6]
            )
            result.append(data)
        return result
