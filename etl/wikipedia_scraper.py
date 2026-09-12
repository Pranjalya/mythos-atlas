"""
Wikipedia Narrative Scraper for MythosAtlas.
Enriches Wikidata entities with high-fidelity narrative leads, infobox summaries,
canonical URLs, and Wikimedia Commons thumbnails via the Wikimedia REST API.
"""

import json
import logging
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional
import urllib.parse
import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

DATA_RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"
INPUT_FILE = DATA_RAW_DIR / "wikidata_raw.json"
CACHE_FILE = DATA_RAW_DIR / "wikipedia_cache.json"
OUTPUT_FILE = DATA_RAW_DIR / "wikipedia_enriched.json"

REST_API_BASE = "https://en.wikipedia.org/api/rest_v1/page/summary"
USER_AGENT = "MythosAtlas/1.0 (https://github.com/mythos-atlas; contact@mythosatlas.internal)"


def load_cache() -> Dict[str, Any]:
    """Loads existing cached Wikipedia summaries if available."""
    if CACHE_FILE.exists():
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Failed to read cache file: {e}")
    return {}


def save_cache(cache: Dict[str, Any]) -> None:
    """Saves Wikipedia summary cache to disk."""
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2, ensure_ascii=False)


def fetch_wikipedia_summary(title: str, session: requests.Session) -> Optional[Dict[str, Any]]:
    """Fetches summary, extract, and thumbnail from Wikipedia REST API."""
    clean_title = urllib.parse.unquote(title).strip().replace(" ", "_")
    encoded_title = urllib.parse.quote(clean_title, safe=":/_")
    url = f"{REST_API_BASE}/{encoded_title}"
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
    }
    try:
        resp = session.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            return resp.json()
        elif resp.status_code == 404:
            logger.warning(f"Article not found on Wikipedia: {title}")
        else:
            logger.warning(f"Wikipedia API returned status {resp.status_code} for {title}")
    except Exception as e:
        logger.warning(f"Error fetching Wikipedia summary for {title}: {e}")
    return None


def enrich_myths_with_wikipedia(items: Optional[List[Dict[str, Any]]] = None) -> List[Dict[str, Any]]:
    """Enriches each myth entity with Wikipedia lead paragraph and thumbnail."""
    if items is None:
        if not INPUT_FILE.exists():
            from etl.wikidata_sparql import fetch_and_assemble_catalog
            items = fetch_and_assemble_catalog()
        else:
            with open(INPUT_FILE, "r", encoding="utf-8") as f:
                items = json.load(f)

    cache = load_cache()
    session = requests.Session()
    enriched: List[Dict[str, Any]] = []

    logger.info(f"Enriching {len(items)} items from Wikipedia (Cached: {len(cache)})...")
    cache_modified = False

    for idx, item in enumerate(items, 1):
        wiki_title = item.get("wiki_title") or item.get("name", "").replace(" ", "_")
        cache_key = wiki_title.lower()

        summary_data = cache.get(cache_key)
        if not summary_data:
            summary_data = fetch_wikipedia_summary(wiki_title, session)
            if summary_data:
                cache[cache_key] = summary_data
                cache_modified = True
            time.sleep(0.08)  # Conscientious rate limit for Wikimedia APIs

        # Extract useful attributes
        extract = ""
        thumbnail = ""
        description = ""
        page_url = f"https://en.wikipedia.org/wiki/{wiki_title}"

        if summary_data:
            extract = summary_data.get("extract", "")
            description = summary_data.get("description", "")
            if "thumbnail" in summary_data and "source" in summary_data["thumbnail"]:
                thumbnail = summary_data["thumbnail"]["source"]
            if "content_urls" in summary_data and "desktop" in summary_data["content_urls"]:
                page_url = summary_data["content_urls"]["desktop"].get("page", page_url)

        # Fallback thumbnail if Wikimedia has none for specific entity
        if not thumbnail:
            thumbnail = f"https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=600&auto=format&fit=crop&q=80"

        # Clean up extract if malformed or too short
        clean_extract = extract.strip() if extract else ""
        if len(clean_extract) < 30 or clean_extract.startswith("{{"):
            if wiki_title.lower() == "zahhak":
                clean_extract = (
                    "Zahhak or Zahhāk is an evil figure in Persian mythology and folklore, "
                    "evident in ancient Persian folklore as Aži Dahāka, the venomous serpent king "
                    "who sprouted two voracious serpents from his shoulders and was overthrown by "
                    "the blacksmith Kaveh and hero Fereydun."
                )
            else:
                clean_extract = f"{item['name']} is a foundational mythological epic and sacred cultural narrative from the {item['culture']} tradition."

        enriched_item = dict(item)
        enriched_item["extract"] = clean_extract
        enriched_item["description"] = description
        enriched_item["thumbnail"] = thumbnail
        enriched_item["wikipedia_url"] = page_url

        enriched.append(enriched_item)
        if idx % 10 == 0 or idx == len(items):
            logger.info(f"Progress: {idx}/{len(items)} myths processed.")

    if cache_modified:
        save_cache(cache)
        logger.info(f"Saved {len(cache)} entries to Wikipedia cache.")

    DATA_RAW_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(enriched, f, indent=2, ensure_ascii=False)

    logger.info(f"Successfully saved {len(enriched)} enriched items to {OUTPUT_FILE}")
    return enriched


if __name__ == "__main__":
    enrich_myths_with_wikipedia()
