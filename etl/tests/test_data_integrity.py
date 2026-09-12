"""
Automated Data Integrity Tests for MythosAtlas.
Validates the baked static bundle and enriched dataset against the technical specifications.
"""

import json
from pathlib import Path
import pytest

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
STATIC_FILE = DATA_DIR / "processed" / "static_myths.json"
ENRICHED_FILE = DATA_DIR / "processed" / "enriched_myths.json"
EMBEDDINGS_FILE = DATA_DIR / "processed" / "motif_embeddings.json"


def test_static_payload_exists_and_size():
    assert STATIC_FILE.exists(), f"Static myths file not found at {STATIC_FILE}"
    file_size_bytes = STATIC_FILE.stat().st_size
    # Must be less than 5MB
    assert file_size_bytes < 5 * 1024 * 1024, f"File size {file_size_bytes} exceeds 5MB limit"
    # Should be non-trivial
    assert file_size_bytes > 5 * 1024, f"File size {file_size_bytes} unexpectedly small"


def test_static_myths_schema():
    with open(STATIC_FILE, "r", encoding="utf-8") as f:
        myths = json.load(f)

    assert isinstance(myths, list), "Expected static myths to be a list"
    assert len(myths) >= 50, f"Expected at least 50 myths, got {len(myths)}"

    required_keys = {"id", "name", "lat", "lng", "epoch_start", "epoch_end", "culture", "archetype", "thumbnail"}
    cultures_found = set()

    for idx, myth in enumerate(myths):
        for k in required_keys:
            assert k in myth, f"Myth index {idx} ({myth.get('name')}) missing key: {k}"

        assert -90.0 <= myth["lat"] <= 90.0, f"Invalid latitude: {myth['lat']} for {myth['name']}"
        assert -180.0 <= myth["lng"] <= 180.0, f"Invalid longitude: {myth['lng']} for {myth['name']}"
        assert -4000 <= myth["epoch_start"] <= 1700, f"Epoch start out of range: {myth['epoch_start']} for {myth['name']}"
        assert myth["epoch_start"] <= myth["epoch_end"], f"epoch_start > epoch_end for {myth['name']}"
        assert myth["culture"], f"Missing culture for {myth['name']}"
        assert myth["archetype"], f"Missing archetype for {myth['name']}"

        cultures_found.add(myth["culture"])

    # Ensure diversity across continents/civilizations
    assert len(cultures_found) >= 5, f"Expected at least 5 distinct cultures, found: {cultures_found}"
    expected_major = {"Mesopotamian", "Egyptian", "Vedic", "Greco-Roman", "Norse", "Mesoamerican"}
    assert expected_major.issubset(cultures_found), f"Missing major civilizational traditions. Found: {cultures_found}"


def test_enriched_dataset_narratives():
    assert ENRICHED_FILE.exists(), f"Enriched myths file not found at {ENRICHED_FILE}"
    with open(ENRICHED_FILE, "r", encoding="utf-8") as f:
        enriched_map = json.load(f)

    assert isinstance(enriched_map, dict), "Expected enriched data to be an ID-keyed dict"
    assert len(enriched_map) >= 50, f"Expected at least 50 items, got {len(enriched_map)}"

    for qid, entry in enriched_map.items():
        assert entry.get("extract"), f"Missing narrative extract for {qid} ({entry.get('name')})"
        assert len(entry["extract"]) > 30, f"Extract too short for {qid}"


def test_embeddings_file():
    if EMBEDDINGS_FILE.exists():
        with open(EMBEDDINGS_FILE, "r", encoding="utf-8") as f:
            embedded_records = json.load(f)
        assert len(embedded_records) >= 50
        for rec in embedded_records:
            assert "vector" in rec
            assert len(rec["vector"]) == 384
