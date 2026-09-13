"""
Script to add 15 new concurrent/co-located myths to world sacred epicenters,
enrich them via Wikipedia API, index them in Qdrant (768D nomic-embed-text),
and bake static data bundles.
"""

import json
import time
import urllib.request
from pathlib import Path
from typing import Any, Dict, List

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
RAW_FILE = DATA_DIR / "raw" / "wikipedia_enriched.json"
WIKIDATA_RAW = DATA_DIR / "raw" / "wikidata_raw.json"

NEW_MYTHS: List[Dict[str, Any]] = [
    {
        "id": "Q196901",
        "name": "Creation of the Fifth Sun (Nanahuatzin's Sacred Leap)",
        "wiki_title": "Nanahuatzin",
        "lat": 19.69,
        "lng": -98.84,  # Teotihuacan
        "epoch_start": -200,
        "epoch_end": 750,
        "culture": "Mesoamerican",
        "archetype": "Cosmic Self-Sacrifice into the Sacred Hearth to Birth the Sun",
        "syncretic_ids": ["Q1263", "Q165998"],
    },
    {
        "id": "Q183414",
        "name": "The Capitoline Triad (Jupiter, Juno, Minerva on the Sacred Hill)",
        "wiki_title": "Capitoline_Triad",
        "lat": 41.89,
        "lng": 12.48,  # Rome (Capitoline Hill)
        "epoch_start": -509,
        "epoch_end": 400,
        "culture": "Greco-Roman",
        "archetype": "Supreme Triadic State Sovereignty and Divine Protector Assembly",
        "syncretic_ids": ["Q183413", "Q12225"],
    },
    {
        "id": "Q183415",
        "name": "Evander and the Arcadian Settlement on the Palatine",
        "wiki_title": "Evander_of_Pallene",
        "lat": 41.89,
        "lng": 12.48,  # Rome (Palatine Hill)
        "epoch_start": -800,
        "epoch_end": -100,
        "culture": "Greco-Roman",
        "archetype": "Exiled Cultural Founder Establishing Wisdom and the Cult of Hercules",
        "syncretic_ids": ["Q183413", "Q130832"],
    },
    {
        "id": "Q213285",
        "name": "The Bhagavad Gita (Vishwarupa Cosmic Revelation at Kurukshetra)",
        "wiki_title": "Bhagavad_Gita",
        "lat": 29.96,
        "lng": 76.88,  # Kurukshetra
        "epoch_start": -400,
        "epoch_end": 400,
        "culture": "Vedic & Hindu",
        "archetype": "Theophany of Cosmic Totality and Righteous Action (Karma Yoga)",
        "syncretic_ids": ["Q1164", "Q213275"],
    },
    {
        "id": "Q213286",
        "name": "Dasharatha's Ashvamedha and the Divine Incarnation at Ayodhya",
        "wiki_title": "Dasharatha",
        "lat": 26.79,
        "lng": 82.20,  # Ayodhya
        "epoch_start": -800,
        "epoch_end": 200,
        "culture": "Vedic & Hindu",
        "archetype": "Royal Sacrificial Yajna Summoning the Golden Vessel of Divine Avatars",
        "syncretic_ids": ["Q37140", "Q213284"],
    },
    {
        "id": "Q841460",
        "name": "Pilgrimage to the West (Xuanzang Departing Chang'an)",
        "wiki_title": "Journey_to_the_West",
        "lat": 34.26,
        "lng": 108.94,  # Chang'an
        "epoch_start": 627,
        "epoch_end": 1500,
        "culture": "East Asian",
        "archetype": "Spiritual Pilgrimage with Immortal Protectors Seeking True Sutras",
        "syncretic_ids": ["Q234988", "Q841458"],
    },
    {
        "id": "Q130834",
        "name": "Cadmus Slaying the Ismenian Dragon and Sowing the Spartoi",
        "wiki_title": "Cadmus",
        "lat": 38.32,
        "lng": 23.32,  # Thebes, Greece
        "epoch_start": -800,
        "epoch_end": -200,
        "culture": "Greco-Roman",
        "archetype": "Slaying the Sacred Serpent and Harvesting Earth-Born Warriors from Its Teeth",
        "syncretic_ids": ["Q130833", "Q12226"],
    },
    {
        "id": "Q188740",
        "name": "Amun-Ra and the Sacred Opet Festival of Karnak and Luxor",
        "wiki_title": "Amun",
        "lat": 25.72,
        "lng": 32.61,  # Thebes / Karnak, Egypt
        "epoch_start": -2000,
        "epoch_end": -300,
        "culture": "Egyptian",
        "archetype": "The Hidden Breath of Creation and Solar Sovereign in the Hypostyle Hall",
        "syncretic_ids": ["Q188735", "Q188738"],
    },
    {
        "id": "Q125437",
        "name": "The Akedah (Binding of Isaac on Mount Moriah)",
        "wiki_title": "Binding_of_Isaac",
        "lat": 31.77,
        "lng": 35.23,  # Mount Moriah, Jerusalem
        "epoch_start": -1000,
        "epoch_end": 300,
        "culture": "Levantine",
        "archetype": "Supreme Test of Patriarchal Faith and Angelic Intervention at the Altar",
        "syncretic_ids": ["Q125436", "Q125435"],
    },
    {
        "id": "Q125438",
        "name": "Solomon's Temple and the Indwelling Shekhinah",
        "wiki_title": "Temple_in_Jerusalem",
        "lat": 31.77,
        "lng": 35.23,  # Temple Mount, Jerusalem
        "epoch_start": -950,
        "epoch_end": 70,
        "culture": "Levantine",
        "archetype": "Sacred Axis Mundi Housing the Divine Presence over the World's Cornerstone",
        "syncretic_ids": ["Q125436", "Q125437"],
    },
    {
        "id": "Q213287",
        "name": "The Awakening under the Bodhi Tree (Defeat of Mara)",
        "wiki_title": "Gautama_Buddha",
        "lat": 24.70,
        "lng": 84.99,  # Bodh Gaya
        "epoch_start": -528,
        "epoch_end": 500,
        "culture": "Vedic & Hindu",
        "archetype": "Earth-Witnessing Gesture (Bhumisparsha) Dissolving Cosmic Illusion and Desire",
        "syncretic_ids": ["Q131804", "Q213283"],
    },
    {
        "id": "Q213288",
        "name": "Mucalinda the Serpent King Shielding the Awakened One",
        "wiki_title": "Mucalinda",
        "lat": 24.70,
        "lng": 84.99,  # Bodh Gaya
        "epoch_start": -528,
        "epoch_end": 500,
        "culture": "Vedic & Hindu",
        "archetype": "Benevolent Multi-Headed Naga King Sheltering the Sage from the Great Deluge",
        "syncretic_ids": ["Q213287", "Q12227"],
    },
    {
        "id": "Q130835",
        "name": "The Titanomachy (The Ten-Year Cosmic War from Mount Olympus)",
        "wiki_title": "Titanomachy",
        "lat": 40.08,
        "lng": 22.36,  # Mount Olympus
        "epoch_start": -800,
        "epoch_end": -200,
        "culture": "Greco-Roman",
        "archetype": "Generational War of Lightning and Earth-Shattering Giants Overthrowing the Old Gods",
        "syncretic_ids": ["Q83364", "Q190864"],
    },
    {
        "id": "Q841461",
        "name": "Konohanasakuya-hime (The Blossom Fire Goddess of Mount Fuji)",
        "wiki_title": "Konohanasakuya-hime",
        "lat": 35.36,
        "lng": 138.73,  # Mount Fuji
        "epoch_start": 712,
        "epoch_end": 1600,
        "culture": "East Asian",
        "archetype": "Ephemeral Cherry Blossom Deity Proving Sacred Purity Amidst Volcano Flames",
        "syncretic_ids": ["Q841455", "Q273898"],
    },
    {
        "id": "Q131349",
        "name": "Freyr's Sacred Boar Gullinbursti and the Royal Mounds of Uppsala",
        "wiki_title": "Freyr",
        "lat": 59.85,
        "lng": 17.63,  # Old Uppsala
        "epoch_start": 800,
        "epoch_end": 1200,
        "culture": "Norse",
        "archetype": "Sacred Lord of Abundant Harvests and Peace Borne by the Luminous Golden Boar",
        "syncretic_ids": ["Q131346", "Q8785"],
    },
]


