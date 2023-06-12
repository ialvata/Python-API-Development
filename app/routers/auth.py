"""
Module responsible for Posts related operations
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.utils import verify
from authetication.oauth2 import Token, create_access_token
from db import schemas
from db.db_orm import database_gen

#################################        Router        ################################
router = APIRouter(tags=["Authentication"])


@router.post("/login", status_code=status.HTTP_202_ACCEPTED, response_model=Token)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db_session: Session = Depends(database_gen),
):
    """
    function docstring
    """
    user_present = (
        db_session.query(schemas.User)
        .where(schemas.User.email == user_credentials.username)
        .first()
    )
    if user_present is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credentials!",
        )
    if not verify(user_credentials.password, str(user_present.password)):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credentials!",
        )
    # create a token
    access_token = create_access_token(data={"email": user_credentials.username})
    # return token
    return Token(access_token=access_token, token_type="Bearer")
