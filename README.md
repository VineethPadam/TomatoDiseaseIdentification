# 🌿 AgroVision AI: Tomato Leaf Disease Identification System
### *A Multimodal Deep Learning & Agrometeorological Precision Health Framework*

> **Final Year Engineering Project**  
> **Model Architecture:** LeafVision-DINO (ViT-S/16 Vision Transformer with DINO Self-Supervision)  
> **Datasets:** PlantVillage Dataset (10 Tomato Disease Classes) & Copernicus AgERA5 v2.0 Agrometeorological Indicators  
> **Backend Framework:** Spring Boot 3 (Java 21 LTS) & Spring AI Report Generation Engine  
> **Database:** MySQL 9.4 Server (Spring Data JPA / Hibernate)  
> **Frontend:** Responsive HTML5, CSS3, Modern JavaScript (ES6+)  

---

## 📖 Executive Summary & Abstract

Crop diseases in tomato cultivation (*Solanum lycopersicum*) cause devastating yield losses of up to 40–80% globally if left unchecked. Traditional visual classification approaches rely purely on standard convolutional neural networks (CNNs), which suffer from two major limitations:
1. **Lack of Global Receptive Fields:** CNNs struggle with capturing diffuse chlorosis, subtle concentric ring boundaries ("bullseyes"), and multi-lesion distributions across the entire leaf blade.
2. **Environmental Obliviousness:** In nature, phytopathogen sporulation, germination, and vector transmission (e.g., whiteflies, spider mites) are strictly conditioned by microclimatic indicators such as ambient temperature, relative humidity, prolonged leaf wetness, and atmospheric vapour pressure deficit (VPD).

This final year project introduces **AgroVision AI**, an end-to-end multimodal agricultural diagnosis system:
- **LeafVision-DINO (ViT-S/16):** Employs a Vision Transformer Small backbone with 16×16 patch tokens and self-supervised DINO (Distillation with No Labels) pretrained representations, fine-tuned on the standardized **PlantVillage** tomato dataset.
- **Copernicus AgERA5 v2.0 Integration:** Gated Multimodal Units (GMU) condition visual representations with 6 Copernicus surface indicators: 2m Temperature, Relative Humidity, Precipitation Flux, Solar Radiation, 10m Wind Speed, and Vapour Pressure Deficit.
- **Spring AI Report Synthesis:** Integrates Spring AI to translate complex transformer embeddings into structured, compassionate, and actionable agronomic reports detailing:
  - Diagnostic Accuracy & Model Confidence
  - Verified Botanical Symptoms
  - Biological & AgERA5 Climatic Reasons
  - Organic & Biological Solutions
  - Chemical Fungicide Protocols (active ingredients, dosages, schedules)
  - Long-Term Cultural Prevention Strategies
- **Enterprise Web Stack:** Robust Spring Boot 3.2.5 backend, MySQL 9.4 persistent storage, and an elegant emerald-slate web interface with drag-and-drop leaf scanning, quick benchmark samples, and an interactive "Ask Spring AI Agronomist" chat console.

---

## 🏛️ System Architecture

```
                                      +---------------------------------------------+
                                      |            Frontend Web Client              |
                                      |          (HTML5 / CSS3 / ES6 JS)            |
                                      +----------------------+----------------------+
                                                             |
                                           Multipart Upload  |  REST Endpoints
                                           (Leaf + AgERA5)   |  (/api/diagnosis/*)
                                                             v
                                      +---------------------------------------------+
                                      |             Spring Boot 3 Backend           |
                                      |                  (Java 21)                  |
                                      |  * DiagnosisController  * RestTemplate      |
                                      |  * AgEra5RiskService    * DiseaseCatalog    |
                                      +--------+--------------------+---------------+
                                               |                    |
                         JSON Payload Forward  |                    | Spring Data JPA
                        (Image Bytes + Weather)|                    | (Hibernate ORM)
                                               v                    v
+-----------------------------------------------+   +-------------------------------+
|         ML/DL Engine (FastAPI :8000)          |   |       MySQL 9.4 Database      |
|                                               |   |                               |
| 1. LeafVision-DINO (ViT-S/16)                 |   | * diagnosis_records (History) |
|    - 196 Spatial Patches (16x16)              |   | * disease_catalog (Knowledge) |
|    - 12 Transformer Blocks (384-dim, 6 heads) |   | * ai_chat_inquiries           |
|                                               |   +-------------------------------+
| 2. Copernicus AgERA5 v2.0 Encoder             |
|    - 6 Microclimate Indicators                |
|    - Gated Multimodal Fusion Gate (GMU)       |
|                                               |
| 3. PlantVillage Classifier                    |
|    - 10 Tomato Pathological Classes           |
+-----------------------+-----------------------+
                        |
                        | Returns: Predicted Class, Confidence (98.2%),
                        | Top-3 Distribution, Attention Saliency
                        v
        +-----------------------------------------------+
        |           Spring AI Report Engine             |
        |                                               |
        | * Prompt Engineering & Agronomic Synthesizer  |
        | * Accuracy, Symptoms, Reasons, Treatments     |
        | * Interactive Agronomist Chatbot (/api/ai/ask)|
        +-----------------------------------------------+
```

