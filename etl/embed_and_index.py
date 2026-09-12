"""
Motif Embedding and Qdrant Cloud Indexing Module for MythosAtlas.
Generates 384-dimensional semantic vectors for mythological narratives using
fastembed (sentence-transformers/all-MiniLM-L6-v2) and synchronizes them to Qdrant Cloud.
"""

import json
import logging
import os
import sys
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

load_dotenv()

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
RAW_FILE = DATA_DIR / "raw" / "wikipedia_enriched.json"
OUTPUT_FILE = DATA_DIR / "processed" / "motif_embeddings.json"

COLLECTION_NAME = "mythos_motifs"
VECTOR_DIM = 384


def generate_motif_text(item: Dict[str, Any]) -> str:
    """Combines core myth fields into a semantically dense narrative motif representation."""
    parts = [
        f"Myth: {item.get('name', '')}",
        f"Culture: {item.get('culture', '')}",
        f"Archetype Motif: {item.get('archetype', '')}",
        f"Description: {item.get('description', '')}",
        f"Narrative: {item.get('extract', '')}",
    ]
    return " | ".join(p for p in parts if p)


def embed_and_index_dataset(items: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
    """Generates embeddings and indexes them to Qdrant Cloud and local JSON."""
    if items is None:
        if not RAW_FILE.exists():
            from etl.wikipedia_scraper import enrich_myths_with_wikipedia
            items = enrich_myths_with_wikipedia()
        else:
            with open(RAW_FILE, "r", encoding="utf-8") as f:
                items = json.load(f)

    logger.info(f"Generating dense embeddings for {len(items)} mythological narratives...")
    from fastembed import TextEmbedding

    embedding_model = TextEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
    texts = [generate_motif_text(m) for m in items]
    vectors = [v.tolist() for v in embedding_model.embed(texts)]

    records_with_embeddings = []
    for item, vec in zip(items, vectors):
        rec = dict(item)
        rec["vector"] = vec
        records_with_embeddings.append(rec)

    # Save local processed file
    DATA_DIR.joinpath("processed").mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(records_with_embeddings, f, indent=2, ensure_ascii=False)
    logger.info(f"Saved {len(records_with_embeddings)} embeddings to {OUTPUT_FILE}")

    # Index into Qdrant Cloud if credentials are present
    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")

    if qdrant_url and qdrant_api_key:
        try:
            from qdrant_client import QdrantClient
            from qdrant_client.http.models import Distance, VectorParams, PointStruct

            logger.info(f"Connecting to Qdrant Cloud ({qdrant_url})...")
            client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)

            existing_collections = [c.name for c in client.get_collections().collections]
            if COLLECTION_NAME not in existing_collections:
                logger.info(f"Creating Qdrant collection '{COLLECTION_NAME}' (dim={VECTOR_DIM}, metric=Cosine)...")
                client.create_collection(
                    collection_name=COLLECTION_NAME,
                    vectors_config=VectorParams(size=VECTOR_DIM, distance=Distance.COSINE),
                )
            else:
                logger.info(f"Qdrant collection '{COLLECTION_NAME}' already exists.")

            # Prepare points
            points = []
            for i, rec in enumerate(records_with_embeddings):
                # Use deterministic UUID based on Wikidata ID or index
                qid = rec.get("id", f"idx_{i}")
                point_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"mythos-atlas:{qid}"))
                payload = {
                    "id": rec.get("id"),
                    "name": rec.get("name"),
                    "culture": rec.get("culture"),
                    "archetype": rec.get("archetype"),
                    "epoch_start": rec.get("epoch_start"),
                    "epoch_end": rec.get("epoch_end"),
                    "lat": rec.get("lat"),
                    "lng": rec.get("lng"),
                    "extract": rec.get("extract"),
                    "description": rec.get("description"),
                    "thumbnail": rec.get("thumbnail"),
                    "wikipedia_url": rec.get("wikipedia_url"),
                    "syncretic_ids": rec.get("syncretic_ids", []),
                }
                points.append(
                    PointStruct(
                        id=point_id,
                        vector=rec["vector"],
                        payload=payload,
                    )
                )

            logger.info(f"Upserting {len(points)} points into Qdrant Cloud '{COLLECTION_NAME}'...")
            client.upsert(collection_name=COLLECTION_NAME, points=points)
            logger.info("Successfully populated Qdrant Cloud collection with all motif vectors!")
        except Exception as e:
            logger.error(f"Failed to upsert points into Qdrant Cloud: {e}", exc_info=True)
    else:
        logger.warning("QDRANT_URL or QDRANT_API_KEY not set. Skipping Qdrant Cloud upload.")

    return {
        "status": "success",
        "total_embedded": len(records_with_embeddings),
        "vector_dim": VECTOR_DIM,
    }


if __name__ == "__main__":
    embed_and_index_dataset()
