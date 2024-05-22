from typing import Optional

from pydantic import BaseModel, field_validator


class CreateLocationModel(BaseModel):
    name: str
    latitude: float
    longitude: float
    category_id: int

    @field_validator("name")
    @classmethod
    def validate_name(cls, name: str) -> Optional[str]:
        if name.isdigit():
            raise ValueError('location name must have letters')

        return name.upper()
