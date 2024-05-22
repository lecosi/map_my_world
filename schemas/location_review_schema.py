from pydantic import BaseModel


class CreateLocationReviewModel(BaseModel):
    location_id: int
    category_id: int
