//! WebAssembly core for MythosAtlas.
//! High-frequency client-side spatio-temporal filtering engine.

pub mod interval_tree;
pub mod spatial;

use std::cell::RefCell;
use interval_tree::{IntervalEntry, IntervalTree};
use serde::{Deserialize, Serialize};
use wasm_bindgen::prelude::*;

#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct MythRecord {
    pub id: String,
    pub name: String,
    pub lat: f32,
    pub lng: f32,
    pub epoch_start: i32,
    pub epoch_end: i32,
    pub culture: String,
    pub archetype: String,
    #[serde(default)]
    pub thumbnail: String,
    #[serde(default)]
    pub syncretic_ids: Vec<String>,
    #[serde(default)]
    pub description: String,
}

#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct ActiveMythResult {
    pub id: String,
    pub name: String,
    pub lat: f32,
    pub lng: f32,
    pub epoch_start: i32,
    pub epoch_end: i32,
    pub culture: String,
    pub archetype: String,
    pub intensity: f32,
    pub thumbnail: String,
    pub syncretic_ids: Vec<String>,
    pub description: String,
    pub cartesian: [f32; 3],
}

#[wasm_bindgen]
pub struct TimelineEngine {
    records: Vec<MythRecord>,
    tree: IntervalTree,
}

impl TimelineEngine {
    /// Internal typed query returning vector of ActiveMythResult.
    pub fn query_timeline_internal(&self, year: i32) -> Vec<ActiveMythResult> {
        let indices = self.tree.query_point(year);
        let mut results = Vec::with_capacity(indices.len());

        for idx in indices {
            if let Some(rec) = self.records.get(idx) {
                let intensity = calculate_intensity(year, rec.epoch_start, rec.epoch_end);
                let coord = spatial::GeoCoord::new(rec.lat, rec.lng);
                let cartesian = coord.to_cartesian_unit(1.0);

                results.push(ActiveMythResult {
                    id: rec.id.clone(),
                    name: rec.name.clone(),
                    lat: rec.lat,
                    lng: rec.lng,
                    epoch_start: rec.epoch_start,
                    epoch_end: rec.epoch_end,
                    culture: rec.culture.clone(),
                    archetype: rec.archetype.clone(),
                    intensity,
                    thumbnail: rec.thumbnail.clone(),
                    syncretic_ids: rec.syncretic_ids.clone(),
                    description: rec.description.clone(),
                    cartesian,
                });
            }
        }
        results
    }
}

#[wasm_bindgen]
impl TimelineEngine {
    #[wasm_bindgen(constructor)]
    pub fn new() -> Self {
        Self {
            records: Vec::new(),
            tree: IntervalTree::new(),
        }
    }

    /// Loads JSON array of MythRecord items and builds the interval tree.
    pub fn load_records(&mut self, records_json: &str) -> bool {
        match serde_json::from_str::<Vec<MythRecord>>(records_json) {
            Ok(parsed) => {
                let mut entries = Vec::with_capacity(parsed.len());
                for (idx, rec) in parsed.iter().enumerate() {
                    entries.push(IntervalEntry {
                        index: idx,
                        start: rec.epoch_start,
                        end: rec.epoch_end,
                    });
                }
                self.tree = IntervalTree::build(entries);
                self.records = parsed;
                true
            }
            Err(_) => false,
        }
    }

    /// Queries active myths for a given year, returning an array of ActiveMythResult objects.
    pub fn query_timeline(&self, year: i32) -> JsValue {
        let results = self.query_timeline_internal(year);
        serde_wasm_bindgen::to_value(&results).unwrap_or(JsValue::NULL)
    }

    /// Returns the total count of loaded records.
    pub fn total_records(&self) -> usize {
        self.records.len()
    }
}

// Global thread-local engine instance for direct functional calls
thread_local! {
    static GLOBAL_ENGINE: RefCell<TimelineEngine> = RefCell::new(TimelineEngine::new());
}

/// Global WASM function: loads records into the global timeline engine.
#[wasm_bindgen]
pub fn load_records(records_json: &str) -> bool {
    GLOBAL_ENGINE.with(|engine| engine.borrow_mut().load_records(records_json))
}

/// Global WASM function: queries active myths from the global timeline engine.
#[wasm_bindgen]
pub fn query_timeline(year: i32) -> JsValue {
    GLOBAL_ENGINE.with(|engine| engine.borrow().query_timeline(year))
}

/// Calculates visual intensity (0.5 to 1.0) based on temporal position within epoch span.
fn calculate_intensity(year: i32, start: i32, end: i32) -> f32 {
    let span = (end - start).max(1) as f32;
    let mid = start as f32 + (span / 2.0);
    let dist_from_mid = ((year as f32) - mid).abs();
    let norm = (1.0 - (dist_from_mid / (span / 2.0))).clamp(0.0, 1.0);
    0.5 + (0.5 * norm)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_engine_load_and_query() {
        let mut engine = TimelineEngine::new();
        let json_data = r#"[
            {
                "id": "Q248352",
                "name": "Epic of Gilgamesh",
                "lat": 31.32,
                "lng": 45.63,
                "epoch_start": -2100,
                "epoch_end": -1200,
                "culture": "Mesopotamian",
                "archetype": "Deluge / Immortality"
            },
            {
                "id": "Q169542",
                "name": "Ragnarok",
                "lat": 64.25,
                "lng": -21.13,
                "epoch_start": 800,
                "epoch_end": 1250,
                "culture": "Norse",
                "archetype": "Eschatological Apocalypse"
            }
        ]"#;

        assert!(engine.load_records(json_data));
        assert_eq!(engine.total_records(), 2);

        // Query -1500 BCE
        let indices = engine.tree.query_point(-1500);
        assert_eq!(indices.len(), 1);
        assert_eq!(engine.records[indices[0]].id, "Q248352");

        // Query 1000 CE
        let indices_ce = engine.tree.query_point(1000);
        assert_eq!(indices_ce.len(), 1);
        assert_eq!(engine.records[indices_ce[0]].id, "Q169542");

        // Query 0 CE (neither active)
        let indices_zero = engine.tree.query_point(0);
        assert_eq!(indices_zero.len(), 0);
    }
}