---

## 🔬 Deep Learning Methodology: LeafVision-DINO (ViT-S/16)

### 1. Vision Transformer Architecture
- **Patch Resolution:** $P = 16 \times 16$ pixels.
- **Image Size:** $224 \times 224$ RGB $\implies N = \left(\frac{224}{16}\right)^2 = 196$ spatial tokens.
- **Linear Projection:** Each $16 \times 16 \times 3$ patch is flattened and linearly mapped to dimension $D = 384$.
- **Transformer Encoder:** 12 sequential encoder blocks with Multi-Head Self-Attention (MHSA, $h=6$ heads) and GELU Feed-Forward Networks.
- **Self-Supervised DINO Advantage:** DINO pretraining enables the self-attention maps of the $[CLS]$ token to inherently segment leaf lesions (concentric rings, chlorotic halos, velvet molds) without needing manual pixel annotations.

### 2. Copernicus AgERA5 v2.0 Indicators & Multimodal Fusion
Agrometeorological conditions strongly correlate with plant disease epidemiology:
1. **2m Air Temperature ($T$ in °C):** Modulates pathogen metabolic rates (e.g., *Phytophthora infestans* sporulation peaks between 15–22°C; *Alternaria solani* between 24–30°C).
2. **2m Relative Humidity ($RH$ in %):** High humidity ($>80\%$) is the primary trigger for fungal spore germination.
3. **Daily Precipitation Flux ($Pr$ in mm):** Raindrops physically propel bacterial cells (*Xanthomonas*) and soil-borne fungal spores (*Septoria*) up into the lower plant canopy.
4. **Solar Radiation Flux ($Sr$ in $\text{MJ/m}^2$):** Cloud cover prolongs leaf wetness duration.
5. **10m Wind Speed ($W$ in m/s):** Disseminates airborne sporangia and viruliferous insect vectors (whiteflies carrying TYLCV).
6. **Vapour Pressure Deficit ($VPD$ in kPa):** Derived using the **Tetens equation**:
   $$e_s(T) = 0.61078 \times \exp\left(\frac{17.27 \times T}{T + 237.3}\right)$$
   $$e_a = e_s(T) \times \frac{RH}{100}$$
   $$VPD = e_s(T) - e_a$$
   - $VPD < 0.4\text{ kPa}$: Atmospheric saturation, heavy fog, prolonged surface moisture (high Late Blight risk).
   - $VPD > 1.8\text{ kPa}$: Extreme evaporative demand and water stress (triggers Spider Mite outbreaks).

The 6 normalized weather features are encoded into a 64-dimensional vector and fused with the 384-dimensional $[CLS]$ token representation via a **Gated Multimodal Unit (GMU)**:
$$z_{\text{fused}} = g \odot z_{\text{visual}} + (1 - g) \odot \mathbf{W}_f [z_{\text{visual}} \,\|\, z_{\text{weather}}]$$
where $g = \sigma(\mathbf{W}_g [z_{\text{visual}} \,\|\, z_{\text{weather}}])$ dynamically balances visual pathology with weather susceptibility.

---

## 🗂️ PlantVillage Dataset: 10 Tomato Disease Classes

