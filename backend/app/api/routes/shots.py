from fastapi import APIRouter, Depends, HTTPException, status

from app.core.dependencies import get_repository
from app.models.schemas import Shot, ShotCreate
from app.services.repository import InMemoryRepository

router = APIRouter(prefix="/shots", tags=["shots"])


@router.get("", response_model=list[Shot], summary="Lister les shots effectués")
def list_shots(repository: InMemoryRepository = Depends(get_repository)) -> list[Shot]:
    return list(repository.list_shots())


@router.post(
    "",
    response_model=Shot,
    status_code=status.HTTP_201_CREATED,
    summary="Enregistrer un shot",
)
def create_shot(
    payload: ShotCreate, repository: InMemoryRepository = Depends(get_repository)
) -> Shot:
    try:
        return repository.add_shot(payload)
    except ValueError as err:
        if str(err) == "coffee_not_found":
            raise HTTPException(status_code=404, detail="Café introuvable") from err
        if str(err) == "water_not_found":
            raise HTTPException(status_code=404, detail="Eau introuvable") from err
        raise
