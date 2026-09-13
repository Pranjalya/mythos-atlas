"""
Qdrant Motif Vector Service for MythosAtlas.
Handles semantic vector search, nearest cross-cultural parallel retrieval, and fallback in-memory search.
"""

import json
import logging
import math
from typing import Any, Dict, List, Optional
import numpy as np

from app.config import settings

logger = logging.getLogger(__name__)


class QdrantService:
    def __init__(self):
        self.client = None
        self.collection_name = settings.QDRANT_COLLECTION
        self.local_records: List[Dict[str, Any]] = []
        self.embedder = None
        self._load_local_records()
        self._init_qdrant()

    def _get_embedder(self):
        """Lazy-loads the lightweight quantized Nomic 1.5 ONNX embedder."""
        if self.embedder is None:
            try:
                from fastembed import TextEmbedding
                logger.info("Initializing in-process nomic-ai/nomic-embed-text-v1.5-Q for inference...")
                self.embedder = TextEmbedding(model_name="nomic-ai/nomic-embed-text-v1.5-Q")
                logger.info("In-process Nomic embedder ready for real-time inference.")
            except Exception as e:
                logger.error(f"Failed to load Nomic embedder: {e}")
                self.embedder = None
        return self.embedder

    def embed_query(self, query: str) -> Optional[List[float]]:
        """Embeds free-form search query with 'search_query:' prefix in ~17ms."""
        embedder = self._get_embedder()
        if not embedder:
            return None
        formatted = f"search_query: {query.strip()}"
        vectors = list(embedder.embed([formatted]))
        if vectors:
            return vectors[0].tolist()
        return None

    def _load_local_records(self):
        """Loads local motif embeddings as high-speed in-memory fallback."""
        if settings.MOTIF_EMBEDDINGS_FILE.exists():
            try:
                with open(settings.MOTIF_EMBEDDINGS_FILE, "r", encoding="utf-8") as f:
                    self.local_records = json.load(f)
                logger.info(f"Loaded {len(self.local_records)} local 768D motif embeddings for vector service.")
            except Exception as e:
                logger.warning(f"Could not load local motif embeddings: {e}")

    def _init_qdrant(self):
        """Initializes connection to Qdrant Cloud if credentials are present."""
        if settings.QDRANT_URL and settings.QDRANT_API_KEY:
            try:
                from qdrant_client import QdrantClient
                self.client = QdrantClient(url=settings.QDRANT_URL, api_key=settings.QDRANT_API_KEY)
                logger.info(f"Connected to Qdrant Cloud at {settings.QDRANT_URL}")
            except Exception as e:
                logger.warning(f"Could not connect to Qdrant Cloud: {e}. Falling back to in-memory vector search.")
                self.client = None

    def get_myth_by_id(self, myth_id: str) -> Optional[Dict[str, Any]]:
        for r in self.local_records:
            if r.get("id") == myth_id:
                return r
        return None

    def find_cross_cultural_parallels(
        self, myth_id: str, limit: int = 3, exclude_same_culture: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Finds the top semantic motif counterparts across the globe.
        If exclude_same_culture is True, filters out items from the same civilization.
        """
        target = self.get_myth_by_id(myth_id)
        if not target or "vector" not in target:
            logger.warning(f"Myth ID {myth_id} not found in local records.")
            return []

        target_vec = np.array(target["vector"], dtype=np.float32)
        target_culture = target.get("culture", "")

        # Try Qdrant Cloud first
        if self.client:
            try:
                from qdrant_client.http import models

                query_filter = None
                if exclude_same_culture and target_culture:
                    query_filter = models.Filter(
                        must_not=[
                            models.FieldCondition(
                                key="culture",
                                match=models.MatchValue(value=target_culture),
                            )
                        ]
                    )

                search_res = self.client.query_points(
                    collection_name=self.collection_name,
                    query=target["vector"],
                    query_filter=query_filter,
                    limit=limit + 1,  # extra in case self is included
                )

                parallels = []
                for hit in search_res.points:
                    payload = hit.payload or {}
                    if payload.get("id") == myth_id:
                        continue
                    parallels.append({
                        "id": payload.get("id"),
                        "name": payload.get("name"),
                        "culture": payload.get("culture"),
                        "archetype": payload.get("archetype"),
                        "score": round(float(hit.score), 4),
                        "thumbnail": payload.get("thumbnail"),
                        "description": payload.get("description"),
                        "extract": payload.get("extract", "")[:300] + "...",
                    })
                    if len(parallels) >= limit:
                        break

                if parallels:
                    return parallels
            except Exception as e:
                logger.warning(f"Qdrant Cloud search failed: {e}. Falling back to local vector search.")

        # In-Memory Cosine Similarity Fallback
        results = []
        target_norm = np.linalg.norm(target_vec)
        if target_norm == 0:
            target_norm = 1.0

        for r in self.local_records:
            if r.get("id") == myth_id:
                continue
            if exclude_same_culture and r.get("culture") == target_culture:
                continue
            if "vector" not in r:
                continue

            r_vec = np.array(r["vector"], dtype=np.float32)
            r_norm = np.linalg.norm(r_vec)
            if r_norm == 0:
                continue

            sim = float(np.dot(target_vec, r_vec) / (target_norm * r_norm))
            results.append({
                "id": r.get("id"),
                "name": r.get("name"),
                "culture": r.get("culture"),
                "archetype": r.get("archetype"),
                "score": round(sim, 4),
                "thumbnail": r.get("thumbnail"),
                "description": r.get("description"),
                "extract": r.get("extract", "")[:300] + "...",
            })

        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:limit]

    def search_by_text(
        self, query: str, limit: int = 6, culture: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Performs semantic motif vector search using a free-form query string.
        Encodes query via nomic-embed-text-v1.5-Q in ~17ms and searches Qdrant Cloud.
        """
        query_vec = self.embed_query(query)
        if not query_vec:
            logger.warning("Failed to generate query embedding.")
            return []

        # Try Qdrant Cloud first
        if self.client:
            try:
                from qdrant_client.http import models

                query_filter = None
                if culture:
                    query_filter = models.Filter(
                        must=[
                            models.FieldCondition(
                                key="culture",
                                match=models.MatchValue(value=culture),
                            )
                        ]
                    )

                search_res = self.client.query_points(
                    collection_name=self.collection_name,
                    query=query_vec,
                    query_filter=query_filter,
                    limit=limit,
                )

                results = []
                for hit in search_res.points:
                    payload = hit.payload or {}
                    results.append({
                        "id": payload.get("id"),
                        "name": payload.get("name"),
                        "culture": payload.get("culture"),
                        "archetype": payload.get("archetype"),
                        "score": round(float(hit.score), 4),
                        "thumbnail": payload.get("thumbnail"),
                        "description": payload.get("description"),
                        "extract": payload.get("extract", "")[:300] + "...",
                    })

                if results:
                    return results
            except Exception as e:
                logger.warning(f"Qdrant Cloud text search failed: {e}. Falling back to in-memory cosine search.")

        # In-Memory Cosine Fallback
        q_arr = np.array(query_vec, dtype=np.float32)
        q_norm = np.linalg.norm(q_arr)
        if q_norm == 0:
            q_norm = 1.0

        results = []
        for r in self.local_records:
            if culture and r.get("culture") != culture:
                continue
            if "vector" not in r:
                continue

            r_vec = np.array(r["vector"], dtype=np.float32)
            r_norm = np.linalg.norm(r_vec)
            if r_norm == 0:
                continue

            sim = float(np.dot(q_arr, r_vec) / (q_norm * r_norm))
            results.append({
                "id": r.get("id"),
                "name": r.get("name"),
                "culture": r.get("culture"),
                "archetype": r.get("archetype"),
                "score": round(sim, 4),
                "thumbnail": r.get("thumbnail"),
                "description": r.get("description"),
                "extract": r.get("extract", "")[:300] + "...",
            })

        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:limit]


qdrant_service = QdrantService()
