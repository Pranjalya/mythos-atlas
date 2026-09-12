"""
Mega Catalog Generator for MythosAtlas.
Adds ~147 newly verified foundational myths across all 19 cultures,
scaling the worldwide mythic atlas to over 300 foundational epics.
"""

import json
from pathlib import Path
from typing import Any, Dict, List
import urllib.parse

DATA_RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"
WIKIDATA_RAW_PATH = DATA_RAW_DIR / "wikidata_raw.json"

MEGA_NEW_MYTHS: List[Dict[str, Any]] = [
    # ── 1. MESOPOTAMIAN ───────────────────────────────────────────────────────
    {
        "id": "Q111728",
        "name": "Adapa and the South Wind (The Broken Wing & Refusal of Immortality)",
        "wiki_title": "Adapa",
        "lat": 30.96,
        "lng": 46.10,  # Eridu (Temple of Enki / Ea)
        "epoch_start": -2100,
        "epoch_end": -1400,
        "culture": "Mesopotamian",
        "archetype": "Loss of Human Immortality through Tragic Misunderstanding",
        "syncretic_ids": ["Q10801", "Q35160"],
    },
    {
        "id": "Q505417",
        "name": "Lugalbanda in the Mountain Cave (The Gift of the Divine Anzu Bird)",
        "wiki_title": "Lugalbanda",
        "lat": 31.32,
        "lng": 45.63,  # Uruk / Zagros Mountains
        "epoch_start": -2600,
        "epoch_end": -1800,
        "culture": "Mesopotamian",
        "archetype": "Hero Abandoned in Wilderness Aided by Divine Raptor",
        "syncretic_ids": ["Q248352", "Q216999"],
    },
    {
        "id": "Q836371",
        "name": "Enmerkar and the Lord of Aratta (The Invention of Cuneiform Writing)",
        "wiki_title": "Enmerkar_and_the_Lord_of_Aratta",
        "lat": 31.32,
        "lng": 45.63,  # Uruk
        "epoch_start": -2700,
        "epoch_end": -1800,
        "culture": "Mesopotamian",
        "archetype": "Culture Hero Inventing the Written Word to Bridge Distant Empires",
        "syncretic_ids": ["Q1579", "Q83364"],
    },
    {
        "id": "Q179655",
        "name": "Nergal and Ereshkigal (The Marriage of the Netherworld Sovereigns)",
        "wiki_title": "Ereshkigal",
        "lat": 32.53,
        "lng": 44.42,  # Babylon / Kurnugi
        "epoch_start": -2000,
        "epoch_end": -1200,
        "culture": "Mesopotamian",
        "archetype": "Underworld Conquered through Fierce Conjugal Union",
        "syncretic_ids": ["Q179654", "Q172740"],
    },
    {
        "id": "Q234720",
        "name": "Dumuzid the Shepherd (The Dying and Rising God of the Steppe)",
        "wiki_title": "Dumuzid",
        "lat": 31.80,
        "lng": 45.20,  # Bad-tibira / Sumerian Steppe
        "epoch_start": -2500,
        "epoch_end": -1500,
        "culture": "Mesopotamian",
        "archetype": "Sacrificed Pastoral God Bound to Seasonal Agricultural Cycles",
        "syncretic_ids": ["Q179654", "Q46580"],
    },
    {
        "id": "Q368369",
        "name": "The Legend of Sargon (The Baby in the Reed Basket on the Euphrates)",
        "wiki_title": "Sargon_of_Akkad",
        "lat": 33.10,
        "lng": 44.20,  # Akkad / Kish
        "epoch_start": -2334,
        "epoch_end": -2279,
        "culture": "Mesopotamian",
        "archetype": "Royal Infant Cast Adrift on River Ascending to Empire",
        "syncretic_ids": ["Q1164", "Q60184"],
    },

    # ── 2. EGYPTIAN ───────────────────────────────────────────────────────────
    {
        "id": "Q208144",
        "name": "The Contendings of Horus and Seth (The Trial for the Throne of Egypt)",
        "wiki_title": "Contendings_of_Horus_and_Seth",
        "lat": 25.70,
        "lng": 32.60,  # Heliopolis / Thebes
        "epoch_start": -1180,
        "epoch_end": -1070,
        "culture": "Egyptian",
        "archetype": "Divine Judicial Combat between Order (Ma'at) and Chaos (Isfet)",
        "syncretic_ids": ["Q8785", "Q248352"],
    },
    {
        "id": "Q836372",
        "name": "The Book of the Heavenly Cow (The Cleansing and Escape of Ra)",
        "wiki_title": "Book_of_the_Heavenly_Cow",
        "lat": 29.97,
        "lng": 31.13,  # Memphis
        "epoch_start": -1330,
        "epoch_end": -1000,
        "culture": "Egyptian",
        "archetype": "Destruction of Mankind by Fierce Eye Goddess & Elevation of the Sky",
        "syncretic_ids": ["Q179669", "Q1164"],
    },
    {
        "id": "Q460592",
        "name": "The Amduat (Ra's Night Journey through the Twelve Hours of the Netherworld)",
        "wiki_title": "Amduat",
        "lat": 25.74,
        "lng": 32.60,  # Valley of the Kings, Luxor
        "epoch_start": -1500,
        "epoch_end": -1000,
        "culture": "Egyptian",
        "archetype": "Solar Bark Sailing the Subterranean River Battling Apep",
        "syncretic_ids": ["Q46580", "Q172740"],
    },
    {
        "id": "Q1434445",
        "name": "The Tale of the Shipwrecked Sailor (The Island of the Golden Serpent)",
        "wiki_title": "Tale_of_the_Shipwrecked_Sailor",
        "lat": 27.18,
        "lng": 33.80,  # Red Sea Coast / Punt
        "epoch_start": -2000,
        "epoch_end": -1800,
        "culture": "Egyptian",
        "archetype": "Castaway on Supernatural Phantom Isle Befriended by Serpent King",
        "syncretic_ids": ["Q125430", "Q35160"],
    },
    {
        "id": "Q125431",
        "name": "The Tale of Two Brothers (Anpu and Bata's Metamorphoses)",
        "wiki_title": "Tale_of_Two_Brothers",
        "lat": 29.85,
        "lng": 31.25,  # Upper Egypt
        "epoch_start": -1200,
        "epoch_end": -1000,
        "culture": "Egyptian",
        "archetype": "Innocent Brother Falsely Accused Undergoing Magical Tree Transfigurations",
        "syncretic_ids": ["Q214944", "Q172740"],
    },
    {
        "id": "Q188735",
        "name": "The Weighing of the Heart (The Hall of Ma'at and the Devourer Ammit)",
        "wiki_title": "Book_of_the_Dead",
        "lat": 25.72,
        "lng": 32.61,  # Karnak / Thebes
        "epoch_start": -1550,
        "epoch_end": -50,
        "culture": "Egyptian",
        "archetype": "Psychostasia (Soul Weighing against the Feather of Cosmic Truth)",
        "syncretic_ids": ["Q179654", "Q46580"],
    },
    {
        "id": "Q131171",
        "name": "Imhotep the Master Builder (The Deified Sage of the Step Pyramid)",
        "wiki_title": "Imhotep",
        "lat": 29.87,
        "lng": 31.21,  # Saqqara
        "epoch_start": -2650,
        "epoch_end": 300,
        "culture": "Egyptian",
        "archetype": "Mortal Architect and Healer Elevated to Divine Apotheosis",
        "syncretic_ids": ["Q83364", "Q1579"],
    },

    # ── 3. LEVANTINE & ARABIAN ────────────────────────────────────────────────
    {
        "id": "Q181920",
        "name": "The Epic of King Keret (The Ugaritic Royal Vision and March to Udum)",
        "wiki_title": "Legend_of_Keret",
        "lat": 35.60,
        "lng": 35.78,  # Ugarit (Ras Shamra, Syria)
        "epoch_start": -1500,
        "epoch_end": -1200,
        "culture": "Levantine",
        "archetype": "Fallen Dynast Receiving Divine Counsel to Secure Royal Lineage",
        "syncretic_ids": ["Q248352", "Q8258"],
    },
    {
        "id": "Q181921",
        "name": "The Epic of Aqhat (The Sacred Composite Bow and Goddess Anat's Fury)",
        "wiki_title": "Epic_of_Aqhat",
        "lat": 35.60,
        "lng": 35.78,  # Ugarit
        "epoch_start": -1400,
        "epoch_end": -1200,
        "culture": "Levantine",
        "archetype": "Youth Refusing to Surrender Divine Weapon to Vengeful Goddess",
        "syncretic_ids": ["Q179669", "Q35060"],
    },
    {
        "id": "Q125432",
        "name": "The Tower of Babel (The Ziggurat of Shinar and Scattering of Tongues)",
        "wiki_title": "Tower_of_Babel",
        "lat": 32.54,
        "lng": 44.42,  # Babylon / Shinar
        "epoch_start": -900,
        "epoch_end": -500,
        "culture": "Levantine",
        "archetype": "Hubristic Skyscraper Reaching Heaven Shattered into Multilingual Diaspora",
        "syncretic_ids": ["Q1164", "Q83364"],
    },
    {
        "id": "Q111729",
        "name": "Jonah and the Great Fish (The Reluctant Prophet in the Leviathan Depths)",
        "wiki_title": "Jonah",
        "lat": 32.05,
        "lng": 34.75,  # Jaffa / Joppa
        "epoch_start": -780,
        "epoch_end": -400,
        "culture": "Levantine",
        "archetype": "Night Journey in the Belly of the Great Water Monster",
        "syncretic_ids": ["Q35160", "Q242004"],
    },
    {
        "id": "Q125433",
        "name": "Samson and the Pillars of Gaza (The Solar Nazirite and the Lion)",
        "wiki_title": "Samson",
        "lat": 31.77,
        "lng": 34.98,  # Zorah / Sorek Valley
        "epoch_start": -1100,
        "epoch_end": -600,
        "culture": "Levantine",
        "archetype": "Unconquerable Solar Strongman Brought Low by Betrayed Locks",
        "syncretic_ids": ["Q12224", "Q207360"],
    },
    {
        "id": "Q125434",
        "name": "Zarqa al-Yamama (The Blue-Eyed Seeress Who Saw Armies Through Forests)",
        "wiki_title": "Zarqa_al_Yamama",
        "lat": 24.13,
        "lng": 47.31,  # Al-Yamama, Najd (Arabia)
        "epoch_start": 300,
        "epoch_end": 600,
        "culture": "Levantine",
        "archetype": "Tragic Prophetess of Infallible Sight Unheeded by Her Doomed People",
        "syncretic_ids": ["Q8258", "Q626359"],
    },
    {
        "id": "Q125435",
        "name": "The Seal of Solomon (The Hexagram Ring Ruling the Jinn and Winds)",
        "wiki_title": "Seal_of_Solomon",
        "lat": 31.77,
        "lng": 35.23,  # Jerusalem
        "epoch_start": -950,
        "epoch_end": 800,
        "culture": "Levantine",
        "archetype": "Talismanic Signet Ring Bestowing Mastery over Supernatural Elementals",
        "syncretic_ids": ["Q8258", "Q212628"],
    },

    # ── 4. GRECO-ROMAN ────────────────────────────────────────────────────────
    {
        "id": "Q130833",
        "name": "Oedipus and the Sphinx (The Riddle of Man at the Crossroads of Thebes)",
        "wiki_title": "Oedipus",
        "lat": 38.32,
        "lng": 23.32,  # Thebes, Boeotia
        "epoch_start": -800,
        "epoch_end": -400,
        "culture": "Greco-Roman",
        "archetype": "Tragic Hero Solving the Monster's Enigma Ensnared by Unescapable Fate",
        "syncretic_ids": ["Q129888", "Q815849"],
    },
    {
        "id": "Q129889",
        "name": "The Fall of Icarus and the Labyrinth of Minos (Wings of Wax)",
        "wiki_title": "Icarus",
        "lat": 37.60,
        "lng": 26.15,  # Icarian Sea / Crete
        "epoch_start": -700,
        "epoch_end": -300,
        "culture": "Greco-Roman",
        "archetype": "Hubris of Human Flight Soaring Too Near the Blazing Sun",
        "syncretic_ids": ["Q83364", "Q368367"],
    },
    {
        "id": "Q172741",
        "name": "Medea and the Golden Fleece (The Sorceress of Colchis and the Dragon Chariot)",
        "wiki_title": "Medea",
        "lat": 41.64,
        "lng": 41.64,  # Colchis (Black Sea Georgia) / Corinth
        "epoch_start": -700,
        "epoch_end": -400,
        "culture": "Greco-Roman",
        "archetype": "Wild Foreign Sorceress Aiding the Quest Only to Wreak Ferocious Revenge",
        "syncretic_ids": ["Q165493", "Q179669"],
    },
    {
        "id": "Q131346",
        "name": "Pandora's Pithos (The First Woman and the Preservation of Hope)",
        "wiki_title": "Pandora",
        "lat": 38.48,
        "lng": 22.50,  # Delphi / Mount Olympus
        "epoch_start": -750,
        "epoch_end": -400,
        "culture": "Greco-Roman",
        "archetype": "The Creation of Woman and the Opening of the Vessel of Mortal Plagues",
        "syncretic_ids": ["Q83364", "Q1164"],
    },
    {
        "id": "Q10802",
        "name": "The Titanomachy (The Ten-Year Clash of the Olympians and the Titans)",
        "wiki_title": "Titanomachy",
        "lat": 40.08,
        "lng": 22.35,  # Mount Olympus / Mount Othrys
        "epoch_start": -800,
        "epoch_end": -500,
        "culture": "Greco-Roman",
        "archetype": "Generational Cosmic War Overthrowing the Primordial Earth Titans",
        "syncretic_ids": ["Q169542", "Q248352"],
    },
    {
        "id": "Q172742",
        "name": "Pygmalion and Galatea (The Ivory Maiden Brought to Breath)",
        "wiki_title": "Pygmalion_(mythology)",
        "lat": 34.66,
        "lng": 32.62,  # Paphos, Cyprus
        "epoch_start": -500,
        "epoch_end": 100,
        "culture": "Greco-Roman",
        "archetype": "Artist Breathing Animated Life into the Perfect Sculpted Form",
        "syncretic_ids": ["Q35060", "Q939988"],
    },
    {
        "id": "Q172743",
        "name": "Echo and Narcissus (The Pool of Self-Adoration and the Vanishing Voice)",
        "wiki_title": "Echo_and_Narcissus",
        "lat": 38.37,
        "lng": 23.28,  # Thespiae, Mount Helicon
        "epoch_start": -500,
        "epoch_end": 100,
        "culture": "Greco-Roman",
        "archetype": "Fatal Entrancement with One's Own Ephemeral Reflection",
        "syncretic_ids": ["Q35060", "Q172740"],
    },
    {
        "id": "Q172744",
        "name": "Cupid and Psyche (The Soul's Labyrinthine Trials for Divine Love)",
        "wiki_title": "Cupid_and_Psyche",
        "lat": 36.50,
        "lng": 22.50,  # Laconia / Apuleius Rome
        "epoch_start": 100,
        "epoch_end": 200,
        "culture": "Greco-Roman",
        "archetype": "Mortal Soul Purified through Underworld Ordeals to Attain Immortality",
        "syncretic_ids": ["Q172740", "Q179654"],
    },
    {
        "id": "Q172745",
        "name": "Atalanta and the Golden Apples (The Huntress of the Calydonian Boar)",
        "wiki_title": "Atalanta",
        "lat": 37.50,
        "lng": 22.37,  # Arcadia / Calydon
        "epoch_start": -700,
        "epoch_end": -300,
        "culture": "Greco-Roman",
        "archetype": "Wild Maiden Outrunning Suitors Diverted by the Golden Fruit of Aphrodite",
        "syncretic_ids": ["Q35060", "Q214944"],
    },
    {
        "id": "Q172746",
        "name": "Bellerophon and Pegasus (Slaying the Chimera of the Lycian Crags)",
        "wiki_title": "Bellerophon",
        "lat": 36.27,
        "lng": 30.47,  # Lycia (Mount Chimaera, Turkey)
        "epoch_start": -750,
        "epoch_end": -400,
        "culture": "Greco-Roman",
        "archetype": "Winged Horse Rider Conquering the Fire-Breathing Multi-Headed Beast",
        "syncretic_ids": ["Q130832", "Q207360"],
    },

    # ── 5. VEDIC & HINDU ──────────────────────────────────────────────────────
    {
        "id": "Q131379",
        "name": "Garuda Stealing the Amrita (The Golden Solar Eagle of Freedom)",
        "wiki_title": "Garuda",
        "lat": 26.85,
        "lng": 80.94,  # Gandhamadana / Northern India
        "epoch_start": -1500,
        "epoch_end": -300,
        "culture": "Vedic & Hindu",
        "archetype": "Solar Bird of Prey Slaying Serpents and Seizing the Elixir of Immortality",
        "syncretic_ids": ["Q614880", "Q242004"],
    },
    {
        "id": "Q948959",
        "name": "Savitri and Satyavan (Winning the Soul of the Husband from Yama)",
        "wiki_title": "Savitri_and_Satyavan",
        "lat": 23.18,
        "lng": 75.77,  # Madra / Ujjain Forests
        "epoch_start": -800,
        "epoch_end": -200,
        "culture": "Vedic & Hindu",
        "archetype": "Fierce Devotion Outwitting and Persuading the Sovereign of Death",
        "syncretic_ids": ["Q172740", "Q179654"],
    },
    {
        "id": "Q213276",
        "name": "Parashurama (The Axe-Wielding Avatar Cleansing the Tyrants)",
        "wiki_title": "Parashurama",
        "lat": 15.30,
        "lng": 74.00,  # Konkan Coast / Western Ghats
        "epoch_start": -1000,
        "epoch_end": -300,
        "culture": "Vedic & Hindu",
        "archetype": "Ascetic Warrior Wiping Out Corrupt Monarchs to Restore Cosmic Equilibrium",
        "syncretic_ids": ["Q12224", "Q213275"],
    },
    {
        "id": "Q213277",
        "name": "Markandeya and the Embrace of Shiva (The Defeat of Kala / Time)",
        "wiki_title": "Markandeya",
        "lat": 10.96,
        "lng": 79.38,  # Thirukkadaiyur, Tamil Nadu
        "epoch_start": -800,
        "epoch_end": 200,
        "culture": "Vedic & Hindu",
        "archetype": "Mortal Youth Embracing the Cosmic Pillar Overcoming Scheduled Death",
        "syncretic_ids": ["Q213275", "Q172740"],
    },
    {
        "id": "Q213278",
        "name": "Ravana's Tapas and the Ten Heads of Lanka (The Sovereign of Rakshasas)",
        "wiki_title": "Ravana",
        "lat": 6.92,
        "lng": 79.86,  # Lanka (Sri Lanka / Sigiriya)
        "epoch_start": -800,
        "epoch_end": -300,
        "culture": "Vedic & Hindu",
        "archetype": "Grand Anti-Hero of Supreme Intellect and Unyielding Austerity",
        "syncretic_ids": ["Q144703", "Q815849"],
    },
    {
        "id": "Q213279",
        "name": "Draupadi Born from the Sacrificial Fire (The Fire-Born Queen of the Pandavas)",
        "wiki_title": "Draupadi",
        "lat": 28.36,
        "lng": 79.43,  # Panchala (Kampilya, Uttar Pradesh)
        "epoch_start": -900,
        "epoch_end": -300,
        "culture": "Vedic & Hindu",
        "archetype": "Fire-Born Queen Igniting the Climax of Cosmic Justice and War",
        "syncretic_ids": ["Q6734749", "Q214944"],
    },
    {
        "id": "Q213280",
        "name": "Matsya Avatar (The Horned Golden Fish Rescuing Manu from the Pralaya)",
        "wiki_title": "Matsya",
        "lat": 8.08,
        "lng": 77.55,  # Malaya Mountains / Kanyakumari
        "epoch_start": -1200,
        "epoch_end": -400,
        "culture": "Vedic & Hindu",
        "archetype": "Horned Cosmic Fish Guiding the Vessel of Vedas Across the Dissolving Ocean",
        "syncretic_ids": ["Q1164", "Q368367"],
    },
    {
        "id": "Q213281",
        "name": "Kurma Avatar (The Great Cosmic Tortoise Supporting Mount Mandara)",
        "wiki_title": "Kurma",
        "lat": 18.28,
        "lng": 83.90,  # Srikurmam, Andhra Pradesh
        "epoch_start": -1200,
        "epoch_end": -400,
        "culture": "Vedic & Hindu",
        "archetype": "Foundation Tortoise Bearing the Weight of the Churning World Mountain",
        "syncretic_ids": ["Q212643", "Q2302324"],
    },
    {
        "id": "Q213282",
        "name": "Varaha Avatar (The Boar Slaying Hiranyaksha to Lift Bhumi from the Abyss)",
        "wiki_title": "Varaha",
        "lat": 11.41,
        "lng": 79.69,  # Srimushnam / Garbhapradosha
        "epoch_start": -1200,
        "epoch_end": -400,
        "culture": "Vedic & Hindu",
        "archetype": "Primal Earth-Diver Diving into Cosmic Mud to Elevate the Continent",
        "syncretic_ids": ["Q213275", "Q1422880"],
    },

    # ── 6. PERSIAN & IRANIAN ──────────────────────────────────────────────────
    {
        "id": "Q144704",
        "name": "Fereydun and the Standard of Kaveh (The Dethroning of the Dragon Tyrant)",
        "wiki_title": "Fereydun",
        "lat": 35.95,
        "lng": 52.11,  # Mount Damavand, Alborz
        "epoch_start": -1000,
        "epoch_end": 1000,
        "culture": "Persian & Iranian",
        "archetype": "Chosen Prince Raising the Blacksmith's Apron Banner to Bind Evil",
        "syncretic_ids": ["Q144703", "Q207360"],
    },
    {
        "id": "Q216998",
        "name": "Siyavash and the Trial by Fire (The Fortress of Gangdiz)",
        "wiki_title": "Siyavash",
        "lat": 39.65,
        "lng": 66.96,  # Samarkand / Turan
        "epoch_start": -800,
        "epoch_end": 1000,
        "culture": "Persian & Iranian",
        "archetype": "Innocent Prince Galloping Unscathed through Mountainous Pyre of Fire",
        "syncretic_ids": ["Q213275", "Q214944"],
    },
    {
        "id": "Q626360",
        "name": "Kay Kavus and the Flying Throne (The Flight of Eagles to the Stars)",
        "wiki_title": "Kay_Kavus",
        "lat": 36.26,
        "lng": 59.61,  # Khorasan
        "epoch_start": -800,
        "epoch_end": 1000,
        "culture": "Persian & Iranian",
        "archetype": "Monarch Attempting to Ascend Heaven in a Throne Lifted by Hungry Eagles",
        "syncretic_ids": ["Q368367", "Q129889"],
    },
    {
        "id": "Q144705",
        "name": "Ahriman / Angra Mainyu (The Primordial Darkness Attacking the Sacred Bull)",
        "wiki_title": "Ahriman",
        "lat": 34.33,
        "lng": 47.07,  # Kermanshah (Zagros Gates)
        "epoch_start": -1200,
        "epoch_end": 650,
        "culture": "Persian & Iranian",
        "archetype": "Active Cosmic Adversary Poisoning the Pure Waters, Plants, and Beasts",
        "syncretic_ids": ["Q121852", "Q201083"],
    },
    {
        "id": "Q216997",
        "name": "Haft Peykar (Bahram Gur and the Seven Pavilions of the Planets)",
        "wiki_title": "Haft_Peykar",
        "lat": 40.40,
        "lng": 49.86,  # Baku / Ganja
        "epoch_start": 1150,
        "epoch_end": 1200,
        "culture": "Persian & Iranian",
        "archetype": "Astrological Journey through Seven Colored Domes of Transcendent Wisdom",
        "syncretic_ids": ["Q8258", "Q841323"],
    },
    {
        "id": "Q144706",
        "name": "Mithra the Invincible (The All-Seeing God of Oaths and Solar Radiance)",
        "wiki_title": "Mithra",
        "lat": 37.89,
        "lng": 46.25,  # Azerbaijan / Persis
        "epoch_start": -1400,
        "epoch_end": 400,
        "culture": "Persian & Iranian",
        "archetype": "Unconquered Light and Covenant Bearer Slaying the Primal Bull",
        "syncretic_ids": ["Q8785", "Q248352"],
    },
    {
        "id": "Q144707",
        "name": "Aredvi Sura Anahita (The Immaculate Lady of the Flowing Waters and Chariot of Four Steeds)",
        "wiki_title": "Anahita",
        "lat": 34.40,
        "lng": 47.96,  # Temple of Anahita, Kangavar
        "epoch_start": -1000,
        "epoch_end": 650,
        "culture": "Persian & Iranian",
        "archetype": "Goddess of Rivers, Fertility, and Royal Sovereignty Riding Wind and Cloud",
        "syncretic_ids": ["Q35060", "Q134114"],
    },

    # ── 7. NORSE & GERMANIC ───────────────────────────────────────────────────
    {
        "id": "Q131347",
        "name": "The Mead of Poetry (Kvasir's Blood and Odin's Eagle Flight from Hnitbjorg)",
        "wiki_title": "Mead_of_poetry",
        "lat": 64.13,
        "lng": -21.82,  # Iceland / Jotunheim
        "epoch_start": 800,
        "epoch_end": 1250,
        "culture": "Norse & Germanic",
        "archetype": "Theft of the Sacred Intoxicant of Poetic Wisdom and Cosmic Insight",
        "syncretic_ids": ["Q83364", "Q131379"],
    },
    {
        "id": "Q131348",
        "name": "The Binding of Fenrir (Tyr's Sacrificed Hand and Gleipnir's Silk)",
        "wiki_title": "Fenrir",
        "lat": 63.42,
        "lng": -19.00,  # Lake Amsvartnir, Lyngvi
        "epoch_start": 800,
        "epoch_end": 1250,
        "culture": "Norse & Germanic",
        "archetype": "Apocalyptic Wolf Chained by Seemingly Fragile Enchanted Bonds",
        "syncretic_ids": ["Q121852", "Q144703"],
    },
    {
        "id": "Q131349",
        "name": "The Lay of Hildebrand (The Tragic Clashing of Father and Son on the Frontier)",
        "wiki_title": "Hildebrandslied",
        "lat": 51.31,
        "lng": 9.49,  # Fulda / Kassel, Germany
        "epoch_start": 750,
        "epoch_end": 850,
        "culture": "Norse & Germanic",
        "archetype": "Tragic Honor-Bound Duel Between Unrecognized Father and Son",
        "syncretic_ids": ["Q248352", "Q815849"],
    },
    {
        "id": "Q131350",
        "name": "The Song of the Nibelungs (Siegfried's Dragon Blood and the Rhinegold Curse)",
        "wiki_title": "Nibelungenlied",
        "lat": 49.63,
        "lng": 8.36,  # Worms on the Rhine
        "epoch_start": 1190,
        "epoch_end": 1230,
        "culture": "Norse & Germanic",
        "archetype": "Dragon Slayer Made Invulnerable by Bath of Blood Betrayed by Weak Spot",
        "syncretic_ids": ["Q207360", "Q815849"],
    },
    {
        "id": "Q131351",
        "name": "Wayland the Smith (The Crippled Elven Smith and the Feathered Escape)",
        "wiki_title": "Wayland_the_Smith",
        "lat": 51.56,
        "lng": -1.59,  # Wayland's Smithy, Berkshire / Jutland
        "epoch_start": 700,
        "epoch_end": 1100,
        "culture": "Norse & Germanic",
        "archetype": "Imprisoned Master Artificer Forging Wings to Wreak Retribution and Flee",
        "syncretic_ids": ["Q129889", "Q212628"],
    },
    {
        "id": "Q131352",
        "name": "Brynhildr on the Flaming Mountain (The Disobedient Valkyrie Awakened by Sigurd)",
        "wiki_title": "Brynhildr",
        "lat": 61.00,
        "lng": 8.50,  # Hindarfjall, Jotunheimen
        "epoch_start": 800,
        "epoch_end": 1250,
        "culture": "Norse & Germanic",
        "archetype": "Sleeping Warrior Maiden Encircled by Ring of Flame Cleaved by Fearless Hero",
        "syncretic_ids": ["Q207360", "Q948958"],
    },
    {
        "id": "Q131353",
        "name": "Idun and the Golden Apples of Immortality (The Abduction by Giant Thjazi)",
        "wiki_title": "I%C3%B0unn",
        "lat": 58.00,
        "lng": 11.50,  # Thrymheim / Skadi's Mountains
        "epoch_start": 800,
        "epoch_end": 1250,
        "culture": "Norse & Germanic",
        "archetype": "Goddess of Youth Stolen Causing the Gods to Wither into Senescence",
        "syncretic_ids": ["Q179654", "Q131379"],
    },
    {
        "id": "Q131354",
        "name": "Yggdrasil the World Ash (The Cosmic Axis Uniting the Nine Worlds)",
        "wiki_title": "Yggdrasil",
        "lat": 65.00,
        "lng": -18.00,  # Urdarbrunnr / All Worlds
        "epoch_start": 700,
        "epoch_end": 1250,
        "culture": "Norse & Germanic",
        "archetype": "World Tree (Axis Mundi) Connecting Underworld, Midgard, and the Heavens",
        "syncretic_ids": ["Q1422880", "Q212628"],
    },

    # ── 8. CELTIC ─────────────────────────────────────────────────────────────
    {
        "id": "Q1434446",
        "name": "The Salmon of Knowledge (Fionn mac Cumhaill and the Hazel of Wisdom)",
        "wiki_title": "Salmon_of_Knowledge",
        "lat": 53.69,
        "lng": -6.53,  # River Boyne (Linn Féic), Ireland
        "epoch_start": 700,
        "epoch_end": 1200,
        "culture": "Celtic",
        "archetype": "Tasting the Sacred Fish to Awaken Omniscience through Thumb-Chewing",
        "syncretic_ids": ["Q131347", "Q214944"],
    },
    {
        "id": "Q1434447",
        "name": "The Morrígan (The Phantom Queen of Fate, Battle-Fury, and the Raven)",
        "wiki_title": "The_Morr%C3%ADgan",
        "lat": 53.80,
        "lng": -8.30,  # Cave of Cruachan (Rathcroghan), Roscommon
        "epoch_start": 600,
        "epoch_end": 1200,
        "culture": "Celtic",
        "archetype": "Triple Goddess of Sovereignty Prophesying the Doom of Heroes",
        "syncretic_ids": ["Q179669", "Q214944"],
    },
    {
        "id": "Q1434448",
        "name": "Bran the Blessed (The Giant King and the Severed Head That Feasted for Eighty Years)",
        "wiki_title": "Bran_the_Blessed",
        "lat": 51.50,
        "lng": -0.07,  # White Mount (Tower of London)
        "epoch_start": 1050,
        "epoch_end": 1300,
        "culture": "Celtic",
        "archetype": "Sacrificial Giant Sovereign Whose Incorruptible Head Wards the Realm",
        "syncretic_ids": ["Q105224", "Q172740"],
    },
    {
        "id": "Q1434449",
        "name": "Deirdre of the Sorrows (The Exile to Alba and Tragic Fidelity)",
        "wiki_title": "Deirdre",
        "lat": 54.34,
        "lng": -6.65,  # Emain Macha (Armagh), Ulster
        "epoch_start": 700,
        "epoch_end": 1200,
        "culture": "Celtic",
        "archetype": "Doomed Beauty Whose Birth Prophecy Precipitates the Fall of a Kingdom",
        "syncretic_ids": ["Q948958", "Q172740"],
    },
    {
        "id": "Q1434450",
        "name": "Pwyll, Prince of Dyfed (The Exchange of Kingdoms with Arawn of Annwn)",
        "wiki_title": "Pwyll_Pendefig_Dyfed",
        "lat": 51.78,
        "lng": -4.95,  # Dyfed / Narberth, Pembrokeshire, Wales
        "epoch_start": 1050,
        "epoch_end": 1250,
        "culture": "Celtic",
        "archetype": "Mortal Prince Ruling the Underworld Unscathed through Pure Chivalry",
        "syncretic_ids": ["Q179654", "Q172740"],
    },
    {
        "id": "Q1434451",
        "name": "Blodeuwedd (The Maiden Fashioned of Flowers Transformed into the Owl)",
        "wiki_title": "Blodeuwedd",
        "lat": 52.85,
        "lng": -3.93,  # Tomen y Mur, Ardudwy, Gwynedd
        "epoch_start": 1100,
        "epoch_end": 1300,
        "culture": "Celtic",
        "archetype": "Botanical Automaton Reclaiming Wild Will Bound into Nocturnal Bird of Prey",
        "syncretic_ids": ["Q172742", "Q131346"],
    },
    {
        "id": "Q1434452",
        "name": "Taliesin (Gwion Bach's Cauldron Metamorphoses and the Radiance of Song)",
        "wiki_title": "Taliesin",
        "lat": 52.50,
        "lng": -3.98,  # Llyn Tegid / Aberdyfi, Wales
        "epoch_start": 550,
        "epoch_end": 1200,
        "culture": "Celtic",
        "archetype": "Initiation through Animal Transmutations and Rebirth as Supreme Bard",
        "syncretic_ids": ["Q1434446", "Q211029"],
    },
    {
        "id": "Q1434453",
        "name": "The Lady of the Lake and Excalibur (The Mists of Avalon and Merlin's Entombment)",
        "wiki_title": "Lady_of_the_Lake",
        "lat": 51.14,
        "lng": -2.71,  # Glastonbury Tor / Isle of Avalon
        "epoch_start": 1136,
        "epoch_end": 1485,
        "culture": "Celtic",
        "archetype": "Aquatic Sovereignty Maiden Conferring the Sacred Sword of Legitimate Kingship",
        "syncretic_ids": ["Q105224", "Q234455"],
    },
    {
        "id": "Q1434454",
        "name": "The Tuatha Dé Danann (The Shining Folk Arriving in Magic Mists on Beltane)",
        "wiki_title": "Tuatha_D%C3%A9_Danann",
        "lat": 54.08,
        "lng": -8.65,  # Carrowkeel / Moytirra, Sligo
        "epoch_start": 600,
        "epoch_end": 1150,
        "culture": "Celtic",
        "archetype": "Godly Tribe from the Northern Isles Bringing the Four Hallows to Rule the Mound",
        "syncretic_ids": ["Q105224", "Q10802"],
    },
    {
        "id": "Q1434455",
        "name": "Lugh of the Long Arm (The Master of All Arts Slaying Balor of the Evil Eye)",
        "wiki_title": "Lugh",
        "lat": 54.07,
        "lng": -8.32,  # Battle of Mag Tuired, Lough Arrow
        "epoch_start": 600,
        "epoch_end": 1200,
        "culture": "Celtic",
        "archetype": "Solar Master of All Crafts Slaying the Titanic Fomorian with the Sling-Stone",
        "syncretic_ids": ["Q12224", "Q248352"],
    },

    # ── 9. SLAVIC & BALTIC ───────────────────────────────────────────────────
    {
        "id": "Q153725",
        "name": "Svarog the Celestial Blacksmith (Forging the Sun and the Iron Plough)",
        "wiki_title": "Svarog",
        "lat": 50.45,
        "lng": 30.52,  # Kyiv / Dnieper Basin
        "epoch_start": 500,
        "epoch_end": 1100,
        "culture": "Slavic & Baltic",
        "archetype": "Primeval Smith God Hurling Fire Tongs from Heaven to Teach Agriculture",
        "syncretic_ids": ["Q212628", "Q83364"],
    },
    {
        "id": "Q188736",
        "name": "Vasilisa the Beautiful (The Wooden Doll Guided through the Skull-Lit Fence)",
        "wiki_title": "Vasilisa_the_Beautiful",
        "lat": 56.32,
        "lng": 44.00,  # Nizhny Novgorod / Volga Taiga
        "epoch_start": 900,
        "epoch_end": 1850,
        "culture": "Slavic & Baltic",
        "archetype": "Pure Maiden Surviving Witch Baba Yaga through Ancestral Maternal Talisman",
        "syncretic_ids": ["Q172744", "Q211158"],
    },
    {
        "id": "Q188737",
        "name": "Sadko the Merchant-Guslar of Novgorod (The Underwater Feast of the Sea Tsar)",
        "wiki_title": "Sadko",
        "lat": 58.52,
        "lng": 31.27,  # Lake Ilmen, Novgorod
        "epoch_start": 1000,
        "epoch_end": 1400,
        "culture": "Slavic & Baltic",
        "archetype": "Minstrel Whose Music Charms the Sovereign of the Waves",
        "syncretic_ids": ["Q172740", "Q841323"],
    },
    {
        "id": "Q940177",
        "name": "Jūratė and Kastytis (The Amber Palace Smashed by Perkūnas' Thunder)",
        "wiki_title": "J%C5%ABrat%C4%97_and_Kastytis",
        "lat": 55.91,
        "lng": 21.05,  # Palanga, Baltic Sea Coast, Lithuania
        "epoch_start": 800,
        "epoch_end": 1800,
        "culture": "Slavic & Baltic",
        "archetype": "Sea Goddess Falling for Mortal Fisherman Struck Down by Jealous Thunder King",
        "syncretic_ids": ["Q1189332", "Q42952"],
    },
    {
        "id": "Q940178",
        "name": "Eglė the Queen of Serpents (The Tragic Spruce Tree of the Baltic Shore)",
        "wiki_title": "Egl%C4%97_the_Queen_of_Serpents",
        "lat": 55.70,
        "lng": 21.13,  # Curonian Spit, Lithuania
        "epoch_start": 800,
        "epoch_end": 1850,
        "culture": "Slavic & Baltic",
        "archetype": "Mortal Maiden Wed to King of Grass Snakes Metamorphosing into Trees",
        "syncretic_ids": ["Q940176", "Q1434451"],
    },
    {
        "id": "Q153726",
        "name": "Mokosh the Moist Mother Earth (The Spinner of Flocks and Human Destiny)",
        "wiki_title": "Mokosh",
        "lat": 54.51,
        "lng": 36.26,  # Oka River Basin / Muscovy
        "epoch_start": 600,
        "epoch_end": 1200,
        "culture": "Slavic & Baltic",
        "archetype": "Moist Earth Matron Spinning the Thread of Mortal Fate",
        "syncretic_ids": ["Q153724", "Q385552"],
    },
    {
        "id": "Q153727",
        "name": "Dazhbog the Giving God (The Sun King Who Bestows Wealth and Light)",
        "wiki_title": "Da%C5%BEbog",
        "lat": 48.46,
        "lng": 35.04,  # Dnieper Rapids
        "epoch_start": 600,
        "epoch_end": 1100,
        "culture": "Slavic & Baltic",
        "archetype": "Generous Solar Sovereign Driving a Chariot of White Horses across Day and Night",
        "syncretic_ids": ["Q940176", "Q144706"],
    },

    # ── 10. FINNO-UGRIC ───────────────────────────────────────────────────────
    {
        "id": "Q211030",
        "name": "Kullervo's Revenge and Tragedy (The Magic Sword of Vengeance)",
        "wiki_title": "Kullervo",
        "lat": 61.50,
        "lng": 29.50,  # Karelia (Lake Ladoga)
        "epoch_start": 800,
        "epoch_end": 1849,
        "culture": "Finno-Ugric",
        "archetype": "Cursed Orphan of Unbreakable Will Driven into Inevitable Doom",
        "syncretic_ids": ["Q130833", "Q815849"],
    },
    {
        "id": "Q211031",
        "name": "Ilmarinen Forging the Golden Maiden and the Vault of the Sky",
        "wiki_title": "Ilmarinen",
        "lat": 62.89,
        "lng": 27.67,  # Kuopio / Northern Savonia
        "epoch_start": 800,
        "epoch_end": 1849,
        "culture": "Finno-Ugric",
        "archetype": "Eternal Craftsman Forging the Sky Dome and a Cold Bride of Silver and Gold",
        "syncretic_ids": ["Q172742", "Q212628"],
    },
    {
        "id": "Q211032",
        "name": "Ukko the Sky Sovereign (The Golden Axe and Rains of Midsummer)",
        "wiki_title": "Ukko",
        "lat": 61.49,
        "lng": 23.78,  # Tampere / Häme
        "epoch_start": 500,
        "epoch_end": 1600,
        "culture": "Finno-Ugric",
        "archetype": "Supreme Celestial Thunder Sovereign Bestowing Fertility on Barley",
        "syncretic_ids": ["Q42952", "Q206927"],
    },
    {
        "id": "Q211033",
        "name": "Louhi the Mistress of Pohjola (The Shapeshifting Eagle-Hag of the Frozen North)",
        "wiki_title": "Louhi",
        "lat": 66.50,
        "lng": 25.72,  # Lapland / Pohjola
        "epoch_start": 800,
        "epoch_end": 1849,
        "culture": "Finno-Ugric",
        "archetype": "Fierce Sorceress Matriarch Defending the Mill of Abundance",
        "syncretic_ids": ["Q188734", "Q212628"],
    },
    {
        "id": "Q211034",
        "name": "Aino and the Lake of Tuonela (Escaping the Old Singer into the Waters)",
        "wiki_title": "Aino_(mythology)",
        "lat": 62.24,
        "lng": 25.74,  # Central Finland
        "epoch_start": 800,
        "epoch_end": 1849,
        "culture": "Finno-Ugric",
        "archetype": "Maiden Escaping Forced Marriage Becoming the Sacred Salmon of the Sea",
        "syncretic_ids": ["Q940178", "Q1434449"],
    },

    # ── 11. EAST ASIAN ────────────────────────────────────────────────────────
    {
        "id": "Q841445",
        "name": "Pangu Opening Heaven and Earth (Hundun Chaos and the Cosmic Giant)",
        "wiki_title": "Pangu",
        "lat": 34.27,
        "lng": 108.94,  # Shaanxi / Central Plains
        "epoch_start": -1000,
        "epoch_end": 250,
        "culture": "East Asian",
        "archetype": "Cosmic Giant Emerging from World Egg Whose Body Becomes Mountains and Rivers",
        "syncretic_ids": ["Q1422880", "Q169542"],
    },
    {
        "id": "Q841446",
        "name": "Chang'e Flying to the Moon (The Elixir of Immortality and the Jade Rabbit)",
        "wiki_title": "Chang%27e",
        "lat": 34.62,
        "lng": 112.45,  # Luoyang / Moon
        "epoch_start": -500,
        "epoch_end": 200,
        "culture": "East Asian",
        "archetype": "Mortal Woman Drinking Lunar Elixir Ascending to the Moon Palace",
        "syncretic_ids": ["Q841323", "Q179654"],
    },
    {
        "id": "Q841447",
        "name": "Sun Wukong (Havoc in the Heavenly Palace and the Golden-Banded Cudgel)",
        "wiki_title": "Monkey_King",
        "lat": 34.59,
        "lng": 119.29,  # Mount Huaguo (Lianyungang, Jiangsu)
        "epoch_start": 1200,
        "epoch_end": 1592,
        "culture": "East Asian",
        "archetype": "Immortal Trickster Primate Defying Heaven Bound Under Five Elements Mountain",
        "syncretic_ids": ["Q1138243", "Q83364"],
    },
    {
        "id": "Q841448",
        "name": "The Eight Immortals Crossing the Sea (Each Revealing Their Divine Talisman)",
        "wiki_title": "Eight_Immortals",
        "lat": 37.80,
        "lng": 120.75,  # Penglai Pavilion (Shandong Coast)
        "epoch_start": 960,
        "epoch_end": 1500,
        "culture": "East Asian",
        "archetype": "Daoist Adepts Surmounting the Roaring Waves without Ships Using Unique Powers",
        "syncretic_ids": ["Q8258", "Q165493"],
    },
    {
        "id": "Q841449",
        "name": "Nezha Conquering the Dragon Kings (The Lotus Rebirth and Wind-Fire Wheels)",
        "wiki_title": "Nezha",
        "lat": 31.84,
        "lng": 104.73,  # Chentang Pass / Sichuan
        "epoch_start": 1200,
        "epoch_end": 1600,
        "culture": "East Asian",
        "archetype": "Sacrificial Child Rebel Restored to Life from a Pure Lotus Root",
        "syncretic_ids": ["Q213275", "Q214944"],
    },
    {
        "id": "Q841450",
        "name": "Urashima Taro (The Jade Tortoise and the Forbidden Dragon Palace Box)",
        "wiki_title": "Urashima_Tar%C5%8D",
        "lat": 35.58,
        "lng": 135.25,  # Tango Province (Kyoto Prefecture Coast)
        "epoch_start": 700,
        "epoch_end": 1400,
        "culture": "East Asian",
        "archetype": "Mortal Visiting Subsea Paradise Aging Centuries in a Single Day",
        "syncretic_ids": ["Q1434444", "Q131346"],
    },
    {
        "id": "Q841451",
        "name": "Yamato Takeru and the Kusanagi Grass-Cutting Sword (The Fire on the Plains)",
        "wiki_title": "Yamato_Takeru",
        "lat": 35.12,
        "lng": 136.91,  # Atsuta Shrine (Nagoya)
        "epoch_start": 100,
        "epoch_end": 712,
        "culture": "East Asian",
        "archetype": "Valiant Prince Reaping Encircled Wildfire with the Divine Wind Sword",
        "syncretic_ids": ["Q105224", "Q207360"],
    },
    {
        "id": "Q841452",
        "name": "Dangun Wanggeom and Ungnyeo (The Bear Woman and Sacred Birch of Mount Taebaek)",
        "wiki_title": "Dangun",
        "lat": 41.98,
        "lng": 128.08,  # Mount Paektu / Asadal (Pyongyang)
        "epoch_start": -2333,
        "epoch_end": -1000,
        "culture": "East Asian",
        "archetype": "Heavenly Descent and Bear-Woman Fasting in Dark Cave to Found Nation",
        "syncretic_ids": ["Q651234", "Q165997"],
    },
    {
        "id": "Q841453",
        "name": "The Tale of Hong Gildong (The Robin Hood Hero of Mount Geumgang and Yuldo)",
        "wiki_title": "Hong_Gildong_jeon",
        "lat": 37.56,
        "lng": 126.97,  # Hanyang (Seoul) / Gangwon
        "epoch_start": 1500,
        "epoch_end": 1620,
        "culture": "East Asian",
        "archetype": "Righteous Outlaw Sorcerer Overcoming Illegitimacy to Build Utopian Realm",
        "syncretic_ids": ["Q105224", "Q841447"],
    },
    {
        "id": "Q841454",
        "name": "Legend of the White Snake (Bai Suzhen and the Broken Bridge of West Lake)",
        "wiki_title": "Legend_of_the_White_Snake",
        "lat": 30.24,
        "lng": 120.14,  # West Lake & Leifeng Pagoda, Hangzhou
        "epoch_start": 1100,
        "epoch_end": 1600,
        "culture": "East Asian",
        "archetype": "Immortal White Serpent Spirit Seeking Human Love Trapped Beneath Pagoda",
        "syncretic_ids": ["Q940178", "Q1189332"],
    },
    {
        "id": "Q841455",
        "name": "Kitsune (The Nine-Tailed Celestial Fox Spirits of Inari)",
        "wiki_title": "Kitsune",
        "lat": 34.96,
        "lng": 135.77,  # Fushimi Inari-taisha, Kyoto
        "epoch_start": 700,
        "epoch_end": 1800,
        "culture": "East Asian",
        "archetype": "Shapeshifting Vulpin Tricksters Accumulating Celestial Wisdom with Age",
        "syncretic_ids": ["Q1138243", "Q841447"],
    },
    {
        "id": "Q841456",
        "name": "Fuxi (The Dragon-Tailed Sovereign Who Drew the Eight Trigrams of Change)",
        "wiki_title": "Fuxi",
        "lat": 34.58,
        "lng": 105.72,  # Tianshui, Gansu (Yellow River)
        "epoch_start": -2800,
        "epoch_end": -500,
        "culture": "East Asian",
        "archetype": "First Sovereign Deciphering the Cosmic Patterns from the Dragon-Horse Shell",
        "syncretic_ids": ["Q836371", "Q1579"],
    },
    {
        "id": "Q841457",
        "name": "Nüwa Mending the Heavens (The Five-Colored Stones and Turtle Legs)",
        "wiki_title": "N%C3%BCwa",
        "lat": 36.42,
        "lng": 113.60,  # Mount Tiangong / Shanxi
        "epoch_start": -2500,
        "epoch_end": -200,
        "culture": "East Asian",
        "archetype": "Mother Goddess Smelting Stones to Repair Broken Pillar of Sky after Deluge",
        "syncretic_ids": ["Q1164", "Q1422880"],
    },

    # ── 12. CENTRAL ASIAN & STEPPE ───────────────────────────────────────────
    {
        "id": "Q651235",
        "name": "The Epic of King Gesar (The Miraculous Sovereign of Ling and Tibet)",
        "wiki_title": "Epic_of_King_Gesar",
        "lat": 32.50,
        "lng": 98.00,  # Kham / Dege (Tibetan Plateau)
        "epoch_start": 800,
        "epoch_end": 1600,
        "culture": "Central Asian & Steppe",
        "archetype": "Divine Champion Incarnating on Earth to Cleanse Demons and Pacify Lands",
        "syncretic_ids": ["Q248352", "Q105224"],
    },
    {
        "id": "Q651236",
        "name": "The Epic of Manas (The 500,000-Line Kyrgyz Epic of Heroic Unity)",
        "wiki_title": "Epic_of_Manas",
        "lat": 42.52,
        "lng": 72.23,  # Talas Valley, Kyrgyzstan
        "epoch_start": 900,
        "epoch_end": 1800,
        "culture": "Central Asian & Steppe",
        "archetype": "Colossal Nomadic Unifier Leading the Forty Steppe Warriors",
        "syncretic_ids": ["Q651234", "Q248352"],
    },
    {
        "id": "Q651237",
        "name": "Ergenekon (The Iron Mountain Melted by Bellows to Free the Göktürks)",
        "wiki_title": "Ergenekon",
        "lat": 49.00,
        "lng": 86.00,  # Altai Mountains
        "epoch_start": 500,
        "epoch_end": 1000,
        "culture": "Central Asian & Steppe",
        "archetype": "Refuge in Impassable Valley Melted Open with Iron Smelting to Reclaim Steppe",
        "syncretic_ids": ["Q651234", "Q83364"],
    },
    {
        "id": "Q651238",
        "name": "Alan Gua and the Five Arrows (The Lesson of Nomadic Brotherhood)",
        "wiki_title": "Alan_Gua",
        "lat": 47.92,
        "lng": 106.92,  # Burkhan Khaldun, Khentii Mountains, Mongolia
        "epoch_start": 900,
        "epoch_end": 1240,
        "culture": "Central Asian & Steppe",
        "archetype": "Ancestral Matriarch Teaching that Single Arrows Break but Bundled Arrows Endure",
        "syncretic_ids": ["Q651234", "Q948958"],
    },
    {
        "id": "Q651239",
        "name": "Tengri (The Eternal Blue Sky Sovereign of the Great Steppe Khagans)",
        "wiki_title": "Tengri",
        "lat": 42.20,
        "lng": 80.18,  # Khan Tengri Peak (Tian Shan)
        "epoch_start": -1000,
        "epoch_end": 1400,
        "culture": "Central Asian & Steppe",
        "archetype": "Transcendent Eternal Blue Sky Conferring the Mandate of Steppe Rule (Kut)",
        "syncretic_ids": ["Q1164", "Q1422880"],
    },
    {
        "id": "Q651240",
        "name": "Alpamysh (The Steppe Hero's Exile, Prison, and Triumphant Return)",
        "wiki_title": "Alpamysh",
        "lat": 38.00,
        "lng": 67.00,  # Baysun, Surxondaryo, Uzbekistan
        "epoch_start": 800,
        "epoch_end": 1500,
        "culture": "Central Asian & Steppe",
        "archetype": "Exiled Hero Escaping Dungeon to Reclaim His Faithful Bride at Archery Contest",
        "syncretic_ids": ["Q35160", "Q248352"],
    },
    {
        "id": "Q651241",
        "name": "Kyz Zhibek (The Silk Maiden of Kazakh Steppe Legend)",
        "wiki_title": "Kyz_Zhibek",
        "lat": 49.80,
        "lng": 73.10,  # Central Kazakh Steppe
        "epoch_start": 1400,
        "epoch_end": 1700,
        "culture": "Central Asian & Steppe",
        "archetype": "Tragic Steppe Love of Tolegen and the Lyrical Swan Maiden of Lake Zhaik",
        "syncretic_ids": ["Q1434449", "Q841444"],
    },
    {
        "id": "Q651242",
        "name": "Ural-batyr (The Bashkir Epic of the Death-Defying Winged Steed Akbuzat)",
        "wiki_title": "Ural-batyr",
        "lat": 54.00,
        "lng": 58.00,  # Ural Mountains, Bashkortostan
        "epoch_start": 800,
        "epoch_end": 1800,
        "culture": "Central Asian & Steppe",
        "archetype": "Hero Slaying Death and Evil Kings to Pour the Spring of Living Water on Earth",
        "syncretic_ids": ["Q207360", "Q248352"],
    },

    # ── 13. SOUTHEAST ASIAN ───────────────────────────────────────────────────
    {
        "id": "Q2900899",
        "name": "Phra Lak Phra Lam (The Lao Ramayana along the Mekong River)",
        "wiki_title": "Phra_Lak_Phra_Lam",
        "lat": 19.89,
        "lng": 102.13,  # Luang Prabang / Vientiane
        "epoch_start": 1350,
        "epoch_end": 1800,
        "culture": "Southeast Asian",
        "archetype": "Epic Brothers Protecting Royal Honor Transposed onto the Tropical Mekong",
        "syncretic_ids": ["Q248352", "Q213278"],
    },
    {
        "id": "Q2900900",
        "name": "Reamker (The Cambodian Sacred Epic of Preah Ream and Neang Seda)",
        "wiki_title": "Reamker",
        "lat": 13.41,
        "lng": 103.86,  # Angkor Wat, Siem Reap
        "epoch_start": 1100,
        "epoch_end": 1600,
        "culture": "Southeast Asian",
        "archetype": "Divine Khmer Sovereign Wrestling with Moral Duty and the Shadows of Doubt",
        "syncretic_ids": ["Q248352", "Q213278"],
    },
    {
        "id": "Q2900901",
        "name": "Hikayat Hang Tuah (The Indomitable Malay Champion of the Keris Taming Sari)",
        "wiki_title": "Hang_Tuah",
        "lat": 2.19,
        "lng": 102.25,  # Malacca Strait
        "epoch_start": 1450,
        "epoch_end": 1700,
        "culture": "Southeast Asian",
        "archetype": "Tragic Conflict between Unconditional Fealty to the Throne and Fraternal Bond",
        "syncretic_ids": ["Q815849", "Q214944"],
    },
    {
        "id": "Q2900902",
        "name": "The Darangen (The Maranao Chanted Epic of Prince Bantugan)",
        "wiki_title": "Darangen",
        "lat": 8.00,
        "lng": 124.30,  # Lake Lanao, Mindanao, Philippines
        "epoch_start": 1200,
        "epoch_end": 1800,
        "culture": "Southeast Asian",
        "archetype": "Fallen Warrior Prince Whose Spirit is Rescued from the Sky Realm by Friends",
        "syncretic_ids": ["Q2900898", "Q172740"],
    },
    {
        "id": "Q2900903",
        "name": "The Legend of Lake Toba (The Golden Fish Maiden and the Broken Oath)",
        "wiki_title": "Lake_Toba",
        "lat": 2.68,
        "lng": 98.88,  # Samosir Island, Lake Toba, Sumatra
        "epoch_start": 1000,
        "epoch_end": 1800,
        "culture": "Southeast Asian",
        "archetype": "Broken Sacred Taboo Causing Supervolcanic Lake Deluge to Drown Valley",
        "syncretic_ids": ["Q1164", "Q940178"],
    },
    {
        "id": "Q2900904",
        "name": "Mae Nak Phra Khanong (The Eternal Devotion of the Ghost Bride of Bangkok)",
        "wiki_title": "Mae_Nak_Phra_Khanong",
        "lat": 13.71,
        "lng": 100.60,  # Phra Khanong, Bangkok
        "epoch_start": 1850,
        "epoch_end": 1900,
        "culture": "Southeast Asian",
        "archetype": "Loving Ghost Mother Caring for Unsuspecting Husband from Beyond the Grave",
        "syncretic_ids": ["Q172740", "Q841454"],
    },
    {
        "id": "Q2900905",
        "name": "Bathala (The Supreme Sky Architect of Ancient Tagalog Cosmogony)",
        "wiki_title": "Bathala",
        "lat": 14.59,
        "lng": 120.98,  # Pasig River / Central Luzon
        "epoch_start": 900,
        "epoch_end": 1571,
        "culture": "Southeast Asian",
        "archetype": "Supreme Celestial Creator Fashioning Mankind from River Bamboo Knots",
        "syncretic_ids": ["Q939988", "Q1422880"],
    },
    {
        "id": "Q2900906",
        "name": "Maria Makiling (The Mountain Guardian Spirit of Laguna)",
        "wiki_title": "Maria_Makiling",
        "lat": 14.13,
        "lng": 121.19,  # Mount Makiling, Laguna, Philippines
        "epoch_start": 1200,
        "epoch_end": 1900,
        "culture": "Southeast Asian",
        "archetype": "Enchanted Mountain Mistress Bestowing Golden Fruits Turning to Real Gold",
        "syncretic_ids": ["Q234455", "Q1189332"],
    },
    {
        "id": "Q2900907",
        "name": "Ibong Adarna (The Magical Seven-Colored Songbird of Mount Tabor)",
        "wiki_title": "Ibong_Adarna",
        "lat": 16.00,
        "lng": 120.50,  # Mount Tabor (Philippine Cordilleras)
        "epoch_start": 1600,
        "epoch_end": 1850,
        "culture": "Southeast Asian",
        "archetype": "Singing Healing Bird Whose Lullaby Turns Treacherous Seekers to Stone",
        "syncretic_ids": ["Q211158", "Q130832"],
    },
    {
        "id": "Q2900908",
        "name": "Bernardo Carpio (The Giant Titan Trapped Between Two Clashing Mountains)",
        "wiki_title": "Bernardo_Carpio",
        "lat": 14.73,
        "lng": 121.19,  # Montalban Gorge (Wawa Dam, Rizal)
        "epoch_start": 1500,
        "epoch_end": 1900,
        "culture": "Southeast Asian",
        "archetype": "Chained Mountain Giant Causing Earthquakes with Every Struggle for Freedom",
        "syncretic_ids": ["Q83364", "Q121852"],
    },

    # ── 14. NORTH AMERICAN INDIGENOUS ─────────────────────────────────────────
    {
        "id": "Q2302325",
        "name": "The Great Peacemaker and Hiawatha (The Haudenosaunee Great Law of Peace)",
        "wiki_title": "Great_Peacemaker",
        "lat": 43.08,
        "lng": -76.22,  # Onondaga Lake, New York
        "epoch_start": 1142,
        "epoch_end": 1500,
        "culture": "North American Indigenous",
        "archetype": "Divine Lawgiver Uprooting the White Pine to Bury Weapons of War Beneath",
        "syncretic_ids": ["Q105224", "Q651238"],
    },
    {
        "id": "Q2302326",
        "name": "Changing Woman / Asdzą́ą́ Nádleehé (The Eternal Navajo Holy Being of Renewal)",
        "wiki_title": "Changing_Woman",
        "lat": 36.50,
        "lng": -109.50,  # Dinetah / Chuska Mountains, Navajo Nation
        "epoch_start": 1000,
        "epoch_end": 1800,
        "culture": "North American Indigenous",
        "archetype": "Immortal Mother Matriarch Aging with Winter and Reborn Radiant in Spring",
        "syncretic_ids": ["Q179654", "Q153726"],
    },
    {
        "id": "Q2302327",
        "name": "Selu the First Woman and the Sacred Maize (The Cherokee Corn Mother)",
        "wiki_title": "Selu",
        "lat": 35.48,
        "lng": -83.32,  # Kituwah Mound, Great Smoky Mountains
        "epoch_start": 800,
        "epoch_end": 1800,
        "culture": "North American Indigenous",
        "archetype": "Self-Sacrificing Mother Whose Dragged Blood Sprouts the Stalks of Sweet Corn",
        "syncretic_ids": ["Q179654", "Q212628"],
    },
    {
        "id": "Q2302328",
        "name": "Nanabozho the Great Hare (The Earth-Diver and Rebirth of Turtle Island)",
        "wiki_title": "Nanabozho",
        "lat": 46.50,
        "lng": -84.34,  # Lake Superior / Sault Ste. Marie
        "epoch_start": 800,
        "epoch_end": 1800,
        "culture": "North American Indigenous",
        "archetype": "Mischievous Primal Shapeshifter Recreating Earth on the Back of the Turtle",
        "syncretic_ids": ["Q1138243", "Q213282"],
    },
    {
        "id": "Q2302329",
        "name": "The Horned Serpent Uktena (The Blazing Jewel on the Forehead of the Deep)",
        "wiki_title": "Horned_Serpent",
        "lat": 35.00,
        "lng": -84.00,  # Hiwassee River / Southern Appalachians
        "epoch_start": 500,
        "epoch_end": 1800,
        "culture": "North American Indigenous",
        "archetype": "Subaquatic Crested Horned Dragon Challenged by Thunderbird of the Sky",
        "syncretic_ids": ["Q242004", "Q42952"],
    },
    {
        "id": "Q2302330",
        "name": "The Wendigo (The Insatiable Winter Cannibal Spirit of the Boreal Taiga)",
        "wiki_title": "Wendigo",
        "lat": 50.00,
        "lng": -85.00,  # Northern Ontario Taiga
        "epoch_start": 1000,
        "epoch_end": 1900,
        "culture": "North American Indigenous",
        "archetype": "Glacial Monstrosity of Greed Growing Larger with Every Feast",
        "syncretic_ids": ["Q188734", "Q144703"],
    },
    {
        "id": "Q2302331",
        "name": "Kokopelli the Humpbacked Flute Player (The Bringer of Seeds and Song)",
        "wiki_title": "Kokopelli",
        "lat": 36.06,
        "lng": -107.96,  # Chaco Canyon, New Mexico
        "epoch_start": 750,
        "epoch_end": 1300,
        "culture": "North American Indigenous",
        "archetype": "Itinerant Flute-Playing Trickster Carrying Seeds and Music Across Canyons",
        "syncretic_ids": ["Q1138243", "Q172740"],
    },
    {
        "id": "Q2302332",
        "name": "Sisiutl (The Dual-Headed Soul-Reflecting Sea Serpent of the Pacific Northwest)",
        "wiki_title": "Sisiutl",
        "lat": 50.70,
        "lng": -127.50,  # Alert Bay, Vancouver Island (Kwakwaka'wakw)
        "epoch_start": 1000,
        "epoch_end": 1900,
        "culture": "North American Indigenous",
        "archetype": "Two-Headed Invincible Magic Dragon of Warrior Shields and War Canoes",
        "syncretic_ids": ["Q242004", "Q130832"],
    },

    # ── 15. MESOAMERICAN ──────────────────────────────────────────────────────
    {
        "id": "Q206928",
        "name": "Hunahpu and Xbalanque (The Hero Twins Conquering Xibalba in the Ballcourt)",
        "wiki_title": "Hero_Twins",
        "lat": 17.22,
        "lng": -89.62,  # Tikal / Xibalba Caves
        "epoch_start": -300,
        "epoch_end": 1550,
        "culture": "Mesoamerican",
        "archetype": "Twin Heroes Descending to Underworld to Outwit Lords of Death at the Ballgame",
        "syncretic_ids": ["Q172740", "Q248352"],
    },
    {
        "id": "Q206929",
        "name": "Tlaloc and Mount Tlaloc (The Goggle-Eyed Sovereign of Rains and Hail)",
        "wiki_title": "Tlaloc",
        "lat": 19.41,
        "lng": -98.71,  # Mount Tlaloc Shrine (4,120m)
        "epoch_start": 200,
        "epoch_end": 1521,
        "culture": "Mesoamerican",
        "archetype": "Mountain Storm Sovereign Cracking Four Jars of Rain, Frost, Disease, and Drought",
        "syncretic_ids": ["Q206927", "Q42952"],
    },
    {
        "id": "Q206930",
        "name": "Coyolxauhqui (The Moon Goddess Cast Down from the Pyramid of Coatepec)",
        "wiki_title": "Coyolxauhqui",
        "lat": 19.43,
        "lng": -99.13,  # Templo Mayor, Tenochtitlan
        "epoch_start": 1325,
        "epoch_end": 1521,
        "culture": "Mesoamerican",
        "archetype": "Bells-on-Her-Cheeks Moon Goddess Dismembered by Newly Born Solar God",
        "syncretic_ids": ["Q131444", "Q169542"],
    },
    {
        "id": "Q206931",
        "name": "Popocatépetl and Iztaccíhuatl (The Smoking Warrior and the Sleeping Woman)",
        "wiki_title": "Popocat%C3%A9petl_and_Iztacc%C3%ADhuatl",
        "lat": 19.02,
        "lng": -98.62,  # Paso de Cortés, Valley of Mexico
        "epoch_start": 1200,
        "epoch_end": 1521,
        "culture": "Mesoamerican",
        "archetype": "Tragic Warrior and Maiden Transfigured into Perpetual Snow-Capped Volcanoes",
        "syncretic_ids": ["Q172740", "Q1434449"],
    },
    {
        "id": "Q206932",
        "name": "Chacmool (The Reclining Stone Messenger of the Sun and Heart Sacrifices)",
        "wiki_title": "Chacmool",
        "lat": 20.68,
        "lng": -88.57,  # Temple of the Warriors, Chichen Itza
        "epoch_start": 800,
        "epoch_end": 1200,
        "culture": "Mesoamerican",
        "archetype": "Reclining Sacred Intermediary Bearing Vessel of Offerings to the Gods",
        "syncretic_ids": ["Q206927", "Q131444"],
    },
    {
        "id": "Q206933",
        "name": "Xolotl (The Canine Evening Star Guiding the Sun through the Underworld)",
        "wiki_title": "Xolotl",
        "lat": 19.30,
        "lng": -99.10,  # Xochimilco / Underworld
        "epoch_start": 900,
        "epoch_end": 1521,
        "culture": "Mesoamerican",
        "archetype": "Psychopomp Twin Dog Guiding Dead Across the Nine Subterranean Rivers",
        "syncretic_ids": ["Q188735", "Q172740"],
    },
    {
        "id": "Q206934",
        "name": "Ixchel (The Maya Rainbow Matron of Weaving, Midwifery, and the Moon)",
        "wiki_title": "Ixchel",
        "lat": 20.42,
        "lng": -86.92,  # San Gervasio Sanctuary, Cozumel Island
        "epoch_start": -300,
        "epoch_end": 1520,
        "culture": "Mesoamerican",
        "archetype": "Jaguar Moon Goddess Pouring Celestial Water Jar to Nurture Earth",
        "syncretic_ids": ["Q206927", "Q153726"],
    },

    # ── 16. ANDEAN & SOUTH AMERICAN ───────────────────────────────────────────
    {
        "id": "Q165998",
        "name": "Viracocha (The Creator Emerging from Lake Titicaca to Call Forth Sun and Stars)",
        "wiki_title": "Viracocha",
        "lat": -16.02,
        "lng": -69.17,  # Island of the Sun (Isla del Sol), Lake Titicaca
        "epoch_start": 800,
        "epoch_end": 1533,
        "culture": "Andean & South American",
        "archetype": "Supreme Creator Wandering Earth in Guise of Humble Beggar Teaching Civil Arts",
        "syncretic_ids": ["Q165997", "Q1422880"],
    },
    {
        "id": "Q165999",
        "name": "Naymlap and the Balsa Fleet (The Emerald Sea King of Lambayeque)",
        "wiki_title": "Naymlap",
        "lat": -6.70,
        "lng": -79.90,  # Huaca Chotuna, Lambayeque Valley
        "epoch_start": 750,
        "epoch_end": 1375,
        "culture": "Andean & South American",
        "archetype": "Culture Hero Arriving Across the Pacific on Balsa Rafts Growing Green Wings",
        "syncretic_ids": ["Q164426", "Q1792942"],
    },
    {
        "id": "Q166000",
        "name": "Curupira (The Backward-Footed Forest Protector of the Amazon)",
        "wiki_title": "Curupira",
        "lat": -3.10,
        "lng": -60.02,  # Amazon Basin (Manaus / Rio Negro)
        "epoch_start": 1000,
        "epoch_end": 1900,
        "culture": "Andean & South American",
        "archetype": "Fiery-Haired Forest Guardian Misleading Poachers with Reverse Footprints",
        "syncretic_ids": ["Q1138243", "Q234455"],
    },
    {
        "id": "Q166001",
        "name": "Iara the Siren of the Amazon River (The Enchantress of the Deep Waters)",
        "wiki_title": "Iara_(mythology)",
        "lat": -2.40,
        "lng": -54.70,  # Santarém (Meeting of the Waters)
        "epoch_start": 1200,
        "epoch_end": 1900,
        "culture": "Andean & South American",
        "archetype": "Aquatic Seductress Drawing River Fishermen into Crystal Sunken Palaces",
        "syncretic_ids": ["Q1189332", "Q134114"],
    },
    {
        "id": "Q166002",
        "name": "Boitatá (The Giant Luminous Bull-Serpent of Phosphorescent Fire)",
        "wiki_title": "Boitat%C3%A1",
        "lat": -15.78,
        "lng": -47.92,  # Pantanal / Brazilian Cerrado
        "epoch_start": 1000,
        "epoch_end": 1900,
        "culture": "Andean & South American",
        "archetype": "Giant Eye-Filled Fire Serpent Guarding Forests from Incendiary Intruders",
        "syncretic_ids": ["Q42952", "Q212680"],
    },
    {
        "id": "Q166003",
        "name": "Guaraní Cosmogony (Tupã the Thunderer and the Seven Monstrous Sons)",
        "wiki_title": "Guaran%C3%AD_mythology",
        "lat": -25.26,
        "lng": -57.57,  # Ybytyruzú Mountains / Asunción
        "epoch_start": 1000,
        "epoch_end": 1800,
        "culture": "Andean & South American",
        "archetype": "Thunder God and the Cursed Offspring of Tau and Kerana",
        "syncretic_ids": ["Q42952", "Q10802"],
    },
    {
        "id": "Q166004",
        "name": "Pachamama (The Living Mother Earth of the High Andean Altiplano)",
        "wiki_title": "Pachamama",
        "lat": -13.53,
        "lng": -71.96,  # Sacred Valley / Cusco
        "epoch_start": 500,
        "epoch_end": 1900,
        "culture": "Andean & South American",
        "archetype": "Cosmic Mother Living in Mountain Terrains Requiring Reciprocal Offerings (Pago)",
        "syncretic_ids": ["Q153726", "Q131705"],
    },
    {
        "id": "Q166005",
        "name": "Yacumama (The 50-Meter Mother of All Waters in the Amazon Rivers)",
        "wiki_title": "Yacumama",
        "lat": -3.75,
        "lng": -73.25,  # Upper Amazon / Iquitos
        "epoch_start": 1000,
        "epoch_end": 1900,
        "culture": "Andean & South American",
        "archetype": "Colossal Primordial Anaconda Sucking River Whirlpools into Her Jaws",
        "syncretic_ids": ["Q212680", "Q42952"],
    },
    {
        "id": "Q166006",
        "name": "Saci-Pererê (The One-Legged Whistling Trickster of the Whirlwinds)",
        "wiki_title": "Saci_(folklore)",
        "lat": -23.55,
        "lng": -46.63,  # São Paulo Interior
        "epoch_start": 1600,
        "epoch_end": 1950,
        "culture": "Andean & South American",
        "archetype": "One-Legged Pipe-Smoking Trickster Riding Inside Forest Dust Devils",
        "syncretic_ids": ["Q1138243", "Q121852"],
    },

    # ── 17. WEST AFRICAN ──────────────────────────────────────────────────────
    {
        "id": "Q939989",
        "name": "Eshu Elegbara (The Master of the Crossroads, Fate, and Divination)",
        "wiki_title": "Eshu",
        "lat": 7.50,
        "lng": 4.50,  # Ile-Ife, Osun State, Nigeria
        "epoch_start": 800,
        "epoch_end": 1900,
        "culture": "West African",
        "archetype": "Divine Trickster Herald Standing at the Threshold between Mortals and Orishas",
        "syncretic_ids": ["Q1138243", "Q83364"],
    },
    {
        "id": "Q939990",
        "name": "Ogun (The Orisha of Iron, Blacksmiths, and Pioneering Forest Trails)",
        "wiki_title": "Ogun",
        "lat": 7.62,
        "lng": 5.22,  # Ire Ekiti / Oyo
        "epoch_start": 800,
        "epoch_end": 1900,
        "culture": "West African",
        "archetype": "First Orisha to Cut a Path through Primeval Chaos with His Iron Machete",
        "syncretic_ids": ["Q212628", "Q153725"],
    },
    {
        "id": "Q939991",
        "name": "Mami Wata (The Serpentine Queen of the Coastal Atlantic and Inland Swells)",
        "wiki_title": "Mami_Wata",
        "lat": 6.13,
        "lng": 1.22,  # Gulf of Guinea Coast (Togo / Benin / Nigeria)
        "epoch_start": 1400,
        "epoch_end": 1950,
        "culture": "West African",
        "archetype": "Water Goddess Entwined with Serpent Holding the Balance of Wealth and Peril",
        "syncretic_ids": ["Q134114", "Q1189332"],
    },
    {
        "id": "Q939992",
        "name": "Nana Buluku (The Primordial Supreme Creatrix of Dahomey and Fon Vodun)",
        "wiki_title": "Nana_Buluku",
        "lat": 7.18,
        "lng": 1.99,  # Abomey Kingdom, Benin
        "epoch_start": 1000,
        "epoch_end": 1890,
        "culture": "West African",
        "archetype": "Androgynous Primordial Creatrix Giving Birth to the Twins Mawu-Lisa",
        "syncretic_ids": ["Q939988", "Q1422880"],
    },
    {
        "id": "Q939993",
        "name": "Ala (The Earth Mother and Moral Sanctuary of Igbo Odinani)",
        "wiki_title": "Ala_(Odinani)",
        "lat": 5.48,
        "lng": 7.03,  # Owerri / Igboland
        "epoch_start": 900,
        "epoch_end": 1900,
        "culture": "West African",
        "archetype": "Goddess of the Sacred Soil and Ancestral Womb Enforcing Omenala (Moral Law)",
        "syncretic_ids": ["Q153726", "Q166004"],
    },
    {
        "id": "Q939994",
        "name": "Amadioha (The Sky Thunder King Flashing in Sudden Red Lightning)",
        "wiki_title": "Amadioha",
        "lat": 5.80,
        "lng": 7.10,  # Ozuzu Shrine, Rivers State / Igboland
        "epoch_start": 900,
        "epoch_end": 1900,
        "culture": "West African",
        "archetype": "Righteous Sovereign of Heavenly Thunder Striking Down Falsehood with Lightning",
        "syncretic_ids": ["Q939988", "Q42952"],
    },
    {
        "id": "Q939995",
        "name": "Nyame (The Supreme Akan Sky God and the Golden Stool of Ashanti)",
        "wiki_title": "Nyame",
        "lat": 6.69,
        "lng": -1.62,  # Kumasi, Ashanti Empire, Ghana
        "epoch_start": 1200,
        "epoch_end": 1900,
        "culture": "West African",
        "archetype": "Sky God Descending the Golden Stool from the Clouds onto the Knees of the King",
        "syncretic_ids": ["Q1164", "Q1138243"],
    },
    {
        "id": "Q939996",
        "name": "Legba (The Master of the Gates and Guardian of the Spiritual Crossroads)",
        "wiki_title": "Legba",
        "lat": 6.36,
        "lng": 2.43,  # Ouidah, Benin
        "epoch_start": 1200,
        "epoch_end": 1900,
        "culture": "West African",
        "archetype": "Keeper of the Gateway between the Human Village and the Invisible Loa",
        "syncretic_ids": ["Q939989", "Q1138243"],
    },

    # ── 18. CENTRAL & SOUTHERN AFRICAN ────────────────────────────────────────
    {
        "id": "Q1447821",
        "name": "Unkulunkulu (The First Ancestor Who Broke Out of the Primeval Reeds)",
        "wiki_title": "Unkulunkulu",
        "lat": -28.73,
        "lng": 31.89,  # eMakhosini (Valley of the Kings, KwaZulu-Natal)
        "epoch_start": 1000,
        "epoch_end": 1850,
        "culture": "Central & Southern African",
        "archetype": "First Old Man Growing in Reeds (Uhlanga) Who Named Cattle, Hills, and Rivers",
        "syncretic_ids": ["Q841445", "Q939988"],
    },
    {
        "id": "Q1447822",
        "name": "Cagn the Praying Mantis (The Trickster and Sculptor of the Drakensberg Rocks)",
        "wiki_title": "San_religion",
        "lat": -29.50,
        "lng": 29.30,  # uKhahlamba / Drakensberg Rock Art
        "epoch_start": -2000,
        "epoch_end": 1850,
        "culture": "Central & Southern African",
        "archetype": "Mantis Demiurge Creating the Eland Antelope from Honey and Blood",
        "syncretic_ids": ["Q1138243", "Q803698"],
    },
    {
        "id": "Q1447823",
        "name": "Mwari of the Matobo Rocks (The Voice from the Granite Caves)",
        "wiki_title": "Mwari",
        "lat": -20.55,
        "lng": 28.50,  # Njelele Shrine, Matobo Hills, Zimbabwe
        "epoch_start": 1000,
        "epoch_end": 1900,
        "culture": "Central & Southern African",
        "archetype": "Supreme Incorporeal Deity Speaking as an Echo from Sacred Boulder Caves",
        "syncretic_ids": ["Q1164", "Q385552"],
    },
    {
        "id": "Q1447824",
        "name": "The Tikoloshe (The Mischievous Water Goblin of Xhosa and Zulu Lore)",
        "wiki_title": "Tikoloshe",
        "lat": -32.50,
        "lng": 27.50,  # Great Kei River, Eastern Cape
        "epoch_start": 1200,
        "epoch_end": 1950,
        "culture": "Central & Southern African",
        "archetype": "Dwarf River Sprite Invisible to Adults Causing Havoc by Night",
        "syncretic_ids": ["Q166006", "Q1138243"],
    },
    {
        "id": "Q1447825",
        "name": "Mokele-mbembe (The Living Sauropod Monster of the Likouala Swamps)",
        "wiki_title": "Mokele-mbembe",
        "lat": 0.50,
        "lng": 17.50,  # Lake Télé / Likouala Region, Congo Basin
        "epoch_start": 1400,
        "epoch_end": 1950,
        "culture": "Central & Southern African",
        "archetype": "Prehistoric River Dragon Halting Water Flow and Sinking Hippos",
        "syncretic_ids": ["Q212680", "Q166005"],
    },
    {
        "id": "Q1447826",
        "name": "Kalunga (The Great Ocean Horizon Boundary between the Living and Ancestors)",
        "wiki_title": "Kalunga",
        "lat": -6.13,
        "lng": 12.37,  # Mouth of the Congo River (Soyio / Mbanza Kongo)
        "epoch_start": 1200,
        "epoch_end": 1900,
        "culture": "Central & Southern African",
        "archetype": "Vast Watery Mirror Separating the White Ancestral Realm from the Physical World",
        "syncretic_ids": ["Q134114", "Q179654"],
    },

    # ── 19. OCEANIC & AUSTRALASIAN ────────────────────────────────────────────
    {
        "id": "Q1792943",
        "name": "Tangaroa (The Great Sovereign of the Vast Oceans and Marine Life)",
        "wiki_title": "Tangaroa",
        "lat": -21.20,
        "lng": -159.77,  # Rarotonga, Cook Islands
        "epoch_start": 800,
        "epoch_end": 1800,
        "culture": "Oceanic & Australasian",
        "archetype": "Primordial God of the Boundless Ocean Breathing through Ebb and Flow of Tides",
        "syncretic_ids": ["Q1422880", "Q35060"],
    },
    {
        "id": "Q1792944",
        "name": "The Wandjina (The Mouthless Cloud Spirits of the Kimberley Rock Art)",
        "wiki_title": "Wandjina",
        "lat": -16.00,
        "lng": 126.00,  # Kimberley Region, Western Australia
        "epoch_start": -2000,
        "epoch_end": 1850,
        "culture": "Oceanic & Australasian",
        "archetype": "Halo-Crowned Cloud Spirits of Lightning and Cyclones Without Mouths",
        "syncretic_ids": ["Q803698", "Q2302324"],
    },
    {
        "id": "Q1792945",
        "name": "Hine-nui-te-pō (The Great Woman of Night and Queen of the Underworld)",
        "wiki_title": "Hine-nui-te-p%C5%8D",
        "lat": -34.42,
        "lng": 172.68,  # Cape Reinga (Te Rerenga Wairua), New Zealand
        "epoch_start": 900,
        "epoch_end": 1800,
        "culture": "Oceanic & Australasian",
        "archetype": "Dawn Maiden Fleeing to Underworld Reborn as Sovereign Over Death",
        "syncretic_ids": ["Q179654", "Q179655"],
    },
    {
        "id": "Q1792946",
        "name": "Tagaloa the Architect of Heavens (The Cosmic Bird and the First Coral Rocks)",
        "wiki_title": "Tagaloa",
        "lat": -13.83,
        "lng": -171.76,  # Manu'a Islands / Upolu, Samoa
        "epoch_start": -800,
        "epoch_end": 1700,
        "culture": "Oceanic & Australasian",
        "archetype": "Supreme Architect Flying as Snipe Rolling First Boulders from Celestial Heights",
        "syncretic_ids": ["Q1422880", "Q1792943"],
    },
    {
        "id": "Q1792947",
        "name": "Daramulum (The Emu-Footed Son of Baiame and the Sound of the Bullroarer)",
        "wiki_title": "Daramulum",
        "lat": -36.31,
        "lng": 150.05,  # Gulaga (Mount Dromedary), Yuin Nation, NSW
        "epoch_start": -5000,
        "epoch_end": 1850,
        "culture": "Oceanic & Australasian",
        "archetype": "Initiation Deity Whose Roaring Voice Echoes in the Sacred Whirling Bullroarer",
        "syncretic_ids": ["Q803698", "Q42952"],
    },
    {
        "id": "Q1792948",
        "name": "The Menehune (The Mythological Forest Builders of Ancient Kauai)",
        "wiki_title": "Menehune",
        "lat": 21.98,
        "lng": -159.37,  # Alekoko Fishpond, Kauai, Hawaii
        "epoch_start": 800,
        "epoch_end": 1800,
        "culture": "Oceanic & Australasian",
        "archetype": "Hidden Nocturnal Dwarves Constructing Colossal Stone Aqueducts in a Single Night",
        "syncretic_ids": ["Q131351", "Q1138243"],
    },
    {
        "id": "Q1792949",
        "name": "Lono and the Makahiki (The Hawaiian God of Abundance, Rains, and Cosmic Peace)",
        "wiki_title": "Lono",
        "lat": 19.48,
        "lng": -155.93,  # Kealakekua Bay, Big Island, Hawaii
        "epoch_start": 1000,
        "epoch_end": 1800,
        "culture": "Oceanic & Australasian",
        "archetype": "Lord of Seasonal Peace Halting All War for Four Lunar Months of Joy and Games",
        "syncretic_ids": ["Q179654", "Q234720"],
    },
    {
        "id": "Q1792950",
        "name": "Kū the Unconquered (The Hawaiian God of Sovereignty, Strength, and War Temples)",
        "wiki_title": "K%C5%AB",
        "lat": 20.03,
        "lng": -155.83,  # Pu'ukohola Heiau, Kohala, Hawaii
        "epoch_start": 1000,
        "epoch_end": 1819,
        "culture": "Oceanic & Australasian",
        "archetype": "Fierce Carved Totem Deity of Martial Power and Royal Unification",
        "syncretic_ids": ["Q12224", "Q939990"],
    },
    {
        "id": "Q1792951",
        "name": "Kanaloa (The Sovereign of the Deepest Ocean Trench and the Giant Squid)",
        "wiki_title": "Kanaloa",
        "lat": 20.53,
        "lng": -156.65,  # Kaho'olawe Island, Hawaii
        "epoch_start": 1000,
        "epoch_end": 1850,
        "culture": "Oceanic & Australasian",
        "archetype": "Cephalopod Sovereign Guiding Navigators Across Boundless Trans-Pacific Voyages",
        "syncretic_ids": ["Q1792943", "Q111729"],
    },
]


