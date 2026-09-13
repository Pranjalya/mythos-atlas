# MythosAtlas 🌐⚔️

> **Interactive 3D Spatio-Temporal Mythic Atlas & Comparative Knowledge Engine**  
> Visualizing how mythological narratives, folklore motifs, and sacred geographies evolved and diffused across civilizations from **-4000 BCE to 1500 CE**.

![Rust](https://img.shields.io/badge/Rust-1.80+-orange.svg?style=flat-square&logo=rust)
![WebAssembly](https://img.shields.io/badge/WASM-engine--wasm-654ff0.svg?style=flat-square&logo=webassembly)
![Three.js](https://img.shields.io/badge/Three.js-WebGL_Cartography-black.svg?style=flat-square&logo=three.js)
![FastAPI](https://img.shields.io/badge/FastAPI-Python_3.12+-009688.svg?style=flat-square&logo=fastapi)
![Qdrant](https://img.shields.io/badge/Qdrant-768D_Dense_Vectors-dc2626.svg?style=flat-square)
![Gemini](https://img.shields.io/badge/Google_Gemini-Comparative_Synthesis-4285f4.svg?style=flat-square&logo=google)
![Dataset](https://img.shields.io/badge/Myths-331_Global_Epics-e6b86a.svg?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green.svg?style=flat-square)

---

## 🏛️ Architectural Paradigm: Tiered Hybrid

MythosAtlas bridges high-frequency client-side WebGL cartography with on-demand cloud intelligence:

```text
                          ┌──────────────────────────────────────────────────────────┐
                          │                Client-Side (Vite + TS)                   │
                          │                                                          │
                          │  ┌───────────────────────┐   ┌────────────────────────┐  │
                          │  │   Three.js 3D Globe   │   │  Timeline UI (-4000 to │  │
                          │  │  InstancedMesh Nodes  │◄──┤       +1500 CE)        │  │
                          │  │  Syncretic Bezier Arcs│   └───────────┬────────────┘  │
                          │  │  Constellation Blooms │               │               │
                          │  └───────────▲───────────┘               │ discrete year │
                          │              │ 60+ FPS direct buffer     │ query         │
                          │              │ updates (0ms network)     │               │
                          │  ┌───────────┴───────────────────────────▼────────────┐  │
                          │  │      Rust WASM Core (engine-wasm)                  │  │
                          │  │   1D Interval Tree + Static Spatial Bounds Index   │  │
                          │  └───────────────────▲────────────────────────────────┘  │
                          │                      │ pre-baked static bundle           │
                          │                      │ (206 KB static_myths.json)        │
                          └──────────────────────┼───────────────────────────────────┘
                                                 │
                                                 │ On-demand hydration & semantic search
                                                 │ (Inspect / Compare / Qdrant Vectors)
                                                 │
                          ┌──────────────────────▼───────────────────────────────────┐
                          │               Backend Dynamic Knowledge Layer            │
                          │                     (FastAPI + Python)                   │
                          │                                                          │
                          │   ┌────────────────────────┐  ┌───────────────────────┐  │
                          │   │   Qdrant Vector DB     │  │   Gemini LLM Engine   │  │
                          │   │  768D nomic-embed-text │  │  Comparative Matrix   │  │
                          │   │  Cross-Cultural Search │  │  Structural Typology  │  │
                          │   └────────────────────────┘  └───────────────────────┘  │
                          └──────────────────────────────────────────────────────────┘
```

1. **Client-Side Spatio-Temporal Core (Static + WASM):** High-frequency timeline scrubbing (-4000 BCE to 1500 CE) runs entirely in the browser at **60+ FPS with 0ms network roundtrips**. A Rust module compiled to WebAssembly (WASM) holds an in-memory 1D interval tree and spatial bounds to filter active entities from a pre-baked static bundle directly into Three.js rendering buffers.
2. **Dynamic Knowledge Layer (FastAPI + Qdrant + Gemini):** On-demand hydration triggered when a user selects a myth node, searches natural language queries, clicks an archetype, or initiates cross-cultural comparison. The backend orchestrates 768-dimensional motif vector retrieval (`nomic-embed-text-v1.5`), syncretic graph traversal, and structuralist synthesis.

---

## ✨ Key Features

### 🎬 Cinematic Curated Expeditions ("Story Mode")
- **Documentary-Style Guided Tours**: Overcomes the "where do I click first?" dilemma with curated planetary camera journeys tracing humanity's foundational mythic motifs across six continents.
- **4 Flagship Curated Expeditions**:
  1. **The Great Deluge Across 6 Continents** (7 Chapters): Mesopotamia (Gilgamesh & Atrahasis) $\rightarrow$ Levant (Noah's Ark) $\rightarrow$ India (Matsya Avatar) $\rightarrow$ China (Nüwa Mends Heavens) $\rightarrow$ Mesoamerica (Popol Vuh) $\rightarrow$ Andes (Mapuche Trentren & Caicai Vilu).
  2. **Descent into the Underworld (Katabasis)** (6 Chapters): Mesopotamia (Inanna) $\rightarrow$ Egypt (Osiris) $\rightarrow$ Greece (Orpheus) $\rightarrow$ Japan (Izanami) $\rightarrow$ Maya (Hero Twins in Xibalba).
  3. **The Promethean Fire-Stealers** (5 Chapters): Greece (Prometheus) $\rightarrow$ North America (Coyote & Raven) $\rightarrow$ Polynesia (Māui) $\rightarrow$ West Africa (Anansi).
  4. **The Chaoskampf: Slaying the Primordial Serpent** (6 Chapters): Mesopotamia (Marduk) $\rightarrow$ Levant (Baal) $\rightarrow$ Greece (Apollo) $\rightarrow$ Norse (Thor) $\rightarrow$ Japan (Susanoo) $\rightarrow$ Cherokee (Uktena).
- **Planetary Great-Circle Glides & Parabolic Flight**: Smooth 3D camera sweeps featuring orbital parabolic ascent and descent over oceans and mountain ranges.
- **Glowing Celestial Historical Trails**: Glowing golden Bezier trails dynamically connecting visited chapters across space and time with pulsing waypoint beacons.
- **Cinematic Story HUD**: Floating glassmorphic narrative cards presenting chapter titles, cultural lineages, atmospheric prose leads, comparative archetype threads, and motif tags.
- **Autonomous Auto-Play Engine**: Integrated 12-second countdown timer, keyboard shortcuts (`Space` to toggle auto-play, `←` / `→` for chapters, `Esc` to exit), and interactive chapter progression track.
- **Odyssey Finale & AI Synthesis**: Concludes with celebratory synthesis cards allowing 1-click comparative copilot analysis between the origin and culmination of the motif.

### 🌍 3D Celestial WebGL Globe (`Three.js`)
- **Modern Country Cartography**: 177 modern vector country boundaries rendered via high-precision GeoJSON line segments with toggleable border overlays (`#btn-toggle-borders`).
- **Country Hover Intelligence**: Raycasts Earth surface coordinates in real time to identify modern sovereign states, continents, and their ancient mythological roots.
- **Concurrent Narrative Constellation Blooming**: When multiple myths occur at the same sacred location and epoch (e.g. Rome, Thebes, Varanasi, Kyoto, Tenochtitlan), the primary locus dynamically blooms satellite nodes in an equilateral orbital ring connected by glowing constellation arcs.
- **Syncretic Diffusion Arcs**: Pulsing quadratic Bezier curves connecting culturally syncretic nodes across continents (e.g., Inanna $\rightarrow$ Ishtar $\rightarrow$ Astarte $\rightarrow$ Aphrodite).
- **Procedural Atmospheres**: Custom atmospheric twilight Fresnel glow shaders, dark ocean textures, graticule gridlines, and smooth camera fly-to transitions.

### ⏳ High-Performance WASM Timeline Scrubber (`Rust`)
- **Continuous Scrubbing**: Scrub across 5,500 years of recorded human narrative (-4000 BCE to 1500 CE).
- **Sub-Millisecond Interval Queries**: 1D Interval Tree queries in $O(\log N + K)$ time with continuous visual intensity calculations.
- **Landmark Epoch Pills**: Instant temporal navigation across civilizational eras (Bronze Age, Bronze Age Collapse, Axial Age, Classical, Medieval, Late Medieval).

### 🔍 Omnisearch with Semantic Natural Language ("Ask the Atlas")
- **Global Keybinding**: Press `Cmd + K` (or `Ctrl + K`) anywhere, or click the search bar in the top navigation.
- **Dual-Engine Discovery**:
  - **⚡ Instant 0ms Keyword Matching**: Instant client-side lookup across all 331 myths for heroes, motifs, deities, and traditions (e.g., *"Gilgamesh"*, *"snake"*, *"underworld"*, *"Norse"*, *"Japan"*).
  - **🔮 Natural Language Vector Search**: Debounced semantic queries dispatched to FastAPI `/api/v1/myths/search/semantic`, matching against Qdrant Cloud's 768-dimensional `nomic-embed-text-v1.5` embeddings (e.g., *"Where did dragon myths come from?"*, *"Show me female sun deities"*), returning ranked results with percentage similarity scores.
- **Interactive Navigation & Temporal Sync**: Selecting any myth updates the timeline epoch to its flourishing era, sweeps the Three.js camera to its exact locus, blooms its constellation, and hydrates the inspector.

### 🧭 "Surprise Me" (Random Pilgrim Mode)
- **Kinetic Pilgrim Journey**: Clicking the glowing compass button (`🧭 Surprise Me`) triggers a 1080° rotating compass animation, picks a random extraordinary myth across worldwide traditions, adjusts the temporal epoch, glides the camera across the globe, blooms the locus, and hydrates the inspector side-panel.

### 📜 Side-Panel Entity Inspector & Sacred Epicenter Cluster Deck
- **Sacred Epicenter Deck**: For multi-epic sites, an interactive horizontal tabbed pill deck allows switching seamlessly between concurrent epics without losing geographical context.
- **Rich Narrative Leads**: Enriched historical summaries, sacred coordinates, and Wikimedia Commons thumbnails.
- **"Find Parallels"**: Queries the 768-dimensional dense motif vector space in **Qdrant Cloud** to retrieve top global counterparts across continents with similarity scores.

### ⚖️ Comparative Copilot Modal (`Google Gemini`)
- **Dual-Tradition Matrix**: Synthesizes structural comparisons analyzing character archetypes (protagonist agency, adversary dynamics, supernatural allies), inciting motifs (catalyst events, sacred taboos), and cosmological resolutions.
- **Structuralist Typology**: Evaluates whether cross-cultural narrative symmetries stem from **Cognitive Convergence** (universal human psychology) or **Historical Diffusion** (trade routes and syncretism) with scholarly rationales.

### 📱 Mobile-Responsive Architecture (`< 900px`)
- **Native Bottom Sheet Inspector**: Transforms the desktop floating panel into a slide-up bottom sheet with tactile drag handle, swipe-down dismissal, and horizontal cluster pill scrolling.
- **Mobile Camera Framing**: Automatically offsets camera latitude (`latOffset = -12°`) to frame the 3D globe in the upper viewport directly above the bottom sheet.
- **Adaptive Touch Controls**: Collapsible hamburger drawer, compact touch timeline, and floating creator pill that expands into a focused modal.

---

## 📁 Monorepo Layout

```text
mythos-atlas/
├── etl/                         # Offline data collection & pipeline scripts
│   ├── wikidata_sparql.py       # SPARQL extraction for entities, inceptions, & coords
│   ├── wikipedia_scraper.py     # Wikipedia narrative extractor with disk caching
│   ├── embed_and_index.py       # Generates 768D dense vectors & populates Qdrant Cloud
│   ├── bake_static_data.py      # Compiles lean JSON bundle for WASM client (206 KB)
│   ├── run_pipeline.py          # Master single-command ETL pipeline orchestrator
│   └── tests/
│       └── test_data_integrity.py# Automated tests for coordinates, epochs, and schemas
├── engine-wasm/                 # Rust core for client-side spatial-temporal filtering
│   ├── Cargo.toml
│   ├── src/
│   │   ├── lib.rs               # wasm-bindgen entry point (load_records, query_timeline)
│   │   ├── interval_tree.rs     # 1D timeline interval tree (BCE/CE intervals)
│   │   └── spatial.rs           # Great circle distance & spherical coordinate math
│   └── tests/
│       └── timeline_tests.rs    # Real-dataset interval query integration tests
├── backend/                     # Dynamic comparative backend
│   ├── app/
│   │   ├── main.py              # FastAPI application entry point with CORS
│   │   ├── config.py            # Pydantic environment settings (.env)
│   │   ├── routes/
│   │   │   ├── myths.py         # Entity detail, semantic search, & syncretic subgraph
│   │   │   └── compare.py       # Cross-tradition semantic & structural comparison
│   │   └── services/
│   │       ├── qdrant_svc.py    # 768D motif vector search & parallel retrieval
│   │       └── llm_svc.py       # Google Gemini structural comparative synthesis
│   ├── tests/
│   │   └── test_api.py          # FastAPI endpoint integration test suite
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/                    # Interactive 3D WebGL client
│   ├── package.json
│   ├── vite.config.ts
│   ├── index.html
│   └── src/
│       ├── main.ts              # App entry point, WASM bootstrap, and UI event binding
│       ├── style.css            # Dark obsidian & celestial gold glassmorphic design system
│       ├── components/
│       │   ├── Globe.ts         # Three.js globe, shader atmospheres, & constellation blooms
│       │   ├── Timeline.ts      # Scrubbing UI slider with WASM interval queries
│       │   ├── Inspector.ts     # Side-panel & sacred epicenter cluster deck
│       │   ├── CompareModal.ts  # Dual-tradition comparison matrix
│       │   ├── Omnisearch.ts    # Dual-engine Cmd+K search ("Ask the Atlas")
│       │   └── PilgrimMode.ts   # "Surprise Me" random discovery engine
│       ├── wasm/                # Generated wasm-pack bindings & WebAssembly binary
│       └── state/
│           └── store.ts         # Reactive state store
└── data/                        # Generated artifacts
    ├── raw/
    │   ├── wikidata_raw.json
    │   ├── wikipedia_cache.json
    │   └── wikipedia_enriched.json
    └── processed/
        ├── static_myths.json    # Lean 206 KB payload serving 331 myths to WASM client
        ├── enriched_myths.json  # Full metadata dictionary for backend hydration (363 KB)
        └── motif_embeddings.json# Local 768D vector cache for offline search (6.9 MB)
```

---

## 📜 Cultural Traditions Covered

MythosAtlas includes **331 foundational narratives** spanning **19 cultural and indigenous traditions** across all inhabited continents:

| Tradition | Count | Representative Epics & Motifs | Temporal Range |
| :--- | :---: | :--- | :--- |
| **Greco-Roman** | 30 | *Iliad & Odyssey*, *Prometheus Bound*, *Eleusinian Mysteries*, *Aeneid*, *Capitoline Triad* | -800 BCE to 395 CE |
| **Vedic & Hindu** | 29 | *Samudra Manthana*, *Nasadiya Sukta*, *Ramayana*, *Mahabharata*, *Descent of Ganges* | -1500 BCE to 600 CE |
| **East Asian** | 27 | *Nuwa Mends Heavens*, *Pangu Cosmic Egg*, *Journey to the West*, *Kojiki (Izanami)*, *Dangun* | -1000 BCE to 1592 CE |
| **Southeast Asian** | 18 | *Dewi Sri (Rice Goddess)*, *Barong vs Rangda*, *Bakunawa and Seven Moons*, *Lac Long Quan* | -700 BCE to 1600 CE |
| **Oceanic & Australasian** | 18 | *Rainbow Serpent (Dreamtime)*, *Māui Fishing Up New Zealand*, *Kumulipo*, *Pele & Namakaokahai* | -4000 BCE to 1700 CE |
| **Levantine** | 17 | *Baal Cycle*, *Astarte and the Sea*, *Genesis Deluge (Noah's Ark)*, *Tower of Babel* | -1500 to -300 BCE |
| **Celtic** | 17 | *Táin Bó Cúailnge (Cú Chulainn)*, *Quest for the Holy Grail*, *Children of Lir*, *Tuatha Dé Danann* | 100 to 1485 CE |
| **North American Indigenous** | 17 | *Diné Bahane' (Navajo Emergence)*, *Sedna (Inuit)*, *Raven Tales*, *White Buffalo Calf Woman* | -1500 BCE to 1700 CE |
| **Mesoamerican** | 17 | *Popol Vuh (Hero Twins)*, *Quetzalcoatl*, *Legend of the Fifth Sun*, *Kukulcan*, *Taino Gourd* | -100 BCE to 1550 CE |
| **West African** | 17 | *Epic of Sundiata (Lion King)*, *Anansi the Spider*, *Yoruba Creation at Ife*, *Shango* | 800 to 1700 CE |
| **Norse & Germanic** | 16 | *Ragnarök*, *Thor's Fishing Trip for Jörmungandr*, *Odin on Yggdrasil*, *Baldr's Death* | 600 to 1250 CE |
| **Andean & South American** | 16 | *Viracocha Creation at Titicaca*, *Ayar Brothers (Cusco)*, *Mapuche Deluge*, *Guarani Creation* | 200 to 1600 CE |
| **Egyptian** | 15 | *Osiris Myth & Resurrection*, *Isis*, *Contendings of Horus and Seth*, *Book of the Dead* | -2600 to 400 CE |
| **Persian & Iranian** | 15 | *Ahura Mazda vs Angra Mainyu*, *Shahnameh (Rostam and Sohrab)*, *Simurgh*, *Jamshid* | -1200 BCE to 1010 CE |
| **Mesopotamian** | 14 | *Epic of Gilgamesh*, *Enuma Elish*, *Descent of Inanna*, *Atrahasis*, *Marduk* | -2300 to -539 BCE |
| **Slavic & Baltic** | 14 | *Perun vs Veles*, *Baba Yaga*, *Perkūnas & Saule (Baltic Sun and Thunder)* | 400 to 1500 CE |
| **Central Asian & Steppe** | 12 | *Tengri and Eternal Blue Sky*, *Epic of King Gesar (Tibet)*, *Epic of Manas (Kyrgyz)* | -1000 BCE to 1500 CE |
| **Central & Southern African** | 12 | *Unkulunkulu (Zulu)*, *Nommo Spirits (Dogon)*, *\|Kaggen (San)*, *Mwindo Epic* | -4000 BCE to 1700 CE |
| **Finno-Ugric** | 10 | *The Kalevala (Forging of Sampo)*, *Lemminkäinen's Resurrection*, *Kalevipoeg* | 800 to 1400 CE |

---

## 🛠️ Prerequisites

- **Rust & Cargo** (1.80+) with `wasm-pack` (`cargo install wasm-pack`)
- **Python 3.12+** (or `uv`)
- **Node.js 20+** and `npm`
- **API Credentials** (Optional, configure in `.env`):
  - `QDRANT_URL` and `QDRANT_API_KEY` (for Qdrant Cloud 768D vector search)
  - `GEMINI_API_KEY` (for Google Gemini structural comparison synthesis)

---

## 🚀 Quickstart Guide

### 1. Clone & Set Up Environment

```bash
git clone https://github.com/Pranjalya/mythos-atlas.git
cd mythos-atlas

# Create Python virtual environment using uv or standard venv
uv venv
source .venv/bin/activate

# Install backend dependencies
uv pip install -r backend/requirements.txt
```

Create a `.env` file in the project root:

```env
QDRANT_URL=https://your-cluster.qdrant.io
QDRANT_API_KEY=your_qdrant_api_key
GEMINI_API_KEY=your_gemini_api_key
```

*(Note: MythosAtlas includes local 768D vector fallback and structural heuristic engines, so the system works even if external API keys are omitted).*

---

### 2. Build the Rust WebAssembly Engine

```bash
cd engine-wasm
wasm-pack build --target web
# Copy generated bindings into the frontend application
cp -r pkg/* ../frontend/src/wasm/
cd ..
```

---

### 3. Run the Data Pipeline (Optional)

The repository already contains the baked static dataset of 331 myths in `data/processed/`. To re-run extraction, Wikipedia scraping, and Qdrant indexing:

```bash
.venv/bin/python etl/run_pipeline.py
```

---

### 4. Start the FastAPI Backend

```bash
cd backend
../.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Interactive OpenAPI documentation is available at:
👉 **`http://127.0.0.1:8000/docs`**

---

### 5. Start the Vite 3D WebGL Client

In a separate terminal:

```bash
cd frontend
npm install
npm run dev
```

Open your browser at:
👉 **`http://127.0.0.1:5173`**

---

## 🧪 Testing & Quality Assurance

### Python Backend & ETL Tests
```bash
# Run ETL data integrity tests
.venv/bin/pytest etl/tests/test_data_integrity.py

# Run FastAPI backend endpoint tests
PYTHONPATH=backend .venv/bin/pytest backend/tests/test_api.py
```

### Rust Engine Tests
```bash
cd engine-wasm
cargo test
cd ..
```

### Frontend Typecheck & Production Build
```bash
cd frontend
npm run build
```

---

## 🔬 Data Contracts

### 1. Static Myth Schema (`static_myths.json`)
```json
[
  {
    "id": "Q248352",
    "name": "Epic of Gilgamesh",
    "lat": 31.32,
    "lng": 45.63,
    "epoch_start": -2100,
    "epoch_end": -1200,
    "culture": "Mesopotamian",
    "archetype": "Deluge / Quest for Immortality",
    "thumbnail": "https://upload.wikimedia.org/wikipedia/commons/...",
    "syncretic_ids": ["Q10801", "Q131379", "Q190535"],
    "description": "Epic poem from Mesopotamia"
  }
]
```

### 2. Rust/WASM Core Contract
- `load_records(records_json: &str) -> bool`: Deserializes records into an in-memory 1D interval tree.
- `query_timeline(year: i32) -> JsValue`: Queries overlapping intervals for a discrete year with continuous visual intensity calculations in $O(\log N + K)$ time.

### 3. Backend Endpoints
- `GET /api/v1/myths`: Lists all 331 available myth entities.
- `GET /api/v1/myths/{id}`: Returns enriched Wikipedia narrative and syncretic edges.
- `GET /api/v1/myths/search/semantic?q=...&limit=6`: Real-time semantic motif vector search using 768D `nomic-embed-text-v1.5` embeddings.
- `GET /api/v1/parallels/{id}?limit=3`: Dense vector search for top cross-cultural counterparts across continents.
- `POST /api/v1/compare`: Synthesizes dual-tradition structuralist matrix (archetypes, inciting motifs, cosmological resolution, and diffusion vs. convergence).

---

## 👤 Author

- **Pranjalya Tiwari**
- **GitHub Profile**: [@Pranjalya](https://github.com/Pranjalya)
- **LinkedIn**: [in/pranjalya-tiwari](https://linkedin.com/in/pranjalya-tiwari)
- **Project Repository**: [github.com/Pranjalya/mythos-atlas](https://github.com/Pranjalya/mythos-atlas)

---

## 📄 License

This project is open source and available under the terms of the [MIT License](LICENSE).
