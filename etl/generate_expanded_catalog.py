"""
Catalog Expansion Generator for MythosAtlas.
Expands the foundational seed catalog from 88 to 150+ diverse worldwide myths,
covering all inhabited continents, indigenous traditions, and civilizations from -4000 BCE to 1500 CE.
"""

import json
from pathlib import Path
from typing import Any, Dict, List

# Load current 88 myths
RAW_PATH = Path(__file__).resolve().parent.parent / "data" / "raw" / "wikidata_raw.json"
with open(RAW_PATH, "r", encoding="utf-8") as f:
    existing_myths = json.load(f)

existing_ids = {m["id"] for m in existing_myths}
existing_titles = {m["wiki_title"].lower() for m in existing_myths}

NEW_MYTHS: List[Dict[str, Any]] = [
    # ── 1. GRECO-ROMAN EXPANSION ─────────────────────────────────────────────
    {
        "id": "Q172723",
        "name": "The Odyssey (Odysseus & the Sirens)",
        "wiki_title": "Odyssey",
        "lat": 38.43,
        "lng": 20.66,  # Ithaca
        "epoch_start": -800,
        "epoch_end": -600,
        "culture": "Greco-Roman",
        "archetype": "Nostos / Heroic Sea Odyssey & Homecoming",
        "syncretic_ids": ["Q248352", "Q165493"],
    },
    {
        "id": "Q165493",
        "name": "Jason and the Golden Fleece (Argonautica)",
        "wiki_title": "Argonautica",
        "lat": 39.36,
        "lng": 22.94,  # Iolcus (Thessaly)
        "epoch_start": -750,
        "epoch_end": -250,
        "culture": "Greco-Roman",
        "archetype": "Heroic Quest for Sacred Fleece / Dragon Slaying",
        "syncretic_ids": ["Q172723", "Q130832"],
    },
    {
        "id": "Q130832",
        "name": "Perseus Slaying the Gorgon Medusa",
        "wiki_title": "Perseus",
        "lat": 37.72,
        "lng": 22.75,  # Mycenae
        "epoch_start": -800,
        "epoch_end": -100,
        "culture": "Greco-Roman",
        "archetype": "Monster Slayer / Chthonic Severance & Mirrored Shield",
        "syncretic_ids": ["Q165493", "Q129888"],
    },
    {
        "id": "Q172740",
        "name": "Orpheus and Eurydice (The Katabasis)",
        "wiki_title": "Orpheus_and_Eurydice",
        "lat": 41.13,
        "lng": 24.88,  # Thrace
        "epoch_start": -700,
        "epoch_end": -100,
        "culture": "Greco-Roman",
        "archetype": "Katabasis / Tragic Underworld Lyre Rescue",
        "syncretic_ids": ["Q272486", "Q46580"],
    },
    {
        "id": "Q60220",
        "name": "The Aeneid (Aeneas & the Destiny of Rome)",
        "wiki_title": "Aeneid",
        "lat": 41.89,
        "lng": 12.49,  # Rome
        "epoch_start": -30,
        "epoch_end": 400,
        "culture": "Greco-Roman",
        "archetype": "Providential Foundation / Exile to Empire",
        "syncretic_ids": ["Q172723", "Q129888"],
    },
    {
        "id": "Q129888",
        "name": "Theseus and the Minotaur in the Labyrinth",
        "wiki_title": "Minotaur",
        "lat": 35.29,
        "lng": 25.16,  # Knossos (Crete)
        "epoch_start": -1400,
        "epoch_end": -400,
        "culture": "Greco-Roman",
        "archetype": "Labyrinthine Monster Slaying / Thread of Ariadne",
        "syncretic_ids": ["Q130832", "Q165493"],
    },

    # ── 2. CELTIC & BRYTTONIC EXPANSION ──────────────────────────────────────
    {
        "id": "Q105224",
        "name": "King Arthur and the Holy Grail",
        "wiki_title": "King_Arthur",
        "lat": 51.14,
        "lng": -2.71,  # Glastonbury / Avalon
        "epoch_start": 500,
        "epoch_end": 1485,
        "culture": "Celtic",
        "archetype": "Sovereign King / Quest for the Life-Giving Grail",
        "syncretic_ids": ["Q248352", "Q165493"],
    },
    {
        "id": "Q1145397",
        "name": "The Táin Bó Cúailnge (Cattle Raid of Cooley)",
        "wiki_title": "Táin_Bó_Cúailnge",
        "lat": 54.00,
        "lng": -6.37,  # Cooley Peninsula
        "epoch_start": 100,
        "epoch_end": 1100,
        "culture": "Celtic",
        "archetype": "Heroic Single-Combat Defense / Sovereignty Bull",
        "syncretic_ids": ["Q214944", "Q105224"],
    },
    {
        "id": "Q214944",
        "name": "Cú Chulainn (The Hound of Ulster)",
        "wiki_title": "Cú_Chulainn",
        "lat": 54.35,
        "lng": -6.65,  # Emain Macha (Navan Fort)
        "epoch_start": 100,
        "epoch_end": 1200,
        "culture": "Celtic",
        "archetype": "Demigod Berserker Rage (Ríastrad) & Tragic Oath",
        "syncretic_ids": ["Q1145397", "Q130832"],
    },
    {
        "id": "Q1074123",
        "name": "The Children of Lir (The Swan Metamorphosis)",
        "wiki_title": "Children_of_Lir",
        "lat": 53.62,
        "lng": -7.34,  # Lake Derravaragh
        "epoch_start": 500,
        "epoch_end": 1500,
        "culture": "Celtic",
        "archetype": "Tragic Metamorphosis into Swans / 900-Year Exile",
        "syncretic_ids": ["Q105224"],
    },
    {
        "id": "Q1434444",
        "name": "Oisín in Tír na nÓg (Land of Eternal Youth)",
        "wiki_title": "Tír_na_nÓg",
        "lat": 53.27,
        "lng": -9.05,  # Western Coasts of Ireland
        "epoch_start": 300,
        "epoch_end": 1400,
        "culture": "Celtic",
        "archetype": "Otherworldly Paradise / Fatal Time Dilation",
        "syncretic_ids": ["Q105224", "Q248352"],
    },

    # ── 3. VEDIC & HINDU EXPANSION ───────────────────────────────────────────
    {
        "id": "Q213275",
        "name": "Narasimha Avatar & Prahlada",
        "wiki_title": "Narasimha",
        "lat": 15.13,
        "lng": 78.71,  # Ahobilam (Andhra Pradesh)
        "epoch_start": -1000,
        "epoch_end": 1200,
        "culture": "Vedic & Hindu",
        "archetype": "Man-Lion Avatar / Destruction of Unkillable Tyrant",
        "syncretic_ids": ["Q11389", "Q188676"],
    },
    {
        "id": "Q6734749",
        "name": "Durga Slaying Mahishasura (Devi Mahatmya)",
        "wiki_title": "Mahishasuramardini",
        "lat": 24.58,
        "lng": 81.30,  # Vindhyas
        "epoch_start": -500,
        "epoch_end": 1500,
        "culture": "Vedic & Hindu",
        "archetype": "Supreme Goddess Conquering Cosmic Demon Shape-shifter",
        "syncretic_ids": ["Q11389", "Q8785"],
    },
    {
        "id": "Q815849",
        "name": "Karna's Invincible Golden Armor & Tragically Bound Vow",
        "wiki_title": "Karna",
        "lat": 25.28,
        "lng": 86.98,  # Anga (Bhagalpur)
        "epoch_start": -800,
        "epoch_end": 400,
        "culture": "Vedic & Hindu",
        "archetype": "Solar Demigod / Sacrificial Loyalty & Generosity",
        "syncretic_ids": ["Q11389", "Q130832"],
    },
    {
        "id": "Q948958",
        "name": "The Legend of Shakuntala and Dushyanta",
        "wiki_title": "Shakuntala",
        "lat": 29.17,
        "lng": 78.02,  # Hastinapur
        "epoch_start": -800,
        "epoch_end": 400,
        "culture": "Vedic & Hindu",
        "archetype": "Sacred Hermitage Love / Forgotten Signet Ring",
        "syncretic_ids": ["Q11389"],
    },
    {
        "id": "Q212643",
        "name": "Vamana Avatar (The Three Cosmic Strides)",
        "wiki_title": "Vamana",
        "lat": 21.70,
        "lng": 72.98,  # Narmada Valley / Bharuch
        "epoch_start": -1000,
        "epoch_end": 1000,
        "culture": "Vedic & Hindu",
        "archetype": "Cosmic Measuring of the Three Worlds / Humbling the Demon King",
        "syncretic_ids": ["Q213275", "Q11389"],
    },
    {
        "id": "Q1579",
        "name": "Ganesha the Scribe of the Mahabharata",
        "wiki_title": "Ganesha",
        "lat": 31.06,
        "lng": 81.31,  # Mount Kailash
        "epoch_start": -500,
        "epoch_end": 1500,
        "culture": "Vedic & Hindu",
        "archetype": "Remover of Obstacles / Broken Tusk as Sacred Pen",
        "syncretic_ids": ["Q11389"],
    },

    # ── 4. NORSE & GERMANIC EXPANSION ────────────────────────────────────────
    {
        "id": "Q170212",
        "name": "Ragnarok (The Twilight of the Gods)",
        "wiki_title": "Ragnarök",
        "lat": 63.85,
        "lng": -19.00,  # Vigrid Plains (Icelandic mythic geography)
        "epoch_start": 750,
        "epoch_end": 1250,
        "culture": "Norse & Germanic",
        "archetype": "Cosmic Apocalypse & World Submersion and Rebirth",
        "syncretic_ids": ["Q190864", "Q248352"],
    },
    {
        "id": "Q207360",
        "name": "Sigurd Slaying the Dragon Fafnir (Völsunga saga)",
        "wiki_title": "Sigurd",
        "lat": 50.11,
        "lng": 8.68,  # Worms / Rhine
        "epoch_start": 800,
        "epoch_end": 1300,
        "culture": "Norse & Germanic",
        "archetype": "Dragon Slayer / Blood of Fafnir & Golden Hoard Curse",
        "syncretic_ids": ["Q48328", "Q165493"],
    },
    {
        "id": "Q48328",
        "name": "Beowulf Slaying Grendel and the Fire Dragon",
        "wiki_title": "Beowulf",
        "lat": 55.65,
        "lng": 12.08,  # Lejre / Zealand (Hall of Heorot)
        "epoch_start": 600,
        "epoch_end": 1000,
        "culture": "Norse & Germanic",
        "archetype": "Monster Slayer / Self-Sacrificing King in Mead Hall",
        "syncretic_ids": ["Q207360", "Q130832"],
    },
    {
        "id": "Q131345",
        "name": "The Theft and Recovery of Mjölnir (Þrymskviða)",
        "wiki_title": "Þrymskviða",
        "lat": 59.85,
        "lng": 17.63,  # Gamla Uppsala
        "epoch_start": 800,
        "epoch_end": 1250,
        "culture": "Norse & Germanic",
        "archetype": "Theft of Divine Weapon / Trickster Bridal Infiltration",
        "syncretic_ids": ["Q170212", "Q43375"],
    },
    {
        "id": "Q43375",
        "name": "The Death of Baldr and the Mistletoe",
        "wiki_title": "Baldr",
        "lat": 59.32,
        "lng": 18.06,  # Breidablik
        "epoch_start": 750,
        "epoch_end": 1250,
        "culture": "Norse & Germanic",
        "archetype": "Tragic Murder of Radiant God / Underworld Detainment",
        "syncretic_ids": ["Q46580", "Q170212"],
    },
    {
        "id": "Q121852",
        "name": "Loki Bound in the Caverns of Venom",
        "wiki_title": "Loki",
        "lat": 64.13,
        "lng": -21.93,  # Thingvellir
        "epoch_start": 800,
        "epoch_end": 1250,
        "culture": "Norse & Germanic",
        "archetype": "Chained Trickster Causing Earthquakes / Harbinger of Apocalypse",
        "syncretic_ids": ["Q170212"],
    },

    # ── 5. LEVANTINE & ARABIAN EXPANSION ─────────────────────────────────────
    {
        "id": "Q8258",
        "name": "One Thousand and One Nights (Scheherazade's Sagas)",
        "wiki_title": "One_Thousand_and_One_Nights",
        "lat": 33.31,
        "lng": 44.36,  # Baghdad
        "epoch_start": 750,
        "epoch_end": 1450,
        "culture": "Levantine",
        "archetype": "Narrative Frame Tale / Storytelling Defeating Execution",
        "syncretic_ids": ["Q248352"],
    },
    {
        "id": "Q125430",
        "name": "Sinbad the Sailor and the Seven Voyages",
        "wiki_title": "Sinbad_the_Sailor",
        "lat": 30.50,
        "lng": 47.81,  # Basra
        "epoch_start": 800,
        "epoch_end": 1400,
        "culture": "Levantine",
        "archetype": "Maritime Odyssey / Monster Islands & Giant Roc",
        "syncretic_ids": ["Q172723", "Q8258"],
    },
    {
        "id": "Q159888",
        "name": "The Queen of Sheba and King Solomon",
        "wiki_title": "Queen_of_Sheba",
        "lat": 15.42,
        "lng": 45.34,  # Marib (Saba')
        "epoch_start": -950,
        "epoch_end": 500,
        "culture": "Levantine",
        "archetype": "Encounter of Sovereign Wisdom / Mirrored Crystal Floor",
        "syncretic_ids": ["Q8258"],
    },
    {
        "id": "Q1140061",
        "name": "Iram of the Pillars (Atlantis of the Sands)",
        "wiki_title": "Iram_of_the_Pillars",
        "lat": 18.25,
        "lng": 53.64,  # Shisr / Rub' al Khali
        "epoch_start": -1000,
        "epoch_end": 800,
        "culture": "Levantine",
        "archetype": "Sunken Desert Metropolis / Divine Retribution for Hubris",
        "syncretic_ids": ["Q10801"],
    },

    # ── 6. EGYPTIAN EXPANSION ────────────────────────────────────────────────
    {
        "id": "Q179669",
        "name": "The Wrath of Sekhmet and the Red Beer",
        "wiki_title": "Sekhmet",
        "lat": 29.85,
        "lng": 31.25,  # Memphis
        "epoch_start": -2400,
        "epoch_end": -30,
        "culture": "Egyptian",
        "archetype": "Lioness Eye of Ra / Devouring Wrath Pacified by Sacred Drink",
        "syncretic_ids": ["Q46580", "Q107873"],
    },
    {
        "id": "Q794",
        "name": "Isis and the Secret Name of Ra",
        "wiki_title": "Isis",
        "lat": 24.02,
        "lng": 32.88,  # Philae
        "epoch_start": -2000,
        "epoch_end": -30,
        "culture": "Egyptian",
        "archetype": "Magical Revelation of the Ineffable True Name",
        "syncretic_ids": ["Q46580", "Q272486"],
    },

    # ── 7. MESOPOTAMIAN EXPANSION ────────────────────────────────────────────
    {
        "id": "Q368367",
        "name": "Etana's Ascent to Heaven on the Eagle",
        "wiki_title": "Etana",
        "lat": 32.55,
        "lng": 44.53,  # Kish
        "epoch_start": -2800,
        "epoch_end": -1600,
        "culture": "Mesopotamian",
        "archetype": "Heavenly Ascent / Quest for the Plant of Birth",
        "syncretic_ids": ["Q248352"],
    },
    {
        "id": "Q614880",
        "name": "Anzu Stealing the Tablet of Destinies",
        "wiki_title": "Anzû",
        "lat": 32.12,
        "lng": 45.23,  # Nippur
        "epoch_start": -2100,
        "epoch_end": -1100,
        "culture": "Mesopotamian",
        "archetype": "Theft of Cosmic Sovereignty / Lion-Headed Eagle Slaying",
        "syncretic_ids": ["Q190864", "Q8785"],
    },

    # ── 8. EAST ASIAN EXPANSION ──────────────────────────────────────────────
    {
        "id": "Q841323",
        "name": "The Tale of the Bamboo Cutter (Princess Kaguya)",
        "wiki_title": "The_Tale_of_the_Bamboo_Cutter",
        "lat": 35.01,
        "lng": 135.76,  # Kyoto (Heian-kyō)
        "epoch_start": 850,
        "epoch_end": 1200,
        "culture": "East Asian",
        "archetype": "Celestial Moon Maiden / Impossible Suitor Quests",
        "syncretic_ids": ["Q214944"],
    },
    {
        "id": "Q714092",
        "name": "Momotaro (The Peach Boy of Onigashima)",
        "wiki_title": "Momotarō",
        "lat": 34.66,
        "lng": 133.93,  # Okayama
        "epoch_start": 1000,
        "epoch_end": 1600,
        "culture": "East Asian",
        "archetype": "Miraculous Birth from Fruit / Island Demon Subjugation",
        "syncretic_ids": ["Q130832"],
    },
    {
        "id": "Q841444",
        "name": "The Cowherd and the Weaver Girl (Qixi Legend)",
        "wiki_title": "The_Cowherd_and_the_Weaver_Girl",
        "lat": 34.34,
        "lng": 108.94,  # Xi'an / Yellow River
        "epoch_start": -300,
        "epoch_end": 1400,
        "culture": "East Asian",
        "archetype": "Celestial Star-Crossed Lovers / Magpie Celestial Bridge",
        "syncretic_ids": ["Q841323"],
    },

    # ── 9. PERSIAN & IRANIAN EXPANSION ───────────────────────────────────────
    {
        "id": "Q144703",
        "name": "Zahhak the Serpent King and Kaveh's Uprising",
        "wiki_title": "Zahhak",
        "lat": 35.95,
        "lng": 52.11,  # Mount Damavand
        "epoch_start": -800,
        "epoch_end": 1000,
        "culture": "Persian & Iranian",
        "archetype": "Shoulder Serpent Tyrant / Blacksmith's Apron of Rebellion",
        "syncretic_ids": ["Q190864", "Q8785"],
    },
    {
        "id": "Q216999",
        "name": "The Seven Labors of Rostam (Haft Khan)",
        "wiki_title": "Rostam",
        "lat": 36.56,
        "lng": 53.06,  # Mazandaran
        "epoch_start": -600,
        "epoch_end": 1050,
        "culture": "Persian & Iranian",
        "archetype": "Hero's Seven Trials / Slaying the White Div",
        "syncretic_ids": ["Q165493", "Q130832"],
    },
    {
        "id": "Q626359",
        "name": "Arash the Archer (The Boundary-Defining Shot)",
        "wiki_title": "Arash",
        "lat": 35.95,
        "lng": 52.11,  # Mount Damavand
        "epoch_start": -500,
        "epoch_end": 800,
        "culture": "Persian & Iranian",
        "archetype": "Sacrificial Arrow Expending the Hero's Life for the Homeland",
        "syncretic_ids": ["Q216999"],
    },

    # ── 10. SLAVIC & BALTIC EXPANSION ────────────────────────────────────────
    {
        "id": "Q211158",
        "name": "The Firebird and Tsarevich Ivan",
        "wiki_title": "Firebird_(Slavic_folklore)",
        "lat": 58.52,
        "lng": 31.27,  # Novgorod
        "epoch_start": 900,
        "epoch_end": 1400,
        "culture": "Slavic & Baltic",
        "archetype": "Luminous Solar Avian Quest / Allied Grey Wolf",
        "syncretic_ids": ["Q165493"],
    },
    {
        "id": "Q188734",
        "name": "Koschei the Deathless and the Hidden Needle",
        "wiki_title": "Koschei",
        "lat": 50.45,
        "lng": 30.52,  # Kyiv
        "epoch_start": 900,
        "epoch_end": 1400,
        "culture": "Slavic & Baltic",
        "archetype": "External Soul (Egg in Duck in Hare in Oak Chest)",
        "syncretic_ids": ["Q248352"],
    },
    {
        "id": "Q153724",
        "name": "Laima and the Weaving of Human Destiny",
        "wiki_title": "Laima",
        "lat": 56.94,
        "lng": 24.10,  # Riga (Daugava River)
        "epoch_start": 500,
        "epoch_end": 1400,
        "culture": "Slavic & Baltic",
        "archetype": "Baltic Fate Goddess Weaving the Sacred Life Thread",
        "syncretic_ids": ["Q10801"],
    },
    {
        "id": "Q940176",
        "name": "Saule the Sun Goddess and Ausrine",
        "wiki_title": "Saulė",
        "lat": 54.68,
        "lng": 25.27,  # Vilnius
        "epoch_start": 500,
        "epoch_end": 1350,
        "culture": "Slavic & Baltic",
        "archetype": "Solar Chariot Riding Across Copper Mountains",
        "syncretic_ids": ["Q153724"],
    },

    # ── 11. FINNO-UGRIC EXPANSION ────────────────────────────────────────────
    {
        "id": "Q212628",
        "name": "Forging of the Sampo (Mill of Eternal Abundance)",
        "wiki_title": "Sampo",
        "lat": 64.22,
        "lng": 27.72,  # Kainuu / North Karelia
        "epoch_start": 800,
        "epoch_end": 1400,
        "culture": "Finno-Ugric",
        "archetype": "Primordial Magic Mill Grinding Grain, Salt, and Gold",
        "syncretic_ids": ["Q105224"],
    },
    {
        "id": "Q211029",
        "name": "Väinämöinen's Shamanic Word Duel with Joukahainen",
        "wiki_title": "Väinämöinen",
        "lat": 61.80,
        "lng": 29.80,  # Lake Ladoga
        "epoch_start": 800,
        "epoch_end": 1400,
        "culture": "Finno-Ugric",
        "archetype": "Singing Wizard Sinking Rival into the Shifting Mire",
        "syncretic_ids": ["Q212628"],
    },

    # ── 12. CENTRAL ASIAN & STEPPE EXPANSION ─────────────────────────────────
    {
        "id": "Q651234",
        "name": "The Legend of Oghuz Khagan and the Blue Wolf",
        "wiki_title": "Oghuz_Khagan",
        "lat": 48.00,
        "lng": 85.00,  # Altai Mountains
        "epoch_start": -300,
        "epoch_end": 1200,
        "culture": "Central Asian & Steppe",
        "archetype": "Wolf-Guided Steppe Sovereign Uniting Nomadic Tribes",
        "syncretic_ids": ["Q216999"],
    },
    {
        "id": "Q494553",
        "name": "The Book of Dede Korkut and the Escape from Death",
        "wiki_title": "Book_of_Dede_Korkut",
        "lat": 44.85,
        "lng": 65.50,  # Syr Darya
        "epoch_start": 700,
        "epoch_end": 1300,
        "culture": "Central Asian & Steppe",
        "archetype": "Minstrel Playing the Kobyz on Water to Evade Death",
        "syncretic_ids": ["Q172740", "Q248352"],
    },
    {
        "id": "Q260570",
        "name": "Umay the Solar Mother of the Steppe",
        "wiki_title": "Umay",
        "lat": 42.00,
        "lng": 80.00,  # Tian Shan Mountains
        "epoch_start": 500,
        "epoch_end": 1200,
        "culture": "Central Asian & Steppe",
        "archetype": "Protective Mother Goddess of Children, Rebirth, and Flocks",
        "syncretic_ids": ["Q153724"],
    },

    # ── 13. SOUTHEAST ASIAN EXPANSION ────────────────────────────────────────
    {
        "id": "Q131804",
        "name": "Phra Mae Thorani (Earth Goddess Drowning Mara)",
        "wiki_title": "Phra_Mae_Thorani",
        "lat": 14.35,
        "lng": 100.56,  # Ayutthaya
        "epoch_start": 500,
        "epoch_end": 1500,
        "culture": "Southeast Asian",
        "archetype": "Earth Goddess Squeezing Water from Hair to Deluge Evil",
        "syncretic_ids": ["Q6734749", "Q10801"],
    },
    {
        "id": "Q1189332",
        "name": "Nyai Roro Kidul (Queen of the Southern Sea)",
        "wiki_title": "Nyai_Roro_Kidul",
        "lat": -8.02,
        "lng": 110.33,  # Parangtritis (Java)
        "epoch_start": 900,
        "epoch_end": 1500,
        "culture": "Southeast Asian",
        "archetype": "Sovereignty Sea Goddess in Green Silk Allied with Mataram Kings",
        "syncretic_ids": ["Q179198"],
    },
    {
        "id": "Q2900898",
        "name": "Biag ni Lam-ang (The Ilocano Folk Epic)",
        "wiki_title": "Biag_ni_Lam-ang",
        "lat": 17.57,
        "lng": 120.38,  # Vigan / Ilocos (Luzon)
        "epoch_start": 1000,
        "epoch_end": 1500,
        "culture": "Southeast Asian",
        "archetype": "Infant Wonder Hero / Death in the Sea & Rebirth from Bones",
        "syncretic_ids": ["Q214944", "Q46580"],
    },
    {
        "id": "Q234455",
        "name": "The Princess of Mount Ledang (Puteri Gunung Ledang)",
        "wiki_title": "Puteri_Gunung_Ledang",
        "lat": 2.37,
        "lng": 102.60,  # Mount Ledang (Malacca)
        "epoch_start": 1300,
        "epoch_end": 1500,
        "culture": "Southeast Asian",
        "archetype": "Mountain Fairy Demanding Bridge of Gold and Tears",
        "syncretic_ids": ["Q841323"],
    },

    # ── 14. NORTH AMERICAN INDIGENOUS EXPANSION ──────────────────────────────
    {
        "id": "Q1138243",
        "name": "Coyote the Trickster and the Theft of Fire",
        "wiki_title": "Coyote_(mythology)",
        "lat": 44.00,
        "lng": -118.00,  # Columbia River Plateau
        "epoch_start": -1000,
        "epoch_end": 1500,
        "culture": "North American Indigenous",
        "archetype": "Promethean Trickster / Passing the Burning Ember in Relay",
        "syncretic_ids": ["Q121852"],
    },
    {
        "id": "Q2302324",
        "name": "Spider Grandmother Weaving the Worlds (Hopi)",
        "wiki_title": "Spider_Grandmother",
        "lat": 35.87,
        "lng": -110.62,  # Old Oraibi (Hopi Mesas)
        "epoch_start": -1000,
        "epoch_end": 1500,
        "culture": "North American Indigenous",
        "archetype": "Cosmic Weaver / Molding Mortals from Colored Clay",
        "syncretic_ids": ["Q153724", "Q1140061"],
    },
    {
        "id": "Q242004",
        "name": "Thunderbird and Whale (The Oceanic Clash)",
        "wiki_title": "Thunderbird_(mythology)",
        "lat": 47.90,
        "lng": -124.63,  # Olympic Peninsula (Pacific Northwest)
        "epoch_start": -1000,
        "epoch_end": 1500,
        "culture": "North American Indigenous",
        "archetype": "Sky Raptor Hurling Lightning against Sub-Sea Leviathan",
        "syncretic_ids": ["Q8785", "Q190864"],
    },
    {
        "id": "Q240679",
        "name": "Gluskabe Slaying the Great Drought Monster (Abenaki)",
        "wiki_title": "Glooscap",
        "lat": 44.90,
        "lng": -68.70,  # Penobscot River (Maine)
        "epoch_start": -500,
        "epoch_end": 1500,
        "culture": "North American Indigenous",
        "archetype": "Transformer Hero / Piercing the Hoarded Waters of the Bullfrog",
        "syncretic_ids": ["Q11389"],
    },

    # ── 15. MESOAMERICAN EXPANSION ───────────────────────────────────────────
    {
        "id": "Q131444",
        "name": "Huitzilopochtli Born to Slay the Stars at Coatepec",
        "wiki_title": "Huitzilopochtli",
        "lat": 19.43,
        "lng": -99.13,  # Tenochtitlan
        "epoch_start": 1100,
        "epoch_end": 1500,
        "culture": "Mesoamerican",
        "archetype": "Solar Warrior Born Fully Armed / Annihilation of Darkness",
        "syncretic_ids": ["Q8785"],
    },
    {
        "id": "Q206927",
        "name": "Chaac the Rain God of Sacred Cenotes",
        "wiki_title": "Chaac",
        "lat": 20.68,
        "lng": -88.57,  # Chichen Itza
        "epoch_start": 300,
        "epoch_end": 1200,
        "culture": "Mesoamerican",
        "archetype": "Lightning Axe Strike Shattering Clouds over the Cenote",
        "syncretic_ids": ["Q131379"],
    },
    {
        "id": "Q201083",
        "name": "Tezcatlipoca and the Smoking Obsidian Mirror",
        "wiki_title": "Tezcatlipoca",
        "lat": 19.51,
        "lng": -98.88,  # Texcoco
        "epoch_start": 900,
        "epoch_end": 1500,
        "culture": "Mesoamerican",
        "archetype": "Lord of the Night Sky, Fate, and Intangible Shadow",
        "syncretic_ids": ["Q121852"],
    },

    # ── 16. ANDEAN & SOUTH AMERICAN EXPANSION ────────────────────────────────
    {
        "id": "Q165997",
        "name": "Manco Cápac & Mama Ocllo (Founding of Cusco)",
        "wiki_title": "Manco_Cápac",
        "lat": -15.84,
        "lng": -69.33,  # Lake Titicaca to Cusco
        "epoch_start": 1100,
        "epoch_end": 1500,
        "culture": "Andean & South American",
        "archetype": "Children of the Sun Sinking the Golden Staff into Sacred Earth",
        "syncretic_ids": ["Q60220"],
    },
    {
        "id": "Q385552",
        "name": "Pachacamac the Earth-Shaker of the Coast",
        "wiki_title": "Pachacamac",
        "lat": -12.26,
        "lng": -76.90,  # Lurin Valley (Lima)
        "epoch_start": 200,
        "epoch_end": 1500,
        "culture": "Andean & South American",
        "archetype": "Seismic Creator God Shaking the Andes with a Head Nod",
        "syncretic_ids": ["Q8785"],
    },
    {
        "id": "Q164426",
        "name": "El Dorado and the Sacred Raft of Lake Guatavita (Muisca)",
        "wiki_title": "El_Dorado",
        "lat": 4.98,
        "lng": -73.77,  # Lake Guatavita (Colombia)
        "epoch_start": 800,
        "epoch_end": 1500,
        "culture": "Andean & South American",
        "archetype": "Gilded King Submerging into High-Mountain Sacred Water",
        "syncretic_ids": ["Q165493"],
    },
    {
        "id": "Q234475",
        "name": "The Mapuche Deluge of the Two Serpents",
        "wiki_title": "Mapuche_mythology",
        "lat": -38.74,
        "lng": -72.60,  # Araucanía (Chile)
        "epoch_start": -500,
        "epoch_end": 1500,
        "culture": "Andean & South American",
        "archetype": "Earth Serpent Raising Mountains Against Oceanic Flood Serpent",
        "syncretic_ids": ["Q10801", "Q190864"],
    },

    # ── 17. WEST AFRICAN EXPANSION ───────────────────────────────────────────
    {
        "id": "Q939988",
        "name": "Obatala Sculpting Human Bodies from Clay",
        "wiki_title": "Obatala",
        "lat": 7.48,
        "lng": 4.56,  # Ile-Ife (Nigeria)
        "epoch_start": 500,
        "epoch_end": 1500,
        "culture": "West African",
        "archetype": "White Robed Sculptor of Mortals / Descent from Iron Chain",
        "syncretic_ids": ["Q2302324"],
    },
    {
        "id": "Q591559",
        "name": "Oya the Goddess of Storms, Winds, and Rebirth",
        "wiki_title": "Oya",
        "lat": 8.00,
        "lng": 5.00,  # Niger River Basin
        "epoch_start": 800,
        "epoch_end": 1500,
        "culture": "West African",
        "archetype": "Fierce Wind Warrior Guiding the Souls across Rebirth",
        "syncretic_ids": ["Q179669"],
    },
    {
        "id": "Q651543",
        "name": "Oshun and the Golden Waters of Healing",
        "wiki_title": "Oshun",
        "lat": 7.76,
        "lng": 4.55,  # Osun-Osogbo Sacred Grove
        "epoch_start": 800,
        "epoch_end": 1500,
        "culture": "West African",
        "archetype": "Goddess of Sweet Waters, Mirrors, and Unconquerable Life",
        "syncretic_ids": ["Q179198"],
    },
    {
        "id": "Q134114",
        "name": "Yemoja Mother of All Waters and Orishas",
        "wiki_title": "Yemoja",
        "lat": 6.52,
        "lng": 3.38,  # Ogun River to Gulf of Guinea
        "epoch_start": 800,
        "epoch_end": 1500,
        "culture": "West African",
        "archetype": "Oceanic Mother Protecting Ships and Birthing Rivers",
        "syncretic_ids": ["Q651543"],
    },

    # ── 18. CENTRAL & SOUTHERN AFRICAN EXPANSION ─────────────────────────────
    {
        "id": "Q679633",
        "name": "Mbombo Vomiting the Sun, Moon, and Stars (Kuba)",
        "wiki_title": "Mbombo",
        "lat": -4.32,
        "lng": 21.05,  # Kasai River / Congo Basin
        "epoch_start": 500,
        "epoch_end": 1500,
        "culture": "Central & Southern African",
        "archetype": "Cosmic Giant Vomiting Light and Living Beings into Darkness",
        "syncretic_ids": ["Q190864"],
    },
    {
        "id": "Q131448",
        "name": "Kintu and Nambi's Descent with Seeds of Life (Buganda)",
        "wiki_title": "Kintu",
        "lat": 0.31,
        "lng": 32.58,  # Lake Victoria / Kampala
        "epoch_start": 1000,
        "epoch_end": 1500,
        "culture": "Central & Southern African",
        "archetype": "First King of Mankind Bringing Banana Palms and Cattle",
        "syncretic_ids": ["Q165997"],
    },
    {
        "id": "Q1447820",
        "name": "Modjadji the Rain Queen of the Balobedu",
        "wiki_title": "Rain_Queen",
        "lat": -23.63,
        "lng": 30.29,  # Ga-Modjadji (Limpopo)
        "epoch_start": 1200,
        "epoch_end": 1600,
        "culture": "Central & Southern African",
        "archetype": "Dynasty of Immortal Rain-Making Queens Holding Cloud Secrets",
        "syncretic_ids": ["Q206927"],
    },
    {
        "id": "Q212680",
        "name": "Nyami Nyami the Zambezi River Dragon Serpent",
        "wiki_title": "Nyami_Nyami",
        "lat": -16.52,
        "lng": 28.76,  # Kariba Gorge (Zambezi)
        "epoch_start": 800,
        "epoch_end": 1500,
        "culture": "Central & Southern African",
        "archetype": "Dragon-Fish River Spirit Sinking Dams and Protecting Fishermen",
        "syncretic_ids": ["Q8785"],
    },

    # ── 19. OCEANIC & AUSTRALASIAN EXPANSION ─────────────────────────────────
    {
        "id": "Q1422880",
        "name": "Tāne Mahuta Pushing Apart Earth and Sky",
        "wiki_title": "Tāne",
        "lat": -35.60,
        "lng": 173.54,  # Waipoua Kauri Forest (New Zealand)
        "epoch_start": 900,
        "epoch_end": 1500,
        "culture": "Oceanic & Australasian",
        "archetype": "Forest Colossus Inverting to Sever Clinging Parents Heaven and Earth",
        "syncretic_ids": ["Q131705"],
    },
    {
        "id": "Q803698",
        "name": "Baiame the Sky Father of the Great Dreamtime",
        "wiki_title": "Baiame",
        "lat": -32.90,
        "lng": 150.85,  # Mount Yengo (New South Wales)
        "epoch_start": -10000,
        "epoch_end": 1500,
        "culture": "Oceanic & Australasian",
        "archetype": "Dreamtime Sky Father Stepping Back to Heaven from Flat Mountain",
        "syncretic_ids": ["Q1422880"],
    },
    {
        "id": "Q212450",
        "name": "Tiddalik the Frog Who Drank the Rivers",
        "wiki_title": "Tiddalik",
        "lat": -34.00,
        "lng": 142.00,  # Murray-Darling River Basin
        "epoch_start": -5000,
        "epoch_end": 1500,
        "culture": "Oceanic & Australasian",
        "archetype": "Giant Thirsty Amphibian Swallowing the Waters Made to Laugh",
        "syncretic_ids": ["Q240679"],
    },
    {
        "id": "Q1792942",
        "name": "Kupe the Navigator and the Giant Octopus Te Wheke",
        "wiki_title": "Kupe",
        "lat": -41.28,
        "lng": 174.77,  # Cook Strait (Raukawa Moana)
        "epoch_start": 950,
        "epoch_end": 1350,
        "culture": "Oceanic & Australasian",
        "archetype": "Star Navigator Crossing Open Pacific to Harpoon the Sea Monster",
        "syncretic_ids": ["Q172723", "Q165493"],
    },

    # ── 20. ADDITIONAL WORLDWIDE MASTER EPICS ────────────────────────────────
    {
        "id": "Q494557",
        "name": "The Tale of Chunhyang (Fidelity & Justice)",
        "wiki_title": "Chunhyangjeon",
        "lat": 35.41,
        "lng": 127.38,  # Namwon (Korea)
        "epoch_start": 1300,
        "epoch_end": 1550,
        "culture": "East Asian",
        "archetype": "Secret Royal Inspector / Undying Love and Justice",
        "syncretic_ids": ["Q948958"],
    },
    {
        "id": "Q283084",
        "name": "Jumong and the Foundation of Goguryeo",
        "wiki_title": "Dongmyeong_of_Goguryeo",
        "lat": 41.12,
        "lng": 126.17,  # Ji'an / Yalu River
        "epoch_start": -58,
        "epoch_end": 200,
        "culture": "East Asian",
        "archetype": "Sun-Born Master Archer / Crossing River on Turtles",
        "syncretic_ids": ["Q626359", "Q651234"],
    },
    {
        "id": "Q131665",
        "name": "Amaterasu Emerging from the Heavenly Rock Cave",
        "wiki_title": "Ama-no-Iwato",
        "lat": 32.71,
        "lng": 131.30,  # Takachiho (Kyushu)
        "epoch_start": 600,
        "epoch_end": 1300,
        "culture": "East Asian",
        "archetype": "Solar Goddess Concealed in Cave / Laughter Restoring Cosmic Light",
        "syncretic_ids": ["Q940176"],
    },
    {
        "id": "Q217448",
        "name": "Susanoo Slaying the Eight-Headed Serpent (Yamata no Orochi)",
        "wiki_title": "Yamata_no_Orochi",
        "lat": 35.36,
        "lng": 133.05,  # Hii River / Izumo
        "epoch_start": 600,
        "epoch_end": 1300,
        "culture": "East Asian",
        "archetype": "Storm Hero Slaying Many-Headed Serpent / Unsheathing the Sacred Sword",
        "syncretic_ids": ["Q8785", "Q207360"],
    },
    {
        "id": "Q1196420",
        "name": "Urashima Taro and the Dragon Palace (Ryūgū-jō)",
        "wiki_title": "Urashima_Tarō",
        "lat": 35.53,
        "lng": 135.21,  # Tango Peninsula
        "epoch_start": 700,
        "epoch_end": 1400,
        "culture": "East Asian",
        "archetype": "Undersea Dragon Kingdom / Tamatebako Box of Irreversible Aging",
        "syncretic_ids": ["Q1434444"],
    },
    {
        "id": "Q273898",
        "name": "Chang'e Ascending to the Moon",
        "wiki_title": "Chang'e",
        "lat": 34.61,
        "lng": 112.45,  # Luoyang
        "epoch_start": -800,
        "epoch_end": 1200,
        "culture": "East Asian",
        "archetype": "Elixir of Immortality / Solitary Moon Maiden and Jade Rabbit",
        "syncretic_ids": ["Q841323"],
    },
    {
        "id": "Q713098",
        "name": "Nezha Conquering the Dragon Kings of the Four Seas",
        "wiki_title": "Nezha",
        "lat": 32.06,
        "lng": 118.79,  # Chentang Pass / Nanjing
        "epoch_start": 600,
        "epoch_end": 1550,
        "culture": "East Asian",
        "archetype": "Lotus Reborn Warrior Hero / Wind Fire Wheels & Universe Ring",
        "syncretic_ids": ["Q214944"],
    },
    {
        "id": "Q898687",
        "name": "Bran the Blessed and the Cauldron of Rebirth",
        "wiki_title": "Bran_the_Blessed",
        "lat": 52.86,
        "lng": -4.11,  # Harlech (Wales)
        "epoch_start": 400,
        "epoch_end": 1300,
        "culture": "Celtic",
        "archetype": "Colossal Guardian King / Severed Head Singing at the Threshold",
        "syncretic_ids": ["Q105224"],
    },
    {
        "id": "Q218967",
        "name": "The Morrígan (Phantom Queen of Battle & Fate)",
        "wiki_title": "The_Morrígan",
        "lat": 53.80,
        "lng": -8.30,  # Cave of the Cats (Rathcroghan)
        "epoch_start": 100,
        "epoch_end": 1200,
        "culture": "Celtic",
        "archetype": "Triple War Goddess / Raven of Prophecy and Sovereignty",
        "syncretic_ids": ["Q1145397", "Q179669"],
    },
    {
        "id": "Q215683",
        "name": "Lugh Lámhfhada and the Spear of Victory",
        "wiki_title": "Lugh",
        "lat": 53.58,
        "lng": -6.61,  # Hill of Tara
        "epoch_start": -300,
        "epoch_end": 1100,
        "culture": "Celtic",
        "archetype": "Master of All Arts / Slaying the Evil-Eyed Titan Balor",
        "syncretic_ids": ["Q130832", "Q8785"],
    },
    {
        "id": "Q179836",
        "name": "Sir Gawain and the Green Knight (The Beheading Game)",
        "wiki_title": "Sir_Gawain_and_the_Green_Knight",
        "lat": 53.07,
        "lng": -1.99,  # The Roaches / Peak District
        "epoch_start": 1300,
        "epoch_end": 1500,
        "culture": "Celtic",
        "archetype": "Chivalric Honor Trial / Green Chapel Beheading Covenant",
        "syncretic_ids": ["Q105224"],
    },
    {
        "id": "Q1089201",
        "name": "Gita Govinda (The Divine Love of Radha & Krishna)",
        "wiki_title": "Gita_Govinda",
        "lat": 19.81,
        "lng": 85.83,  # Puri (Odisha)
        "epoch_start": 1100,
        "epoch_end": 1500,
        "culture": "Vedic & Hindu",
        "archetype": "Mystic Devotional Love / Soul Longing for the Supreme Divinity",
        "syncretic_ids": ["Q841444"],
    },
    {
        "id": "Q188683",
        "name": "Hanuman Leaping across the Ocean to Lanka",
        "wiki_title": "Hanuman",
        "lat": 15.33,
        "lng": 76.46,  # Kishkindha (Hampi)
        "epoch_start": -800,
        "epoch_end": 1500,
        "culture": "Vedic & Hindu",
        "archetype": "Selfless Devotion and Superhuman Strength / Mountain Lifter",
        "syncretic_ids": ["Q11389"],
    },
    {
        "id": "Q80930",
        "name": "The Iliad (The Wrath of Achilles)",
        "wiki_title": "Iliad",
        "lat": 39.95,
        "lng": 26.24,  # Troy (Hisarlik)
        "epoch_start": -800,
        "epoch_end": -600,
        "culture": "Greco-Roman",
        "archetype": "Tragic Mortal Heroism / Hubris and Ineluctable Fate",
        "syncretic_ids": ["Q172723", "Q815849"],
    },
    {
        "id": "Q122248",
        "name": "The Twelve Labors of Heracles",
        "wiki_title": "Heracles",
        "lat": 37.64,
        "lng": 22.72,  # Tiryns / Nemea
        "epoch_start": -900,
        "epoch_end": -200,
        "culture": "Greco-Roman",
        "archetype": "Archetypal Demigod / Twelve Cosmic Labors and Apotheosis",
        "syncretic_ids": ["Q216999", "Q130832"],
    },
    {
        "id": "Q183413",
        "name": "Romulus and Remus (The She-Wolf and Sacred Furrow)",
        "wiki_title": "Romulus_and_Remus",
        "lat": 41.89,
        "lng": 12.48,  # Palatine Hill (Rome)
        "epoch_start": -753,
        "epoch_end": 400,
        "culture": "Greco-Roman",
        "archetype": "Twin Founders Reared by Beast / Fratricidal Sacred Boundary",
        "syncretic_ids": ["Q60220"],
    },
    {
        "id": "Q2634351",
        "name": "Jamshid's Seven-Ringed Cup of Divination",
        "wiki_title": "Cup_of_Jamshid",
        "lat": 29.93,
        "lng": 52.89,  # Persepolis
        "epoch_start": -800,
        "epoch_end": 1000,
        "culture": "Persian & Iranian",
        "archetype": "Omniscient Golden Cup Reflecting the Universe and Immortality",
        "syncretic_ids": ["Q105224", "Q212628"],
    },
    {
        "id": "Q1144883",
        "name": "Quetzalcoatl's Descent into Mictlan for the Bones of Humanity",
        "wiki_title": "Mictlan",
        "lat": 19.69,
        "lng": -98.84,  # Teotihuacan
        "epoch_start": 200,
        "epoch_end": 1500,
        "culture": "Mesoamerican",
        "archetype": "Katabasis for Ancestral Bones / Resurrected by Blood of Quetzalcoatl",
        "syncretic_ids": ["Q272486", "Q46580"],
    },
]

def main():
    print(f"Existing myths: {len(existing_myths)}")
    unique_new = []
    for m in NEW_MYTHS:
        if m["id"] in existing_ids:
            print(f"Skipping duplicate ID: {m['id']} ({m['name']})")
            continue
        if m["wiki_title"].lower() in existing_titles:
            print(f"Skipping duplicate title: {m['wiki_title']} ({m['name']})")
            continue
        unique_new.append(m)
        existing_ids.add(m["id"])
        existing_titles.add(m["wiki_title"].lower())

    print(f"Adding {len(unique_new)} new unique myths.")
    combined = existing_myths + unique_new
    print(f"Total myths in expanded catalog: {len(combined)}")

    # Save to data/raw/wikidata_raw.json
    with open(RAW_PATH, "w", encoding="utf-8") as f:
        json.dump(combined, f, indent=2, ensure_ascii=False)
    print(f"Successfully wrote {len(combined)} myths to {RAW_PATH}")

if __name__ == "__main__":
    main()
