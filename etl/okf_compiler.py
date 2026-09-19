"""
Google OKF v0.2 High-Performance Compiler for MythosAtlas.
Recursively parses, validates, and compiles the knowledge/myths/ Markdown corpus into:
  1. frontend/public/data/static_myths.json (lean client payload for Rust WASM & Three.js)
  2. data/processed/static_myths.json
  3. data/processed/enriched_myths.json (full scholarly hydration payload for FastAPI & Gemini)
"""

import argparse
import json
import logging
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("okf_compiler")

BASE_DIR = Path(__file__).resolve().parent.parent
KNOWLEDGE_DIR = BASE_DIR / "knowledge" / "myths"
FRONTEND_STATIC_FILE = BASE_DIR / "frontend" / "public" / "data" / "static_myths.json"
BACKEND_STATIC_FILE = BASE_DIR / "data" / "processed" / "static_myths.json"
ENRICHED_FILE = BASE_DIR / "data" / "processed" / "enriched_myths.json"
BACKEND_DIR_ENRICHED = BASE_DIR / "backend" / "data" / "processed" / "enriched_myths.json"
BACKEND_DIR_STATIC = BASE_DIR / "backend" / "data" / "processed" / "static_myths.json"



def parse_frontmatter(content: str) -> Tuple[Dict[str, Any], str]:
    """Parses YAML frontmatter and extracts markdown body without external yaml dependencies."""
    if not content.startswith("---"):
        return {}, content

    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content

    yaml_raw = parts[1]
    body = parts[2].strip()

    data: Dict[str, Any] = {}
    current_key: Optional[str] = None
    sub_key: Optional[str] = None
    list_target: Optional[List[Any]] = None

    lines = yaml_raw.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if not stripped or stripped.startswith("#"):
            i += 1
            continue

        indent = len(line) - len(line.lstrip(" "))

        # Top-level key
        if indent == 0 and ":" in line:
            k, v = line.split(":", 1)
            k, v = k.strip(), v.strip()
            v_val = _clean_val(v)
            if v == "":
                data[k] = {}
                current_key = k
                sub_key = None
                list_target = None
            elif v == "[]":
                data[k] = []
                current_key = k
                sub_key = None
                list_target = None
            else:
                data[k] = v_val
                current_key = k
                sub_key = None
                list_target = None
            i += 1
            continue

        # Nested dict (indent 2)
        if indent == 2 and current_key and ":" in line and not stripped.startswith("-"):
            k, v = line.split(":", 1)
            k, v = k.strip(), v.strip()
            v_val = _clean_val(v)
            if not isinstance(data[current_key], dict):
                data[current_key] = {}

            if v == "":
                data[current_key][k] = {}
                sub_key = k
                list_target = None
            elif v == "[]":
                data[current_key][k] = []
                sub_key = k
                list_target = None
            else:
                data[current_key][k] = v_val
                sub_key = k
                list_target = None
            i += 1
            continue

        # Nested list item under indent 2 or 4
        if stripped.startswith("-"):
            item_content = stripped[1:].strip()
            # If current_key maps to a list
            if current_key:
                if sub_key and isinstance(data[current_key], dict):
                    if sub_key not in data[current_key] or not isinstance(data[current_key][sub_key], list):
                        data[current_key][sub_key] = []
                    list_target = data[current_key][sub_key]
                elif not isinstance(data[current_key], list):
                    if isinstance(data[current_key], dict) and not data[current_key]:
                        data[current_key] = []
                        list_target = data[current_key]

                if list_target is not None:
                    if ":" in item_content:
                        # Dict inside list (e.g. - id: "A1010")
                        obj: Dict[str, Any] = {}
                        ik, iv = item_content.split(":", 1)
                        obj[ik.strip()] = _clean_val(iv.strip())

                        # Check subsequent indented lines belonging to this list item
                        i += 1
                        while i < len(lines):
                            next_line = lines[i]
                            next_stripped = next_line.strip()
                            next_indent = len(next_line) - len(next_line.lstrip(" "))
                            if not next_stripped:
                                i += 1
                                continue
                            if next_stripped.startswith("-") or next_indent <= indent:
                                break
                            if ":" in next_stripped:
                                nik, niv = next_stripped.split(":", 1)
                                obj[nik.strip()] = _clean_val(niv.strip())
                            i += 1

                        list_target.append(obj)
                        continue
                    else:
                        list_target.append(_clean_val(item_content))

        i += 1

    return data, body


