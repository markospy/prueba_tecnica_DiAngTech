class RepositoryException(Exception):
    pass


class RepositoryNotFoundException(RepositoryException):

    def __init__(self, entity_name: str, id: int):
        super().__init__(f"{entity_name} with id {id} not found")


class RepositoryAlreadyExistsException(RepositoryException):
    def __init__(self, entity_name: str, name: str):
        super().__init__(f"{entity_name} with name {name} already exists")
