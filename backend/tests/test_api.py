"""
FastAPI Backend Integration Tests for MythosAtlas.
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_list_myths():
    response = client.get("/api/v1/myths")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 50
    assert any(m["name"] == "Epic of Gilgamesh" for m in data)


def test_get_myth_detail():
    # Gilgamesh ID
    response = client.get("/api/v1/myths/Q248352")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Epic of Gilgamesh"
    assert "extract" in data
    assert "syncretic_targets" in data
    assert isinstance(data["syncretic_targets"], list)


def test_get_cross_cultural_parallels():
    response = client.get("/api/v1/parallels/Q248352?limit=3")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    # Parallels should have name and score
    for p in data:
        assert "name" in p
        assert "score" in p
        assert "culture" in p


def test_compare_myths():
    # Compare Gilgamesh (Mesopotamian) with Popol Vuh (Mesoamerican)
    response = client.post(
        "/api/v1/compare",
        json={"myth_a_id": "Q248352", "myth_b_id": "Q190828"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "synthesis" in data
    syn = data["synthesis"]
    assert "character_archetypes" in syn
    assert "inciting_motifs" in syn
    assert "cosmological_resolution" in syn
    assert "structural_typology" in syn
    assert "key_takeaways" in syn
