"""
Master ETL Pipeline Orchestrator for MythosAtlas.
Executes the full pipeline: Wikidata SPARQL extraction -> Wikipedia scraping -> Qdrant indexing -> Static data baking.
"""

import argparse
import logging
import time
from pathlib import Path

from etl.wikidata_sparql import fetch_and_assemble_catalog
from etl.wikipedia_scraper import enrich_myths_with_wikipedia
from etl.embed_and_index import embed_and_index_dataset
from etl.bake_static_data import bake_static_dataset

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def run_pipeline(skip_qdrant: bool = False, force_refresh: bool = False) -> None:
    start_time = time.time()
    logger.info("=" * 60)
    logger.info("STARTING MYTHOSATLAS ETL DATA PIPELINE")
    logger.info("=" * 60)

    # Step 1: Wikidata SPARQL / Seed Catalog
    logger.info("\n--- STEP 1: WIKIDATA EXTRACTION ---")
    raw_items = fetch_and_assemble_catalog()
    logger.info(f"Retrieved {len(raw_items)} base entities.")

    # Step 2: Wikipedia Scraping & Enrichment
    logger.info("\n--- STEP 2: WIKIPEDIA NARRATIVE & THUMBNAIL SCRAPING ---")
    enriched_items = enrich_myths_with_wikipedia(raw_items)
    logger.info(f"Enriched {len(enriched_items)} entities with leads and media.")

    # Step 3: Embeddings & Vector Indexing
    logger.info("\n--- STEP 3: NARRATIVE VECTOR EMBEDDING & INDEXING ---")
    if not skip_qdrant:
        embed_result = embed_and_index_dataset(enriched_items)
        logger.info(f"Vector indexing status: {embed_result}")
    else:
        logger.info("Skipping Qdrant indexing as requested.")

    # Step 4: Bake Lean Static Bundle
    logger.info("\n--- STEP 4: BAKING CLIENT-SIDE STATIC PAYLOAD ---")
    bake_result = bake_static_dataset(enriched_items)
    logger.info(f"Bake complete: {bake_result}")

    elapsed = time.time() - start_time
    logger.info("=" * 60)
    logger.info(f"ETL PIPELINE COMPLETED SUCCESSFULLY IN {elapsed:.2f}s")
    logger.info("=" * 60)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MythosAtlas Data Pipeline Runner")
    parser.add_argument("--skip-qdrant", action="store_true", help="Skip Qdrant Cloud vector indexing")
    parser.add_argument("--force-refresh", action="store_true", help="Force fresh downloads of Wikipedia data")
    args = parser.parse_args()

    run_pipeline(skip_qdrant=args.skip_qdrant, force_refresh=args.force_refresh)
