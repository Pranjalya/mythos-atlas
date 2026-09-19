# MythosAtlas Open Knowledge Format (OKF v0.2) Profile Specification

## 1. Overview

This document defines the normative specification for **MythosAtlas Open Knowledge Format (OKF v0.2)**, adhering to the open, vendor-neutral specification published under `GoogleCloudPlatform/open-knowledge-format`.

The purpose of this format is to establish a human-readable, agent-traversable, and Git-versioned knowledge graph of global mythological narratives, folkloric motifs, and sacred geographies from **-4000 BCE to 1500 CE**.

## 2. Directory Structure

```text
knowledge/
├── SPEC.md                           # This normative specification
├── log.md                            # Append-only chronological provenance ledger
└── myths/
    ├── ancient_near_east/            # Cultural Zone
    │   ├── mesopotamian/             # Tradition / Culture
    │   │   ├── epic_of_gilgamesh.md  # OKF Concept Node
    │   │   ├── atrahasis_epic.md
    │   │   └── ...
    │   ├── egyptian/
    │   └── levantine_canaanite/
    ├── greco_roman/
    │   ├── classical_greek/
    │   └── roman/
    ├── indic/
    │   ├── vedic_hindu/
    │   └── buddhist_jain/
    ├── east_asian/
    │   ├── chinese/
    │   └── japanese/
    ├── mesoamerican/
    │   ├── maya/
    │   └── aztec_nahua/
    ├── andean/
    ├── nordic_germanic/
    ├── celtic/
    ├── african_diaspora/
    │   ├── yoruba/
    │   └── bantu_congo/
    ├── polynesian_oceanic/
    ├── north_american_indigenous/
    └── finno_ugric_slavic/
```

## 3. OKF Concept Node Schema (Markdown + YAML Frontmatter)

Every mythological narrative is stored in a standalone `.md` file consisting of:
1. **Strict YAML Frontmatter** containing typed spatio-temporal, folkloristic, and provenance metadata.
2. **Markdown Narrative Body** containing the scholarly synopsis, structural analysis, and excerpted primary text translations.

### 3.1 YAML Frontmatter Fields

```yaml
---
# === Identity ===
id: "Q248352"                          # Wikidata QID or unique canonical slug
title: "Epic of Gilgamesh"             # Standard scholarly title
type: "myth_narrative"                 # Concept type: myth_narrative | archetype | motif
status: "active"                       # Lifecycle: active | draft | deprecated

# === Google OKF v0.2 Trust & Verification Signals ===
trust:
  tier: "scholarly_consensus"          # scholarly_consensus | canonical_scripture | academic_peer_reviewed | folklore_variant | machine_confirmed
  verified: true                       # Boolean attestation flag
  reviewer: "MythosAtlas Academic Editorial Board"
  attested_date: "2026-09-19"

# === Spatio-Temporal Anchor ===
spatio_temporal:
  culture: "Mesopotamian"              # Cultural tradition
  cultural_zone: "ancient_near_east"   # High-level regional classification
  epoch_start: -2100                   # Proved inception year (BCE negative, CE positive)
  epoch_end: -1200                     # Historical canonization terminus
  lat: 31.32                           # Geographic latitude anchor (decimal degrees)
  lng: 45.63                           # Geographic longitude anchor (decimal degrees)
  historical_locus: "Uruk, Sumer (Modern Warka, Iraq)"

# === Comparative Folklore Taxonomy ===
folklore_taxonomy:
  archetype: "Deluge / Quest for Immortality"
  thompson_motifs:                     # Stith Thompson Motif-Index of Folk-Literature
    - id: "A1010"
      name: "Deluge: Inundation of whole world"
    - id: "D1856"
      name: "Immortality through sacred plant or herb"
    - id: "F81"
      name: "Descent to lower world (Katabasis)"
  campbell_stages:                     # Joseph Campbell Monomyth Stages
    - "Call to Adventure"
    - "Supernatural Aid (Shamash)"
    - "Crossing the First Threshold (Cedar Forest)"
    - "Abyss / Ultimate Ordeal (Death of Enkidu)"
  binary_oppositions:                  # Claude Lévi-Strauss Structuralist Dualities
    - "Mortal Fragility vs. Divine Immortality"
    - "Wild Nature (Enkidu) vs. Urban Statecraft (Uruk)"
    - "Heroic Fame vs. Inevitable Dust"

# === Primary Ancient Sources & Academic Provenance ===
sources:
  - title: "The Epic of Gilgamesh: The Babylonian Epic Poem and Other Texts"
    citation: "Standard Babylonian 12-tablet version attributed to Sîn-lēqi-unninni; critical edition & translation by Andrew George (Penguin Classics, 2003)"
    url: "https://www.britishmuseum.org/collection/object/W_K-3375"
    credibility: "primary_ancient_text"
  - title: "The Sumerian Bilgames Poems"
    citation: "Old Babylonian cuneiform tablets from Nippur and Ur; trans. Jeremy Black et al., Electronic Text Corpus of Sumerian Literature (ETCSL)"
    url: "https://etcsl.orinst.ox.ac.uk/"
    credibility: "academic_peer_reviewed"

# === Cross-Cultural Links & Graph Edges ===
cross_references:
  syncretic:
    - "[[Atrahasis Epic]]"
    - "[[Noah's Ark and the Great Flood]]"
    - "[[Matsya Avatar and King Manu]]"
  variants:
    - "[[Sumerian Poem of Bilgames and the Netherworld]]"
---
```

## 4. Compilation Contract

The OKF compiler (`etl/okf_compiler.py`) transforms the directory of Markdown documents into runtime assets:

1. **`frontend/public/data/static_myths.json`**:
   Quantized, minimal representation required by WebAssembly Interval Tree and Three.js 3D rendering.
2. **`backend/data/processed/enriched_myths.json`**:
   Full hydration object including primary citations, trust badges, and Thompson motifs for API delivery.
3. **Qdrant Vector Embeddings**:
   768D dense vector space computed from combined narrative and folkloric taxonomy.

## 5. Trust Tier Definitions

- `scholarly_consensus`: Validated by broad modern academic consensus (peer-reviewed critical editions, archaeological evidence).
- `canonical_scripture`: Documented in historical canonical religious/literary codices (e.g., Vedas, Torah, Homeric epics).
- `academic_peer_reviewed`: Supported by specific published folkloristic or philological scholarship.
- `folklore_variant`: Living or recorded oral tradition variant.
- `machine_confirmed`: Synthesized by automated pipeline with algorithmic cross-referencing, pending human scholarly review.
