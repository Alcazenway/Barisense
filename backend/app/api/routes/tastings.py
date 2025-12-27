from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.dependencies import get_repository, require_api_key
from app.models.schemas import TastingCreate, TastingRead
from app.services.analysis import mean_to_label, verdict_from_mean, verdict_label
from app.services.repository import Repository

router = APIRouter(prefix="/tastings", tags=["dégustations"], dependencies=[Depends(require_api_key)])


@router.get("", response_model=list[TastingRead], summary="Lister les dégustations")
def list_tastings(repository: Repository = Depends(get_repository)) -> list[TastingRead]:
    return [serialize_tasting(t) for t in repository.list_tastings()]


@router.get("/{tasting_id}", response_model=TastingRead, summary="Détail d'une dégustation")
def get_tasting(tasting_id: UUID, repository: Repository = Depends(get_repository)) -> TastingRead:
    tasting = repository.get_tasting(tasting_id)
    if not tasting:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dégustation introuvable")
    return serialize_tasting(tasting)


@router.post(
    "",
    response_model=TastingRead,
    status_code=status.HTTP_201_CREATED,
    summary="Enregistrer une dégustation",
)
def create_tasting(
    payload: TastingCreate, repository: Repository = Depends(get_repository)
) -> TastingRead:
    try:
        tasting = repository.add_tasting(payload)
    except ValueError as err:
        if str(err).startswith("unknown_label"):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Libellé sensoriel invalide"
            ) from err
        if str(err) == "shot_not_found":
            raise HTTPException(status_code=404, detail="Shot introuvable") from err
        raise
    return serialize_tasting(tasting)


@router.delete(
    "/{tasting_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Supprimer une dégustation",
)
def delete_tasting(tasting_id: UUID, repository: Repository = Depends(get_repository)) -> None:
    if not repository.get_tasting(tasting_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dégustation introuvable")
    repository.delete_tasting(tasting_id)


def serialize_tasting(tasting) -> TastingRead:
    return TastingRead(
        id=tasting.id,
        shot_id=tasting.shot_id,
        acidity_label=mean_to_label(tasting.acidity_score),
        bitterness_label=mean_to_label(tasting.bitterness_score),
        body_label=mean_to_label(tasting.body_score),
        aroma_label=mean_to_label(tasting.aroma_score),
        balance_label=mean_to_label(tasting.balance_score),
        finish_label=mean_to_label(tasting.finish_score),
        overall_label=mean_to_label(tasting.overall_score),
        mean_label=mean_to_label(tasting.sensory_mean),
        verdict_label=verdict_label(verdict_from_mean(tasting.sensory_mean)),
        comments=tasting.comments,
        created_at=tasting.created_at,
    )
