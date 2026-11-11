package com.agri.tomatodisease.service;

import com.agri.tomatodisease.model.DiseaseEntity;
import com.agri.tomatodisease.repository.DiseaseEntityRepository;
import jakarta.annotation.PostConstruct;
import org.springframework.stereotype.Service;

import java.util.*;

@Service
public class DiseaseCatalogService {

    private final DiseaseEntityRepository repository;

    public DiseaseCatalogService(DiseaseEntityRepository repository) {
        this.repository = repository;
    }

    @PostConstruct
    public void seedInitialCatalog() {
        if (repository.count() > 0) {
            return;
        }

        List<DiseaseEntity> seeds = new ArrayList<>();

        // 1. Bacterial Spot
        seeds.add(createEntity(
                "Tomato___Bacterial_spot",
                "Bacterial Spot",
                "Xanthomonas campestris pv. vesicatoria",
                "Bacterial",
                "[\"Small dark brown-black circular water-soaked spots (<3mm)\", \"Chlorotic yellow halos surrounding lesions\", \"Angular, scab-like appearance on mature leaves\", \"Extensive blighting and defoliation causing fruit sunscald\"]",
                "[\"Infected seed or greenhouse transplant stock\", \"Warm temperatures (24-30°C) with elevated humidity (>80%)\", \"Rain splash and overhead irrigation propelling bacteria across canopy\", \"Infection through natural stomatal openings or abrasion wounds\"]",
                "{\"temp_range\": [24.0, 30.0], \"humidity_threshold\": 80.0, \"precipitation_risk\": \"High (rain splash)\", \"vpd_risk\": \"< 0.8 kPa (high surface moisture)\"}",
                "[\"Apply fixed copper bactericides combined with Bacillus amyloliquefaciens\", \"Cold-pressed neem oil sprays early morning\", \"Compost tea foliar sprays to build leaf surface microbiome\", \"Prune and destroy infected lower foliage\"]",
                "[\"Copper hydroxide (Kocide 3000) tank-mixed with Mancozeb\", \"Streptomycin or Kasugamycin where agricultural antibiotics are permitted\", \"Acibenzolar-S-methyl for systemic acquired resistance induction\"]",
                "[\"Use certified pathogen-free, hot-water treated seeds (50°C for 25 min)\", \"Switch to drip irrigation beneath plastic mulch\", \"Implement 3-year crop rotation away from solanaceous plants\", \"Disinfect pruning tools with 10% bleach solution between rows\"]"
        ));

        // 2. Early Blight
        seeds.add(createEntity(
                "Tomato___Early_blight",
                "Early Blight",
                "Alternaria solani",
                "Fungal",
                "[\"Circular brown-black spots with distinct concentric rings ('bullseye' or 'target-board' pattern)\", \"Surrounding chlorotic yellow halos spreading across the leaf\", \"Infection begins on oldest lower leaves and climbs upward\", \"Sunken leathery stem cankers and fruit stem-end rot\"]",
                "[\"Soilborne mycelia and conidia overwintering in unburied crop residues\", \"Alternating cycles of high humidity/heavy dew followed by warm days (24-29°C)\", \"Plant stress from heavy fruit set or nutritional nitrogen exhaustion\", \"Wind and rain-driven conidial dispersal\"]",
                "{\"temp_range\": [22.0, 30.0], \"humidity_threshold\": 75.0, \"precipitation_risk\": \"Moderate to High\", \"vpd_risk\": \"Fluctuating between 0.5 and 1.8 kPa\"}",
                "[\"Biofungicide sprays with Bacillus subtilis (Serenade ASO) or Trichoderma harzianum\", \"Copper soap / copper octanoate applied every 7-10 days\", \"Potassium bicarbonate foliar sprays to shift leaf pH\", \"Prune the lowest 12-18 inches of canopy foliage\"]",
                "[\"Chlorothalonil (Bravo WeatherStik) as preventive contact protectant\", \"Azoxystrobin + Difenoconazole (Amistar Top) for systemic curative control\", \"Pyraclostrobin (Cabrio) applied during early canopy closure\"]",
                "[\"Thick organic or plastic mulching to eliminate soil-splash inoculations\", \"Enforce a minimum 3-year solanaceous crop rotation\", \"Stake and prune indeterminate vines to enhance air movement\", \"Ensure balanced nitrogen fertilization throughout vegetative growth\"]"
        ));

        // 3. Late Blight
        seeds.add(createEntity(
                "Tomato___Late_blight",
                "Late Blight",
                "Phytophthora infestans",
                "Oomycete / Water Mold",
                "[\"Irregular rapidly expanding water-soaked pale-green to dark brown lesions\", \"Delicate white downy fungal-like sporulation on leaf undersides in humid conditions\", \"Catastrophic foliar collapse appearing frosted or burned\", \"Greasy dark brown firm leathery rot on green and ripe fruits\"]",
                "[\"Airborne sporangia carried for miles on storm fronts and humid wind currents\", \"Cool, damp weather (15-22°C) with persistent relative humidity (>90%)\", \"Continuous free water or heavy dew on foliage for >6-8 hours\", \"Extreme reproduction rate capable of total crop loss within 4-7 days\"]",
                "{\"temp_range\": [14.0, 22.0], \"humidity_threshold\": 90.0, \"precipitation_risk\": \"Critical (frequent rain / persistent fog)\", \"vpd_risk\": \"< 0.4 kPa (saturated boundary air)\"}",
                "[\"Preventive copper hydroxide / Bordeaux mixture at first regional forecast warning\", \"Bacillus amyloliquefaciens as biological shield\", \"Immediate total rogueing and bagging of infected plants on dry afternoons\", \"Never compost infected tissue—deep bury (>2 ft) or burn immediately\"]",
                "[\"Mandipropamid (Revus) or Cyazofamid (Ranman) - specialized oomycete inhibitors\", \"Mefenoxam / Metalaxyl (Ridomil Gold) in rotation with Fluopicolide\", \"Mancozeb or Chlorothalonil as tank-mix anti-resistance partners\"]",
                "[\"Track AgERA5 microclimatic late-blight risk forecasting daily\", \"Plant resistant cultivars (Mountain Magic, Defiant, Plum Regal)\", \"Eradicate all volunteer potato and tomato plants in field vicinity\", \"Maximize row spacing along the path of prevailing dry winds\"]"
        ));

        // 4. Leaf Mold
        seeds.add(createEntity(
                "Tomato___Leaf_Mold",
                "Leaf Mold",
                "Passalora fulva (Cladosporium)",
                "Fungal",
                "[\"Pale yellowish-green chlorotic patches with indefinite margins on upper leaf blade\", \"Dense olive-green to velvet brown moldy spore mat on corresponding lower surface\", \"Leaves curl, wilt, wither, and drop prematurely from the lower canopy upwards\", \"Blossom rot and blossom drop causing severe yield reduction\"]",
                "[\"High relative humidity (>85%) inside greenhouses, polytunnels, or dense field canopies\", \"Moderate temperatures (20-25°C) with restricted air turbulence\", \"Poor ventilation and overcrowded planting geometry\", \"Conidia surviving for over a year on structural stakes and greenhouse plastic\"]",
                "{\"temp_range\": [20.0, 26.0], \"humidity_threshold\": 85.0, \"precipitation_risk\": \"Moderate (high condensation risk)\", \"vpd_risk\": \"< 0.6 kPa\"}",
                "[\"Aggressive ventilation and dehumidification to hold ambient RH below 85%\", \"Bio-fungicide sprays with Streptomyces lydicus (Actinovate) or Bacillus subtilis\", \"Soluble potassium silicate sprays to harden leaf cell walls\", \"Liquid copper octanoate application to leaf undersides\"]",
                "[\"Boscalid + Pyraclostrobin (Pristine)\", \"Difenoconazole (Inspire Super)\", \"Chlorothalonil targeted directly at lower leaf surfaces\"]",
                "[\"Install horizontal airflow (HAF) circulation fans in protected structures\", \"Prune suckers and senescent foliage for maximum interior light penetration\", \"Select cultivars possessing Cf resistance genes (Cf-4, Cf-9)\", \"Thoroughly sterilize greenhouse structures with peracetic acid between crops\"]"
        ));

        // 5. Septoria Leaf Spot
        seeds.add(createEntity(
                "Tomato___Septoria_leaf_spot",
                "Septoria Leaf Spot",
                "Septoria lycopersici",
                "Fungal",
                "[\"Numerous circular lesions (1.5-3mm) with dark brown borders and grayish-white sunken centers\", \"Tiny black specks (pycnidia fruiting bodies) discernible in the center of spots\", \"Rapid yellowing of leaf tissue surrounding spots followed by leaf drop\", \"Extensive upward defoliation exposing green tomatoes to sunscald\"]",
                "[\"Soilborne pycnidia surviving on solanaceous residues and wild weed hosts\", \"Prolonged leaf wetness paired with warm temperatures (20-26°C)\", \"Raindrops splashing pycnidiospores upward from infected soil onto basal foliage\", \"Handling plants while leaves are wet with early morning dew\"]",
                "{\"temp_range\": [20.0, 27.0], \"humidity_threshold\": 80.0, \"precipitation_risk\": \"High (rain splash dispersal)\", \"vpd_risk\": \"< 0.7 kPa\"}",
                "[\"Liquid copper sulfate or copper soap sprays on 7-day intervals\", \"Biofungicide Bacillus amyloliquefaciens strain D747\", \"Neem extract formulations as protective fungistatic barrier\", \"Prompt manual removal of early-spotted bottom leaflets\"]",
                "[\"Chlorothalonil applied preventively from transplanting forward\", \"Azoxystrobin rotated with Mancozeb\", \"Penthiopyrad (Fontelis) or Trifloxystrobin\"]",
                "[\"Apply clean straw or plastic mulch immediately upon transplanting\", \"Strictly avoid overhead irrigation; use drip irrigation exclusively\", \"Maintain 3-year rotational separation from solanaceous crops\", \"Sanitize trellising stakes with 10% bleach prior to new season\"]"
        ));

        // 6. Spider Mites
        seeds.add(createEntity(
                "Tomato___Spider_mites_Two_spotted_spider_mite",
                "Two-Spotted Spider Mites",
                "Tetranychus urticae",
                "Arachnid Pest",
                "[\"Fine yellow, white, or bronze stippling / tiny speckled dots covering upper leaf lamina\", \"Fine silky webbing visible on undersides of leaves, growing shoots, and petioles\", \"Leaves turn yellow-bronze, become dry and brittle like parchment, and drop\", \"Stunted terminal growth and total canopy desiccation\"]",
                "[\"Hot, dry, and dusty microclimate (temperatures 28-35°C with relative humidity <50%)\", \"Over-application of broad-spectrum synthetic pyrethroids killing natural predatory mites\", \"Drought stress increasing leaf soluble nitrogen content favorable for mite feeding\", \"Ultra-short egg-to-adult generation span (under 5 days in hot conditions)\"]",
                "{\"temp_range\": [28.0, 38.0], \"humidity_threshold\": 45.0, \"precipitation_risk\": \"Low (drought stimulates population surge)\", \"vpd_risk\": \"> 1.8 kPa (high evaporative stress)\"}",
                "[\"Release predatory biological mites: Phytoseiulus persimilis or Neoseiulus californicus\", \"Spray insecticidal soap (potassium salts of fatty acids) targeting leaf undersides\", \"Cold-pressed pure Neem oil (1% emulsion) with wetting agent\", \"Overhead high-pressure water rinse to knock down web colonies during peak heat\"]",
                "[\"Bifenazate (Acramite) - selective miticide safe for beneficial predators\", \"Abamectin (Agri-Mek) translaminar acaricide\", \"Spiromesifen (Oberon) or Hexythiazox targeting juvenile mite stages\"]",
                "[\"Maintain steady drip irrigation to prevent crop moisture stress and wilting\", \"Dampen perimeter farm access tracks to suppress blowing road dust\", \"Avoid excessive synthetic nitrogen fertigation\", \"Regular scouting of lower leaf undersides with 15x magnifier\"]"
        ));

        // 7. Target Spot
        seeds.add(createEntity(
                "Tomato___Target_Spot",
                "Target Spot",
                "Corynespora cassiicola",
                "Fungal",
                "[\"Small brown pinpoint spots growing into circular necrotic lesions with concentric rings\", \"Lesions display light tan centers with dark brown concentric margins\", \"Dead center of lesions often cracks and tears out forming a 'shot-hole' appearance\", \"Deep pitted brown crater lesions on developing green and ripe fruits\"]",
                "[\"Warm, humid subtropical weather (25-32°C and relative humidity >80%)\", \"Dense foliage retaining moisture on lower canopy leaves for prolonged hours\", \"Pathogen survival on solanaceous weeds and unplowed crop debris\", \"Airborne and splash dissemination of conidiospores\"]",
                "{\"temp_range\": [25.0, 32.0], \"humidity_threshold\": 80.0, \"precipitation_risk\": \"High (frequent warm precipitation)\", \"vpd_risk\": \"0.6 - 1.2 kPa\"}",
                "[\"Preventative liquid copper sprays applied prior to canopy closure\", \"Biofungicides containing Bacillus amyloliquefaciens\", \"Aggressive lower canopy pruning to permit direct sunlight and air penetration\", \"Complete gathering and deep burial of dropped fruit and infected foliage\"]",
                "[\"Pyraclostrobin + Fluxapyroxad (Priaxor)\", \"Boscalid (Endura)\", \"Chlorothalonil + Famoxadone\"]",
                "[\"Provide wide plant spacing (at least 60-75cm between plants)\", \"Train vines upright on tall trellises off the ground\", \"Eradicate nightshade weed species surrounding field perimeters\", \"Perform deep tillage post-harvest to decompose fungal debris\"]"
        ));

        // 8. Tomato Yellow Leaf Curl Virus
        seeds.add(createEntity(
                "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
                "Yellow Leaf Curl Virus (TYLCV)",
                "Begomovirus / Geminiviridae",
                "Viral (Whitefly Vector)",
                "[\"Severe upward rolling, cupping, and crinkling of leaf margins into a 'spoon' shape\", \"Prominent interveinal chlorosis: vivid yellowing of leaf borders while veins remain green\", \"Marked reduction in leaflet size; foliage becomes thick, brittle, and leathery\", \"Severe plant stunting, erect bushy 'bonsai' architecture, and near total flower abortion\"]",
                "[\"Persistent transmission by the Sweetpotato Whitefly (Bemisia tabaci)\", \"Hot, dry tropical and subtropical conditions favoring explosive whitefly reproduction\", \"Weed reservoirs (Malva, Datura, Solanum) maintaining virus in surrounding ecology\", \"Long-distance wind dispersal of viruliferous whiteflies\"]",
                "{\"temp_range\": [26.0, 36.0], \"humidity_threshold\": 50.0, \"precipitation_risk\": \"Low (dry weather maximizes vector flight)\", \"vpd_risk\": \"> 1.5 kPa\"}",
                "[\"No direct plant cure exists; immediately rogue, bag, and burn infected plants\", \"Deploy yellow sticky insect monitoring cards above crop canopy\", \"Install aluminized reflective silver mulch to disorient incoming whiteflies\", \"Spray Beauveria bassiana (entomopathogenic fungus) for biological whitefly control\"]",
                "[\"Systemic neonicotinoids (Imidacloprid, Thiamethoxam) applied at nursery transplanting\", \"Cyantraniliprole (Verimark / Exirel) diamide insecticide\", \"Pyriproxyfen or Spiromesifen insect growth regulators to disrupt nymph cycles\"]",
                "[\"Plant certified TYLCV-resistant hybrid tomato varieties (Tyking, SV7846TH)\", \"Cover seedling beds with 50-mesh whitefly-proof insect exclusion netting\", \"Enforce a mandatory 2-month host-free window between tomato planting seasons\", \"Eradicate all broadleaf weeds around greenhouses and farm borders\"]"
        ));

        // 9. Tomato Mosaic Virus
        seeds.add(createEntity(
                "Tomato___Tomato_mosaic_virus",
                "Tomato Mosaic Virus (ToMV)",
                "Tobamovirus",
                "Viral (Mechanical Contact)",
                "[\"Alternating dark green and light yellowish-green mosaic mottling on leaf surfaces\", \"Severe leaflet distortion: 'shoestringing' and fern-like narrowing of leaves\", \"Raised blister-like dark green islands on upper leaf lamina\", \"Internal brown necrosis within fruit walls and uneven blotchy fruit ripening\"]",
                "[\"Exceptional environmental stability; transmitted mechanically via hands, tools, and clothing\", \"Seedborne on the seed coat (testa) of uncertified seed stocks\", \"Smokers handling plants with tobacco-contaminated hands\", \"Survival for years in dry root debris and contaminated greenhouse soil\"]",
                "{\"temp_range\": [20.0, 30.0], \"humidity_threshold\": 60.0, \"precipitation_risk\": \"Any (mechanical transmission)\", \"vpd_risk\": \"Any\"}",
                "[\"No curative antiviral spray exists; immediately rogue and destroy diseased vines\", \"Sanitize hands and tools with whole milk or 20% non-fat dry milk solution\", \"Steam pasteurization of greenhouse soil and seedling trays before replanting\", \"Promptly burn infected crop residues away from cultivation area\"]",
                "[\"No chemical curative sprays are effective against plant viruses\", \"Trisodium phosphate (TSP) 10% solution for thorough equipment and tray sterilization\", \"Chitosan oligosaccharide elicitor sprays to induce systemic plant resilience\"]",
                "[\"Select certified virus-resistant varieties carrying Tm-1 or Tm-2² resistance alleles\", \"Treat seed stocks with 10% trisodium phosphate for 30 minutes before sowing\", \"Strict ban on tobacco use and smoking within 100 meters of tomato greenhouses\", \"Dip pruning shears into virucidal disinfectant between every plant pruned\"]"
        ));

        // 10. Healthy
        seeds.add(createEntity(
                "Tomato___healthy",
                "Healthy Tomato Leaf",
                "Solanum lycopersicum (Optimal Health)",
                "Healthy / Vigorous",
                "[\"Vibrant, deep uniform emerald green leaflet coloration\", \"Clean, intact leaf margins with characteristic serrations and smooth epidermal texture\", \"Complete absence of chlorosis, necrosis, water-soaked spots, webbing, or viral mottling\", \"Robust turgid petioles and vigorous vegetative photosynthetic canopy\"]",
                "[\"Balanced macro and micronutrient fertility (N-P-K, Ca, Mg, Fe, Zn)\", \"Microclimate falling directly into optimal tomato physiological comfort zone\", \"Consistent drip irrigation maintaining soil water tension at field capacity (-10 to -30 kPa)\", \"Rigorous preventative Integrated Pest and Disease Management (IPM) practices\"]",
                "{\"temp_range\": [20.0, 26.0], \"humidity_threshold\": 65.0, \"precipitation_risk\": \"Well-drained\", \"vpd_risk\": \"Optimal (0.8 - 1.3 kPa)\"}",
                "[\"Continue regular biostimulant sprays with cold-water Kelp extract or fish hydrolysate\", \"Inoculate root zone with beneficial mycorrhizal fungi (Glomus intraradices)\", \"Apply soluble silica foliar nutrition to reinforce plant cuticle cell walls\", \"Maintain soil biology with vermicompost topdressings\"]",
                "[\"No corrective chemical applications necessary\", \"Maintain weekly scouting routine using yellow and blue sticky traps\", \"Periodic prophylactic micronutrient foliar feeding (chelated zinc, boron)\"]",
                "[\"Maintain strict field sanitary hygiene on pruning and trellising tools\", \"Follow balanced fertigation schedules according to plant phenological growth stages\", \"Ensure proper plant spacing and weed suppression with mulch\", \"Continuously monitor local AgERA5 weather trends to anticipate disease pressures\"]"
        ));

        repository.saveAll(seeds);
        System.out.println("Seeded " + seeds.size() + " PlantVillage tomato disease classes into the database.");
    }

    public List<DiseaseEntity> getAllDiseases() {
        return repository.findAll();
    }

    public Optional<DiseaseEntity> getDiseaseByKey(String diseaseKey) {
        return repository.findByDiseaseKey(diseaseKey);
    }

    private DiseaseEntity createEntity(String key, String commonName, String scientificName, String category,
                                       String symptoms, String reasons, String agera5, String organic,
                                       String chemical, String prevention) {
        DiseaseEntity e = new DiseaseEntity();
        e.setDiseaseKey(key);
        e.setCommonName(commonName);
        e.setScientificName(scientificName);
        e.setCategory(category);
        e.setSymptomsJson(symptoms);
        e.setReasonsJson(reasons);
        e.setAgera5TriggersJson(agera5);
        e.setOrganicTreatmentJson(organic);
        e.setChemicalTreatmentJson(chemical);
        e.setPreventionJson(prevention);
        return e;
    }
}
