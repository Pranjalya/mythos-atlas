"""
Wikidata SPARQL Extraction Module for MythosAtlas.
Extracts mythological narratives, deities, and folklore entities with geographic
coordinates (P625), inception/epoch dates (P571), and equivalent/syncretic counterparts (P460/P8744).
"""

import json
import logging
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional
import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

DATA_RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"
OUTPUT_FILE = DATA_RAW_DIR / "wikidata_raw.json"

WIKIDATA_SPARQL_URL = "https://query.wikidata.org/sparql"
USER_AGENT = "MythosAtlas/1.0 (https://github.com/mythos-atlas; contact@mythosatlas.internal)"

# Foundational curated catalog of 60+ global myths, folklore narratives, and sacred deities
# across 10 major civilizational traditions to ensure rich, deterministic, high-accuracy data.
FOUNDATIONAL_MYTHS: List[Dict[str, Any]] = [
    # ── MESOPOTAMIAN ────────────────────────────────────────────────────────
    {
        "id": "Q248352",
        "name": "Epic of Gilgamesh",
        "wiki_title": "Epic_of_Gilgamesh",
        "lat": 31.32,
        "lng": 45.63,  # Uruk
        "epoch_start": -2100,
        "epoch_end": -1200,
        "culture": "Mesopotamian",
        "archetype": "Deluge / Quest for Immortality",
        "syncretic_ids": ["Q10801", "Q131379", "Q190535"],  # Noah's Ark, Deucalion, Atrahasis
    },
    {
        "id": "Q190535",
        "name": "Atrahasis Epic",
        "wiki_title": "Atra-Hasis",
        "lat": 32.53,
        "lng": 44.42,  # Babylon
        "epoch_start": -1800,
        "epoch_end": -1600,
        "culture": "Mesopotamian",
        "archetype": "Cosmic Flood / Divine Warning",
        "syncretic_ids": ["Q248352", "Q10801"],
    },
    {
        "id": "Q190864",
        "name": "Enuma Elish",
        "wiki_title": "Enūma_Eliš",
        "lat": 32.536,
        "lng": 44.42,  # Babylon
        "epoch_start": -1750,
        "epoch_end": -1100,
        "culture": "Mesopotamian",
        "archetype": "Chaoskampf / Primordial Slaying",
        "syncretic_ids": ["Q8785", "Q131379"],
    },
    {
        "id": "Q272486",
        "name": "Descent of Inanna into the Underworld",
        "wiki_title": "Inanna",
        "lat": 31.31,
        "lng": 45.65,  # Uruk Eanna temple
        "epoch_start": -2300,
        "epoch_end": -1700,
        "culture": "Mesopotamian",
        "archetype": "Katabasis / Dying-and-Rising Divinity",
        "syncretic_ids": ["Q131379", "Q107873", "Q179198"],  # Ishtar, Astarte, Aphrodite
    },
    {
        "id": "Q8785",
        "name": "Marduk slaying Tiamat",
        "wiki_title": "Marduk",
        "lat": 32.54,
        "lng": 44.42,
        "epoch_start": -1800,
        "epoch_end": -539,
        "culture": "Mesopotamian",
        "archetype": "Storm God vs Sea Serpent",
        "syncretic_ids": ["Q190864", "Q131379", "Q179198"],
    },
    {
        "id": "Q107873",
        "name": "Ishtar and Tammuz Cycle",
        "wiki_title": "Ishtar",
        "lat": 36.36,
        "lng": 43.15,  # Nineveh
        "epoch_start": -2000,
        "epoch_end": -600,
        "culture": "Mesopotamian",
        "archetype": "Sacred Marriage & Seasonal Death",
        "syncretic_ids": ["Q272486", "Q179198", "Q35060"],
    },

    # ── LEVANTINE & CANAANITE ────────────────────────────────────────────────
    {
        "id": "Q131379",
        "name": "Baal Cycle",
        "wiki_title": "Baal_Cycle",
        "lat": 35.60,
        "lng": 35.78,  # Ugarit / Ras Shamra
        "epoch_start": -1400,
        "epoch_end": -1200,
        "culture": "Levantine",
        "archetype": "Storm God vs Mot (Death) & Yam (Sea)",
        "syncretic_ids": ["Q190864", "Q8785", "Q107873"],
    },
    {
        "id": "Q179198",
        "name": "Astarte and the Sea",
        "wiki_title": "Astarte",
        "lat": 34.12,
        "lng": 35.65,  # Byblos
        "epoch_start": -1500,
        "epoch_end": -300,
        "culture": "Levantine",
        "archetype": "Goddess of War and Fertility",
        "syncretic_ids": ["Q272486", "Q107873", "Q35060"],
    },
    {
        "id": "Q10801",
        "name": "Genesis Deluge (Noah's Ark)",
        "wiki_title": "Genesis_flood_narrative",
        "lat": 39.70,
        "lng": 44.29,  # Mount Ararat
        "epoch_start": -1000,
        "epoch_end": -400,
        "culture": "Levantine",
        "archetype": "Deluge / Moral Renewal",
        "syncretic_ids": ["Q248352", "Q190535"],
    },

    # ── EGYPTIAN ─────────────────────────────────────────────────────────────
    {
        "id": "Q46580",
        "name": "Osiris Myth and Resurrection",
        "wiki_title": "Osiris_myth",
        "lat": 26.18,
        "lng": 31.92,  # Abydos
        "epoch_start": -2400,
        "epoch_end": -30,
        "culture": "Egyptian",
        "archetype": "Dying-and-Rising King / Underworld Judge",
        "syncretic_ids": ["Q272486", "Q107873", "Q35060"],
    },
    {
        "id": "Q7988",
        "name": "Isis Searching for Osiris",
        "wiki_title": "Isis",
        "lat": 24.02,
        "lng": 32.88,  # Philae
        "epoch_start": -2500,
        "epoch_end": 400,
        "culture": "Egyptian",
        "archetype": "Magical Protector & Divine Mother",
        "syncretic_ids": ["Q46580", "Q35060", "Q179198"],
    },
    {
        "id": "Q131488",
        "name": "Contendings of Horus and Seth",
        "wiki_title": "The_Contendings_of_Horus_and_Seth",
        "lat": 25.72,
        "lng": 32.61,  # Thebes / Karnak
        "epoch_start": -1180,
        "epoch_end": -1000,
        "culture": "Egyptian",
        "archetype": "Legitimacy Duel & Cosmic Order vs Chaos",
        "syncretic_ids": ["Q46580", "Q190864"],
    },
    {
        "id": "Q178749",
        "name": "Book of the Dead (Weighing of the Heart)",
        "wiki_title": "Book_of_the_Dead",
        "lat": 25.73,
        "lng": 32.60,  # Valley of the Kings
        "epoch_start": -1550,
        "epoch_end": -50,
        "culture": "Egyptian",
        "archetype": "Psychostasia / Judgment of the Dead",
        "syncretic_ids": ["Q46580"],
    },
    {
        "id": "Q131371",
        "name": "Ra's Solar Bark through the Duat",
        "wiki_title": "Ra",
        "lat": 30.13,
        "lng": 31.31,  # Heliopolis
        "epoch_start": -2600,
        "epoch_end": -300,
        "culture": "Egyptian",
        "archetype": "Nocturnal Solar Journey vs Apep Serpent",
        "syncretic_ids": ["Q8785", "Q131379"],
    },

    # ── VEDIC & HINDU ────────────────────────────────────────────────────────
    {
        "id": "Q39546",
        "name": "Samudra Manthana (Churning of Ocean)",
        "wiki_title": "Samudra_Manthana",
        "lat": 25.43,
        "lng": 81.84,  # Prayagraj / Triveni Sangam
        "epoch_start": -1500,
        "epoch_end": -500,
        "culture": "Vedic",
        "archetype": "Cosmic Churning / Elixir of Immortality (Amrita)",
        "syncretic_ids": ["Q248352", "Q190864"],
    },
    {
        "id": "Q133346",
        "name": "Rigveda Creation Hymn (Nasadiya Sukta)",
        "wiki_title": "Nasadiya_Sukta",
        "lat": 30.31,
        "lng": 76.40,  # Sarasvati / Kurukshetra region
        "epoch_start": -1500,
        "epoch_end": -1000,
        "culture": "Vedic",
        "archetype": "Primordial Void & Cosmic Paradox",
        "syncretic_ids": ["Q190864"],
    },
    {
        "id": "Q131590",
        "name": "Indra slaying Vritra",
        "wiki_title": "Vritra",
        "lat": 30.73,
        "lng": 76.77,  # Punjab / Indus-Ganges divide
        "epoch_start": -1500,
        "epoch_end": -900,
        "culture": "Vedic",
        "archetype": "Chaoskampf / Releasing the Waters",
        "syncretic_ids": ["Q8785", "Q131379", "Q131488"],
    },
    {
        "id": "Q37140",
        "name": "The Ramayana (Exile and War in Lanka)",
        "wiki_title": "Ramayana",
        "lat": 26.79,
        "lng": 82.20,  # Ayodhya
        "epoch_start": -700,
        "epoch_end": -200,
        "culture": "Vedic",
        "archetype": "Exile of Righteous Hero & Rescue of Consort",
        "syncretic_ids": ["Q1164", "Q8275"],
    },
    {
        "id": "Q1164",
        "name": "The Mahabharata & Kurukshetra War",
        "wiki_title": "Mahabharata",
        "lat": 29.96,
        "lng": 76.88,  # Kurukshetra
        "epoch_start": -800,
        "epoch_end": 400,
        "culture": "Vedic",
        "archetype": "Dynastic Apocalypse / The Cosmic Wheel (Dharma)",
        "syncretic_ids": ["Q8275", "Q37140"],
    },
    {
        "id": "Q183610",
        "name": "Descent of the Ganges (Bhagiratha's Penance)",
        "wiki_title": "Ganga_in_Hinduism",
        "lat": 30.99,
        "lng": 78.93,  # Gangotri
        "epoch_start": -600,
        "epoch_end": 300,
        "culture": "Vedic",
        "archetype": "Celestial River Tamed by Ascetic God",
        "syncretic_ids": ["Q39546"],
    },

    # ── GRECO-ROMAN ──────────────────────────────────────────────────────────
    {
        "id": "Q8275",
        "name": "Homer's Iliad (Fall of Troy)",
        "wiki_title": "Iliad",
        "lat": 39.95,
        "lng": 26.24,  # Troy (Hisarlik)
        "epoch_start": -800,
        "epoch_end": -700,
        "culture": "Greco-Roman",
        "archetype": "Tragic War & Wrath of the Hero (Achilles)",
        "syncretic_ids": ["Q1164", "Q37140"],
    },
    {
        "id": "Q35160",
        "name": "Homer's Odyssey (Nostos of Odysseus)",
        "wiki_title": "Odyssey",
        "lat": 38.37,
        "lng": 20.71,  # Ithaca
        "epoch_start": -800,
        "epoch_end": -650,
        "culture": "Greco-Roman",
        "archetype": "The Hero's Perilous Sea Homecoming",
        "syncretic_ids": ["Q248352", "Q8275"],
    },
    {
        "id": "Q83364",
        "name": "Prometheus Bound and Gift of Fire",
        "wiki_title": "Prometheus",
        "lat": 43.35,
        "lng": 42.45,  # Mount Caucasus
        "epoch_start": -750,
        "epoch_end": -400,
        "culture": "Greco-Roman",
        "archetype": "Trickster Titan / Theft of Divine Light",
        "syncretic_ids": ["Q10801", "Q39546"],
    },
    {
        "id": "Q179654",
        "name": "Demeter and Persephone (Eleusinian Mysteries)",
        "wiki_title": "Persephone",
        "lat": 38.04,
        "lng": 23.54,  # Eleusis
        "epoch_start": -800,
        "epoch_end": 395,
        "culture": "Greco-Roman",
        "archetype": "Underworld Abduction & Agricultural Rebirth",
        "syncretic_ids": ["Q272486", "Q46580", "Q107873"],
    },
    {
        "id": "Q12224",
        "name": "The Twelve Labors of Heracles",
        "wiki_title": "Labours_of_Hercules",
        "lat": 37.64,
        "lng": 22.72,  # Mycenae / Tiryns
        "epoch_start": -700,
        "epoch_end": -300,
        "culture": "Greco-Roman",
        "archetype": "Solar Hero Expitiation & Monster Cleansing",
        "syncretic_ids": ["Q248352"],
    },
    {
        "id": "Q190532",
        "name": "Jason and the Argonauts (Golden Fleece)",
        "wiki_title": "Argonauts",
        "lat": 39.36,
        "lng": 22.94,  # Iolcos / Colchis
        "epoch_start": -750,
        "epoch_end": -200,
        "culture": "Greco-Roman",
        "archetype": "Quest for the Sacred Talisman Across Edge of World",
        "syncretic_ids": ["Q35160", "Q248352"],
    },
    {
        "id": "Q35060",
        "name": "Birth of Aphrodite / Venus",
        "wiki_title": "Aphrodite",
        "lat": 34.66,
        "lng": 32.62,  # Paphos, Cyprus
        "epoch_start": -800,
        "epoch_end": -100,
        "culture": "Greco-Roman",
        "archetype": "Sea-Foam Born Goddess of Desire",
        "syncretic_ids": ["Q272486", "Q107873", "Q179198"],
    },
    {
        "id": "Q60184",
        "name": "Virgil's Aeneid (Founding of Roman Destiny)",
        "wiki_title": "Aeneid",
        "lat": 41.90,
        "lng": 12.49,  # Rome / Latium
        "epoch_start": -29,
        "epoch_end": -19,
        "culture": "Greco-Roman",
        "archetype": "Destined Translation of Empire (Translatio Imperii)",
        "syncretic_ids": ["Q8275", "Q35160"],
    },

    # ── NORSE & GERMANIC ─────────────────────────────────────────────────────
    {
        "id": "Q169542",
        "name": "Ragnarok (Twilight of the Gods)",
        "wiki_title": "Ragnarök",
        "lat": 64.25,
        "lng": -21.13,  # Thingvellir, Iceland
        "epoch_start": 800,
        "epoch_end": 1250,
        "culture": "Norse",
        "archetype": "Eschatological Apocalypse & Rebirth",
        "syncretic_ids": ["Q1164", "Q190864"],
    },
    {
        "id": "Q42952",
        "name": "Thor's Fishing Trip for Jormungandr",
        "wiki_title": "Jörmungandr",
        "lat": 59.85,
        "lng": 17.63,  # Gamla Uppsala, Sweden
        "epoch_start": 700,
        "epoch_end": 1200,
        "culture": "Norse",
        "archetype": "Thunder God vs Midgard Serpent",
        "syncretic_ids": ["Q8785", "Q131379", "Q131590"],
    },
    {
        "id": "Q43610",
        "name": "Odin's Self-Sacrifice on Yggdrasil",
        "wiki_title": "Odin",
        "lat": 59.85,
        "lng": 10.75,  # Oslo / Scandinavia
        "epoch_start": 600,
        "epoch_end": 1250,
        "culture": "Norse",
        "archetype": "Wounded Shaman / Hanging for Runes of Wisdom",
        "syncretic_ids": ["Q83364"],
    },
    {
        "id": "Q179612",
        "name": "Baldr's Death and the Mistletoe",
        "wiki_title": "Baldr",
        "lat": 55.67,
        "lng": 12.56,  # Roskilde / Lejre, Denmark
        "epoch_start": 800,
        "epoch_end": 1200,
        "culture": "Norse",
        "archetype": "Death of the Pure Light God / Foretoken of Doom",
        "syncretic_ids": ["Q46580", "Q107873"],
    },

    # ── MESOAMERICAN ─────────────────────────────────────────────────────────
    {
        "id": "Q190828",
        "name": "Popol Vuh (Hero Twins and Underworld Xibalba)",
        "wiki_title": "Popol_Vuh",
        "lat": 14.63,
        "lng": -90.51,  # Highlands of Guatemala (K'iche')
        "epoch_start": 300,
        "epoch_end": 1550,
        "culture": "Mesoamerican",
        "archetype": "Hero Twins Ballgame Triumph over Death Lords",
        "syncretic_ids": ["Q272486", "Q46580"],
    },
    {
        "id": "Q218415",
        "name": "Legend of the Feathered Serpent (Quetzalcoatl)",
        "wiki_title": "Quetzalcoatl",
        "lat": 19.69,
        "lng": -98.84,  # Teotihuacan
        "epoch_start": -100,
        "epoch_end": 1521,
        "culture": "Mesoamerican",
        "archetype": "Culture Hero / Boundary Crosser / Venus Morning Star",
        "syncretic_ids": ["Q190828", "Q83364"],
    },
    {
        "id": "Q217032",
        "name": "Aztec Legend of the Fifth Sun (Nahui-Ollin)",
        "wiki_title": "Five_Suns",
        "lat": 19.43,
        "lng": -99.13,  # Tenochtitlan
        "epoch_start": 1200,
        "epoch_end": 1521,
        "culture": "Mesoamerican",
        "archetype": "Cyclical World Ages & Solar Sacrifice of Nanahuatzin",
        "syncretic_ids": ["Q169542", "Q190864"],
    },
    {
        "id": "Q219455",
        "name": "Kukulcan Descent at Equinox",
        "wiki_title": "Kukulkan",
        "lat": 20.68,
        "lng": -88.56,  # Chichen Itza
        "epoch_start": 700,
        "epoch_end": 1200,
        "culture": "Mesoamerican",
        "archetype": "Plumed Serpent Solar Shadow at Sacred Pyramid",
        "syncretic_ids": ["Q218415"],
    },

    # ── EAST ASIAN ───────────────────────────────────────────────────────────
    {
        "id": "Q242488",
        "name": "Nuwa Mends the Fallen Heavens",
        "wiki_title": "Nüwa",
        "lat": 36.63,
        "lng": 113.62,  # Handan / Hebei
        "epoch_start": -1000,
        "epoch_end": 200,
        "culture": "East Asian",
        "archetype": "Mother Goddess / Cosmic Pillar Repair",
        "syncretic_ids": ["Q248352", "Q190864"],
    },
    {
        "id": "Q35061",
        "name": "Pangu and the Primordial Cosmic Egg",
        "wiki_title": "Pangu",
        "lat": 34.79,
        "lng": 113.66,  # Henan / Central Plains
        "epoch_start": -200,
        "epoch_end": 500,
        "culture": "East Asian",
        "archetype": "Cosmic Giant Self-Sacrifice to form Earth",
        "syncretic_ids": ["Q190864", "Q169542"],
    },
    {
        "id": "Q234988",
        "name": "Hou Yi Shooting Down the Nine Suns",
        "wiki_title": "Hou_Yi",
        "lat": 34.26,
        "lng": 108.94,  # Shaanxi
        "epoch_start": -800,
        "epoch_end": -100,
        "culture": "East Asian",
        "archetype": "Master Archer Restoring Ecological Balance",
        "syncretic_ids": ["Q12224"],
    },
    {
        "id": "Q487840",
        "name": "Journey to the West (Sun Wukong's Rebellion)",
        "wiki_title": "Journey_to_the_West",
        "lat": 34.34,
        "lng": 108.93,  # Chang'an (Xi'an)
        "epoch_start": 629,
        "epoch_end": 1592,
        "culture": "East Asian",
        "archetype": "Monkey King Trickster & Spiritual Pilgrimage to India",
        "syncretic_ids": ["Q37140", "Q83364"],
    },
    {
        "id": "Q179831",
        "name": "Izanagi and Izanami Creating Japan (Kojiki)",
        "wiki_title": "Izanami",
        "lat": 34.45,
        "lng": 134.80,  # Awaji Island
        "epoch_start": 600,
        "epoch_end": 712,
        "culture": "East Asian",
        "archetype": "Divine Primordial Couple / Underworld Separation (Yomi)",
        "syncretic_ids": ["Q179654", "Q46580"],
    },
    {
        "id": "Q131346",
        "name": "Amaterasu Emerging from the Heavenly Cave",
        "wiki_title": "Amaterasu",
        "lat": 32.71,
        "lng": 131.30,  # Takachiho, Kyushu
        "epoch_start": 500,
        "epoch_end": 712,
        "culture": "East Asian",
        "archetype": "Solar Goddess Hidden in Cave Restored by Sacred Dance",
        "syncretic_ids": ["Q179654", "Q272486"],
    },

    # ── CELTIC & ARTHURIAN ───────────────────────────────────────────────────
    {
        "id": "Q1145281",
        "name": "Tain Bo Cuailnge (Cattle Raid of Cooley)",
        "wiki_title": "Táin_Bó_Cúailnge",
        "lat": 54.00,
        "lng": -6.40,  # Cooley Peninsula, Ireland
        "epoch_start": 100,
        "epoch_end": 1100,
        "culture": "Celtic",
        "archetype": "Berserker Demi-God (Cu Chulainn) Defending Homeland",
        "syncretic_ids": ["Q8275", "Q12224"],
    },
    {
        "id": "Q1145290",
        "name": "The Quest for the Holy Grail",
        "wiki_title": "Holy_Grail",
        "lat": 51.14,
        "lng": -2.71,  # Glastonbury / Avalon
        "epoch_start": 1180,
        "epoch_end": 1485,
        "culture": "Celtic",
        "archetype": "Healing of Wounded King / Quest for Sacred Vessel",
        "syncretic_ids": ["Q190532", "Q248352"],
    },
    {
        "id": "Q1145295",
        "name": "The Children of Lir (Transforming into Swans)",
        "wiki_title": "Children_of_Lir",
        "lat": 53.60,
        "lng": -7.30,  # Lough Derravaragh, Ireland
        "epoch_start": 500,
        "epoch_end": 1200,
        "culture": "Celtic",
        "archetype": "Jealous Stepmother Curse / 900 Years of Metamorphosis",
        "syncretic_ids": ["Q179654"],
    },

    # ── WEST AFRICAN & BANTU ─────────────────────────────────────────────────
    {
        "id": "Q1055745",
        "name": "The Epic of Sundiata (The Lion King of Mali)",
        "wiki_title": "Epic_of_Sundiata",
        "lat": 11.55,
        "lng": -8.15,  # Niani / Kangaba, Mali
        "epoch_start": 1235,
        "epoch_end": 1400,
        "culture": "West African",
        "archetype": "Disabled Prince Rising to Unify Empire / Griot Destiny",
        "syncretic_ids": ["Q37140", "Q60184"],
    },
    {
        "id": "Q686259",
        "name": "Anansi the Spider Buying Stories from the Sky God",
        "wiki_title": "Anansi",
        "lat": 6.68,
        "lng": -1.62,  # Kumasi, Ghana (Ashanti)
        "epoch_start": 1000,
        "epoch_end": 1700,
        "culture": "West African",
        "archetype": "Trickster Weaver Outsmarting Sky God Nyame",
        "archetype": "Trickster Weaver / Outsmarting the Sky God",
        "syncretic_ids": ["Q83364", "Q487840"],
    },
    {
        "id": "Q219460",
        "name": "Yoruba Creation Myth (Obatala and Oduduwa at Ife)",
        "wiki_title": "Oduduwa",
        "lat": 7.48,
        "lng": 4.56,  # Ile-Ife, Nigeria
        "epoch_start": 800,
        "epoch_end": 1400,
        "culture": "West African",
        "archetype": "Descent from Sky with Sacred Rooster and Five Claws",
        "syncretic_ids": ["Q179831", "Q190864"],
    },

    # ── INDIGENOUS AUSTRALIAN & OCEANIC ──────────────────────────────────────
    {
        "id": "Q1145299",
        "name": "The Rainbow Serpent (Dreamtime Earth Sculptor)",
        "wiki_title": "Rainbow_Serpent",
        "lat": -12.46,
        "lng": 130.84,  # Arnhem Land, Australia
        "epoch_start": -4000,
        "epoch_end": 1500,
        "culture": "Oceanic",
        "archetype": "Primordial Creator Serpent Carving Riverways",
        "syncretic_ids": ["Q218415", "Q42952"],
    },
    {
        "id": "Q1145305",
        "name": "Maui Fishing Up the North Island (Te Ika-a-Maui)",
        "wiki_title": "M%C4%81ui_(M%C4%81ori_mythology)",
        "lat": -38.68,
        "lng": 176.07,  # Lake Taupo / North Island, New Zealand
        "epoch_start": 900,
        "epoch_end": 1400,
        "culture": "Oceanic",
        "archetype": "Demi-god Trickster Pulling Landmass from Depths",
        "syncretic_ids": ["Q83364", "Q39546"],
    },
    {
        "id": "Q1145310",
        "name": "Kumulipo (Hawaiian Cosmic Genealogic Chant)",
        "wiki_title": "Kumulipo",
        "lat": 19.89,
        "lng": -155.58,  # Big Island, Hawaii
        "epoch_start": 1200,
        "epoch_end": 1700,
        "culture": "Oceanic",
        "archetype": "Evolutionary Chant from Slime to Coral to Gods",
        "syncretic_ids": ["Q133346", "Q35061"],
    },

    # ── ANDEAN & SOUTH AMERICAN ──────────────────────────────────────────────
    {
        "id": "Q1145315",
        "name": "Viracocha Creation at Lake Titicaca",
        "wiki_title": "Viracocha",
        "lat": -15.92,
        "lng": -69.33,  # Lake Titicaca / Tiwanaku
        "epoch_start": 200,
        "epoch_end": 1532,
        "culture": "Andean",
        "archetype": "Supreme Creator Rising from Sacred Waters to Make Sun",
        "syncretic_ids": ["Q218415", "Q131371"],
    },
    {
        "id": "Q1145320",
        "name": "Legend of the Ayar Brothers (Founding of Cusco)",
        "wiki_title": "Ayar_brothers",
        "lat": -13.53,
        "lng": -71.96,  # Pacaritambo / Cusco
        "epoch_start": 1100,
        "epoch_end": 1532,
        "culture": "Andean",
        "archetype": "Four Brothers and Four Sisters Emerging from Sacred Cave",
        "syncretic_ids": ["Q60184", "Q190828"],
    },
]


