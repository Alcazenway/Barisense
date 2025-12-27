from fastapi import APIRouter, Depends, status

from app.core.dependencies import get_repository
from app.models.schemas import Coffee, CoffeeCreate
from app.services.repository import InMemoryRepository

router = APIRouter(prefix="/coffees", tags=["coffees"])


@router.get("", response_model=list[Coffee], summary="Lister les cafés enregistrés")
def list_coffees(repository: InMemoryRepository = Depends(get_repository)) -> list[Coffee]:
    return list(repository.list_coffees())


@router.post(
    "",
    response_model=Coffee,
    status_code=status.HTTP_201_CREATED,
    summary="Ajouter un lot de café",
)
def create_coffee(
    payload: CoffeeCreate, repository: InMemoryRepository = Depends(get_repository)
) -> Coffee:
    return repository.add_coffee(payload)
