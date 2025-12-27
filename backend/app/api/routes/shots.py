from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.dependencies import get_repository, require_api_key
from app.models.schemas import ShotCreate, ShotRead
from app.services.repository import Repository

router = APIRouter(prefix="/shots", tags=["shots"], dependencies=[Depends(require_api_key)])


@router.get("", response_model=list[ShotRead], summary="Lister les shots effectués")
def list_shots(repository: Repository = Depends(get_repository)) -> list[ShotRead]:
    return [ShotRead.model_validate(shot) for shot in repository.list_shots()]


@router.get("/{shot_id}", response_model=ShotRead, summary="Récupérer un shot")
def get_shot(shot_id: UUID, repository: Repository = Depends(get_repository)) -> ShotRead:
    shot = repository.get_shot(shot_id)
    if not shot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shot introuvable")
    return ShotRead.model_validate(shot)


@router.post(
    "",
    response_model=ShotRead,
    status_code=status.HTTP_201_CREATED,
    summary="Enregistrer un shot",
)
def create_shot(
    payload: ShotCreate, repository: Repository = Depends(get_repository)
) -> ShotRead:
    try:
        created = repository.add_shot(payload)
    except ValueError as err:
        if str(err) == "coffee_not_found":
            raise HTTPException(status_code=404, detail="Café introuvable") from err
        if str(err) == "water_not_found":
            raise HTTPException(status_code=404, detail="Eau introuvable") from err
        raise
    return ShotRead.model_validate(created)


@router.put(
    "/{shot_id}",
    response_model=ShotRead,
    summary="Mettre à jour un shot",
)
def update_shot(
    shot_id: UUID, payload: ShotCreate, repository: Repository = Depends(get_repository)
) -> ShotRead:
    try:
        updated = repository.update_shot(shot_id, payload)
    except ValueError as err:
        if str(err) == "shot_not_found":
            raise HTTPException(status_code=404, detail="Shot introuvable") from err
        if str(err) == "coffee_not_found":
            raise HTTPException(status_code=404, detail="Café introuvable") from err
        if str(err) == "water_not_found":
            raise HTTPException(status_code=404, detail="Eau introuvable") from err
        raise
    return ShotRead.model_validate(updated)


@router.delete(
    "/{shot_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Supprimer un shot",
)
def delete_shot(shot_id: UUID, repository: Repository = Depends(get_repository)) -> None:
    if not repository.get_shot(shot_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shot introuvable")
    repository.delete_shot(shot_id)