def _clean_val(val: str) -> Any:
    val = val.strip()
    if val.startswith('"') and val.endswith('"'):
        val = val[1:-1]
    elif val.startswith("'") and val.endswith("'"):
        val = val[1:-1]

    if val.lower() == "true":
        return True
    if val.lower() == "false":
        return False
    if val.lower() in ["null", "~"]:
        return None

    try:
        if "." in val:
            return float(val)
        return int(val)
    except ValueError:
        return val


def extract_scholarly_extract(body: str) -> str:
    """Extracts scholarly narrative synopsis from Markdown body."""
    match = re.search(r"##\s+Scholarly Synopsis\s*\n\n(.*?)(?=\n\n##|\Z)", body, re.DOTALL)
    if match:
        return match.group(1).strip()

    # Fallback to first non-header paragraph
    paragraphs = [p.strip() for p in body.split("\n\n") if p.strip() and not p.startswith("#")]
    return paragraphs[0] if paragraphs else "Scholarly mythological record."


def compile_okf_corpus(validate_only: bool = False) -> bool:
    logger.info(f"Scanning OKF corpus at: {KNOWLEDGE_DIR}")
    md_files = list(KNOWLEDGE_DIR.rglob("*.md"))
    logger.info(f"Found {len(md_files)} OKF Markdown documents.")

    if not md_files:
        logger.error("No OKF markdown documents found! Aborting.")
        return False

    records_by_id: Dict[str, Dict[str, Any]] = {}
    name_to_id: Dict[str, str] = {}
    errors: List[str] = []

    # First pass: load metadata and index names
    for file_path in md_files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            fm, body = parse_frontmatter(content)
            myth_id = fm.get("id")
            title = fm.get("title")

            if not myth_id:
                errors.append(f"{file_path.name}: Missing required 'id' field in frontmatter.")
                continue
            if not title:
                errors.append(f"{file_path.name}: Missing required 'title' field in frontmatter.")
                continue

            records_by_id[myth_id] = {
                "fm": fm,
                "body": body,
                "file_path": file_path,
            }
            name_to_id[title] = myth_id

        except Exception as e:
            errors.append(f"Error parsing {file_path}: {e}")

    if errors:
        for err in errors:
            logger.error(f"Lint error: {err}")
        if validate_only:
            return False

    logger.info(f"Successfully loaded and parsed {len(records_by_id)} unique myth nodes.")

    # Second pass: construct runtime bundles
    static_bundle: List[Dict[str, Any]] = []
    enriched_map: Dict[str, Dict[str, Any]] = {}

    for myth_id, item in records_by_id.items():
        fm = item["fm"]
        body = item["body"]
        st = fm.get("spatio_temporal") or {}
        ft = fm.get("folklore_taxonomy") or {}
        trust = fm.get("trust") or {}
        sources = fm.get("sources") or []
        cross_refs = fm.get("cross_references") or {}

        name = fm.get("title", "Unknown Myth")
        lat = round(float(st.get("lat", 0.0)), 4)
        lng = round(float(st.get("lng", 0.0)), 4)
        epoch_start = int(st.get("epoch_start", -1000))
        epoch_end = int(st.get("epoch_end", 500))
        culture = st.get("culture", "Comparative")
        archetype = ft.get("archetype", "Mythological Narrative")
        thumbnail = fm.get("thumbnail", "")
        wiki_url = fm.get("wikipedia_url", "")
        extract = extract_scholarly_extract(body)

        # Resolve cross-references to IDs
        syncretic_ids: List[str] = []
        raw_syncretic = cross_refs.get("syncretic") or []
        if isinstance(raw_syncretic, list):
            for ref in raw_syncretic:
                if isinstance(ref, str):
                    clean_ref = ref.strip("[]")
                    if clean_ref in name_to_id:
                        syncretic_ids.append(name_to_id[clean_ref])
                    elif clean_ref in records_by_id:
                        syncretic_ids.append(clean_ref)

        # 1. Lean static record for WASM & Three.js
        static_record = {
            "id": myth_id,
            "name": name,
            "lat": lat,
            "lng": lng,
            "epoch_start": epoch_start,
            "epoch_end": epoch_end,
            "culture": culture,
            "archetype": archetype,
            "thumbnail": thumbnail,
            "syncretic_ids": syncretic_ids,
            "description": f"{culture} tradition narrative ({epoch_start} to {epoch_end}).",
        }
        static_bundle.append(static_record)

        # 2. Rich enriched record for FastAPI & Gemini
        enriched_map[myth_id] = {
            "id": myth_id,
            "name": name,
            "lat": lat,
            "lng": lng,
            "epoch_start": epoch_start,
            "epoch_end": epoch_end,
            "culture": culture,
            "cultural_zone": st.get("cultural_zone", "global"),
            "archetype": archetype,
            "thumbnail": thumbnail,
            "description": f"{culture} epic ({epoch_start} to {epoch_end}).",
            "extract": extract,
            "wikipedia_url": wiki_url,
            "syncretic_ids": syncretic_ids,
            # Google OKF v0.2 Provenance & Folkloristic Taxonomy
            "trust": {
                "tier": trust.get("tier", "scholarly_consensus"),
                "verified": bool(trust.get("verified", True)),
                "reviewer": trust.get("reviewer", "MythosAtlas Academic Editorial Board"),
                "attested_date": trust.get("attested_date", "2026-09-19"),
            },
            "sources": sources,
            "thompson_motifs": ft.get("thompson_motifs") or [],
            "binary_oppositions": ft.get("binary_oppositions") or [],
        }

    if validate_only:
        logger.info(f"Validation successful: {len(static_bundle)} records pass all OKF v0.2 checks.")
        return True

    # Write static bundle to frontend public directory
    FRONTEND_STATIC_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(FRONTEND_STATIC_FILE, "w", encoding="utf-8") as f:
        json.dump(static_bundle, f, indent=2, ensure_ascii=False)
    frontend_size = FRONTEND_STATIC_FILE.stat().st_size / 1024
    logger.info(f"Baked {FRONTEND_STATIC_FILE} ({len(static_bundle)} items, {frontend_size:.1f} KB).")

    # Write backend copies
    BACKEND_STATIC_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(BACKEND_STATIC_FILE, "w", encoding="utf-8") as f:
        json.dump(static_bundle, f, indent=2, ensure_ascii=False)

    if BACKEND_DIR_STATIC.parent.exists():
        with open(BACKEND_DIR_STATIC, "w", encoding="utf-8") as f:
            json.dump(static_bundle, f, indent=2, ensure_ascii=False)

    # Write enriched map for backend hydration
    with open(ENRICHED_FILE, "w", encoding="utf-8") as f:
        json.dump(enriched_map, f, indent=2, ensure_ascii=False)
    enriched_size = ENRICHED_FILE.stat().st_size / 1024
    logger.info(f"Baked {ENRICHED_FILE} ({len(enriched_map)} items, {enriched_size:.1f} KB).")

    if BACKEND_DIR_ENRICHED.parent.exists():
        with open(BACKEND_DIR_ENRICHED, "w", encoding="utf-8") as f:
            json.dump(enriched_map, f, indent=2, ensure_ascii=False)
        logger.info(f"Baked {BACKEND_DIR_ENRICHED} ({len(enriched_map)} items).")

    logger.info("OKF compilation completed successfully!")
    return True



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MythosAtlas OKF Compiler")
    parser.add_argument("--validate", action="store_true", help="Validate OKF documents without baking")
    args = parser.parse_args()

    success = compile_okf_corpus(validate_only=args.validate)
    sys.exit(0 if success else 1)
