from typing import Optional, List
from datetime import datetime, timedelta

from sqlalchemy import select, func, asc
from sqlalchemy.orm import Session
from db.models import LocationCategoryReviewed, Category, Location
from db.selectors.constants import MAX_LIMIT_RECORDS_PER_REVIEW, \
    MAX_DAYS_PER_REVIEW


def get_location_review_by_params(
    *,
    location_id: int,
    category_id: int,
    session_db: Session
) -> Optional[LocationCategoryReviewed]:
    query = select(LocationCategoryReviewed).where(
        LocationCategoryReviewed.location_id == location_id,
        LocationCategoryReviewed.category_id == category_id
    )
    return session_db.execute(query).first()


def get_location_review_list(
    *,
    session_db: Session
) -> Optional[List[LocationCategoryReviewed]]:
    date_now = datetime.now()
    limit_date = (date_now - timedelta(days=MAX_DAYS_PER_REVIEW)).date()
    formatted_date = limit_date.strftime('%Y-%m-%d')
    query = session_db.query(
        LocationCategoryReviewed.id,
        LocationCategoryReviewed.created_at,
        LocationCategoryReviewed.is_active,
        LocationCategoryReviewed.last_verification_date,
        Category.name,
        Location.latitude,
        Location.longitude,
        Location.id,
        Category.id
    ).select_from(
        LocationCategoryReviewed
    ).join(Category).join(
        Location, Location.id == LocationCategoryReviewed.location_id
    ).filter(
        LocationCategoryReviewed.is_active == True,
        func.DATE(LocationCategoryReviewed.last_verification_date) <= formatted_date
    ).group_by(
        LocationCategoryReviewed.id, Category.id, Location.id
    ).order_by(
        asc(LocationCategoryReviewed.last_verification_date)
    ).limit(MAX_LIMIT_RECORDS_PER_REVIEW).all()

    return query
