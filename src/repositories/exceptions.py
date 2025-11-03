class RepositoryException(Exception):
    pass


class RepositoryNotFoundException(RepositoryException):
    def __init__(self, message: str | None = None, entity_name: str | None = None, id: int | None = None):
        if message:
            super().__init__(message)
        else:
            super().__init__(f"{entity_name} with id {id} not found")


class RepositoryAlreadyExistsException(RepositoryException):
    def __init__(self, message: str | None = None, entity_name: str | None = None, name: str | None = None):
        if message:
            super().__init__(message)
        else:
            super().__init__(f"{entity_name} with name {name} already exists")
