"""
Static Data Baking Module for MythosAtlas.
Compiles a lean, quantized JSON bundle for static client-side and WASM consumption,
guaranteeing zero network roundtrips for spatio-temporal timeline queries.
"""

import json
import logging
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
RAW_FILE = DATA_DIR / "raw" / "wikipedia_enriched.json"
PROCESSED_DIR = DATA_DIR / "processed"
STATIC_OUTPUT_FILE = PROCESSED_DIR / "static_myths.json"
ENRICHED_OUTPUT_FILE = PROCESSED_DIR / "enriched_myths.json"

MAX_ALLOWED_SIZE_BYTES = 5 * 1024 * 1024  # 5 MB ceiling


def bake_static_dataset(items: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
    """Bakes raw enriched data into static lean JSON bundles."""
    if items is None:
        if not RAW_FILE.exists():
            from etl.wikipedia_scraper import enrich_myths_with_wikipedia
            items = enrich_myths_with_wikipedia()
        else:
            with open(RAW_FILE, "r", encoding="utf-8") as f:
                items = json.load(f)

    logger.info(f"Baking static data for {len(items)} myth items...")
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    static_bundle: List[Dict[str, Any]] = []
    enriched_map: Dict[str, Dict[str, Any]] = {}

    for item in items:
        # Client-side lean static schema contract
        static_record = {
            "id": item.get("id"),
            "name": item.get("name"),
            "lat": round(float(item.get("lat", 0.0)), 4),
            "lng": round(float(item.get("lng", 0.0)), 4),
            "epoch_start": int(item.get("epoch_start", -1000)),
            "epoch_end": int(item.get("epoch_end", 500)),
            "culture": item.get("culture", "Unknown"),
            "archetype": item.get("archetype", "Mythological Narrative"),
            "thumbnail": item.get("thumbnail", ""),
            "syncretic_ids": item.get("syncretic_ids", []),
            "description": item.get("description", ""),
        }
        static_bundle.append(static_record)

        # Enriched dictionary keyed by ID for backend fast hydration
        item_id = item.get("id")
        if item_id:
            enriched_map[item_id] = {
                "id": item_id,
                "name": item.get("name"),
                "lat": item.get("lat"),
                "lng": item.get("lng"),
                "epoch_start": item.get("epoch_start"),
                "epoch_end": item.get("epoch_end"),
                "culture": item.get("culture"),
                "archetype": item.get("archetype"),
                "thumbnail": item.get("thumbnail"),
                "description": item.get("description"),
                "extract": item.get("extract"),
                "wikipedia_url": item.get("wikipedia_url"),
                "syncretic_ids": item.get("syncretic_ids", []),
            }

    # Write static_myths.json
    with open(STATIC_OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(static_bundle, f, indent=2, ensure_ascii=False)

    # Write enriched_myths.json
    with open(ENRICHED_OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(enriched_map, f, indent=2, ensure_ascii=False)

    file_size = STATIC_OUTPUT_FILE.stat().st_size
    size_kb = file_size / 1024
    logger.info(f"Generated {STATIC_OUTPUT_FILE} ({size_kb:.2f} KB, {len(static_bundle)} items).")

    if file_size > MAX_ALLOWED_SIZE_BYTES:
        raise ValueError(
            f"Static bundle exceeded 5MB ceiling! Actual size: {size_kb:.2f} KB"
        )

    logger.info(f"Generated {ENRICHED_OUTPUT_FILE} ({len(enriched_map)} indexed entries).")
    return {
        "static_records": len(static_bundle),
        "file_size_kb": round(size_kb, 2),
        "static_path": str(STATIC_OUTPUT_FILE),
        "enriched_path": str(ENRICHED_OUTPUT_FILE),
    }


if __name__ == "__main__":
    bake_static_dataset()
