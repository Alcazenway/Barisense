from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.dependencies import get_repository, require_api_key
from app.models.schemas import VerdictCreate, VerdictRead
from app.services.repository import Repository

router = APIRouter(prefix="/verdicts", tags=["verdicts"], dependencies=[Depends(require_api_key)])


@router.get("", response_model=list[VerdictRead], summary="Lister les verdicts calculés")
def list_verdicts(repository: Repository = Depends(get_repository)) -> list[VerdictRead]:
    return [VerdictRead.model_validate(verdict) for verdict in repository.list_verdicts()]


@router.get("/{verdict_id}", response_model=VerdictRead, summary="Consulter un verdict")
def get_verdict(verdict_id: UUID, repository: Repository = Depends(get_repository)) -> VerdictRead:
    verdict = repository.get_verdict(verdict_id)
    if not verdict:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Verdict introuvable")
    return VerdictRead.model_validate(verdict)


@router.post(
    "",
    response_model=VerdictRead,
    status_code=status.HTTP_201_CREATED,
    summary="Créer ou mettre à jour un verdict",
)
def upsert_verdict(payload: VerdictCreate, repository: Repository = Depends(get_repository)) -> VerdictRead:
    verdict = repository.upsert_verdict(payload)
    return VerdictRead.model_validate(verdict)


@router.delete(
    "/{verdict_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Supprimer un verdict manuel",
)
def delete_verdict(verdict_id: UUID, repository: Repository = Depends(get_repository)) -> None:
    if not repository.get_verdict(verdict_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Verdict introuvable")
    repository.delete_verdict(verdict_id)
