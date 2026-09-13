/**
 * Curated Guided Expeditions Registry for MythosAtlas ("Story Mode").
 * Documentary-style narrative odysseys tracing universal motifs across human history.
 */

export interface ExpeditionStop {
  mythId: string;
  chapterNumber: number;
  chapterTitle: string;
  mythName: string;
  culture: string;
  year: number;
  lat: number;
  lng: number;
  cameraAltitude?: number;
  narrativeLead: string;
  comparativeInsight: string;
  keyMotifs: string[];
}

export interface Expedition {
  id: string;
  title: string;
  subtitle: string;
  durationLabel: string;
  heroIcon: string;
  badge: string;
  synopsis: string;
  traditionTags: string[];
  stops: ExpeditionStop[];
}

export const CURATED_EXPEDITIONS: Expedition[] = [
  {
    id: 'the-great-deluge',
    title: 'The Great Deluge Across 6 Continents',
    subtitle: 'Universal Flood Cycles & the Rebirth of Civilization',
    durationLabel: '7 Chapters',
    heroIcon: '🌊',
    badge: 'Universal Cataclysm',
    synopsis:
      'From the muddy banks of the Euphrates to the volcanic ridges of the Andes, explore how humanity across 6 disconnected continents shared an identical archetypal nightmare: the submergence of an imperfect world and its divine rebirth through a lone surviving vessel.',
    traditionTags: ['Mesopotamian', 'Levantine', 'Vedic & Hindu', 'East Asian', 'Mesoamerican', 'Andean'],
    stops: [
      {
        mythId: 'Q248352',
        chapterNumber: 1,
        chapterTitle: 'The Scribe of Shuruppak',
        mythName: 'Epic of Gilgamesh (Utnapishtim)',
        culture: 'Mesopotamian',
        year: -2100,
        lat: 31.32,
        lng: 45.63,
        narrativeLead:
          'Before biblical Genesis was inked, tablet XI of Gilgamesh recorded how Enki whispered through a reed wall to Utnapishtim: "Tear down thy house, build a ship, abandon wealth and seek living things!"',
        comparativeInsight:
          'The Mesopotamian deluge is rooted in the violent, unpredictable seasonal flooding of the Tigris and Euphrates rivers, framing divine wrath as irritation at mortal noise.',
        keyMotifs: ['Cosmic Ark', 'Divine Whisper', 'Dove and Raven Release', 'Quest for Immortality'],
      },
      {
        mythId: 'Q190535',
        chapterNumber: 2,
        chapterTitle: 'The Seven Days of Tempests',
        mythName: 'Atrahasis Epic',
        culture: 'Mesopotamian',
        year: -1700,
        lat: 32.53,
        lng: 44.42,
        narrativeLead:
          'Atrahasis, whose name means "Exceedingly Wise", gathers his family and beasts aboard a pitch-coated reed boat as the sky gods blacken the sun and unleash seven days of torrential cataclysm.',
        comparativeInsight:
          'The vessel described in Atrahasis is a massive circular coracle (quffa), engineered precisely like traditional Mesopotamian river crafts made of woven palm reeds and bitumen.',
        keyMotifs: ['Circular Coracle', 'Mortal Noise', 'Gods Like Flies', 'Covenant of Survival'],
      },
      {
        mythId: 'Q10801',
        chapterNumber: 3,
        chapterTitle: 'The Covenant on Ararat',
        mythName: "Genesis Deluge (Noah's Ark)",
        culture: 'Levantine',
        year: -700,
        lat: 39.7,
        lng: 44.29,
        narrativeLead:
          'In the Judeo-Levantine tradition, the cataclysm shifts from arbitrary divine annoyance to moral judgment: God grieves at humanity’s violence and commissions a gopher-wood tebah to preserve the righteous.',
        comparativeInsight:
          'The biblical narrative preserves the exact tripartite bird sequence (raven, dove, second dove returning with an olive leaf) found in the cuneiform flood tablets of Nineveh.',
        keyMotifs: ['Moral Retribution', 'Rainbow Covenant', 'Gopher Wood Ark', 'Mount Ararat Resting'],
      },
      {
        mythId: 'Q39546',
        chapterNumber: 4,
        chapterTitle: 'The Horned Fish & the Seven Rishis',
        mythName: 'Samudra Manthana & Matsya Avatar',
        culture: 'Vedic & Hindu',
        year: -1200,
        lat: 25.43,
        lng: 81.84,
        narrativeLead:
          'Lord Vishnu manifests as Matsya, a golden horned fish, warning King Manu of the coming Pralaya (cosmic dissolution) and guiding a great ship tethered to his horn by the giant serpent Vasuki.',
        comparativeInsight:
          'Unlike Western deluges of permanent linear punishment, Vedic flood mythology operates within cyclical time (Yugas): water dissolves the spent universe so a fresh cosmic cycle may begin.',
        keyMotifs: ['Matsya Horned Fish', 'Cyclical Pralaya', 'Preservation of the Vedas', 'Sacred King Manu'],
      },
      {
        mythId: 'Q242488',
        chapterNumber: 5,
        chapterTitle: 'The Smelting of Five-Colored Stones',
        mythName: 'Nuwa Mends the Fallen Heavens',
        culture: 'East Asian',
        year: -1000,
        lat: 36.63,
        lng: 113.62,
        narrativeLead:
          'When the water god Gonggong smashed Mount Buzhou in rage, the celestial vault cracked and sky-waters poured upon Earth. The half-human, half-serpent mother goddess Nüwa smelted stones of five colors to patch the heavens.',
        comparativeInsight:
          'In Chinese mythology, the hero does not flee the flood aboard an ark; instead, humanity and goddess triumph through architectural repair and civil engineering.',
        keyMotifs: ['Five-Colored Stones', 'Cosmic Pillar Collapse', 'Serpent Mother Goddess', 'Flood Remediation'],
      },
      {
        mythId: 'Q190828',
        chapterNumber: 6,
        chapterTitle: 'The Drowning of the Wooden Men',
        mythName: 'Popol Vuh (The Mayan Cataclysm)',
        culture: 'Mesoamerican',
        year: 300,
        lat: 14.63,
        lng: -90.51,
        narrativeLead:
          'The Mayan Creator gods Heart of Sky and Sovereign Plumed Serpent grew weary of the Second Creation—wooden mannequins with no memory of their makers—and summoned a sticky rain of black resin to drown them.',
        comparativeInsight:
          'The Popol Vuh features a unique vengeance motif: kitchen grinding stones, cooking pots, and domesticated dogs rise up against the wooden men to strike back before the waters engulf them.',
        keyMotifs: ['Wooden Mannequins', 'Black Resin Rain', 'Uprising of Utensils', 'Birth of Monkeys'],
      },
      {
        mythId: 'Q131670',
        chapterNumber: 7,
        chapterTitle: 'The Battle of Earth and Ocean',
        mythName: 'Trentren Vilu and Caicai Vilu',
        culture: 'Andean & South American',
        year: 500,
        lat: -39.0,
        lng: -72.5,
        narrativeLead:
          'Along the stormy coasts of southern Chile, the sea serpent Caicai Vilu surged to drown the world in salt water, while the mountain serpent Trentren Vilu raised the Andean peaks to rescue humanity from the abyss.',
        comparativeInsight:
          'Reflects profound indigenous geological awareness of Pacific subduction zone mega-tsunamis and seismic land uplift along the Ring of Fire.',
        keyMotifs: ['Dual Cosmic Serpents', 'Pacific Mega-Tsunami', 'Mountain Elevation', 'Marine Metamorphosis'],
      },
    ],
  },
  {
    id: 'descent-into-the-underworld',
    title: 'Descent into the Underworld (Katabasis)',
    subtitle: 'The Soul’s Journey into Death and Resurrection',
    durationLabel: '6 Chapters',
    heroIcon: '💀',
    badge: 'Psychological Descent',
    synopsis:
      'Explore the universal human archetype of Katabasis: descending past seven gates of darkness, confronting the lord of the dead, surviving the dissolution of the ego, and emerging reborn with forbidden wisdom.',
    traditionTags: ['Mesopotamian', 'Egyptian', 'Greco-Roman', 'East Asian', 'Mesoamerican'],
    stops: [
      {
        mythId: 'Q272486',
        chapterNumber: 1,
        chapterTitle: 'The Stripping of the Seven Royal Veils',
        mythName: 'Descent of Inanna into the Underworld',
        culture: 'Mesopotamian',
        year: -2100,
        lat: 31.31,
        lng: 45.65,
        narrativeLead:
          'Inanna, Queen of Heaven, descends to the Great Below to confront her dark sister Ereshkigal. At each of the underworld’s seven gates, she must surrender a sacred vestment until she stands naked and vulnerable before the throne of death.',
        comparativeInsight:
          'One of the oldest surviving psychological mythologems: the voluntary shedding of social status and worldly power required to enter the shadow unconscious.',
        keyMotifs: ['Seven Underworld Gates', 'Shedding of Vestments', 'Corpse on a Meat Hook', 'Three-Day Resurrection'],
      },
      {
        mythId: 'Q46580',
        chapterNumber: 2,
        chapterTitle: 'The Scales of Truth and Feather of Maat',
        mythName: 'Osiris Myth and Resurrection',
        culture: 'Egyptian',
        year: -2400,
        lat: 26.18,
        lng: 31.92,
        narrativeLead:
          'Murdered and dismembered into fourteen pieces by his brother Seth, Osiris is painstakingly gathered by Isis and resurrected as the eternal Judge of the Dead in the subterranean Duat.',
        comparativeInsight:
          'Egyptian Katabasis transformed the underworld from a bleak prison into an ethical proving ground where every soul is weighed against truth itself.',
        keyMotifs: ['Fourteen Severed Pieces', 'Hall of Two Truths', 'Heart vs Feather', 'Eternal Lord of the Duat'],
      },
      {
        mythId: 'Q179654',
        chapterNumber: 3,
        chapterTitle: 'The Seeds of the Pomegranate',
        mythName: 'Demeter and Persephone (Eleusinian Mysteries)',
        culture: 'Greco-Roman',
        year: -800,
        lat: 38.04,
        lng: 23.54,
        narrativeLead:
          'Abducted into the kingdom of Hades, Persephone consumes six seeds of the underworld pomegranate, binding her forever to split her year between subterranean dormancy and blooming terrestrial spring.',
        comparativeInsight:
          'Formed the foundational mystery cult of classical antiquity (Eleusis), assuring initiates that biological death is merely the seed of cyclical spiritual rebirth.',
        keyMotifs: ['Pomegranate Seeds', 'Eleusinian Mysteries', 'Mother’s Cosmic Grief', 'Seasonal Resurrection'],
      },
      {
        mythId: 'Q172740',
        chapterNumber: 4,
        chapterTitle: 'The Lyre at the River Styx',
        mythName: 'Orpheus and Eurydice (The Tragic Turn)',
        culture: 'Greco-Roman',
        year: -700,
        lat: 41.13,
        lng: 24.88,
        narrativeLead:
          'Armed only with his golden lyre, Orpheus enchants the three-headed dog Cerberus and softens the stone heart of Hades. But a single forbidden glance backward on the ascent dissolves his beloved forever into shade.',
        comparativeInsight:
          'Highlights the human terror of mortality: how anxious attachment and lack of faith can unravel the delicate journey back into the light.',
        keyMotifs: ['Musical Enchantment of Hades', 'Forbidden Backward Glance', 'River Styx Crossing', 'Tragic Loss'],
      },
      {
        mythId: 'Q179831',
        chapterNumber: 5,
        chapterTitle: 'The Corpse in the Land of Yomi',
        mythName: 'Izanagi’s Flight from the Land of Gloom',
        culture: 'East Asian',
        year: 712,
        lat: 34.45,
        lng: 134.8,
        narrativeLead:
          'Grieving his consort Izanami who died giving birth to fire, Izanagi descends into Yomi. Breaking his promise, he lights a comb tooth and is horrified to see her body crawling with thunder maggots, fleeing as she sends the crones of night in pursuit.',
        comparativeInsight:
          'Parallels Orpheus directly: breaking the taboo of seeing death’s raw physical decay creates the eternal barrier between the living world and the land of shades.',
        keyMotifs: ['Land of Gloom (Yomi)', 'Lighted Comb Tooth', 'Pollution of Death', 'Misogi Purification'],
      },
      {
        mythId: 'Q190828',
        chapterNumber: 6,
        chapterTitle: 'The Labyrinthine Trials of Xibalba',
        mythName: 'Popol Vuh (The Hero Twins in the Maya Underworld)',
        culture: 'Mesoamerican',
        year: 300,
        lat: 14.63,
        lng: -90.51,
        narrativeLead:
          'Summoned by the sadistic Lords of Xibalba to play the sacred ballgame, Hero Twins Hunahpu and Xbalanque navigate the Dark House, Razor House, Cold House, and Bat House through trickery, dying in a fiery pit only to resurrect as the Sun and Moon.',
        comparativeInsight:
          'A triumphant culmination of Katabasis: the initiates don’t merely escape the underworld—they conquer it from within through intellect and ascend as celestial bodies.',
        keyMotifs: ['Underworld Ballgame', 'Chambers of Torture', 'Decapitation and Rebirth', 'Celestial Ascension'],
      },
    ],
  },
  {
    id: 'the-fire-stealers',
    title: 'The Promethean Fire-Stealers',
    subtitle: 'Tricksters of Divine Light & Sacred Knowledge',
    durationLabel: '5 Chapters',
    heroIcon: '🔥',
    badge: 'Trickster Archetype',
    synopsis:
      'Trace humanity’s greatest rebel archetype across continents: the fearless culture-hero trickster who defies authoritarian gods, steals forbidden technology, and suffers eternal punishment so humanity can emerge from darkness.',
    traditionTags: ['Greco-Roman', 'North American Indigenous', 'Oceanic & Australasian', 'West African'],
    stops: [
      {
        mythId: 'Q83364',
        chapterNumber: 1,
        chapterTitle: 'The Fennel Stalk on Mount Olympus',
        mythName: 'Prometheus Bound and the Gift of Fire',
        culture: 'Greco-Roman',
        year: -750,
        lat: 43.35,
        lng: 42.45,
        narrativeLead:
          'Defying Zeus who wished humanity to starve in freezing caves, the Titan Prometheus concealed a glowing ember of divine fire within a hollow fennel stalk and gifted it to mortals, enduring an eagle tearing his liver on the Caucasian crags.',
        comparativeInsight:
          'Fire is not merely warmth; in the Western tradition it represents logos, metallurgy, science, and the burden of intellectual autonomy.',
        keyMotifs: ['Hollow Fennel Stalk', 'Rebellion Against Zeus', 'Chained to Caucasian Crag', 'Gift of Technology'],
      },
      {
        mythId: 'Q1138243',
        chapterNumber: 2,
        chapterTitle: 'The Animal Relay Race',
        mythName: 'Coyote and the Theft of Fire',
        culture: 'North American Indigenous',
        year: -500,
        lat: 44.0,
        lng: -118.0,
        narrativeLead:
          'On top of a snowy mountain guarded by cruel Fire Beings, Coyote tricked the guards by staging an animal relay race, passing the burning coal down the mountain from cougar to bear to squirrel, singeing their tails into their modern shapes.',
        comparativeInsight:
          'Unlike Prometheus who acts alone in tragic grandeur, indigenous North American fire myths emphasize communal ecological collaboration among all animal nations.',
        keyMotifs: ['Animal Relay', 'Fire Beings on Mountain', 'Singeing of Squirrel Tail', 'Cooperative Trickery'],
      },
      {
        mythId: 'Q131650',
        chapterNumber: 3,
        chapterTitle: 'The Cedar Box of the Sun',
        mythName: 'Raven Stealing the Light of the Sun',
        culture: 'North American Indigenous',
        year: -1000,
        lat: 53.25,
        lng: -132.0,
        narrativeLead:
          'In the eternal darkness of the Pacific Northwest, Raven transformed into a pine needle, was swallowed by a chief’s daughter, and was born as a child who wept until given the nested cedar box containing the Sun, flying up through the smokehole into the sky.',
        comparativeInsight:
          'Raven is both creator and gluttonous shapeshifter: liberation of cosmic light occurs not out of pure altruism, but through the trickster’s insatiable appetite and curiosity.',
        keyMotifs: ['Nested Cedar Boxes', 'Pine Needle Conception', 'Smokehole Escape', 'Creation of Stars and Moon'],
      },
      {
        mythId: 'Q1145305',
        chapterNumber: 4,
        chapterTitle: 'The Fingernails of Mahuika',
        mythName: 'Māui Bringing Fire to the Islands',
        culture: 'Oceanic & Australasian',
        year: 1100,
        lat: -38.68,
        lng: 176.07,
        narrativeLead:
          'Māui journeyed to the subterranean hearth of his grandmother, the fire goddess Mahuika, tricking her into surrendering her burning fingernails one by one until her wrath set the earth ablaze, forcing him to hide the last embers in the bark of forest trees.',
        comparativeInsight:
          'Explains the Polynesian technology of fire-making: rubbing dry Kaikōmako wood draws forth the divine sparks hidden there by Māui during his escape.',
        keyMotifs: ['Fingernails of Fire', 'Fire Hidden in Trees', 'Extinguishing of the Hearth', 'Trickster Demigod'],
      },
      {
        mythId: 'Q686259',
        chapterNumber: 5,
        chapterTitle: 'The Pot of Wisdom on the High Branch',
        mythName: 'Anansi Buying Stories from Nyame',
        culture: 'West African',
        year: 1200,
        lat: 6.68,
        lng: -1.62,
        narrativeLead:
          'Sky God Nyame owned all wisdom and stories, demanding impossible prices: the leopard with venomous teeth, the hornets that sting like fire, and the invisible fairy. Anansi outsmarted them all with a hollow gourd and spun the tales down to mortals.',
        comparativeInsight:
          'In West Africa, the stolen divine fire is the spoken word and communal folklore—the greatest weapon of the physically vulnerable against oppressive power.',
        keyMotifs: ['Sky God Nyame', 'Hollow Gourd Trap', 'Stories as Cosmic Fire', 'Triumph of Mind over Brawn'],
      },
    ],
  },
  {
    id: 'the-chaoskampf',
    title: 'The Chaoskampf: Slaying the Primordial Serpent',
    subtitle: 'Cosmic Order Conquering the Primordial Abyss',
    durationLabel: '6 Chapters',
    heroIcon: '🐉',
    badge: 'Cosmic Conflict',
    synopsis:
      'Witness the most pervasive storm-god combat myth across Indo-European, Semitic, and Asian traditions: the champion of celestial lightning clashing with the colossal multi-headed water dragon of the chaotic depths.',
    traditionTags: ['Mesopotamian', 'Levantine', 'Greco-Roman', 'Norse & Germanic', 'East Asian', 'North American Indigenous'],
    stops: [
      {
        mythId: 'Q190864',
        chapterNumber: 1,
        chapterTitle: 'The Cleaving of the Salt Sea Beast',
        mythName: 'Enuma Elish (Marduk vs Tiamat)',
        culture: 'Mesopotamian',
        year: -1750,
        lat: 32.536,
        lng: 44.42,
        narrativeLead:
          'When primordial mother Tiamat spawned an army of horned vipers and sea monsters to swallow the universe, young storm-champion Marduk rode the cyclone chariot, drove the four winds down her throat, and split her carcass like a shellfish to form heaven and earth.',
        comparativeInsight:
          'The foundational archetype of Chaoskampf: cosmogony through violence, where order must be physically carved out of untamed oceanic chaos.',
        keyMotifs: ['Four Winds Arrow', 'Tiamat Salt Water Dragon', 'Splitting the Beast', 'Creation of Heaven and Earth'],
      },
      {
        mythId: 'Q131379',
        chapterNumber: 2,
        chapterTitle: 'The Seven-Headed Twisting Serpent',
        mythName: 'Baal vs Lotan (The Ugaritic Cycle)',
        culture: 'Levantine',
        year: -1400,
        lat: 35.6,
        lng: 35.78,
        narrativeLead:
          'On the limestone bluffs of ancient Ugarit, storm-rider Baal Hadad wielded dual enchanted maces forged by the divine artisan Kothar, battering Yam (Sea) and slaughtering Lotan, the seven-headed coiled serpent.',
        comparativeInsight:
          'Lotan is the direct etymological and mythical ancestor of the biblical Leviathan and the Revelation seven-headed sea beast.',
        keyMotifs: ['Seven-Headed Dragon', 'Enchanted Maces', 'Storm God Baal', 'Taming of the Coastal Seas'],
      },
      {
        mythId: 'Q12227',
        chapterNumber: 3,
        chapterTitle: 'The Arrows at the Sacred Omphalos',
        mythName: 'Apollo Slaying Python at Delphi',
        culture: 'Greco-Roman',
        year: -800,
        lat: 38.48,
        lng: 22.5,
        narrativeLead:
          'Newly born on Delos, golden sun-archer Apollo flew to Mount Parnassus and fired a hundred shafts of bronze into Python, the chthonic earth-dragon of Gaia, establishing the Delphic oracle upon the navel of the world.',
        comparativeInsight:
          'Represents the historic replacement of ancient matriarchal earth-serpent cults by Olympian solar patriarchy and rational prophecy.',
        keyMotifs: ['Omphalos Navel Stone', 'Python of Mount Parnassus', 'Golden Solar Arrows', 'Establishment of Delphi'],
      },
      {
        mythId: 'Q42952',
        chapterNumber: 4,
        chapterTitle: 'The Ox-Head Bait & the Midgard Wyrm',
        mythName: "Thor's Fishing Trip for Jörmungandr",
        culture: 'Norse & Germanic',
        year: 800,
        lat: 59.85,
        lng: 17.63,
        narrativeLead:
          'Rowing far beyond the safe coastal banks with giant Hymir, Thor baited a huge iron hook with the head of a black ox. When Jörmungandr took the bait, Thor smashed his feet through the boat bottom onto the sea floor to haul the world-encircling serpent up.',
        comparativeInsight:
          'A foreboding rehearsal for Ragnarök, where the thunder-god and world-serpent are destined to mutually annihilate each other.',
        keyMotifs: ['Black Ox Head Bait', 'Midgard Serpent', 'Smashed Boat Bottom', 'Mjölnir Strike'],
      },
      {
        mythId: 'Q131610',
        chapterNumber: 5,
        chapterTitle: 'The Eight Vats of Refined Sake',
        mythName: 'Susanoo Slaying Yamata no Orochi',
        culture: 'East Asian',
        year: 712,
        lat: 35.36,
        lng: 133.05,
        narrativeLead:
          'Exiled storm deity Susanoo found an elderly couple weeping over their eighth daughter, marked for sacrifice to the eight-headed, eight-tailed dragon Yamata no Orochi. He prepared eight vats of sake to intoxicate the beast before dismembering it, discovering the sacred Kusanagi sword inside its tail.',
        comparativeInsight:
          'Shows how the Chaoskampf produces the sacred regalia of the imperial state—the Grass-Cutting Sword that validates political sovereignty.',
        keyMotifs: ['Eight-Headed Serpent', 'Vats of Brewed Sake', 'Kusanagi Sacred Sword', 'Imperial Regalia'],
      },
      {
        mythId: 'Q2302329',
        chapterNumber: 6,
        chapterTitle: 'The Blazing Jewel of the Great Deep',
        mythName: 'The Horned Serpent Uktena',
        culture: 'North American Indigenous',
        year: 1150,
        lat: 35.59,
        lng: -83.51,
        narrativeLead:
          'In Cherokee cosmology, the Uktena was a colossal horned serpent with deer antlers and a blinding diamond (Ulunsuti) upon its forehead, dwelling in mountain pools and emitting a venomous breath that struck down any who looked directly into its luminous eye.',
        comparativeInsight:
          'Demonstrates the pan-global presence of the horned water monster: not as evil, but as dangerous primeval sacred power associated with underground aquifers and healing medicine.',
        keyMotifs: ['Ulunsuti Blazing Diamond', 'Horned Underwater Panther', 'Venomous Chthonic Power', 'Appalachian Deep Waters'],
      },
    ],
  },
];
