from abc import ABC, abstractmethod
from typing import Any, List, Optional

from sqlalchemy.ext.asyncio import AsyncSession


class RepositoryBase(ABC):

    def __init__(self, session: AsyncSession):
        self.session = session

    @abstractmethod
    async def get_all(self, **kwargs: Any) -> Optional[List[Any]]:
        pass

    @abstractmethod
    async def get_by_id(self, id: int) -> Optional[Any]:
        pass

    @abstractmethod
    async def create(self, schema: Any) -> Optional[Any]:
        pass

    @abstractmethod
    async def update(self, id: int, schema: Any) -> Optional[Any]:
        pass

    @abstractmethod
    async def delete(self, id: int) -> None:
        pass
