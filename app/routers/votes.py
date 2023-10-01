"""
Module responsible for Posts related operations
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from authetication.oauth2 import TokenData, get_current_user
from db import schemas
from db.db_orm import database_gen
from pydantic_models.votes import VoteInput, VoteResponse

#################################        Router        ################################
router = APIRouter(prefix="/votes", tags=["Votes"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(
    vote: VoteInput,
    current_user: schemas.User = Depends(get_current_user),
    db_session: Session = Depends(database_gen),
    token_data: TokenData = Depends(get_current_user),
):
    """
    This creates a row in the vote table.

    Parameters
    ----------
    current_user:.
    """
    post = db_session.query(schemas.Post).filter(schemas.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {vote.post_id} does not exist",
        )
    vote_query = db_session.query(schemas.Vote).filter(
        schemas.Vote.post_id == vote.post_id, schemas.Vote.user_id == current_user.id
    )
    found_vote = vote_query.first()
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"user {current_user.id} has already voted on post {vote.post_id}",
            )
        new_vote = schemas.Vote(
            post_id=vote.post_id,
            user_id=current_user.id,
            username=current_user.username,
            rating=vote.rating,
            published=vote.published,
        )
        db_session.add(new_vote)
        db_session.commit()
        return {"message": "successfully added vote"}

    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist"
            )
        vote_query.delete(synchronize_session=False)
        db_session.commit()
        return {"message": "successfully deleted vote"}


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[VoteResponse])
def get_votes(
    username: str,
    num_votes: int = 10,
    skip: int = 0,
    db_session: Session = Depends(database_gen),
    token_data: TokenData = Depends(get_current_user),
):
    """
    restric_user: If True, then we only show posts for the user that's logged in.
    num_posts: number of posts to show.

    To implement pagination in results, we should use .offset(num_pag) in the query below,
    where the results thrown will be offsetted by num_pag:int.
    """

    votes = (
        db_session.query(schemas.Vote)
        .where(
            schemas.Vote.username == username,
        )
        .offset(skip)
        .limit(num_votes)
        .all()
    )
    return votes
