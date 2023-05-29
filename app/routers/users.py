"""
Module responsible for User related operations
"""


from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.utils import hash
from db import models, schemas
from db.db_orm import database_gen

#################################        Router        ################################
router = APIRouter(prefix="/users")


#################################        User Endpoints        ################################
@router.get("/", response_model=models.UserResponse | list[models.UserResponse])
def get_user(email: str | None = None, db_session: Session = Depends(database_gen)):
    """
    Creates endpoint to fetch specific user information, or all users if email is None
    """
    if email is None:
        users = db_session.query(schemas.User).all()
        return users
    user_wanted = db_session.query(schemas.User).where(schemas.User.email == email).first()
    if user_wanted is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with email {email} not found!",
        )
    # response.status_code = status.HTTP_404_NOT_FOUND
    return user_wanted


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=models.UserResponse)
def create_user(payload: models.UserCreate, db_session: Session = Depends(database_gen)):
    """
    function docstring
    """

    # hashing the password
    hashed_pwd = hash(payload.password)
    payload.password = hashed_pwd
    # creating a data according to schema
    new_user = schemas.User(**(payload.dict()))
    # adding data to session, moving it to pending state.
    user_present = (
        db_session.query(schemas.User).where(schemas.User.email == new_user.email).first()
    )
    if user_present is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with email {new_user.email} already exists!",
        )
    db_session.add(new_user)
    # moving all data in pending state, in this session, to persistant state.
    db_session.commit()
    # update new_post with data returned from db_session
    db_session.refresh(new_user)

    return new_user