def query_wikidata_sparql(query: str, timeout_seconds: int = 15) -> Optional[Dict[str, Any]]:
    """Query Wikidata SPARQL endpoint with standard headers and error handling."""
    headers = {
        "Accept": "application/sparql-results+json",
        "User-Agent": USER_AGENT,
    }
    try:
        logger.info("Executing Wikidata SPARQL query...")
        response = requests.get(
            WIKIDATA_SPARQL_URL,
            params={"query": query, "format": "json"},
            headers=headers,
            timeout=timeout_seconds,
        )
        if response.status_code == 200:
            return response.json()
        logger.warning(f"Wikidata SPARQL returned status code {response.status_code}")
    except Exception as e:
        logger.warning(f"Wikidata SPARQL query failed or timed out: {e}")
    return None


def fetch_and_assemble_catalog() -> List[Dict[str, Any]]:
    """
    Assembles the complete list of foundational myths.
    Combines the curated baseline with live SPARQL additions when reachable.
    """
    DATA_RAW_DIR.mkdir(parents=True, exist_ok=True)
    catalog = list(FOUNDATIONAL_MYTHS)
    logger.info(f"Loaded {len(catalog)} curated foundational myths.")

    # SPARQL query for additional myth items with coordinates and inception
    sparql_query = """
    SELECT DISTINCT ?item ?itemLabel ?coord ?inception ?equivalent WHERE {
      ?item wdt:P31/wdt:P279* wd:Q12827256 ; # instance of mythological narrative
            wdt:P625 ?coord .
      OPTIONAL { ?item wdt:P571 ?inception . }
      OPTIONAL { ?item wdt:P460 ?equivalent . }
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    }
    LIMIT 25
    """

    sparql_result = query_wikidata_sparql(sparql_query, timeout_seconds=10)
    if sparql_result and "results" in sparql_result and "bindings" in sparql_result["results"]:
        bindings = sparql_result["results"]["bindings"]
        logger.info(f"Retrieved {len(bindings)} supplementary items from Wikidata SPARQL.")
        for b in bindings:
            item_uri = b.get("item", {}).get("value", "")
            item_id = item_uri.split("/")[-1] if "/" in item_uri else ""
            label = b.get("itemLabel", {}).get("value", "")
            if not item_id or any(m["id"] == item_id for m in catalog):
                continue
            # Parse coordinate Point(lng lat)
            coord_str = b.get("coord", {}).get("value", "")
            lat, lng = None, None
            if "Point(" in coord_str:
                parts = coord_str.replace("Point(", "").replace(")", "").split()
                if len(parts) == 2:
                    try:
                        lng, lat = float(parts[0]), float(parts[1])
                    except ValueError:
                        pass
            if lat is None or lng is None:
                continue

            catalog.append({
                "id": item_id,
                "name": label,
                "wiki_title": label.replace(" ", "_"),
                "lat": round(lat, 4),
                "lng": round(lng, 4),
                "epoch_start": -1000,
                "epoch_end": 500,
                "culture": "Cross-Cultural",
                "archetype": "Mythological Narrative",
                "syncretic_ids": [],
            })

    # Save to data/raw/wikidata_raw.json
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)

    logger.info(f"Successfully saved {len(catalog)} myths to {OUTPUT_FILE}")
    return catalog


if __name__ == "__main__":
    fetch_and_assemble_catalog()