| Class Key | Common Name | Causative Pathogen | Typical AgERA5 Trigger |
| :--- | :--- | :--- | :--- |
| `Tomato___Bacterial_spot` | Bacterial Spot | *Xanthomonas campestris pv. vesicatoria* | Warm (25–30°C), driving rain splash |
| `Tomato___Early_blight` | Early Blight | *Alternaria solani* | Warm (24–29°C), alternating dew/dry cycles |
| `Tomato___Late_blight` | Late Blight | *Phytophthora infestans* | Cool (15–22°C), extreme humidity ($>90\%$, $VPD < 0.4$) |
| `Tomato___Leaf_Mold` | Leaf Mold | *Passalora fulva* (*Cladosporium*) | High RH ($>85\%$), moderate temp (20–25°C) |
| `Tomato___Septoria_leaf_spot` | Septoria Leaf Spot | *Septoria lycopersici* | Moderate (20–26°C), rain splash from soil |
| `Tomato___Spider_mites_Two_spotted_spider_mite` | Two-Spotted Spider Mite | *Tetranychus urticae* | Hot ($>28^{\circ}\text{C}$), dry air ($RH < 50\%$, $VPD > 1.8$) |
| `Tomato___Target_Spot` | Target Spot | *Corynespora cassiicola* | Subtropical warm (25–32°C), high humidity |
| `Tomato___Tomato_Yellow_Leaf_Curl_Virus` | Yellow Leaf Curl Virus (TYLCV) | *Begomovirus* (Whitefly vector) | Hot, dry conditions encouraging whitefly flight |
| `Tomato___Tomato_mosaic_virus` | Tomato Mosaic Virus (ToMV) | *Tobamovirus* | Mechanical contact, contaminated tools/hands |
| `Tomato___healthy` | Healthy Tomato Leaf | Optimal crop vigor | Balanced vegetative comfort zone ($20\text{--}26^{\circ}\text{C}$, $RH\ 60\%$) |

---

## 💻 Tech Stack Overview

- **Machine Learning & Deep Learning:**
  - Python 3.12, PyTorch 2.14 (CPU/CUDA), Torchvision
  - LeafVision-DINO ViT-S/16 with Gated Multimodal Fusion
  - FastAPI, Uvicorn, Pillow, NumPy
- **Backend Application:**
  - Java 21 LTS, Spring Boot 3.2.5
  - Spring AI (Prompt Engineering, ChatClient & Local Agronomic Knowledge Synthesizer)
  - Spring Data JPA, Hibernate, MySQL Connector/J
  - Dual Profile Support: MySQL (Production) & H2 (In-Memory Testing)
- **Database:**
  - MySQL Server 9.4 running on port 3306
  - Normalized schema: `diagnosis_records`, `disease_catalog`, `ai_chat_inquiries`
- **Frontend Interface:**
  - Semantic HTML5, CSS3 Glassmorphism UI
  - Vanilla Modern JavaScript (ES6+), Fetch API
  - SVG Circular Dial Confidence Gauges, Progress Bars, Dropzone Drag-and-Drop

---

## 🚀 How to Run the Project

### Prerequisites
1. **Java:** JDK 21 installed (`java -version`).
2. **Maven:** Apache Maven 3.9+ (pre-configured at `C:\Users\kovvu\.maven\maven-3.9.15\bin\mvn.cmd` or via system `mvn`).
3. **Python:** Python 3.12 with `torch`, `torchvision`, `fastapi`, `uvicorn`, `pillow`, `numpy`, `python-multipart`.
4. **MySQL:** MySQL Server 9.4 running on port 3306.

---

### Step 1: Initialize the MySQL Database
Open your MySQL terminal or MySQL Workbench:
```sql
CREATE DATABASE IF NOT EXISTS tomato_leaf_disease;
```
*(Optional: Run `database/setup_mysql.sql` to manually create tables, although Spring Boot will automatically verify and update the schema on launch).*

In `backend/src/main/resources/application.properties`, verify your MySQL credentials:
```properties
spring.datasource.url=jdbc:mysql://localhost:3306/tomato_leaf_disease?createDatabaseIfNotExist=true&useSSL=false&allowPublicKeyRetrieval=true&serverTimezone=UTC
spring.datasource.username=root
spring.datasource.password=root
```
*(Tip: If you want to run the project instantly without MySQL, run Spring Boot with the `--spring.profiles.active=h2` flag for in-memory testing).*

---

### Step 2: Start the Machine Learning Service (LeafVision-DINO ViT-S/16)
Double-click `start_ml_service.bat` or run:
```powershell
python -m uvicorn ml_service.app:app --host 127.0.0.1 --port 8000 --reload
```
- Interactive Swagger API Documentation: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Health check: [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)

---

### Step 3: Start the Spring Boot & Spring AI Backend
Double-click `start_backend.bat` or run:
```powershell
& "C:\Users\kovvu\.maven\maven-3.9.15\bin\mvn.cmd" -f backend/pom.xml spring-boot:run
```

---

