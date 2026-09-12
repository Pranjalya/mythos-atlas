"""
Myth entity detail retrieval routes for MythosAtlas.
"""

import json
import logging
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException

from app.config import settings

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/myths", tags=["myths"])

# In-memory enriched myths cache
_ENRICHED_CACHE: Dict[str, Dict[str, Any]] = {}


def _get_enriched_myths() -> Dict[str, Dict[str, Any]]:
    global _ENRICHED_CACHE
    if not _ENRICHED_CACHE and settings.ENRICHED_MYTHS_FILE.exists():
        try:
            with open(settings.ENRICHED_MYTHS_FILE, "r", encoding="utf-8") as f:
                _ENRICHED_CACHE = json.load(f)
        except Exception as e:
            logger.error(f"Failed to load enriched myths: {e}")
    return _ENRICHED_CACHE


@router.get("", response_model=List[Dict[str, Any]])
def list_myths():
    """Lists all available myth entities."""
    enriched = _get_enriched_myths()
    return [
        {
            "id": m["id"],
            "name": m["name"],
            "culture": m.get("culture"),
            "archetype": m.get("archetype"),
            "epoch_start": m.get("epoch_start"),
            "epoch_end": m.get("epoch_end"),
            "lat": m.get("lat"),
            "lng": m.get("lng"),
            "thumbnail": m.get("thumbnail"),
        }
        for m in enriched.values()
    ]


@router.get("/{myth_id}", response_model=Dict[str, Any])
def get_myth_detail(myth_id: str):
    """
    Returns enriched Wikipedia narrative, syncretic edges (said to be same as, influenced by),
    and historical coordinates for an entity.
    """
    enriched = _get_enriched_myths()
    myth = enriched.get(myth_id)
    if not myth:
        raise HTTPException(status_code=404, detail=f"Myth ID '{myth_id}' not found")

    # Hydrate syncretic edge objects
    syncretic_targets = []
    for s_id in myth.get("syncretic_ids", []):
        if s_id in enriched:
            target = enriched[s_id]
            syncretic_targets.append({
                "id": target["id"],
                "name": target["name"],
                "culture": target["culture"],
                "lat": target["lat"],
                "lng": target["lng"],
                "relation": "syncretic / diffused counterpart",
            })

    result = dict(myth)
    result["syncretic_targets"] = syncretic_targets
    return result
