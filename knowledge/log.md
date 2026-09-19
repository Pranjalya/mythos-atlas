# MythosAtlas OKF Corpus Provenance Ledger (log.md)

All entries are strictly append-only in accordance with Google Open Knowledge Format (OKF v0.2) specifications.

---

### [2026-09-19T08:25:00Z] - Genesis of OKF v0.2 Knowledge Substrate
- **Action**: Initialized MythosAtlas Open Knowledge Format repository conforming to Google OKF v0.2.
- **Specification**: Defined `knowledge/SPEC.md` with strict YAML frontmatter schema:
  - Provenance trust signals (`trust.tier`, `trust.verified`, `trust.reviewer`).
  - Scholarly source attribution with primary ancient text citations and academic URLs.
  - Folkloric indexing using the Stith Thompson Motif-Index of Folk-Literature (`thompson_motifs`), Joseph Campbell monomyth stages, and Claude Lévi-Strauss binary structuralist oppositions.
  - Spatio-temporal coordinate anchors with discrete BCE/CE epoch bounding.
- **Attestation**: Initial migration of 331 global myth records from legacy JSON format into hierarchical cultural zones (`knowledge/myths/`).
- **Compiler**: Attached `etl/okf_compiler.py` ensuring continuous synchronization with the client-side WebAssembly Interval Tree and Three.js runtime.
