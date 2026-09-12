//! Integration tests for engine-wasm against real baked static dataset.

use engine_wasm::TimelineEngine;
use std::fs;
use std::path::Path;

#[test]
fn test_real_dataset_interval_queries() {
    let dataset_path = Path::new("../data/processed/static_myths.json");
    if !dataset_path.exists() {
        // Fallback for direct crate testing
        return;
    }

    let raw_json = fs::read_to_string(dataset_path).expect("Failed to read static_myths.json");
    let mut engine = TimelineEngine::new();
    assert!(engine.load_records(&raw_json));
    assert!(engine.total_records() >= 50);

    // Test -2100 BCE: Should include Early Bronze Age Mesopotamian & Egyptian epics
    let active_2100 = engine.query_timeline_internal(-2100);
    assert!(!active_2100.is_empty(), "Expected active myths at -2100 BCE");
    assert!(active_2100.iter().any(|m| m.name.contains("Gilgamesh") || m.name.contains("Inanna") || m.name.contains("Osiris")));

    // Test -1200 BCE (Late Bronze Age): Gilgamesh, Enuma Elish, Baal Cycle, Rigveda
    let active_1200 = engine.query_timeline_internal(-1200);
    assert!(active_1200.len() >= 4, "Expected multiple Bronze Age myths active at -1200 BCE");

    // Test -800 BCE (Axial Age / Homeric era): Iliad, Odyssey, Hesiod, Ramayana
    let active_800 = engine.query_timeline_internal(-800);
    assert!(active_800.iter().any(|m| m.culture == "Greco-Roman" || m.culture == "Vedic"));

    // Test 1000 CE (Medieval): Ragnarok, Sundiata, Popol Vuh, Anansi
    let active_1000 = engine.query_timeline_internal(1000);
    assert!(active_1000.iter().any(|m| m.culture == "Norse" || m.culture == "West African" || m.culture == "Mesoamerican"));
}
