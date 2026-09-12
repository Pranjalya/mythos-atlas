# MythosAtlas 🌐⚔️

> **Interactive 3D Spatio-Temporal Mythic Atlas & Comparative Knowledge Engine**  
> Visualizing how mythological narratives, folklore motifs, and sacred geographies evolved and diffused across civilizations from **-4000 BCE to 1500 CE**.

---

## 🏛️ Architectural Paradigm: Tiered Hybrid

MythosAtlas bridges high-frequency client-side cartography with on-demand cloud intelligence:

```text
                          ┌──────────────────────────────────────────────────────────┐
                          │                Client-Side (Vite + TS)                   │
                          │                                                          │
                          │  ┌───────────────────────┐   ┌────────────────────────┐  │
                          │  │   Three.js 3D Globe   │   │  Timeline UI (-4000 to │  │
                          │  │  InstancedMesh Nodes  │◄──┤       +1500 CE)        │  │
                          │  │  Syncretic Bezier Arcs│   └───────────┬────────────┘  │
                          │  └───────────▲───────────┘               │               │
                          │              │ 60+ FPS direct buffer     │ discrete year │
                          │              │ updates (0ms network)     │ query         │
                          │  ┌───────────┴───────────────────────────▼────────────┐  │
                          │  │      Rust WASM Core (engine-wasm)                  │  │
                          │  │   1D Interval Tree + Static Spatial Bounds Index   │  │
                          │  └───────────────────▲────────────────────────────────┘  │
                          │                      │ pre-baked static bundle           │
                          │                      │ (<5MB static_myths.json)          │
                          └──────────────────────┼───────────────────────────────────┘
                                                 │
                                                 │ On-demand hydration
                                                 │ (Inspect / Compare / Vector Search)
                                                 │
                          ┌──────────────────────▼───────────────────────────────────┐
                          │               Backend Dynamic Knowledge Layer            │
                          │                     (FastAPI + Python)                   │
                          │                                                          │
                          │   ┌────────────────────────┐  ┌───────────────────────┐  │
                          │   │   Qdrant Vector DB     │  │   Gemini LLM Engine   │  │
                          │   │  Motif Semantic Search │  │  Comparative Matrix   │  │
                          │   │  Cross-Cultural Matches│  │  Structural Typology  │  │
                          │   └────────────────────────┘  └───────────────────────┘  │
                          └──────────────────────────────────────────────────────────┘
```

1. **Client-Side Spatio-Temporal Core (Static + WASM):** High-frequency timeline scrubbing (-4000 BCE to 1500 CE) runs entirely in the browser at **60+ FPS with 0ms network roundtrips**. A Rust module compiled to WebAssembly (WASM) holds an in-memory 1D interval tree and spatial bounds to filter active entities from a pre-baked static bundle directly into Three.js rendering buffers.
2. **Dynamic Knowledge Layer (FastAPI + Qdrant + Gemini):** On-demand hydration triggered only when a user selects a myth node, clicks an archetype, or initiates a cross-cultural comparison. The backend orchestrates motif vector retrieval, syncretic graph traversal, and comparative structuralist synthesis.

---

## ✨ Key Features

- **3D Celestial WebGL Globe (`Three.js`)**:
  - **Modern Country Cartography**: 177 modern vector country boundaries rendered via high-precision GeoJSON line segments with toggleable border overlays (`#btn-toggle-borders`).
  - **Country Hover Intelligence**: Raycasts Earth surface coordinates in real time to identify modern sovereign states, continents, and their ancient mythological roots.
  - Procedural atmospheric twilight Fresnel glow shaders.
  - Interactive sphere with custom dark ocean textures, graticule gridlines, and topography.
  - Active myths rendered via `THREE.InstancedMesh` with visual scaling and colors mapped to civilizational traditions.
  - Pulsing quadratic Bezier curve arcs connecting culturally syncretic nodes (e.g. Inanna $\rightarrow$ Ishtar $\rightarrow$ Astarte $\rightarrow$ Aphrodite).
  - Smooth camera fly-to transitions and constrained OrbitControls.
- **High-Performance WASM Timeline Scrubber (`Rust`)**:
  - Continuous scrubbing across 5,500 years of recorded human narrative (-4000 BCE to 1500 CE).
  - 1D Interval Tree queries in $O(\log N + K)$ time with continuous visual intensity calculations.
  - Epoch landmark pills for instant temporal jumping (Early Bronze, Collapse, Axial Age, Classical, Medieval).
