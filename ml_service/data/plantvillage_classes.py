"""
PlantVillage Dataset Tomato Disease Class Definitions and Agronomic Metadata
=============================================================================
Contains canonical class mappings, scientific pathogen names, visual symptoms,
environmental trigger parameters, and treatment protocols for all 10 classes.
"""

PLANTVILLAGE_TOMATO_CLASSES = [
    "Tomato___Bacterial_spot",
    "Tomato___Early_blight",
    "Tomato___Late_blight",
    "Tomato___Leaf_Mold",
    "Tomato___Septoria_leaf_spot",
    "Tomato___Spider_mites_Two_spotted_spider_mite",
    "Tomato___Target_Spot",
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
    "Tomato___Tomato_mosaic_virus",
    "Tomato___healthy"
]

DISEASE_METADATA = {
    "Tomato___Bacterial_spot": {
        "common_name": "Bacterial Spot",
        "scientific_name": "Xanthomonas campestris pv. vesicatoria",
        "category": "Bacterial",
        "symptoms": [
            "Small (less than 3mm), dark brown-black circular water-soaked spots on leaves",
            "Yellow halo (chlorotic margin) around lesions",
            "Lesions become angular and scab-like as they mature",
            "Severe blighting, leaf drop, and defoliation leading to sunscald on fruits"
        ],
        "reasons": [
            "Infected seed or infected transplant seedlings",
            "High relative humidity (>80%) accompanied by warm temperatures (24-30°C)",
            "Rain splash or overhead sprinkler irrigation dispersing bacteria across foliage",
            "Pathogen enters through natural openings (stomata, hydathodes) or mechanical abrasions"
        ],
        "agera5_triggers": {
            "temp_range": [24.0, 30.0],
            "humidity_threshold": 80.0,
            "precipitation_risk": "High (rain splash spreading)",
            "vpd_risk": "Low (< 0.8 kPa indicates prolonged leaf wetness)"
        },
        "organic_treatment": [
            "Apply copper octanoate or fixed copper bactericide combined with Bacillus amyloliquefaciens",
            "Spray certified neem oil or horticultural oils early in the morning",
            "Compost tea spray to build beneficial leaf surface phyllosphere microbes",
            "Remove and incinerate severely infected lower leaves"
        ],
        "chemical_treatment": [
            "Copper hydroxide (e.g. Kocide 3000) mixed with Mancozeb (protectant synergy)",
            "Streptomycin sulfate or Kasugamycin (in regions where agricultural antibiotics are approved)",
            "Acibenzolar-S-methyl (systemic acquired resistance inducer)"
        ],
        "prevention": [
            "Use certified pathogen-free, hot-water treated seeds (50°C for 25 min)",
            "Employ drip irrigation instead of overhead watering to keep foliage dry",
            "Maintain at least a 2-3 year crop rotation away from solanaceous crops (peppers, eggplants)",
            "Sterilize pruning tools with 10% bleach or 70% isopropyl alcohol between plants"
        ]
    },
    "Tomato___Early_blight": {
        "common_name": "Early Blight",
        "scientific_name": "Alternaria solani",
        "category": "Fungal",
        "symptoms": [
            "Circular brown-black spots with distinct concentric rings ('target board' / 'bullseye' pattern)",
            "Chlorotic yellowing around leaf lesions spreading to entire leaflet",
            "Infection starts on the oldest lower leaves and progresses upward",
            "Stem collar rot and sunken dark leathery lesions at stem base or fruit calyx"
        ],
        "reasons": [
            "Overwintering fungal mycelia and conidia in infected crop debris and soil",
            "Alternating periods of heavy dew/rain followed by warm, sunny days (24-29°C)",
            "Plant stress caused by heavy fruit load, nitrogen deficiency, or drought cycles",
            "Conidia carried by wind, splashing rain, or farm machinery"
        ],
        "agera5_triggers": {
            "temp_range": [22.0, 30.0],
            "humidity_threshold": 75.0,
            "precipitation_risk": "Moderate to High (frequent dew cycles)",
            "vpd_risk": "Fluctuating between 0.5 kPa (wet nights) and 1.8 kPa (dry days)"
        },
        "organic_treatment": [
            "Spray bio-fungicide Bacillus subtilis (Serenade ASO) or Trichoderma harzianum",
            "Apply copper soap / copper octanoate every 7-10 days",
            "Potassium bicarbonate foliar spray (MilStop) to alter leaf surface pH",
            "Prune off the lowest 12-18 inches of foliage to stop soil-splash inoculation"
        ],
        "chemical_treatment": [
            "Chlorothalonil (Bravo WeatherStik) as a protective contact fungicide",
            "Azoxystrobin (Heritage) or Pyraclostrobin (strobilurin class fungicides)",
            "Difenoconazole + Azoxystrobin (Amistar Top) for curative and translaminar control"
        ],
        "prevention": [
            "Thoroughly mulch soil with clean straw or plastic to create a splash barrier",
            "3-year crop rotation avoiding tomato, potato, eggplant, and solanaceous weeds",
            "Stake and prune indeterminate vines to enhance air circulation and quick leaf drying",
            "Incorporate balanced fertilization, avoiding nitrogen exhaustion during fruit swell"
        ]
    },
    "Tomato___Late_blight": {
        "common_name": "Late Blight",
        "scientific_name": "Phytophthora infestans",
        "category": "Oomycete / Water Mold",
        "symptoms": [
            "Irregular, rapidly enlarging water-soaked pale-green to dark-brown lesions",
            "Delicate white downy fungal-like sporulation visible on undersides of leaves under humid conditions",
            "Rapid collapse and browning of foliage (leaves look frost-damaged or scorched)",
            "Dark brown greasy or leathery rot on green and ripe tomato fruits"
        ],
        "reasons": [
            "Windborne sporangia travelling miles from infected potato cull piles or greenhouse sources",
            "Cool, damp, fog-laden weather (temperatures 15-22°C with persistent RH > 90%)",
            "Free water persisting on leaf surfaces for > 6-8 continuous hours",
            "Extremely high reproduction rate: explosive epidemic potential within 3-5 days"
        ],
        "agera5_triggers": {
            "temp_range": [14.0, 22.0],
            "humidity_threshold": 90.0,
            "precipitation_risk": "Critical (frequent rain, heavy fog, prolonged dew)",
            "vpd_risk": "Very Low (< 0.4 kPa, saturated atmosphere)"
        },
        "organic_treatment": [
            "Copper hydroxide / Bordeaux mixture applied immediately upon disease forecast alert",
            "Biological suppressants like Bacillus amyloliquefaciens (preventative only)",
            "Aggressive rogued destruction: uproot and bag entire diseased plants during dry midday",
            "Never compost infected vines—burn or deep-bury (>2 feet) immediately"
        ],
        "chemical_treatment": [
            "Mandipropamid (Revus) or Cyazofamid (Ranman) - highly targeted oomycete specialists",
            "Metalaxyl / Mefenoxam (Ridomil Gold) in rotation with Fluopicolide (Presidio)",
            "Mancozeb or Chlorothalonil as tank-mix protectants to prevent fungicide resistance"
        ],
        "prevention": [
            "Monitor local late-blight forecast systems (e.g. BlightCast / AgERA5 threshold monitors)",
            "Plant resistant tomato cultivars (e.g. Mountain Magic, Defiant PhR, Plum Regal)",
            "Eliminate volunteer tomato and potato plants within 500 meters of fields",
            "Keep high row spacing and orient crop rows in the direction of prevailing winds"
        ]
    },
    "Tomato___Leaf_Mold": {
        "common_name": "Leaf Mold",
        "scientific_name": "Passalora fulva (syn. Cladosporium fulvum)",
        "category": "Fungal",
        "symptoms": [
            "Pale green to distinct yellowish chlorotic spots on the upper leaf surface with diffuse margins",
            "Dense, olive-green to velvet brown moldy spore patches directly beneath spots on the lower leaf surface",
            "Leaves curl, wilt, turn brown, and drop prematurely starting from lower canopy",
            "Blossoms and developing fruits occasionally become infected and abort"
        ],
        "reasons": [
            "High relative humidity (>85%) inside high tunnels, polyhouses, or dense field canopies",
            "Moderate to warm temperatures (20-25°C)",
            "Poor air circulation and close plant spacing in protected agriculture",
            "Conidia survive for over a year in greenhouse structural cracks, stakes, or debris"
        ],
        "agera5_triggers": {
            "temp_range": [20.0, 26.0],
            "humidity_threshold": 85.0,
            "precipitation_risk": "Moderate (driven primarily by greenhouse condensation/humidity)",
            "vpd_risk": "Low (< 0.6 kPa)"
        },
        "organic_treatment": [
            "Exhaustive ventilation and heating to drive humidity below 85%",
            "Bio-fungicides: Bacillus subtilis or Streptomyces lydicus (Actinovate)",
            "Potassium silicate sprays to strengthen leaf epidermal cuticles",
            "Copper octanoate foliar spray"
        ],
        "chemical_treatment": [
            "Boscalid + Pyraclostrobin (Pristine)",
            "Difenoconazole (Inspire Super)",
            "Chlorothalonil applied thoroughly to under-leaf surfaces"
        ],
        "prevention": [
            "Install horizontal airflow (HAF) circulation fans in polytunnels",
            "Prune suckers and lower senescent leaves to allow sunlight penetration",
            "Select Cf-gene resistant varieties (e.g. varieties with Cf-9, Cf-5 resistance genes)",
            "Disinfect greenhouse surfaces with quaternary ammonium or peracetic acid before planting"
        ]
    },
    "Tomato___Septoria_leaf_spot": {
        "common_name": "Septoria Leaf Spot",
        "scientific_name": "Septoria lycopersici",
        "category": "Fungal",
        "symptoms": [
            "Numerous small (1.5-3mm), circular spots with dark brown margins and sunken grayish-white centers",
            "Tiny black specks (pycnidia - fruiting bodies) visible with hand lens in lesion centers",
            "Leaves turn yellow around spots, wither, dry out, and drop prematurely",
            "Extensive defoliation exposing green fruit to severe sunscald damage"
        ],
        "reasons": [
            "Soilborne pycnidia surviving on solanaceous crop debris and weed hosts (e.g. Horsenettle)",
            "Prolonged leaf wetness and warm temperatures (20-26°C)",
            "Raindrop splashing propelling pycnidiospores from soil onto lower leaves",
            "Foliage handled or worked while leaves are wet with morning dew"
        ],
        "agera5_triggers": {
            "temp_range": [20.0, 27.0],
            "humidity_threshold": 80.0,
            "precipitation_risk": "High (rain splash primary dispersal mechanism)",
            "vpd_risk": "Low (< 0.7 kPa)"
        },
        "organic_treatment": [
            "Liquid copper fungicides (copper sulfate / copper diammonia diacetate complex)",
            "Bacillus amyloliquefaciens strain D747",
            "Neem seed oil extracts as botanical fungistatic barriers",
            "Prompt removal of all infected bottom foliage showing early spotting"
        ],
        "chemical_treatment": [
            "Chlorothalonil at 7-14 day intervals beginning at transplant establishment",
            "Azoxystrobin alternating with Mancozeb",
            "Trifloxystrobin (Flint) or Penthiopyrad (Fontelis)"
        ],
        "prevention": [
            "Apply thick organic mulch (straw, woodchips, or black plastic) immediately after transplanting",
            "Avoid overhead irrigation; use drip lines positioned beneath mulch",
            "Maintain strict 3-year crop rotation away from solanaceae",
            "Sanitize trellising stakes with 10% bleach solution before re-use"
        ]
    },
    "Tomato___Spider_mites_Two_spotted_spider_mite": {
        "common_name": "Two-Spotted Spider Mite Infestation",
        "scientific_name": "Tetranychus urticae",
        "category": "Arachnid Pest",
        "symptoms": [
            "Fine yellow, white, or bronze stippling / speckled dots across the upper leaf blade",
            "Fine silky webbing on undersides of leaves, growing tips, and leaf petioles",
            "Leaves become bleached, turn yellow or bronze, dry up, and feel brittle like paper",
            "Severe canopy defoliation and stunted plant growth"
        ],
        "reasons": [
            "Hot, dry, and dusty microclimate (temperatures > 28-35°C with low humidity < 50%)",
            "Overuse of broad-spectrum synthetic pyrethroids or carbamates that kill natural predator mites",
            "Water-stressed plants having higher leaf nitrogen concentrations favored by mites",
            "Rapid generation cycle: eggs to adults in just 5-7 days under hot conditions"
        ],
        "agera5_triggers": {
            "temp_range": [28.0, 38.0],
            "humidity_threshold": 45.0,  # favored by low humidity
            "precipitation_risk": "Low (drought conditions favor mite population explosions)",
            "vpd_risk": "High (> 1.8 kPa, dry evaporative demand)"
        },
        "organic_treatment": [
            "Release predatory biological mites: Phytoseiulus persimilis or Neoseiulus californicus",
            "Foliar spray with Insecticidal Soap (potassium salts of fatty acids) or Horticultural Oil",
            "Cold-pressed Neem Oil (0.5 - 1.0% emulsion) targeting leaf undersides",
            "High-pressure overhead water blast to physically dislodge mites and disrupt web colonies"
        ],
        "chemical_treatment": [
            "Bifenazate (Acramite) - selective miticide safe for beneficial predatory insects",
            "Abamectin (Agri-Mek) translaminar acaricide",
            "Spiromesifen (Oberon) or Etoxazole targeting mite eggs and nymph stages"
        ],
        "prevention": [
            "Ensure regular, adequate irrigation to avoid plant moisture stress and leaf wilting",
            "Keep perimeter roadways damp to suppress blowing road dust",
            "Avoid excessive synthetic nitrogen applications which stimulate mite oviposition",
            "Scout leaf undersides weekly with a 10x-20x hand lens"
        ]
    },
    "Tomato___Target_Spot": {
        "common_name": "Target Spot",
        "scientific_name": "Corynespora cassiicola",
        "category": "Fungal",
        "symptoms": [
            "Small brown pinpoint lesions expanding into large circular brown spots with concentric rings",
            "Lesions often exhibit a distinct pale or tan center with dark brown concentric halos",
            "Lesions can crack or fall out leaving a 'shot-hole' appearance",
            "Deep, sunken dark crater-like spots on green and ripe tomato fruit surfaces"
        ],
        "reasons": [
            "Warm, humid subtropical/tropical weather (25-32°C and RH > 80%)",
            "Dense canopy shading retaining moisture on lower leaves for prolonged hours",
            "Pathogen survives on alternate weed hosts and unburied crop residue",
            "Spreads via airborne conidia and rain splash"
        ],
        "agera5_triggers": {
            "temp_range": [25.0, 32.0],
            "humidity_threshold": 80.0,
            "precipitation_risk": "High (frequent warm showers)",
            "vpd_risk": "Moderate (0.6 - 1.2 kPa)"
        },
        "organic_treatment": [
            "Liquid copper fungicides applied as preventive coats",
            "Biofungicide: Bacillus amyloliquefaciens or Streptomyces lydicus",
            "Thorough bottom pruning to open the plant base to light and air movement",
            "Collection and deep burial of dropped infected leaves and fruits"
        ],
        "chemical_treatment": [
            "Pyraclostrobin + Fluxapyroxad (Priaxor)",
            "Boscalid (Endura)",
            "Chlorothalonil + Famoxadone / Cymoxanil"
        ],
        "prevention": [
            "Provide wide plant spacing (at least 60-75 cm between plants in the row)",
            "Train vines on tall stakes or trellis wires to lift foliage away from soil",
            "Eliminate nightshade family weeds surrounding field borders",
            "Deep-plow crop residue immediately following final harvest"
        ]
    },
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
        "common_name": "Tomato Yellow Leaf Curl Virus (TYLCV)",
        "scientific_name": "Begomovirus / Geminiviridae",
        "category": "Viral (Vector: Whitefly)",
        "symptoms": [
            "Severe upward curling, cupping, and crinkling of leaf margins ('spoon-shaped' leaves)",
            "Interveinal chlorosis: striking yellowing of leaf borders while veins remain greenish",
            "Noticeable reduction in leaf size, leaflets become distorted, thick, and leathery",
            "Extreme plant stunting with bushy 'bonsai' erect appearance and near 100% flower abortion"
        ],
        "reasons": [
            "Transmitted persistently by the Sweetpotato Whitefly (Bemisia tabaci)",
            "Hot, dry tropical and subtropical conditions that drive explosive whitefly proliferation",
            "Presence of virus reservoirs in nearby weeds (e.g. Malva, Datura) or infected crops",
            "Wind dispersal carrying viruliferous whiteflies over long distances"
        ],
        "agera5_triggers": {
            "temp_range": [26.0, 36.0],
            "humidity_threshold": 50.0,
            "precipitation_risk": "Low (dry spells maximize whitefly flight and transmission)",
            "vpd_risk": "Moderate to High (> 1.5 kPa)"
        },
        "organic_treatment": [
            "No direct antiviral cure exists—immediate rogueing and bagging of infected plants",
            "Yellow sticky traps placed above canopy to capture adult whiteflies",
            "Reflective silver / aluminized mulch to disorient incoming whiteflies",
            "Spray Beauveria bassiana (entomopathogenic fungus) or insecticidal potassium soaps"
        ],
        "chemical_treatment": [
            "Systemic neonicotinoids (Imidacloprid, Thiamethoxam) at transplanting for whitefly vector control",
            "Cyantraniliprole (Verimark/Exirel) diamide insecticide",
            "Pyriproxyfen or Spiromesifen insect growth regulators to interrupt whitefly nymph development"
        ],
        "prevention": [
            "Grow TYLCV-resistant or tolerant hybrid varieties (e.g. Tyking, Charger, SV7846TH)",
            "Install 50-mesh insect-exclusion netting over nursery seedling beds and greenhouse vents",
            "Maintain a 6-8 week host-free planting window between tomato crop seasons",
            "Eradicate weed hosts around field margins"
        ]
    },
    "Tomato___Tomato_mosaic_virus": {
        "common_name": "Tomato Mosaic Virus (ToMV)",
        "scientific_name": "Tobamovirus",
        "category": "Viral (Mechanically Transmitted)",
        "symptoms": [
            "Alternating light green and dark green mosaic / mottling patterns on leaf blades",
            "Leaf distortion: 'shoestringing' or fern-like thinning of leaflets",
            "Blister-like raised dark green areas on the upper leaf lamina",
            "Internal brown necrosis (browning) of fruit walls and uneven fruit ripening"
        ],
        "reasons": [
            "Extremely stable virus transmitted mechanically by hands, tools, grafting knives, and pruning shears",
            "Seedborne on the seed coat (testa) of uncertified tomato seeds",
            "Tobacco smokers handling plants with contaminated hands (tobacco contains related viruses)",
            "Virus can persist for years in dry root debris and contaminated greenhouse soil"
        ],
        "agera5_triggers": {
            "temp_range": [20.0, 30.0],
            "humidity_threshold": 60.0,
            "precipitation_risk": "Any (infection is mechanical/touch-based, not moisture-dependent)",
            "vpd_risk": "Any"
        },
        "organic_treatment": [
            "No chemical or organic curative spray can cure a virally infected plant",
            "Immediately rogue, bag, and destroy infected plants without brushing against healthy neighbors",
            "Wash hands and tools thoroughly with whole milk or 20% non-fat dry milk solution",
            "Steam sterilization of soil or potting medium prior to replanting"
        ],
        "chemical_treatment": [
            "No synthetic chemical curative agents exist for plant viruses",
            "Trisodium phosphate (TSP) 10% solution for thorough tool and surface sanitization",
            "Chitosan oligosaccharide sprays to stimulate plant systemic defense responses"
        ],
        "prevention": [
            "Plant ToMV-resistant cultivars carrying Tm-1, Tm-2, or Tm-2² resistance alleles",
            "Use certified virus-indexed seeds treated with trisodium phosphate (10% for 30 min)",
            "Strict no-smoking / no-tobacco policy in tomato nurseries and greenhouses",
            "Dip pruning shears in skim milk or virucidal disinfectant between every single plant"
        ]
    },
    "Tomato___healthy": {
        "common_name": "Healthy Tomato Leaf",
        "scientific_name": "Solanum lycopersicum (Optimal Health)",
        "category": "Healthy / Vigorous",
        "symptoms": [
            "Vibrant, uniform emerald green leaf color across all leaflets",
            "Intact leaf margins with characteristic serrations and smooth epidermal surface",
            "Absence of chlorosis, necrosis, water-soaking, pustules, webbing, or viral mottling",
            "Turgid, robust petiole and vigorous photosynthetic canopy development"
        ],
        "reasons": [
            "Optimal agronomic nutrient balance (N-P-K and trace micronutrients Ca, Mg, Fe, Zn)",
            "Favorable microclimatic AgERA5 conditions within the optimal vegetative comfort zone",
            "Well-regulated drip irrigation maintaining soil moisture at field capacity (-10 to -30 kPa)",
            "Effective preventative Integrated Pest and Disease Management (IPM) practices"
        ],
        "agera5_triggers": {
            "temp_range": [20.0, 26.0],
            "humidity_threshold": 65.0,
            "precipitation_risk": "Normal / Well-drained",
            "vpd_risk": "Optimal (0.8 - 1.3 kPa, facilitating healthy transpiration without stress)"
        },
        "organic_treatment": [
            "Continue proactive seaweed extract or fish emulsion biostimulant sprays",
            "Inoculate root zone with beneficial mycorrhizal fungi (Glomus intraradices)",
            "Apply foliar bio-fertilizers rich in silica to reinforce cellular cell walls",
            "Maintain soil organic matter through regular compost or vermicompost topdressing"
        ],
        "chemical_treatment": [
            "No corrective chemical fungicides or pesticides required",
            "Routine preventive scouting and monitoring with yellow and blue sticky traps",
            "Maintain baseline prophylactic micronutrient sprays (chelated iron, boron, zinc)"
        ],
        "prevention": [
            "Maintain clean field hygiene and sanitize all pruning and trellising equipment",
            "Stick to systematic soil testing and balanced fertigation schedules",
            "Ensure good row ventilation and mulch coverage to sustain optimal plant health",
            "Keep monitoring local AgERA5 weather trends to prepare for disease risk spikes"
        ]
    }
}
