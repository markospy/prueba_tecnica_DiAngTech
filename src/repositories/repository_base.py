from typing import Any, List, Optional

from sqlalchemy.orm import Session


class RepositoryBase:

    def __init__(self, session: Session):
        self.session = session

    def get_all(self, **kwargs: Any) -> Optional[List[Any]]:
        pass

    def get_by_id(self, id: int) -> Optional[Any]:
        pass

    def create(self, schema: Any) -> Optional[Any]:
        pass

    def update(self, id: int, schema: Any) -> Optional[Any]:
        pass

    def delete(self, id: int) -> None:
        pass
