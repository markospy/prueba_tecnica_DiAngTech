# features/_class/exception_handlers.py
from fastapi import Request, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from src.repositories.exceptions import RepositoryAlreadyExistsException, RepositoryNotFoundException


async def repository_not_found_handler(request: Request, exc: RepositoryNotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc)},
    )


async def repository_already_exists_handler(request: Request, exc: RepositoryAlreadyExistsException):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": str(exc)},
    )


async def validation_error_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)},
    )


# Registra los handlers en tu aplicación principal
def register_repository_exception_handlers(app):
    # Errores 404 - Not Found
    app.add_exception_handler(RepositoryNotFoundException, repository_not_found_handler)
    app.add_exception_handler(RepositoryAlreadyExistsException, repository_already_exists_handler)

    # Errores 400 - Bad Request (validaciones)
    for exc_type in [
        ValidationError,
    ]:
        app.add_exception_handler(exc_type, validation_error_handler)
