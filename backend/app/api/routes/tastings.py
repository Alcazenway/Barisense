from fastapi import APIRouter, Depends, HTTPException, status

from app.core.dependencies import get_repository
from app.models.schemas import Tasting, TastingCreate
from app.services.repository import InMemoryRepository

router = APIRouter(prefix="/tastings", tags=["dégustations"])


@router.get("", response_model=list[Tasting], summary="Lister les dégustations")
def list_tastings(repository: InMemoryRepository = Depends(get_repository)) -> list[Tasting]:
    return list(repository.list_tastings())


@router.post(
    "",
    response_model=Tasting,
    status_code=status.HTTP_201_CREATED,
    summary="Enregistrer une dégustation",
)
def create_tasting(
    payload: TastingCreate, repository: InMemoryRepository = Depends(get_repository)
) -> Tasting:
    try:
        return repository.add_tasting(payload)
    except ValueError as err:
        if str(err) == "shot_not_found":
            raise HTTPException(status_code=404, detail="Shot introuvable") from err
        raise