def fetch_wiki_enrichment(title: str) -> Dict[str, Any]:
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{title}"
    req = urllib.request.Request(url, headers={"User-Agent": "MythosAtlas/1.0 (academic research; contact@mythosatlas.internal)"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            extract = data.get("extract", "")
            description = data.get("description", "")
            thumbnail = ""
            if "thumbnail" in data and "source" in data["thumbnail"]:
                thumbnail = data["thumbnail"]["source"]
            wiki_url = data.get("content_urls", {}).get("desktop", {}).get("page", f"https://en.wikipedia.org/wiki/{title}")
            return {
                "extract": extract,
                "description": description,
                "thumbnail": thumbnail,
                "wikipedia_url": wiki_url,
            }
    except Exception as e:
        print(f"Error fetching {title}: {e}")
        return {
            "extract": "",
            "description": "",
            "thumbnail": "",
            "wikipedia_url": f"https://en.wikipedia.org/wiki/{title}",
        }


def main():
    with open(RAW_FILE, "r", encoding="utf-8") as f:
        enriched_list = json.load(f)

    existing_ids = {m["id"] for m in enriched_list}
    new_added = 0

    for item in NEW_MYTHS:
        if item["id"] in existing_ids:
            print(f"Skipping existing: {item['id']}")
            continue

        print(f"Enriching {item['name']} ({item['wiki_title']})...")
        time.sleep(0.5)  # respectful rate limit
        wiki_data = fetch_wiki_enrichment(item["wiki_title"])
        
        full_record = {
            **item,
            "extract": wiki_data["extract"],
            "description": wiki_data["description"] or item["archetype"],
            "thumbnail": wiki_data["thumbnail"] or "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=600&auto=format&fit=crop&q=80",
            "wikipedia_url": wiki_data["wikipedia_url"],
        }
        enriched_list.append(full_record)
        existing_ids.add(item["id"])
        new_added += 1

    print(f"Added and enriched {new_added} new myths! Total now: {len(enriched_list)}")

    with open(RAW_FILE, "w", encoding="utf-8") as f:
        json.dump(enriched_list, f, indent=2, ensure_ascii=False)

    # Also sync to wikidata_raw.json
    with open(WIKIDATA_RAW, "r", encoding="utf-8") as f:
        raw_list = json.load(f)
    raw_ids = {m["id"] for m in raw_list}
    for item in NEW_MYTHS:
        if item["id"] not in raw_ids:
            raw_list.append(item)
    with open(WIKIDATA_RAW, "w", encoding="utf-8") as f:
        json.dump(raw_list, f, indent=2, ensure_ascii=False)

    print("Sync complete. Re-indexing into Qdrant Cloud...")
    from etl.index_qdrant import index_all_myths
    indexed = index_all_myths()
    print(f"Qdrant indexed: {indexed} items.")

    # Bake static data
    from etl.bake_static_data import bake_static_dataset
    bake_static_dataset()
    print("Static dataset baked successfully!")


if __name__ == "__main__":
    main()
