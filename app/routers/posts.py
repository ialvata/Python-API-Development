"""
Module responsible for Posts related operations
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from authetication.oauth2 import TokenData, get_current_user
from db import schemas
from db.db_orm import database_gen
from pydantic_models import posts

#################################        Router        ################################
router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=list[posts.PostResponse])
def get_posts(
    restrict_user: bool,  # query parameter and not a path operation
    num_posts: int = 10,
    db_session: Session = Depends(database_gen),
    token_data: TokenData = Depends(get_current_user),
):
    """
    restric_user: If True, then we only show posts for the user that's logged in.
    num_posts: number of posts to show.
    """
    if restrict_user:
        posts = (
            db_session.query(schemas.Post)
            .where(schemas.Post.username == token_data.username)
            .limit(num_posts)
            .all()
        )
    else:
        posts = db_session.query(schemas.Post).limit(num_posts).all()

    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=posts.PostResponse)
def create_post(
    payload: posts.PostCreate,
    db_session: Session = Depends(database_gen),
    token_data: TokenData = Depends(get_current_user),
):
    """
    function docstring
    """
    # creating a data according to schema
    new_post = schemas.Post(**(payload.dict()))
    # adding data to session, moving it to pending state.
    db_session.add(new_post)
    # moving all data in pending state, in this session, to persistant state.
    db_session.commit()
    # update new_post with data returned from db_session
    db_session.refresh(new_post)
    return new_post


# path operations are evaluated in order,
# you need to make sure that the path for /posts/latest
# is declared before the one for /posts/{identifier}
@router.get("/latest", response_model=posts.PostResponse)
def get_latest_post(db_session: Session = Depends(database_gen)):
    """
    function docstring
    """
    length_db = db_session.query(schemas.Post).count()
    post_wanted = db_session.query(schemas.Post).where(schemas.Post.id == length_db).first()
    return post_wanted


# identifier is an example of a path parameter
@router.get("/{identifier}", response_model=posts.PostResponse)
def get_post(identifier: int, db_session: Session = Depends(database_gen)):
    """
    Creates endpoint to fetch specific post
    """
    post_wanted = db_session.query(schemas.Post).where(schemas.Post.id == identifier).first()
    if post_wanted is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {identifier} not found!",
        )
    return post_wanted


# here identifier is a Query parameter
@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    identifier: int,
    db_session: Session = Depends(database_gen),
    token_data: TokenData = Depends(get_current_user),
):
    """
    Function that creates the resource to delete a specified post, by identifier.
    """
    post_wanted = db_session.query(schemas.Post).where(schemas.Post.id == identifier).first()
    if post_wanted is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {identifier} not found!",
        )
    if post_wanted.username != token_data.username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Logged username different from post owner username!",
        )
    db_session.delete(post_wanted)
    db_session.commit()


@router.patch("/", status_code=status.HTTP_200_OK, response_model=posts.PostResponse)
def patch_post(
    identifier: int,
    payload: posts.PostUpdate,
    db_session: Session = Depends(database_gen),
    token_data: TokenData = Depends(get_current_user),
):
    """
    function docstring
    """
    post_wanted_query = db_session.query(schemas.Post).where(schemas.Post.id == identifier)
    post_wanted = post_wanted_query.first()
    if post_wanted is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {identifier} not found!",
        )
    if post_wanted.username != token_data.username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Logged username different from post owner username!",
        )
    # pylance type checker says that payload.dict() is incompatible with type of `values` from
    # update... hence the extra dict()
    post_wanted_query.update(dict(payload.dict()), synchronize_session=False)
    db_session.commit()
    return post_wanted
