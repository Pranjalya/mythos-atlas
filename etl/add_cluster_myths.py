"""
Script to add co-located / concurrent myths to famous worldwide sacred epicenters.
"""

import json
from pathlib import Path

DATA_RAW_FILE = Path(__file__).resolve().parent.parent / "data" / "raw" / "wikidata_raw.json"

CLUSTER_MYTHS = [
    {
        "id": "Q12225",
        "name": "Contest of Athena and Poseidon for the Acropolis",
        "wiki_title": "Athena",
        "lat": 37.97,
        "lng": 23.72,  # Acropolis of Athens
        "epoch_start": -800,
        "epoch_end": -200,
        "culture": "Greco-Roman",
        "archetype": "Civic Patronage Contest (Sacred Olive Tree vs Salt Spring)",
        "syncretic_ids": ["Q129888", "Q35060"],
    },
    {
        "id": "Q12226",
        "name": "Erichthonius the Earth-Born Serpent King of the Acropolis",
        "wiki_title": "Erichthonius_of_Athens",
        "lat": 37.97,
        "lng": 23.72,  # Acropolis of Athens
        "epoch_start": -750,
        "epoch_end": -300,
        "culture": "Greco-Roman",
        "archetype": "Autochthonous Serpent-Tailed Founder Born Directly of Sacred Soil",
        "syncretic_ids": ["Q12225", "Q129888"],
    },
    {
        "id": "Q12227",
        "name": "Apollo Slaying Python at the Sacred Omphalos",
        "wiki_title": "Python_(mythology)",
        "lat": 38.48,
        "lng": 22.50,  # Delphi
        "epoch_start": -800,
        "epoch_end": -300,
        "culture": "Greco-Roman",
        "archetype": "Solar God Slaying Chthonic Earth Serpent to Establish the Oracle",
        "syncretic_ids": ["Q131346", "Q8785"],
    },
    {
        "id": "Q12228",
        "name": "Deucalion and Pyrrha (The Deluge on Mount Parnassus)",
        "wiki_title": "Deucalion",
        "lat": 38.48,
        "lng": 22.50,  # Mount Parnassus / Delphi
        "epoch_start": -800,
        "epoch_end": -300,
        "culture": "Greco-Roman",
        "archetype": "Cosmic Flood Survivors Re-creating Humanity by Casting the Bones of Mother Earth",
        "syncretic_ids": ["Q10801", "Q1164"],
    },
    {
        "id": "Q213283",
        "name": "Shiva's Jyotirlinga (The Infinite Pillar of Cosmic Light at Kashi)",
        "wiki_title": "Jyotirlinga",
        "lat": 25.31,
        "lng": 83.00,  # Kashi Vishwanath Temple, Varanasi
        "epoch_start": -1000,
        "epoch_end": 500,
        "culture": "Vedic & Hindu",
        "archetype": "Boundless Fiery Pillar Shaming Pride of Creator and Preserver Gods",
        "syncretic_ids": ["Q213275", "Q1422880"],
    },
    {
        "id": "Q213284",
        "name": "King Harishchandra's Ordeal of Truth at the Manikarnika Ghat",
        "wiki_title": "Harishchandra",
        "lat": 25.31,
        "lng": 83.00,  # Manikarnika Cremation Ghat, Varanasi
        "epoch_start": -800,
        "epoch_end": 200,
        "culture": "Vedic & Hindu",
        "archetype": "Righteous Monarch Sacrificing Kingdom and Family for Absolute Truth (Satya)",
        "syncretic_ids": ["Q948959", "Q815849"],
    },
    {
        "id": "Q125436",
        "name": "The Foundation Stone (Even ha-Shetiya Sealing the Abyssal Waters)",
        "wiki_title": "Foundation_Stone",
        "lat": 31.77,
        "lng": 35.23,  # Temple Mount / Mount Moriah, Jerusalem
        "epoch_start": -950,
        "epoch_end": 600,
        "culture": "Levantine",
        "archetype": "Primordial Keystone of Creation Plugged over the Subterranean Chaos Abyss",
        "syncretic_ids": ["Q125435", "Q125432"],
    },
    {
        "id": "Q188738",
        "name": "The Benben Stone (The Primordial Island Rising from Nun)",
        "wiki_title": "Benben",
        "lat": 30.12,
        "lng": 31.31,  # Heliopolis (Iunu), Egypt
        "epoch_start": -2500,
        "epoch_end": -1000,
        "culture": "Egyptian",
        "archetype": "First Pyramidal Mound of Earth Piercing Primeval Waters upon which Sunlight Broke",
        "syncretic_ids": ["Q188735", "Q1422880"],
    },
    {
        "id": "Q188739",
        "name": "The Bennu Bird (The Solar Heron of Eternal Rebirth)",
        "wiki_title": "Bennu",
        "lat": 30.12,
        "lng": 31.31,  # Heliopolis, Egypt
        "epoch_start": -2400,
        "epoch_end": -1000,
        "culture": "Egyptian",
        "archetype": "Luminous Bird of Resurrection Perched on the Primordial Pillar",
        "syncretic_ids": ["Q188738", "Q211158"],
    },
    {
        "id": "Q841458",
        "name": "Abe no Seimei and the Twelve Shikigami (Master of Onmyōdō)",
        "wiki_title": "Abe_no_Seimei",
        "lat": 35.01,
        "lng": 135.76,  # Heian-kyō (Kyoto), Japan
        "epoch_start": 950,
        "epoch_end": 1200,
        "culture": "East Asian",
        "archetype": "Celestial Diviner and Sorcerer Commanding Invisible Spirits to Ward the Capital",
        "syncretic_ids": ["Q841455", "Q125435"],
    },
    {
        "id": "Q841459",
        "name": "Minamoto no Yorimitsu Slaying the Demon King Shuten-dōji",
        "wiki_title": "Shuten-d%C5%8Dji",
        "lat": 35.01,
        "lng": 135.76,  # Mount Ōe / Kyoto
        "epoch_start": 990,
        "epoch_end": 1300,
        "culture": "East Asian",
        "archetype": "Heroic Imperial Samurai Infiltrating Demon Citadel with Poisoned Sake",
        "syncretic_ids": ["Q841451", "Q130832"],
    },
    {
        "id": "Q166007",
        "name": "Manco Cápac and Mama Ocllo (The Sinking of the Golden Sun Staff)",
        "wiki_title": "Manco_C%C3%A1pac",
        "lat": -16.02,
        "lng": -69.17,  # Lake Titicaca (Isla del Sol)
        "epoch_start": 1100,
        "epoch_end": 1533,
        "culture": "Andean & South American",
        "archetype": "Children of the Sun Emerging from Sacred Waters to Found Imperial Civilization",
        "syncretic_ids": ["Q165998", "Q165997"],
    },
]


def add_cluster_myths():
    with open(DATA_RAW_FILE, "r", encoding="utf-8") as f:
        existing = json.load(f)

    existing_ids = {x.get("id") for x in existing}
    added = 0

    for m in CLUSTER_MYTHS:
        if m["id"] in existing_ids:
            print(f"Skipping duplicate ID: {m['id']}")
            continue
        existing.append(m)
        existing_ids.add(m["id"])
        added += 1

    print(f"Added {added} new co-located cluster myths!")
    print(f"New total catalog size: {len(existing)}")

    with open(DATA_RAW_FILE, "w", encoding="utf-8") as f:
        json.dump(existing, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    add_cluster_myths()
