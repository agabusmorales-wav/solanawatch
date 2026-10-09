# 🌿 SolanaWatch: Project Summary & Technical Overview

> **Project Title:** SolanaWatch: An IoT-Based Disease Early Warning System for Soil-Grown Solanaceae Crops  
> **Academic Institution:** University of Santo Tomas – College of Information and Computing Sciences (CICS)  
> **Degree Program:** Bachelor of Science in Information Technology (Department of Information Technology)  
> **Academic Term:** Special Term, A/Y 2025–2026  
> **Project Adviser:** Prof. Eugenia R. Zhuo, DIT  
> **Panel of Examiners:**  
> - **Lead Panel:** Inst. Gabriel Emanuel D. Montano  
> - **Member Panel 1:** Prof. Noel E. Estrella  
> - **Member Panel 2:** Mr. Karlo Angelo Tino  
> **Project Team Members (3ITC - Group 1):**  
> 1. Morales, Simeon Agabus S.  
> 2. Rapada, Raven M.  
> 3. Hernandez, Andrei S.  
> 4. Eugenio, Vince Angelo  

---

## 📌 1. Executive Summary

**SolanaWatch** is an open-source, solar-assisted IoT microclimatic monitoring and disease early warning system designed specifically for smallholder **Solanaceae crop farmers** (Tomato, Eggplant, Bell Pepper, and Potato) in the Philippines.

### The Problem
Solanaceae crops are high-value staples vital to Philippine food security (e.g., quarterly eggplant yields surpass 100,000 MT; tomato yields range between 70,000–93,000 MT). However, cultivation is severely threatened by two devastating pathologies:
1. **Late Blight (*Phytophthora infestans*):** Foliar oomycete thriving in high humidity ($\ge 90\%$), prolonged leaf wetness ($\ge 10\text{ h}$), and moderate temperatures ($12^\circ\text{C}-22^\circ\text{C}$).
2. **Bacterial Wilt (*Ralstonia pseudosolanacearum*):** Soilborne vascular bacterium proliferating under warm root-zone temperatures ($28^\circ\text{C}-35^\circ\text{C}$) and saturated soil moisture ($\ge 75\%$ VWC).

Delayed detection frequently causes **50% to 90% crop losses**, forcing farmers into costly, reactive chemical use.

### The SolanaWatch Solution
Unlike camera-based computer vision AI tools that detect disease only **post-symptomatically** (after irreversible leaf lesions and vascular damage have already occurred), SolanaWatch monitors physical microclimatic conditions directly in the field in real time. It evaluates disease favorability against validated plant pathology models, alerting farmers **pre-symptomatically** so they can take preventive cultural actions (canopy aeration, drainage, targeted bio-fungicides) before infection spreads.

---

## 🏛️ 2. System Architecture & Flow

```
+---------------------------------------------------------------------------------------------------------+
|                                    SOLANAWATCH SYSTEM ARCHITECTURE                                      |
+---------------------------------------------------------------------------------------------------------+
|                                                                                                         |
|  [ SENSING NODE (ESP32 DevKit V1) ]                                                                     |
|   ├── DHT22 / AM2302 (Ambient Temp & Relative Humidity inside Louvered Stevenson Shield)                |
|   ├── DS18B20 Waterproof Probe (Subsurface Root-Zone Soil Temp @ 10cm depth, 1-Wire)                    |
|   ├── Capacitive Soil Moisture v1.2 (Volumetric Water Content @ 10cm depth, Analog ADC)                 |
|   ├── Industrial Dielectric Leaf Wetness Grid (IP68, RS485 Modbus-RTU over MAX485 Transceiver)          |
|   ├── SPI MicroSD Card Module (Offline FIFO JSON Lines buffer: telemetry_buffer.jsonl)                 |
|   └── Autonomous Power (20W Monocrystalline PV + 12V 10A MPPT + 12.8V 12Ah LiFePO4 Battery = 47d Autonomy)
|                                                  │                                                      |
|                                    2.4 GHz Wi-Fi │ HTTP POST /api/telemetry (JSON)                      |
|                                                  ▼                                                      |
|  [ CLOUD BACKEND & DATABASE ]                                                                           |
|   ├── Node.js & Express.js REST API Server                                                              |
|   ├── Turso Cloud Database (Distributed libSQL / SQLite with UNIQUE(node_id, recorded_at))              |
|   └── Literature-Grounded Disease Risk Engine:                                                          |
|       ├── Late Blight: Adapted Wallin Severity Values (SV) & Leaf Wetness Duration (LWD >= 10h)         |
|       └── Bacterial Wilt: Hydrothermal Risk Score R_BW = (0.50 * S_ST) + (0.50 * S_SM)                  |
|                                                  │                                                      |
|                                       JSON HTTPS │ WebSockets / REST API                                |
|                                                  ▼                                                      |
|  [ USER DASHBOARD & DECISION SUPPORT ]                                                                  |
|   ├── React.js + Vite + Tailwind CSS + Chart.js                                                         |
|   ├── Live Environmental Gauges & Multi-Series Historical Time-Series Visualizations                    |
|   ├── Color-Coded Early Warning Banners (Green = Low, Yellow = Moderate, Red = High Risk Alert)         |
|   └── Contextual Agronomic Recommendations & Hardware Health Telemetry (Battery / RSSI / Solar Status)  |
+---------------------------------------------------------------------------------------------------------+
```

