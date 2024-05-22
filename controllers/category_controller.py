
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

from sqlalchemy.orm import Session

from db.models import Category
from db.selectors.category import get_category_by_name
from schemas.category_schema import CreateCategoryModel


class CategoryBase(ABC):
    @abstractmethod
    def create(self, data: Dict[str, Any]):
        pass


class CategoryCrudController(CategoryBase):
    def __init__(self, session: Session):
        self._db_connection = session

    def validate_and_create(
        self,
        category_data: CreateCategoryModel,
    ) -> Optional[Category]:
        category_qs = get_category_by_name(
            name=category_data.name,
            session_db=self._db_connection
        )
        if category_qs:
            return

        return self.create(data=category_data)

    def create(self, data: CreateCategoryModel) -> Optional[Category]:
        new_category = Category(is_active=data.is_active, name=data.name)
        self._db_connection.add(new_category)
        self._db_connection.commit()
        self._db_connection.refresh(new_category)
        return new_category