- **Side-Panel Entity Inspector**:
  - Live hydration of enriched narrative leads, sacred coordinates, and Wikimedia Commons thumbnails.
  - Interactive syncretic links allowing users to jump across cultural counterpart nodes.
  - **"Find Parallels" Button**: Queries the 384-dimensional dense motif vector space in **Qdrant Cloud** to retrieve top global counterparts across continents with similarity scores.
- **Comparative Copilot Modal (`Google Gemini`)**:
  - Dual-tradition comparison matrix analyzing character archetypes (protagonist agency, adversary dynamics, supernatural allies), inciting motifs (catalyst events, sacred taboos), and cosmological resolutions.
  - **Structuralist Typology**: Evaluates whether cross-cultural narrative symmetries stem from **Cognitive Convergence** (universal human psychology) or **Historical Diffusion** (trade routes and syncretism) with scholarly rationales.

---

## 📁 Monorepo Layout

```text
mythos-atlas/
├── etl/                         # Offline data collection & pipeline scripts
│   ├── wikidata_sparql.py       # SPARQL extraction for entities, inceptions, & coords
│   ├── wikipedia_scraper.py     # Wikipedia narrative extractor with disk caching
│   ├── embed_and_index.py       # Generates dense vectors & populates Qdrant Cloud
│   ├── bake_static_data.py      # Compiles lean JSON bundle for WASM client (<5MB)
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
│   │   │   ├── myths.py         # Entity detail retrieval & syncretic subgraph
│   │   │   └── compare.py       # Cross-tradition semantic & structural comparison
│   │   └── services/
│   │       ├── qdrant_svc.py    # Motif vector search & parallel retrieval
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
│       │   ├── Globe.ts         # Three.js globe, shader atmospheres, & instanced meshes
│       │   ├── Timeline.ts      # Scrubbing UI slider with WASM interval queries
│       │   ├── Inspector.ts     # Side-panel for entity deep-dives
│       │   └── CompareModal.ts  # Dual-tradition comparison matrix
│       ├── wasm/                # Generated wasm-pack bindings & WebAssembly binary
│       └── state/
│           └── store.ts         # Reactive state store
└── data/                        # Generated artifacts
    ├── raw/
    │   ├── wikidata_raw.json
    │   ├── wikipedia_cache.json
    │   └── wikipedia_enriched.json
    └── processed/
        ├── static_myths.json    # Quantized 31 KB payload served to WASM client
        ├── enriched_myths.json  # Full metadata dictionary for backend hydration
        └── motif_embeddings.json# Local 384D vector cache for offline search
```

---

## 📜 Cultural Traditions Covered

MythosAtlas includes 88+ foundational narratives spanning 19 cultural and indigenous traditions across all inhabited continents:

