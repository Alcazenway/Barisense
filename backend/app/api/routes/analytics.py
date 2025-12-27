from fastapi import APIRouter, Depends

from app.core.dependencies import get_repository
from app.models.schemas import AnalyticsSummary
from app.services.analysis import AnalyticsEngine

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("", response_model=AnalyticsSummary, summary="Synthèse analytics Barisense")
def list_analytics(repository=Depends(get_repository)) -> AnalyticsSummary:
    """Retourne les ratios, diagnostics, suggestions et classements d'eau."""
    engine = AnalyticsEngine(repository)
    return engine.build_summary()
