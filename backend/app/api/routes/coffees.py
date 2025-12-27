from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.dependencies import get_repository, require_api_key
from app.models.schemas import CoffeeCreate, CoffeeRead
from app.services.repository import Repository

router = APIRouter(prefix="/coffees", tags=["coffees"], dependencies=[Depends(require_api_key)])


@router.get("", response_model=list[CoffeeRead], summary="Lister les cafés enregistrés")
def list_coffees(repository: Repository = Depends(get_repository)) -> list[CoffeeRead]:
    return [CoffeeRead.model_validate(coffee) for coffee in repository.list_coffees()]


@router.get("/{coffee_id}", response_model=CoffeeRead, summary="Détail d'un café")
def get_coffee(coffee_id: UUID, repository: Repository = Depends(get_repository)) -> CoffeeRead:
    coffee = repository.get_coffee(coffee_id)
    if not coffee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Café introuvable")
    return CoffeeRead.model_validate(coffee)


@router.post(
    "",
    response_model=CoffeeRead,
    status_code=status.HTTP_201_CREATED,
    summary="Ajouter un lot de café",
)
def create_coffee(
    payload: CoffeeCreate, repository: Repository = Depends(get_repository)
) -> CoffeeRead:
    created = repository.upsert_coffee(payload)
    return CoffeeRead.model_validate(created)


@router.put(
    "/{coffee_id}",
    response_model=CoffeeRead,
    summary="Mettre à jour un lot de café",
)
def update_coffee(
    coffee_id: UUID, payload: CoffeeCreate, repository: Repository = Depends(get_repository)
) -> CoffeeRead:
    if not repository.get_coffee(coffee_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Café introuvable")
    updated = repository.upsert_coffee(payload, coffee_id=coffee_id)
    return CoffeeRead.model_validate(updated)


@router.delete(
    "/{coffee_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Supprimer un café et ses données associées",
)
def delete_coffee(coffee_id: UUID, repository: Repository = Depends(get_repository)) -> None:
    if not repository.get_coffee(coffee_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Café introuvable")
    repository.delete_coffee(coffee_id)
