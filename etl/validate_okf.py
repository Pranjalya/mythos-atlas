"""
OKF v0.2 Linter and Corpus Validator for MythosAtlas.
Enforces strict compliance with knowledge/SPEC.md:
  - Required frontmatter fields
  - Spatio-temporal bounding
  - OKF trust tier validation
  - Primary source citation integrity
  - Cross-reference wikilink resolution
"""

import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Set

from okf_compiler import parse_frontmatter

BASE_DIR = Path(__file__).resolve().parent.parent
KNOWLEDGE_DIR = BASE_DIR / "knowledge" / "myths"

VALID_TRUST_TIERS = {
    "scholarly_consensus",
    "canonical_scripture",
    "academic_peer_reviewed",
    "folklore_variant",
    "machine_confirmed",
}


def validate_corpus() -> bool:
    print(f"🔍 Validating Google OKF v0.2 compliance in {KNOWLEDGE_DIR}...")
    md_files = list(KNOWLEDGE_DIR.rglob("*.md"))
    if not md_files:
        print("❌ No OKF documents found!")
        return False

    all_ids: Set[str] = set()
    all_titles: Set[str] = set()
    errors: List[str] = []
    warnings: List[str] = []

    # First pass: collect IDs and Titles
    for f in md_files:
        with open(f, "r", encoding="utf-8") as fp:
            content = fp.read()
        fm, _ = parse_frontmatter(content)
        mid = fm.get("id")
        title = fm.get("title")

        if not mid:
            errors.append(f"{f.name}: Missing 'id'")
        elif mid in all_ids:
            errors.append(f"{f.name}: Duplicate id '{mid}'")
        else:
            all_ids.add(mid)

        if not title:
            errors.append(f"{f.name}: Missing 'title'")
        else:
            all_titles.add(title)

    # Second pass: validate detailed schema
    for f in md_files:
        with open(f, "r", encoding="utf-8") as fp:
            content = fp.read()
        fm, body = parse_frontmatter(content)
        name = f.name

        # Trust signals
        trust = fm.get("trust") or {}
        tier = trust.get("tier")
        if not tier:
            errors.append(f"{name}: Missing 'trust.tier'")
        elif tier not in VALID_TRUST_TIERS:
            errors.append(f"{name}: Invalid trust tier '{tier}' (must be one of {VALID_TRUST_TIERS})")

        # Spatio-temporal
        st = fm.get("spatio_temporal") or {}
        lat = st.get("lat")
        lng = st.get("lng")
        start = st.get("epoch_start")
        end = st.get("epoch_end")

        if lat is None or not (-90.0 <= float(lat) <= 90.0):
            errors.append(f"{name}: Invalid latitude '{lat}'")
        if lng is None or not (-180.0 <= float(lng) <= 180.0):
            errors.append(f"{name}: Invalid longitude '{lng}'")
        if start is None or end is None:
            errors.append(f"{name}: Missing epoch_start or epoch_end")
        elif int(start) > int(end):
            errors.append(f"{name}: epoch_start ({start}) > epoch_end ({end})")

        # Sources
        sources = fm.get("sources")
        if not sources or not isinstance(sources, list):
            warnings.append(f"{name}: No primary sources cited in frontmatter.")
        else:
            for s in sources:
                if not isinstance(s, dict) or not s.get("title") or not s.get("citation"):
                    errors.append(f"{name}: Malformed source entry (requires title and citation)")

        # Cross references wikilinks
        cross_refs = fm.get("cross_references") or {}
        syncretic = cross_refs.get("syncretic") or []
        if isinstance(syncretic, list):
            for ref in syncretic:
                if isinstance(ref, str) and ref.startswith("[[") and ref.endswith("]]"):
                    target_name = ref[2:-2]
                    if target_name not in all_titles:
                        warnings.append(f"{name}: Wikilink '{ref}' does not match any known title.")

        # Body check
        if not body or len(body) < 50:
            warnings.append(f"{name}: Narrative body is very short (<50 chars)")

    print(f"\n✅ Analyzed {len(md_files)} OKF documents.")
    if warnings:
        print(f"⚠️  {len(warnings)} Warnings:")
        for w in warnings[:10]:
            print(f"   • {w}")
        if len(warnings) > 10:
            print(f"   ... and {len(warnings) - 10} more warnings.")

    if errors:
        print(f"\n❌ {len(errors)} Validation Errors:")
        for e in errors:
            print(f"   • {e}")
        return False

    print("🎉 All OKF v0.2 validation checks passed successfully!")
    return True


if __name__ == "__main__":
    success = validate_corpus()
    sys.exit(0 if success else 1)
