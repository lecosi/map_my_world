from typing import Optional

from pydantic import BaseModel, field_validator


class CreateCategoryModel(BaseModel):
    name: str
    is_active: bool = True

    @field_validator("name")
    @classmethod
    def validate_name(cls, name: str) -> Optional[str]:
        if name.isdigit():
            raise ValueError('category name must have letters')

        return name.upper()
