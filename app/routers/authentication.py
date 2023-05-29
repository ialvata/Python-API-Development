"""
Module responsible for Posts related operations
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.utils import verify
from db import models, schemas
from db.db_orm import database_gen

#################################        Router        ################################
router = APIRouter(tags=["Authentication"])


@router.post("/login", status_code=status.HTTP_202_ACCEPTED)
def login(payload: models.UserLogin, db_session: Session = Depends(database_gen)):
    """
    function docstring
    """
    user_present = (
        db_session.query(schemas.User).where(schemas.User.email == payload.email).first()
    )
    if user_present is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid credentials!",
        )
    if not verify(payload.password, str(user_present.password)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid credentials!",
        )
    # create a token
    # return token
    return {"token": "example_token"}
