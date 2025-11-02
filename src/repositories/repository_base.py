from abc import ABC, abstractmethod
from typing import Any, List, Optional

from sqlalchemy.orm import Session


class RepositoryBase(ABC):

    def __init__(self, session: Session):
        self.session = session

    @abstractmethod
    def get_all(self, **kwargs: Any) -> Optional[List[Any]]:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[Any]:
        pass

    @abstractmethod
    def create(self, schema: Any) -> Optional[Any]:
        pass

    @abstractmethod
    def update(self, id: int, schema: Any) -> Optional[Any]:
        pass

    @abstractmethod
    def delete(self, id: int) -> None:
        pass
