"""
Module responsible for Posts related operations
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.utils import verify
from authetication.oauth2 import create_access_token
from db import schemas
from db.db_orm import database_gen
from pydantic_models import users

#################################        Router        ################################
router = APIRouter(tags=["Authentication"])


@router.post("/login", status_code=status.HTTP_202_ACCEPTED)
def login(payload: users.UserLogin, db_session: Session = Depends(database_gen)):
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
    access_token = create_access_token(data={"email": payload.email})
    # return token
    return {"token": access_token, "token_type": "Bearer"}
