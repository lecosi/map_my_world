from datetime import datetime

from pydantic import BaseModel


class CreateLocationReviewModel(BaseModel):
    location_id: int
    category_id: int


class UpdateLocationReviewModel(BaseModel):
    is_valid: bool = False


class GetLocationReviewModel(BaseModel):
    id: int
    created_at: datetime
    is_active: bool
    category_name: str
    latitude: float
    longitude: float
    last_verification_date: datetime = None
