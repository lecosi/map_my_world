import logging

from fastapi import FastAPI, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session

from controllers.category_controller import CategoryCrudController
from controllers.location_controller import LocationCrudController
from controllers.location_review_controller import LocationReviewCrudController
from db.connection import get_database_session
from schemas.category_schema import CreateCategoryModel
from schemas.location_schema import CreateLocationModel
from schemas.location_review_schema import CreateLocationReviewModel

logger = logging.getLogger(__name__)

app = FastAPI()


@app.get('/')
def home():
    return {"message": "Hello World"}


@app.get('/exploration-recommender', tags=['LocationReview'])
def get_recommendation(
    session_db: Session = Depends(get_database_session)
):
    location_review = LocationReviewCrudController(session=session_db)
    return location_review.get_data_list()
    """try:
        location_review = LocationReviewCrudController(session=session_db)
        return location_review.get_data_list()
    except ValueError as e:
        return HTTPException(status.HTTP_400_BAD_REQUEST, e)

    except Exception as e:
        logger.error(f'API :: get_recommendation :: {e}')
        msg = \
            'there is a problem when get recommendation list, try again later'
        return HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, msg)"""


@app.post('/category', tags=['Category'])
def create_category(
    category_data: CreateCategoryModel,
    session_db: Session = Depends(get_database_session)
):
    category_control = CategoryCrudController(session=session_db)
    try:
        category_control.validate_and_create(
            category_data=category_data
        )
    except ValueError as e:
        return HTTPException(status.HTTP_400_BAD_REQUEST, e)

    except Exception as e:
        logger.error(f'API :: create_category :: {e}')
        msg = 'there is a problem when creating a category, try again later'
        return HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, msg)

    return Response(status_code=status.HTTP_201_CREATED)


@app.post('/location', tags=['Location'])
def create_location(
    location_data: CreateLocationModel,
    session_db: Session = Depends(get_database_session)
):
    location_control = LocationCrudController(session=session_db)
    location_review_control = LocationReviewCrudController(session=session_db)
    try:
        new_location = location_control.validate_and_create(
            location_data=location_data
        )
        location_review_data = CreateLocationReviewModel(
            location_id=new_location.id,
            category_id=new_location.category_id
        )
        location_review_control.validate_and_create(
            location_review_data=location_review_data
        )
    except ValueError as e:
        return HTTPException(status.HTTP_400_BAD_REQUEST, e.args[0])

    except Exception as e:
        logger.error(f'API :: create_location :: {e}')
        msg = 'there is a problem when creating a location, try again later'
        return HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, msg)

    return Response(status_code=status.HTTP_201_CREATED)