| Tradition | Representative Epics & Motifs | Temporal Range |
| :--- | :--- | :--- |
| **Mesopotamian** | *Epic of Gilgamesh*, *Enuma Elish*, *Descent of Inanna*, *Atrahasis*, *Marduk* | -2300 to -539 BCE |
| **Levantine** | *Baal Cycle*, *Astarte and the Sea*, *Genesis Deluge (Noah's Ark)* | -1500 to -300 BCE |
| **Egyptian** | *Osiris Myth & Resurrection*, *Isis*, *Contendings of Horus and Seth*, *Book of the Dead* | -2600 to 400 CE |
| **Greco-Roman** | *Homer's Iliad & Odyssey*, *Prometheus Bound*, *Eleusinian Mysteries*, *Aeneid* | -800 BCE to 395 CE |
| **Vedic & Hindu** | *Samudra Manthana*, *Nasadiya Sukta*, *Ramayana*, *Mahabharata*, *Descent of Ganges*, *Nataraja* | -1500 BCE to 600 CE |
| **Persian & Iranian** | *Ahura Mazda vs Angra Mainyu*, *Shahnameh (Rostam and Sohrab)*, *Simurgh*, *Jamshid* | -1200 BCE to 1010 CE |
| **Norse & Germanic** | *Ragnarök*, *Thor's Fishing Trip for Jormungandr*, *Odin on Yggdrasil*, *Baldr's Death* | 600 to 1250 CE |
| **Celtic** | *Táin Bó Cúailnge (Cu Chulainn)*, *Quest for the Holy Grail*, *Children of Lir* | 100 to 1485 CE |
| **Slavic & Baltic** | *Perun vs Veles*, *Baba Yaga*, *Perkūnas & Saule (Baltic Sun and Thunder)* | 400 to 1500 CE |
| **Finno-Ugric** | *The Kalevala (Forging of Sampo)*, *Lemminkäinen's Resurrection*, *Kalevipoeg* | 800 to 1400 CE |
| **East Asian** | *Nuwa Mends Heavens*, *Pangu Cosmic Egg*, *Journey to the West*, *Kojiki (Izanami)*, *Dangun* | -1000 BCE to 1592 CE |
| **Central Asian & Steppe** | *Tengri and Eternal Blue Sky*, *Epic of King Gesar (Tibet)*, *Epic of Manas (Kyrgyz)* | -1000 BCE to 1500 CE |
| **Southeast Asian** | *Dewi Sri (Rice Goddess)*, *Barong vs Rangda*, *Bakunawa and Seven Moons*, *Lac Long Quan* | -700 BCE to 1600 CE |
| **North American Indigenous** | *Diné Bahane' (Navajo Emergence)*, *Sedna (Inuit)*, *Raven Tales (Haida)*, *White Buffalo Calf Woman*, *Sky Woman* | -1500 BCE to 1700 CE |
| **Mesoamerican** | *Popol Vuh (Hero Twins)*, *Quetzalcoatl*, *Legend of the Fifth Sun*, *Kukulcan*, *Taino Gourd* | -100 BCE to 1550 CE |
| **Andean & South American** | *Viracocha Creation at Titicaca*, *Ayar Brothers (Cusco)*, *Mapuche Deluge*, *Guarani Creation* | 200 to 1600 CE |
| **West African** | *Epic of Sundiata (Lion King)*, *Anansi the Spider*, *Yoruba Creation at Ife*, *Shango* | 800 to 1700 CE |
| **Central & Southern African** | *Unkulunkulu (Zulu)*, *Nommo Spirits (Dogon)*, *\|Kaggen (San)*, *Mwindo Epic*, *Kintu (Buganda)* | -4000 BCE to 1700 CE |
| **Oceanic & Australasian** | *Rainbow Serpent (Dreamtime)*, *Māui Fishing Up New Zealand*, *Kumulipo*, *Pele & Namakaokahai*, *Rangi & Papa* | -4000 BCE to 1700 CE |

---

## 🛠️ Prerequisites

- **Rust & Cargo** (1.80+) with `wasm-pack` (`cargo install wasm-pack`)
- **Python 3.12+** (or `uv`)
- **Node.js 20+** and `npm`
- **API Credentials** (Optional, configure in `.env`):
  - `QDRANT_URL` and `QDRANT_API_KEY` (for Qdrant Cloud vector search)
  - `GEMINI_API_KEY` (for Google Gemini structural comparison synthesis)

---

## 🚀 Quickstart Guide

### 1. Clone & Set Up Environment

```bash
git clone https://github.com/pranjalya/mythos-atlas.git
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

*(Note: MythosAtlas includes local vector fallback and structural heuristic engines, so the system works even if external API keys are omitted).*

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

The repository already contains the baked static dataset in `data/processed/`. To re-run extraction, Wikipedia scraping, and Qdrant indexing:

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
- `query_timeline(year: i32) -> JsValue`: Queries overlapping intervals for a discrete year with continuous visual intensity calculations.

### 3. Backend Endpoints
- `GET /api/v1/myths/{id}`: Returns enriched Wikipedia narrative and syncretic edges.
- `GET /api/v1/parallels/{id}?limit=3`: Vector search for top cross-cultural counterparts across continents.
- `POST /api/v1/compare`: Synthesizes dual-tradition structuralist matrix (archetypes, inciting motifs, cosmological resolution, and diffusion vs. convergence).

---

## 👤 Author & Architecture

- **Lead Architect & Creator**: **Pranjalya Tiwari**
- **GitHub Profile**: [@Pranjalya](https://github.com/Pranjalya)
- **LinkedIn**: [in/pranjalya-tiwari](https://linkedin.com/in/pranjalya-tiwari)
- **Project Repository**: [github.com/Pranjalya/mythos-atlas](https://github.com/Pranjalya/mythos-atlas)

---

## 📄 License

This project is open source and available under the terms of the [MIT License](LICENSE).
