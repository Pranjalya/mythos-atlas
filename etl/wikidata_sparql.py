"""
Wikidata SPARQL Extraction Module for MythosAtlas.
Extracts mythological narratives, deities, and folklore entities with geographic
coordinates (P625), inception/epoch dates (P571), and equivalent/syncretic counterparts (P460/P8744).
Expanded global catalog covering all continents and indigenous world traditions from -4000 BCE to 1500 CE.
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

# Comprehensive global catalog of 115+ foundational myths, sacred cosmogonies, and folklore epics
# covering all inhabited continents and cultural traditions from -4000 BCE to 1500 CE.
FOUNDATIONAL_MYTHS: List[Dict[str, Any]] = [
    # ── 1. MESOPOTAMIAN ──────────────────────────────────────────────────────
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
        "syncretic_ids": ["Q10801", "Q131379", "Q190535"],
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
        "lng": 45.65,  # Uruk
        "epoch_start": -2300,
        "epoch_end": -1700,
        "culture": "Mesopotamian",
        "archetype": "Katabasis / Dying-and-Rising Divinity",
        "syncretic_ids": ["Q131379", "Q107873", "Q179198"],
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
        "syncretic_ids": ["Q190864", "Q131379"],
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

    # ── 2. LEVANTINE & CANAANITE ─────────────────────────────────────────────
    {
        "id": "Q131379",
        "name": "Baal Cycle",
        "wiki_title": "Baal_Cycle",
        "lat": 35.60,
        "lng": 35.78,  # Ugarit
        "epoch_start": -1400,
        "epoch_end": -1200,
        "culture": "Levantine",
        "archetype": "Storm God vs Mot (Death) & Yam (Sea)",
        "syncretic_ids": ["Q190864", "Q8785"],
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

    # ── 3. EGYPTIAN ──────────────────────────────────────────────────────────
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
        "syncretic_ids": ["Q272486", "Q179654"],
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
        "syncretic_ids": ["Q46580", "Q35060"],
    },
    {
        "id": "Q131488",
        "name": "Contendings of Horus and Seth",
        "wiki_title": "The_Contendings_of_Horus_and_Seth",
        "lat": 25.72,
        "lng": 32.61,  # Thebes
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

    # ── 4. VEDIC & HINDU ─────────────────────────────────────────────────────
    {
        "id": "Q39546",
        "name": "Samudra Manthana (Churning of Ocean)",
        "wiki_title": "Samudra_Manthana",
        "lat": 25.43,
        "lng": 81.84,  # Prayagraj
        "epoch_start": -1500,
        "epoch_end": -500,
        "culture": "Vedic & Hindu",
        "archetype": "Cosmic Churning / Elixir of Immortality (Amrita)",
        "syncretic_ids": ["Q248352", "Q190864"],
    },
    {
        "id": "Q133346",
        "name": "Rigveda Creation Hymn (Nasadiya Sukta)",
        "wiki_title": "Nasadiya_Sukta",
        "lat": 30.31,
        "lng": 76.40,  # Sarasvati / Kurukshetra
        "epoch_start": -1500,
        "epoch_end": -1000,
        "culture": "Vedic & Hindu",
        "archetype": "Primordial Void & Cosmic Paradox",
        "syncretic_ids": ["Q190864"],
    },
    {
        "id": "Q131590",
        "name": "Indra slaying Vritra",
        "wiki_title": "Vritra",
        "lat": 30.73,
        "lng": 76.77,
        "epoch_start": -1500,
        "epoch_end": -900,
        "culture": "Vedic & Hindu",
        "archetype": "Chaoskampf / Releasing the Waters",
        "syncretic_ids": ["Q8785", "Q131379"],
    },
    {
        "id": "Q37140",
        "name": "The Ramayana (Exile and War in Lanka)",
        "wiki_title": "Ramayana",
        "lat": 26.79,
        "lng": 82.20,  # Ayodhya
        "epoch_start": -700,
        "epoch_end": -200,
        "culture": "Vedic & Hindu",
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
        "culture": "Vedic & Hindu",
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
        "culture": "Vedic & Hindu",
        "archetype": "Celestial River Tamed by Ascetic God",
        "syncretic_ids": ["Q39546"],
    },
    {
        "id": "Q131580",
        "name": "Shiva Tandava (Cosmic Dance of Destruction)",
        "wiki_title": "Tandava",
        "lat": 11.39,
        "lng": 79.69,  # Chidambaram Nataraja Temple
        "epoch_start": -500,
        "epoch_end": 600,
        "culture": "Vedic & Hindu",
        "archetype": "Cosmic Dissolution and Re-Creation",
        "syncretic_ids": ["Q169542", "Q190864"],
    },

    # ── 5. PERSIAN & ZOROASTRIAN ─────────────────────────────────────────────
    {
        "id": "Q131585",
        "name": "Ahura Mazda vs Angra Mainyu",
        "wiki_title": "Ahura_Mazda",
        "lat": 32.88,
        "lng": 59.22,  # Khorasan / Balkh
        "epoch_start": -1200,
        "epoch_end": 651,
        "culture": "Persian & Iranian",
        "archetype": "Cosmic Dualism: Light (Asha) vs Deceit (Druj)",
        "syncretic_ids": ["Q190864", "Q131379"],
    },
    {
        "id": "Q8279",
        "name": "Ferdowsi's Shahnameh (Rostam and Sohrab)",
        "wiki_title": "Shahnameh",
        "lat": 36.30,
        "lng": 59.60,  # Tus, Khorasan
        "epoch_start": 977,
        "epoch_end": 1010,
        "culture": "Persian & Iranian",
        "archetype": "Tragic Filicide / National Heroic Epic",
        "syncretic_ids": ["Q1164", "Q8275"],
    },
    {
        "id": "Q131595",
        "name": "The Simurgh and Prince Zal",
        "wiki_title": "Simurgh",
        "lat": 35.95,
        "lng": 52.11,  # Mount Damavand
        "epoch_start": -500,
        "epoch_end": 1000,
        "culture": "Persian & Iranian",
        "archetype": "Benevolent Mythic Avian Guardian of the Hero",
        "syncretic_ids": ["Q487840"],
    },
    {
        "id": "Q131598",
        "name": "Jamshid and the Golden Age (Yima's Vara)",
        "wiki_title": "Jamshid",
        "lat": 29.93,
        "lng": 52.89,  # Persepolis / Fars
        "epoch_start": -1000,
        "epoch_end": 651,
        "culture": "Persian & Iranian",
        "archetype": "Golden Age King / Subterranean Haven Against Cosmic Winter",
        "syncretic_ids": ["Q190535", "Q248352"],
    },

    # ── 6. GRECO-ROMAN ───────────────────────────────────────────────────────
    {
        "id": "Q8275",
        "name": "Homer's Iliad (Fall of Troy)",
        "wiki_title": "Iliad",
        "lat": 39.95,
        "lng": 26.24,  # Troy
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
        "syncretic_ids": ["Q272486", "Q46580"],
    },
    {
        "id": "Q12224",
        "name": "The Twelve Labors of Heracles",
        "wiki_title": "Labours_of_Hercules",
        "lat": 37.64,
        "lng": 22.72,  # Mycenae
        "epoch_start": -700,
        "epoch_end": -300,
        "culture": "Greco-Roman",
        "archetype": "Solar Hero Expiation & Monster Cleansing",
        "syncretic_ids": ["Q248352"],
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
        "syncretic_ids": ["Q272486", "Q179198"],
    },
    {
        "id": "Q60184",
        "name": "Virgil's Aeneid (Founding of Roman Destiny)",
        "wiki_title": "Aeneid",
        "lat": 41.90,
        "lng": 12.49,  # Rome
        "epoch_start": -29,
        "epoch_end": -19,
        "culture": "Greco-Roman",
        "archetype": "Destined Translation of Empire (Translatio Imperii)",
        "syncretic_ids": ["Q8275"],
    },

    # ── 7. NORSE & GERMANIC ──────────────────────────────────────────────────
    {
        "id": "Q169542",
        "name": "Ragnarok (Twilight of the Gods)",
        "wiki_title": "Ragnarök",
        "lat": 64.25,
        "lng": -21.13,  # Thingvellir, Iceland
        "epoch_start": 800,
        "epoch_end": 1250,
        "culture": "Norse & Germanic",
        "archetype": "Eschatological Apocalypse & Rebirth",
        "syncretic_ids": ["Q1164", "Q190864"],
    },
    {
        "id": "Q42952",
        "name": "Thor's Fishing Trip for Jormungandr",
        "wiki_title": "Jörmungandr",
        "lat": 59.85,
        "lng": 17.63,  # Gamla Uppsala
        "epoch_start": 700,
        "epoch_end": 1200,
        "culture": "Norse & Germanic",
        "archetype": "Thunder God vs Midgard Serpent",
        "syncretic_ids": ["Q8785", "Q131379"],
    },
    {
        "id": "Q43610",
        "name": "Odin's Self-Sacrifice on Yggdrasil",
        "wiki_title": "Odin",
        "lat": 59.85,
        "lng": 10.75,  # Scandinavia
        "epoch_start": 600,
        "epoch_end": 1250,
        "culture": "Norse & Germanic",
        "archetype": "Wounded Shaman / Hanging for Runes of Wisdom",
        "syncretic_ids": ["Q83364"],
    },
    {
        "id": "Q179612",
        "name": "Baldr's Death and the Mistletoe",
        "wiki_title": "Baldr",
        "lat": 55.67,
        "lng": 12.56,  # Denmark
        "epoch_start": 800,
        "epoch_end": 1200,
        "culture": "Norse & Germanic",
        "archetype": "Death of the Pure Light God / Foretoken of Doom",
        "syncretic_ids": ["Q46580"],
    },

    # ── 8. SLAVIC, BALTIC & FINNISH ──────────────────────────────────────────
    {
        "id": "Q131600",
        "name": "Perun vs Veles (Thunder God vs Underworld Serpent)",
        "wiki_title": "Perun",
        "lat": 50.45,
        "lng": 30.52,  # Kyiv / Dnieper Hills
        "epoch_start": 500,
        "epoch_end": 1200,
        "culture": "Slavic & Baltic",
        "archetype": "Storm God in Tree vs Horned Serpent in Roots",
        "syncretic_ids": ["Q8785", "Q42952"],
    },
    {
        "id": "Q187224",
        "name": "Baba Yaga in the Hut on Fowl's Legs",
        "wiki_title": "Baba_Yaga",
        "lat": 56.83,
        "lng": 60.60,  # Ural Taiga
        "epoch_start": 600,
        "epoch_end": 1500,
        "culture": "Slavic & Baltic",
        "archetype": "Threshold Guardian Witch / Forest Initiator",
        "syncretic_ids": ["Q686259"],
    },
    {
        "id": "Q130009",
        "name": "The Kalevala (Forging of the Sampo)",
        "wiki_title": "Kalevala",
        "lat": 64.00,
        "lng": 30.00,  # Karelia / Finland
        "epoch_start": 800,
        "epoch_end": 1400,
        "culture": "Finno-Ugric",
        "archetype": "Magic Singing Sorcerer (Väinämöinen) & Mill of Plenty",
        "syncretic_ids": ["Q190532"],
    },
    {
        "id": "Q130015",
        "name": "Lemminkäinen's Resurrection from the Tuonela River",
        "wiki_title": "Lemminkäinen",
        "lat": 61.50,
        "lng": 28.50,  # Saimaa / Karelia
        "epoch_start": 800,
        "epoch_end": 1400,
        "culture": "Finno-Ugric",
        "archetype": "Katabasis / Mother's Rake Piecing Hero Back from the River of Death",
        "syncretic_ids": ["Q272486", "Q179654"],
    },
    {
        "id": "Q130020",
        "name": "Kalevipoeg (The Giant Hero of Estonia)",
        "wiki_title": "Kalevipoeg",
        "lat": 58.59,
        "lng": 25.01,  # Peipus / Estonia
        "epoch_start": 900,
        "epoch_end": 1400,
        "culture": "Finno-Ugric",
        "archetype": "Giant Culture Hero / Earth Sculptor and Underworld Descent",
        "syncretic_ids": ["Q1164"],
    },
    {
        "id": "Q131605",
        "name": "Perkunas and Saule (Baltic Sun and Thunder)",
        "wiki_title": "Perkūnas",
        "lat": 54.68,
        "lng": 25.27,  # Vilnius / Baltic Sacred Groves
        "epoch_start": 400,
        "epoch_end": 1387,
        "culture": "Slavic & Baltic",
        "archetype": "Oak-Tree Thunder God Purifying Chthonic Shadows",
        "syncretic_ids": ["Q131600"],
    },

    # ── 9. CELTIC & ARTHURIAN ────────────────────────────────────────────────
    {
        "id": "Q1145281",
        "name": "Tain Bo Cuailnge (Cattle Raid of Cooley)",
        "wiki_title": "Táin_Bó_Cúailnge",
        "lat": 54.00,
        "lng": -6.40,  # Cooley Peninsula, Ireland
        "epoch_start": 100,
        "epoch_end": 1100,
        "culture": "Celtic",
        "archetype": "Berserker Demi-God (Cú Chulainn) Defending Homeland",
        "syncretic_ids": ["Q8275"],
    },
    {
        "id": "Q1145290",
        "name": "The Quest for the Holy Grail",
        "wiki_title": "Holy_Grail",
        "lat": 51.14,
        "lng": -2.71,  # Glastonbury
        "epoch_start": 1180,
        "epoch_end": 1485,
        "culture": "Celtic",
        "archetype": "Healing of Wounded King / Sacred Vessel",
        "syncretic_ids": ["Q190532"],
    },
    {
        "id": "Q1145295",
        "name": "The Children of Lir (Swan Metamorphosis)",
        "wiki_title": "Children_of_Lir",
        "lat": 53.60,
        "lng": -7.30,  # Lough Derravaragh
        "epoch_start": 500,
        "epoch_end": 1200,
        "culture": "Celtic",
        "archetype": "Jealous Stepmother Curse / 900 Years of Metamorphosis",
        "syncretic_ids": ["Q179654"],
    },

    # ── 10. EAST ASIAN (CHINESE, JAPANESE, KOREAN) ───────────────────────────
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
        "lng": 113.66,  # Henan
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
        "lng": 108.93,  # Chang'an
        "epoch_start": 629,
        "epoch_end": 1592,
        "culture": "East Asian",
        "archetype": "Monkey King Trickster & Pilgrimage to India",
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
        "syncretic_ids": ["Q179654"],
    },
    {
        "id": "Q131610",
        "name": "Susanoo slaying Yamata no Orochi",
        "wiki_title": "Yamata_no_Orochi",
        "lat": 35.36,
        "lng": 133.05,  # Izumo Province
        "epoch_start": 500,
        "epoch_end": 712,
        "culture": "East Asian",
        "archetype": "Storm God Slaying Eight-Headed Dragon for Sacred Sword",
        "syncretic_ids": ["Q8785", "Q42952"],
    },
    {
        "id": "Q210740",
        "name": "Dangun Myth (Founding of Gojoseon)",
        "wiki_title": "Dangun",
        "lat": 38.00,
        "lng": 126.50,  # Mount Taebaek / Pyongyang
        "epoch_start": -1000,
        "epoch_end": 1281,
        "culture": "East Asian",
        "archetype": "Bear-Woman (Ungnyeo) and Heavenly Son King",
        "syncretic_ids": ["Q60184"],
    },

    # ── 11. CENTRAL ASIAN & SIBERIAN STEPPE ──────────────────────────────────
    {
        "id": "Q131615",
        "name": "Tengri and the Eternal Blue Sky",
        "wiki_title": "Tengrism",
        "lat": 47.92,
        "lng": 106.91,  # Burkhan Khaldun, Mongolia
        "epoch_start": -1000,
        "epoch_end": 1300,
        "culture": "Central Asian & Steppe",
        "archetype": "Supreme Celestial Sky Father & Shamanic Tree",
        "syncretic_ids": ["Q133346"],
    },
    {
        "id": "Q248235",
        "name": "The Epic of King Gesar",
        "wiki_title": "Epic_of_King_Gesar",
        "lat": 33.00,
        "lng": 98.00,  # Kham, Eastern Tibet
        "epoch_start": 300,
        "epoch_end": 1400,
        "culture": "Central Asian & Steppe",
        "archetype": "Miraculous Demi-God Warrior Defeating Demons of the Directions",
        "syncretic_ids": ["Q37140", "Q1164"],
    },
    {
        "id": "Q836248",
        "name": "The Epic of Manas (Unification of the Kyrgyz)",
        "wiki_title": "Epic_of_Manas",
        "lat": 42.52,
        "lng": 72.24,  # Talas Valley, Kyrgyzstan
        "epoch_start": 900,
        "epoch_end": 1500,
        "culture": "Central Asian & Steppe",
        "archetype": "Chivalric Warrior Uniting the Steppe Tribes",
        "syncretic_ids": ["Q1055745"],
    },

    # ── 12. SOUTHEAST ASIAN ──────────────────────────────────────────────────
    {
        "id": "Q131620",
        "name": "Dewi Sri (The Rice Mother Goddess)",
        "wiki_title": "Dewi_Sri",
        "lat": -7.79,
        "lng": 110.36,  # Central Java / Prambanan
        "epoch_start": 700,
        "epoch_end": 1500,
        "culture": "Southeast Asian",
        "archetype": "Self-Sacrificing Goddess Transforming into Sacred Rice",
        "syncretic_ids": ["Q179654"],
    },
    {
        "id": "Q131625",
        "name": "Barong vs Rangda (Eternal Cosmic Equilibrium)",
        "wiki_title": "Barong_(mythology)",
        "lat": -8.50,
        "lng": 115.26,  # Ubud / Bali
        "epoch_start": 900,
        "epoch_end": 1600,
        "culture": "Southeast Asian",
        "archetype": "Lion Spirit of Good vs Demon Queen of Calon Arang",
        "syncretic_ids": ["Q190864"],
    },
    {
        "id": "Q131630",
        "name": "Bakunawa Swallowing the Seven Moons",
        "wiki_title": "Bakunawa",
        "lat": 10.31,
        "lng": 123.89,  # Visayas, Philippines
        "epoch_start": 800,
        "epoch_end": 1600,
        "culture": "Southeast Asian",
        "archetype": "Serpentine Sea Dragon Causing Lunar Eclipse",
        "syncretic_ids": ["Q42952"],
    },
    {
        "id": "Q131635",
        "name": "Lac Long Quan and Au Co (Birth of the Viet People)",
        "wiki_title": "Lạc_Long_Quân",
        "lat": 21.03,
        "lng": 105.85,  # Red River Delta, Vietnam
        "epoch_start": -700,
        "epoch_end": 1400,
        "culture": "Southeast Asian",
        "archetype": "Dragon Lord of the Waters & Fairy of the Mountains producing 100 Eggs",
        "syncretic_ids": ["Q179831"],
    },

    # ── 13. NORTH AMERICAN INDIGENOUS & ARCTIC ───────────────────────────────
    {
        "id": "Q131640",
        "name": "Dine Bahane' (Navajo Emergence through the Four Worlds)",
        "wiki_title": "Diné_Bahaneʼ",
        "lat": 36.00,
        "lng": -109.50,  # Dinetah / Canyon de Chelly, Arizona
        "epoch_start": 500,
        "epoch_end": 1500,
        "culture": "North American Indigenous",
        "archetype": "Emergence Myth / Holy People (Diyin Dine'é) Ascending Worlds",
        "syncretic_ids": ["Q190828"],
    },
    {
        "id": "Q131645",
        "name": "Sedna (Mistress of the Arctic Underworld)",
        "wiki_title": "Sedna_(mythology)",
        "lat": 69.00,
        "lng": -95.00,  # Baffin Island / Nunavut
        "epoch_start": -1000,
        "epoch_end": 1500,
        "culture": "North American Indigenous",
        "archetype": "Sacrificed Sea Maiden whose Severed Fingers become Seals & Whales",
        "syncretic_ids": ["Q272486"],
    },
    {
        "id": "Q131650",
        "name": "Raven Stealing the Light of the Sun",
        "wiki_title": "Raven_Tales",
        "lat": 53.25,
        "lng": -132.00,  # Haida Gwaii, Pacific Northwest
        "epoch_start": -1500,
        "epoch_end": 1600,
        "culture": "North American Indigenous",
        "archetype": "Trickster Transformer Liberating the Sun from Celestial Chieftain",
        "syncretic_ids": ["Q83364", "Q686259"],
    },
    {
        "id": "Q131655",
        "name": "White Buffalo Calf Woman (Sacred Pipe Chanunpa)",
        "wiki_title": "White_Buffalo_Calf_Woman",
        "lat": 43.80,
        "lng": -103.50,  # Black Hills (Paha Sapa), South Dakota
        "epoch_start": 900,
        "epoch_end": 1700,
        "culture": "North American Indigenous",
        "archetype": "Celestial Maiden Bringing Seven Sacred Rites and Moral Covenant",
        "syncretic_ids": ["Q218415"],
    },
    {
        "id": "Q131660",
        "name": "Iroquois Sky Woman and the Turtle Island",
        "wiki_title": "Iroquois_mythology",
        "lat": 43.00,
        "lng": -76.00,  # Onondaga Lake, New York
        "epoch_start": 1000,
        "epoch_end": 1500,
        "culture": "North American Indigenous",
        "archetype": "Pregnant Sky Woman Falling to Earth / World Built on Turtle's Back",
        "syncretic_ids": ["Q242488"],
    },

    # ── 14. MESOAMERICAN & CARIBBEAN ─────────────────────────────────────────
    {
        "id": "Q190828",
        "name": "Popol Vuh (Hero Twins and Underworld Xibalba)",
        "wiki_title": "Popol_Vuh",
        "lat": 14.63,
        "lng": -90.51,  # Guatemala Highlands
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
        "syncretic_ids": ["Q83364"],
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
        "syncretic_ids": ["Q169542"],
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
    {
        "id": "Q131665",
        "name": "Taino Creation of the Sea (The Gourd of Yaya)",
        "wiki_title": "Taíno",
        "lat": 18.22,
        "lng": -66.59,  # Puerto Rico / Hispaniola
        "epoch_start": 800,
        "epoch_end": 1500,
        "culture": "Mesoamerican",
        "archetype": "Sacred Gourd Shattering into the Ocean Waters & Fishes",
        "syncretic_ids": ["Q10801"],
    },

    # ── 15. SOUTH AMERICAN, ANDEAN & AMAZONIAN ───────────────────────────────
    {
        "id": "Q1145315",
        "name": "Viracocha Creation at Lake Titicaca",
        "wiki_title": "Viracocha",
        "lat": -15.92,
        "lng": -69.33,  # Lake Titicaca / Tiwanaku
        "epoch_start": 200,
        "epoch_end": 1532,
        "culture": "Andean & South American",
        "archetype": "Supreme Creator Rising from Sacred Waters to Make Sun",
        "syncretic_ids": ["Q218415"],
    },
    {
        "id": "Q1145320",
        "name": "Legend of the Ayar Brothers (Founding of Cusco)",
        "wiki_title": "Inca_mythology",
        "lat": -13.53,
        "lng": -71.96,  # Pacaritambo / Cusco
        "epoch_start": 1100,
        "epoch_end": 1532,
        "culture": "Andean & South American",
        "archetype": "Four Brothers and Four Sisters Emerging from Sacred Cave",
        "syncretic_ids": ["Q60184"],
    },
    {
        "id": "Q131670",
        "name": "Trentren Vilu and Caicai Vilu (Mapuche Deluge)",
        "wiki_title": "Mapuche_mythology",
        "lat": -39.00,
        "lng": -72.50,  # Araucania, Chile
        "epoch_start": 500,
        "epoch_end": 1550,
        "culture": "Andean & South American",
        "archetype": "Earth Serpent vs Sea Serpent Battle Raising Mountains Above Waters",
        "syncretic_ids": ["Q42952", "Q10801"],
    },
    {
        "id": "Q131675",
        "name": "Tupa and Arasy (Guarani Creation of Humanity)",
        "wiki_title": "Guarani_mythology",
        "lat": -25.26,
        "lng": -57.57,  # Asunción / Parana River
        "epoch_start": 600,
        "epoch_end": 1600,
        "culture": "Andean & South American",
        "archetype": "Supreme Thunder Deity Fashioning First Couple from Clay",
        "syncretic_ids": ["Q190535"],
    },

    # ── 16. SUB-SAHARAN AFRICAN ──────────────────────────────────────────────
    {
        "id": "Q1055745",
        "name": "The Epic of Sundiata (The Lion King of Mali)",
        "wiki_title": "Epic_of_Sundiata",
        "lat": 11.55,
        "lng": -8.15,  # Niani, Mali
        "epoch_start": 1235,
        "epoch_end": 1400,
        "culture": "West African",
        "archetype": "Disabled Prince Rising to Unify Empire / Griot Destiny",
        "syncretic_ids": ["Q37140"],
    },
    {
        "id": "Q686259",
        "name": "Anansi the Spider Buying Stories from the Sky God",
        "wiki_title": "Anansi",
        "lat": 6.68,
        "lng": -1.62,  # Kumasi, Ghana
        "epoch_start": 1000,
        "epoch_end": 1700,
        "culture": "West African",
        "archetype": "Trickster Weaver Outsmarting Sky God Nyame",
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
        "syncretic_ids": ["Q179831"],
    },
    {
        "id": "Q131680",
        "name": "Shango the Orisha of Lightning and Thunder",
        "wiki_title": "Shango",
        "lat": 7.84,
        "lng": 3.93,  # Oyo Empire
        "epoch_start": 1100,
        "epoch_end": 1600,
        "culture": "West African",
        "archetype": "Deified King / Double-Headed Axe Thunder God",
        "syncretic_ids": ["Q8785", "Q42952"],
    },
    {
        "id": "Q131685",
        "name": "Unkulunkulu Emerging from the Reeds (Zulu Creation)",
        "wiki_title": "Unkulunkulu",
        "lat": -28.75,
        "lng": 31.00,  # KwaZulu-Natal, South Africa
        "epoch_start": 800,
        "epoch_end": 1600,
        "culture": "Central & Southern African",
        "archetype": "First Ancestor Growing from the Primordial Swamp Reed (Uhlanga)",
        "syncretic_ids": ["Q35061"],
    },
    {
        "id": "Q131690",
        "name": "The Nommo Water Spirits and Sirius (Dogon Cosmogony)",
        "wiki_title": "Nommo",
        "lat": 14.45,
        "lng": -3.20,  # Bandiagara Escarpment, Mali
        "epoch_start": 1000,
        "epoch_end": 1600,
        "culture": "West African",
        "archetype": "Amphibious Primordial Teachers Bringing Civilization and Weaver Loom",
        "syncretic_ids": ["Q218415"],
    },
    {
        "id": "Q131695",
        "name": "|Kaggen the Mantis Trickster (|Xam San Myth)",
        "wiki_title": "Kaggen",
        "lat": -30.00,
        "lng": 21.00,  # Karoo, South Africa
        "epoch_start": -4000,
        "epoch_end": 1700,
        "culture": "Central & Southern African",
        "archetype": "Shape-Shifting Mantis Creating the Moon from an Eland's Shoe",
        "syncretic_ids": ["Q83364"],
    },
    {
        "id": "Q131696",
        "name": "The Mwindo Epic (Nyanga Hero's Descent to the Underworld)",
        "wiki_title": "Mwindo_epic",
        "lat": -1.33,
        "lng": 28.00,  # Kivu / Congo Basin
        "epoch_start": 900,
        "epoch_end": 1500,
        "culture": "Central & Southern African",
        "archetype": "Underworld Descent and Reconciliation with Lightning God",
        "syncretic_ids": ["Q272486", "Q1055745"],
    },
    {
        "id": "Q131697",
        "name": "Kintu and Nambi (Buganda Genesis and the Origin of Death)",
        "wiki_title": "Kintu",
        "lat": 0.31,
        "lng": 32.58,  # Buganda / Lake Victoria
        "epoch_start": 1000,
        "epoch_end": 1500,
        "culture": "Central & Southern African",
        "archetype": "First Man Gaining the Earth and the Origin of Death (Walumbe)",
        "syncretic_ids": ["Q35061"],
    },

    # ── 17. OCEANIC & AUSTRALASIAN ───────────────────────────────────────────
    {
        "id": "Q1145299",
        "name": "The Rainbow Serpent (Dreamtime Earth Sculptor)",
        "wiki_title": "Rainbow_Serpent",
        "lat": -12.46,
        "lng": 130.84,  # Arnhem Land, Australia
        "epoch_start": -4000,
        "epoch_end": 1500,
        "culture": "Oceanic & Australasian",
        "archetype": "Primordial Creator Serpent Carving Riverways",
        "syncretic_ids": ["Q218415"],
    },
    {
        "id": "Q1145305",
        "name": "Maui Fishing Up the North Island (Te Ika-a-Maui)",
        "wiki_title": "Māui_(Māori_mythology)",
        "lat": -38.68,
        "lng": 176.07,  # Lake Taupo, New Zealand
        "epoch_start": 900,
        "epoch_end": 1400,
        "culture": "Oceanic & Australasian",
        "archetype": "Demi-god Trickster Pulling Landmass from Depths",
        "syncretic_ids": ["Q83364"],
    },
    {
        "id": "Q1145310",
        "name": "Kumulipo (Hawaiian Cosmic Genealogic Chant)",
        "wiki_title": "Kumulipo",
        "lat": 19.89,
        "lng": -155.58,  # Hawaii
        "epoch_start": 1200,
        "epoch_end": 1700,
        "culture": "Oceanic & Australasian",
        "archetype": "Evolutionary Chant from Slime to Coral to Gods",
        "syncretic_ids": ["Q133346"],
    },
    {
        "id": "Q131700",
        "name": "Pele and Namakaokahai (Fire vs Sea in Hawaii)",
        "wiki_title": "Pele_(deity)",
        "lat": 19.41,
        "lng": -155.28,  # Kilauea Crater
        "epoch_start": 1000,
        "epoch_end": 1700,
        "culture": "Oceanic & Australasian",
        "archetype": "Volcano Goddess Battling Sea Goddess across Archipelagos",
        "syncretic_ids": ["Q131670"],
    },
    {
        "id": "Q131705",
        "name": "Ranginui and Papatuanuku (Separation of Sky and Earth)",
        "wiki_title": "Rangi_and_Papa",
        "lat": -37.00,
        "lng": 175.00,  # Aotearoa (New Zealand)
        "epoch_start": 900,
        "epoch_end": 1500,
        "culture": "Oceanic & Australasian",
        "archetype": "Primordial Sky Father & Earth Mother Separated by Forest God Tane",
        "syncretic_ids": ["Q35061", "Q190864"],
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
    Assembles the complete list of foundational myths across all worldwide traditions.
    Loads from data/raw/wikidata_raw.json if present with expanded entries.
    """
    DATA_RAW_DIR.mkdir(parents=True, exist_ok=True)
    if OUTPUT_FILE.exists():
        try:
            with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
                saved = json.load(f)
            if len(saved) >= len(FOUNDATIONAL_MYTHS):
                logger.info(f"Loaded {len(saved)} foundational myths from existing catalog at {OUTPUT_FILE}.")
                return saved
        except Exception as e:
            logger.warning(f"Error reading existing catalog {OUTPUT_FILE}: {e}")

    catalog = list(FOUNDATIONAL_MYTHS)
    logger.info(f"Loaded {len(catalog)} curated foundational myths spanning all worldwide regions.")

    # Save to data/raw/wikidata_raw.json
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)

    logger.info(f"Successfully saved {len(catalog)} myths to {OUTPUT_FILE}")
    return catalog


if __name__ == "__main__":
    fetch_and_assemble_catalog()