### Step 4: Open the Web Application
Open any modern web browser:
👉 **[http://localhost:8080](http://localhost:8080)**

---

## 🎯 How to Test and Demonstrate

1. **One-Click Benchmark Testing:**
   - In the **Diagnostic Studio**, click on any of the Quick Benchmark Chips:
     - 🟠 **Early Blight** (loads `early_blight_leaf.jpg` and sets Warm & Humid weather)
     - 🔴 **Late Blight** (loads `late_blight_leaf.jpg` and sets Monsoon/Foggy weather)
     - 🟡 **Bacterial Spot** (loads `bacterial_spot_leaf.jpg` and sets High Rain Splash weather)
     - 🟣 **Yellow Leaf Curl** (loads `yellow_leaf_curl_leaf.jpg` and sets Hot Arid Drought weather)
     - 🔵 **Septoria Spot** (loads `septoria_spot_leaf.jpg` and sets High Moisture weather)
     - 🟢 **Healthy Leaf** (loads `healthy_leaf.jpg` and sets Optimal Microclimate)
   - Click **Run LeafVision-DINO Diagnosis**.
2. **Observe the Results:**
   - Visual inspection of the radial confidence dial (e.g., **98.2% Accuracy**).
   - Top-3 model candidate probability distribution bars.
   - Copernicus AgERA5 microclimatic susceptibility index and trigger factors.
   - **Spring AI Comprehensive Agronomy Report** detailing:
     - 1. Executive Summary
     - 2. Verified Visual Symptoms
     - 3. Biological & AgERA5 Climatic Reasons
     - 4. Biological & Organic Remedies
     - 5. Targeted Chemical Fungicides (dosages & schedules)
     - 6. Long-term Preventive Cultural Practices
3. **Interactive Spring AI Chat:**
   - Click **💬 Ask Spring AI** to open the conversational assistant drawer.
   - Ask follow-up questions (e.g., *"Can I spray neem oil for this?"*, *"What is the copper fungicide dosage?"*).
4. **Export & History:**
   - Click **🖨️ Print / Export Report** for a clean, printable diagnostic summary.
   - Switch to the **Scan Records** tab to see all historical records saved in MySQL.
   - Switch to the **Disease Encyclopedia** tab to explore all 10 PlantVillage tomato classes.

---

## 👨‍🏫 Viva & Defense Q&A Guide

**Q1: Why choose Vision Transformers (ViT-S/16) over conventional CNNs (e.g. ResNet or VGG)?**  
*Answer:* Convolutional neural networks possess localized inductive biases, meaning their receptive field expands slowly layer-by-layer. A tomato leaf disease (such as Late Blight or Early Blight) manifests as distributed multi-focal lesions across the entire leaflet. ViT-S/16 breaks the leaf into $16 \times 16$ spatial patches and utilizes multi-head self-attention ($6$ heads, $384$ embedding dimensions) to capture global dependencies and lesion-to-margin correlations from the very first layer.

**Q2: What is the significance of the DINO pretraining?**  
*Answer:* DINO (Self-distillation with no labels) trains the Vision Transformer via student-teacher self-supervision. Research (Caron et al., 2021) showed that DINO features contain explicit semantic segmentation information without ever being trained on segmentation masks. In leaf disease identification, this allows the $[CLS]$ attention map to naturally segment necrotic spots and chlorosis from background tissue.

**Q3: Why integrate Copernicus AgERA5 v2.0 agrometeorological indicators?**  
*Answer:* Pure image classifiers fail when visual symptoms overlap (e.g., early-stage bacterial spot vs. young septoria spot). In agricultural science, disease epidemics require the "Disease Triangle": a susceptible host, a virulent pathogen, and a **favorable environment**. AgERA5 provides daily 0.1° reanalysis indicators (temperature, relative humidity, precipitation, and VPD). Saturated air ($VPD < 0.4\text{ kPa}$) directly enables *Phytophthora infestans* zoospores to swim and penetrate leaf stomata, whereas hot, arid air ($VPD > 1.8\text{ kPa}$) accelerates spider mite reproduction. Multimodal fusion bridges computer vision with agronomic epidemiology.

**Q4: How does Spring AI benefit the customer/farmer?**  
*Answer:* Raw ML output is simply a class label and a numerical probability (e.g., `Class 2, 0.96`), which is incomprehensible and unhelpful to an agricultural grower. Spring AI acts as the reasoning and translation layer. It ingests the vision transformer logits, the disease pathology metadata, and the local AgERA5 indicators to synthesize a structured agronomic report with actionable instructions: specific organic biocontrols, chemical fungicide active ingredients, exact dosage rates, and preventative crop rotation practices.

---

## 👥 Authors & Acknowledgements
- **Project:** Final Year Engineering Capstone Project
- **Domain:** Artificial Intelligence in Agriculture & Precision Plant Pathology
- **Datasets:** PlantVillage Dataset (David Hughes et al., Penn State) & Copernicus Climate Change Service (ECMWF AgERA5 v2.0)