---

## 🔬 3. Core Technical Specifications

### Hardware Bill of Materials (₱7,208.00 Total Prototype Cost)
* **Microcontroller:** Espressif ESP32 DevKit V1 (Dual-Core Xtensa LX6 @ 240 MHz, 520 KB SRAM, 4 MB Flash, FreeRTOS).
* **Air Temperature & RH:** DHT22 / AM2302 placed inside a UV-stabilized louvered Stevenson Radiation Shield.
* **Soil Temperature:** Dallas DS18B20 waterproof stainless-steel digital probe (1-Wire bus @ 10 cm depth).
* **Soil Moisture:** Capacitive Soil Moisture Sensor v1.2 (Dielectric insulated PCB @ 10 cm depth).
* **Leaf Surface Wetness:** Industrial IP68 dielectric leaf grid (RS485 Modbus-RTU over MAX485 transceiver).
* **Offline Edge Storage:** SPI MicroSD module with 16GB FAT32 card (`telemetry_buffer.jsonl`).
* **Power Subsystem:**
  - 20W 12V Monocrystalline Solar PV Panel
  - 12V 10A IP67 MPPT Solar Charge Controller
  - 12.8V 12Ah ($153.6\text{ Wh}$) $\text{LiFePO}_4$ Battery Pack with built-in 15A BMS
  - **47.0 Days of Zero-Sunlight Battery Autonomy** ($2.30\text{ Wh/day}$ duty-cycled budget).
* **Hardware Packaging:** Custom FR-4 fabricated PCB shield housed inside an IP65/IP66 weatherproof polycarbonate enclosure with PG7/PG9 compression cable glands.

### Disease Risk Algorithms & Formulas
1. **Late Blight (*Phytophthora infestans*):**
   - Evaluated using adapted **Wallin Severity Values (SV)** / BLITECAST rules based on cumulative **Leaf Wetness Duration (LWD $\ge 10\text{ h}$)** and concurrent ambient temperature ($12^\circ\text{C}-22^\circ\text{C}$) with $RH \ge 90\%$.
2. **Bacterial Wilt (*Ralstonia pseudosolanacearum*):**
   - Evaluated using the **Hydrothermal Soil Risk Index**:
     $$R_{\text{BW}} = (0.50 \times S_{\text{ST}}) + (0.50 \times S_{\text{SM}})$$
   - Where $S_{\text{ST}}$ is the soil temperature risk sub-score (optimal $28^\circ\text{C}-35^\circ\text{C}$) and $S_{\text{SM}}$ is the soil moisture risk sub-score (high risk $\ge 75\%\text{ VWC}$).
3. **Alert Categories:**
   - **Low Risk (Green):** Normal microclimate; routine cultural maintenance.
   - **Moderate Risk (Yellow):** Conducive weather developing; prompt canopy aeration and reduced irrigation.
   - **High Risk (Red Alert):** Critical infection threshold reached; apply immediate preventive bio-fungicides/cultural containment.

---

## 🧪 4. Quality Assurance & Verification (ISO/IEC 25010)

| Quality Metric | Target Acceptance Criteria | Verification Method |
| :--- | :--- | :--- |
| **Sensor Measurement Accuracy** | **90% – 95%** | 2-point moisture calibration, ice-point bath ($0.0^\circ\text{C}$), NaCl salt chamber ($75.3\%\text{ RH}$) |
| **Communication Reliability** | **≥ 95% Packet Delivery** | Multi-distance RSSI (dBm) and PDR (%) testing at 5m, 10m, 20m, 30m, 50m |
| **Continuous Device Uptime** | **≥ 99% Operational Uptime** | 7-day continuous field deployment logging ($672\text{ cycles}$) |
| **Disease Rule Logic Accuracy** | **≥ 95% Logical Accuracy** | Synthetic threshold boundary validation test suite |
| **Zero-Sunlight Battery Autonomy**| **≥ 3 Days (72 Hours)** | Physical solar disconnection load testing |
| **System Usability Scale (SUS)** | **≥ 80.0 / 100 (Grade A)** | 10-question SUS questionnaire with farmers & technicians ($N=10$) |

---

## 📂 5. Project Repository File Structure

