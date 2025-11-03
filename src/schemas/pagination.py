from typing import Generic, List, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    size: int
    pages: int

    model_config = {
        "json_schema_extra": {
            "example": {
                "items": [],
                "total": 156,
                "page": 2,
                "size": 10,
                "pages": 16,
            }
        }
    }
