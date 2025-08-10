from pydantic import BaseModel


class BaseResponseSchema[T](BaseModel):
    """Base response schema for API responses."""

    status: int
    message: str
    data: T