```
SOLANAWATCH/
├── figures/                                              # High-resolution 300 DPI system diagrams
│   ├── figure1_context_diagram.png                       # High-level operational boundary & context
│   ├── figure2_activity_diagram.png                      # 3-swimlane activity flow diagram
│   ├── figure3_prototyping_model.png                     # Iterative prototyping development cycle
│   ├── figure4_system_architecture.png                   # Multi-tier hardware-cloud-frontend architecture
│   ├── figure5_er_diagram.png                            # Relational Turso libSQL database schema
│   └── figure6_circuit_schematic.png                     # Comprehensive circuit pinout & wiring schematic
├── SolanaWatch_Proposal_Chapters_1-3_REVISED.docx        # Complete revised academic proposal manuscript (APA 7th)
├── SolanaWatch_Proposal_Chapters_1-3_REVISED.html        # Interactive HTML view of revised proposal
├── SolanaWatch_Revision_Matrix_Official.docx             # Official 24-point defense revision compliance matrix (DOCX)
├── SolanaWatch_Revision_Matrix_Official.pdf              # Official 24-point defense revision compliance matrix (PDF)
├── SolanaWatch_Project_Documentation.md                  # Comprehensive 936-line technical specification
├── PROJECT_SUMMARY.md                                    # High-level project executive summary
├── generate_revision_matrix.py                           # Python generator for official revision matrix
├── generate_diagrams.py                                  # Matplotlib generator for all 6 system diagrams
├── convert_to_docx.py                                    # Markdown to styled DOCX manuscript compiler
├── convert_to_html.py                                    # Markdown to styled HTML compiler
└── README.md                                             # Repository overview & quick-start guide
```

---

## 📋 6. Summary of Defense Compliance (24-Point Matrix)

All 24 comments from the initial proposal oral defense evaluation have been fully resolved in the revised manuscript:
1. **Comparative Analysis:** Added ESP32 vs. Leonardo vs. Raspberry Pi in Chapter 2 (*p. 21*).
2. **ESP32 Selection Justification:** Grounded in dual-core architecture, deep sleep, and peripheral buses (*p. 22, 32*).
3. **Exact Component Models:** Specified DHT22, DS18B20, Capacitive v1.2, RS485 Leaf Grid, MPPT, and LiFePO4 battery (*p. 41–49*).
4. **Battery Reassessment:** Upgraded from 3.7V 2600 mAh Li-ion to 12.8V 12Ah LiFePO4 (*p. 25, 44, 68*).
5. **Solar System:** Added 20W PV panel and MPPT controller for 24/7 grid-free operation (*p. 26, 57*).
6. **Power Testing:** Formulated current draw test bench across TX, sensing, and deep sleep (*p. 78–80*).
7. **Mathematical Sizing:** Derived formulas proving 47-day autonomy on $2.30\text{ Wh/day}$ consumption (*p. 26, 68*).
8. **Footprint vs. Range:** Differentiated microclimate footprint (5–15m) from Wi-Fi RF range (30–50m) (*p. 27–28*).
9. **RF Experimental Test:** Added RSSI and PDR (%) testing protocol from 5m to 50m (*p. 28, 79*).
10. **Agronomic RRL:** Cited pathology literature for *P. infestans* and *R. pseudosolanacearum* (*p. 5–6, 18–21*).
11. **Threshold Basis:** Grounded in Wallin SV / BLITECAST and Hydrothermal soil indices (*p. 19–20, 61–65*).
12. **Multi-Parameter Combination:** Defined decision rules and alert classification logic (*p. 30–31, 65*).
13. **Risk Assessment vs. Diagnosis:** Explicitly clarified pre-symptomatic risk modeling vs. biological diagnosis (*p. 8, 14, 15*).
14. **Intended Users:** Identified smallholder farmers (primary) and extension officers/researchers (secondary) (*p. 12–14, 85*).
15. **Diagram Annotation:** Annotated all figures with GPIO pins, buck converters, and pull-up resistors (*p. 13, 58, 74*).
16. **PCB Evaluation:** Evaluated contact resistance and durability; adopted custom FR-4 PCB shield (*p. 28, 49*).
17. **ISO Test Cases:** Added comprehensive test suites across accuracy, Wi-Fi, SD logging, and sync (*p. 76–82*).
18. **Network Loss & Deduplication:** Documented MicroSD FIFO logging and database composite uniqueness (*p. 26–27, 58*).
19. **Sensor Calibration:** Detailed 2-point soil, ice bath ($0.0^\circ\text{C}$), and salt chamber ($75.3\%$) procedures (*p. 24–25*).
20. **Delimited Crops:** Specified Tomato, Eggplant, Pepper, and Potato in open-field/screenhouses (*p. 5–6, 15*).
21. **Enclosure Rating:** Selected IP65/IP66 box with cable glands, desiccants, and Stevenson shield (*p. 28, 45*).
22. **Reliability Plan:** Added 7-day field test, hardware watchdog timer recovery, and water spray tests (*p. 39, 81*).
23. **Solar & Autonomy Validation:** Added 72-hour solar deprivation test and 48-hour MPPT charging curve test (*p. 68, 80*).
24. **APA 7th References:** Updated references with 2020–2026 high-impact publications and datasheets (*p. 93–101*).

---

*Compiled for the University of Santo Tomas – College of Information and Computing Sciences Capstone Project (AY 2025–2026).*
