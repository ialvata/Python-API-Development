"""
Module responsible for pydantic models/schemas
"""
from pydantic import BaseModel, confloat, conint


class VoteBase(BaseModel):
    """
    Pydantic class that represents a Vote.
    """

    post_id: int
    published: bool = True
    rating: confloat(ge=0, le=10)  # type: ignore


class VoteInput(VoteBase):
    dir: conint(ge=0, le=1)  # type: ignore


class VoteResponse(VoteBase):
    """
    Pydantic class that represents a Vote result.
    """

    username: str
    user_id: int

    class Config:
        """
        Behaviour of pydantic can be controlled via the Config class on a model
        or a pydantic dataclass.
        Pydantic's `orm_mode` will tell the Pydantic model to read the data
        even if it is not a dict, but an ORM model
        (or any other arbitrary object with attributes).
        With this, the Pydantic model is compatible with ORMs, and you can just declare
        it in the response_model argument in your path operations.
        You will be able to return a database model and it will read the data from it.
        https://fastapi.tiangolo.com/tutorial/response-model/?h=
        """

        orm_mode = True
