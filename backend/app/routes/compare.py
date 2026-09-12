"""
Cross-Tradition Comparison and Semantic Parallels Routes for MythosAtlas.
"""

import logging
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.routes.myths import _get_enriched_myths
from app.services.llm_svc import llm_service
from app.services.qdrant_svc import qdrant_service

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1", tags=["compare"])


class CompareRequest(BaseModel):
    myth_a_id: str = Field(..., description="Wikidata ID of the first myth")
    myth_b_id: str = Field(..., description="Wikidata ID of the second myth")


@router.post("/compare", response_model=Dict[str, Any])
def compare_myths(req: CompareRequest):
    """
    Accepts two myth IDs, retrieves their narrative vectors and subgraphs,
    and runs a structuralist comparative analysis synthesizing archetype alignment,
    inciting motifs, cosmological resolution, and historical diffusion vs. cognitive convergence.
    """
    enriched = _get_enriched_myths()
    myth_a = enriched.get(req.myth_a_id)
    myth_b = enriched.get(req.myth_b_id)

    if not myth_a:
        raise HTTPException(status_code=404, detail=f"Myth ID '{req.myth_a_id}' not found")
    if not myth_b:
        raise HTTPException(status_code=404, detail=f"Myth ID '{req.myth_b_id}' not found")

    analysis = llm_service.synthesize_comparison(myth_a, myth_b)
    return analysis


@router.get("/parallels/{myth_id}", response_model=List[Dict[str, Any]])
def get_cross_cultural_parallels(myth_id: str, limit: int = 3):
    """
    Uses vector embedding distance to retrieve the top global counterparts
    across different continents and cultural traditions.
    """
    enriched = _get_enriched_myths()
    if myth_id not in enriched:
        raise HTTPException(status_code=404, detail=f"Myth ID '{myth_id}' not found")

    parallels = qdrant_service.find_cross_cultural_parallels(myth_id, limit=limit)
    return parallels