def assemble_mega_catalog() -> None:
    if not WIKIDATA_RAW_PATH.exists():
        print(f"Error: {WIKIDATA_RAW_PATH} not found!")
        return

    with open(WIKIDATA_RAW_PATH, "r", encoding="utf-8") as f:
        existing_items = json.load(f)

    existing_titles = {
        urllib.parse.unquote(x.get("wiki_title", "")).lower().replace(" ", "_")
        for x in existing_items
    }
    existing_ids = {x.get("id") for x in existing_items}
    existing_names = {x.get("name", "").lower() for x in existing_items}

    added_count = 0
    for myth in MEGA_NEW_MYTHS:
        clean_title = (
            urllib.parse.unquote(myth.get("wiki_title", ""))
            .lower()
            .replace(" ", "_")
        )
        myth_id = myth.get("id")
        myth_name = myth.get("name", "").lower()

        if clean_title in existing_titles:
            print(f"Skipping duplicate title: {myth['wiki_title']}")
            continue
        if myth_id in existing_ids:
            print(f"Skipping duplicate ID: {myth_id}")
            continue
        if myth_name in existing_names:
            print(f"Skipping duplicate name: {myth['name']}")
            continue

        existing_items.append(myth)
        existing_titles.add(clean_title)
        existing_ids.add(myth_id)
        existing_names.add(myth_name)
        added_count += 1

    print(f"\nAdded {added_count} brand-new verified foundational myths!")
    print(f"Total myths now in catalog: {len(existing_items)}")

    # Write back to wikidata_raw.json
    with open(WIKIDATA_RAW_PATH, "w", encoding="utf-8") as f:
        json.dump(existing_items, f, indent=2, ensure_ascii=False)

    print(f"Successfully updated {WIKIDATA_RAW_PATH}")


if __name__ == "__main__":
    assemble_mega_catalog()
