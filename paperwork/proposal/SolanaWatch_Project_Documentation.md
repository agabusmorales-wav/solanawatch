# SolanaWatch: Complete Project Documentation & Technical Specification

> **Project Title:** SolanaWatch: An IoT-Based Disease Early Warning System for Soil-Grown Solanaceae Crops  
> **Academic Context:** Capstone Project Proposal (Chapters 1–3) & Technical Specification  
> **Institution:** University of Santo Tomas – College of Information and Computing Sciences (Department of Information Technology)  
> **Academic Year:** Special Term, A/Y 2025–2026  
> **Adviser:** Prof. Eugenia R. Zhuo, DIT  
> **Panel of Examiners:** Prof. Noel E. Estrella, Mr. Karlo Angelo Tino, Inst. Gabriel Emanuel D. Montano (Head Panel)  
> **Repository / Project Location:** `C:\Users\agabu\Downloads\CODE PROJECTS\SOLANAWATCH`  

---

## Table of Contents

1. [Executive Summary & Project Overview](#1-executive-summary--project-overview)
2. [Chapter 1: Introduction & Project Context](#2-chapter-1-introduction--project-context)
   - 2.1 [Agricultural Background & Problem Statement](#21-agricultural-background--problem-statement)
   - 2.2 [Purpose and Description](#22-purpose-and-description)
   - 2.3 [Target Beneficiaries](#23-target-beneficiaries)
   - 2.4 [System Conceptual Overview](#24-system-conceptual-overview)
   - 2.5 [Project Objectives (General & Specific)](#25-project-objectives-general--specific)
   - 2.6 [Scope and Delimitations](#26-scope-and-delimitations)
3. [Chapter 2: Review of Related Literature & Technical Grounding](#3-chapter-2-review-of-related-literature--technical-grounding)
   - 3.1 [Environmental Determinants of Target Solanaceae Pathologies](#31-environmental-determinants-of-target-solanaceae-pathologies)
   - 3.2 [Comparative Analysis of Embedded Computing Platforms](#32-comparative-analysis-of-embedded-computing-platforms)
   - 3.3 [Sensor Selection, Operational Principles & Calibration](#33-sensor-selection-operational-principles--calibration)
   - 3.4 [Solar-Assisted Power & Battery Storage Technology](#34-solar-assisted-power--battery-storage-technology)
   - 3.5 [Edge Data Buffering, Wireless Range vs. Microclimatic Footprint](#35-edge-data-buffering-wireless-range-vs-microclimatic-footprint)
   - 3.6 [Hardware Packaging: Custom PCB vs. Breadboards & IP Enclosure](#36-hardware-packaging-custom-pcb-vs-breadboards--ip-enclosure)
   - 3.7 [State-of-the-Art Comparative Synthesis & Research Gaps](#37-state-of-the-art-comparative-synthesis--research-gaps)
4. [Chapter 3: Technical Background, System Design & Architecture](#4-chapter-3-technical-background-system-design--architecture)
   - 4.1 [Requirements Analysis (ISO/IEC 25010)](#41-requirements-analysis-isoiec-25010)
     - 4.1.1 [Functional Requirements (FR-1 to FR-10)](#411-functional-requirements-fr-1-to-fr-10)
     - 4.1.2 [Non-Functional Requirements (NFR-1 to NFR-6)](#412-non-functional-requirements-nfr-1-to-nfr-6)
   - 4.2 [Bill of Materials (Hardware & Software Specifications)](#42-bill-of-materials-hardware--software-specifications)
   - 4.3 [Development Methodology (Prototyping Model)](#43-development-methodology-prototyping-model)
   - 4.4 [System Architecture & Data Flow](#44-system-architecture--data-flow)
   - 4.5 [Circuit Pinout & Hardware Interfacing Schematic](#45-circuit-pinout--hardware-interfacing-schematic)
   - 4.6 [Mathematical Power Subsystem Sizing & Verification](#46-mathematical-power-subsystem-sizing--verification)
   - 4.7 [Literature-Grounded Disease-Risk Algorithms & Mathematical Models](#47-literature-grounded-disease-risk-algorithms--mathematical-models)
     - 4.7.1 [Late Blight Severity Value Algorithm (Wallin / BLITECAST)](#471-late-blight-severity-value-algorithm-wallin--blitecast)
     - 4.7.2 [Bacterial Wilt Hydrothermal Risk Index](#472-bacterial-wilt-hydrothermal-risk-index)
   - 4.8 [Database Schema & Data Architecture (Turso libSQL)](#48-database-schema--data-architecture-turso-libsql)
   - 4.9 [Offline Edge Resilient Data Synchronization Protocol](#49-offline-edge-resilient-data-synchronization-protocol)
5. [Quality Assurance, Verification & Testing Framework](#5-quality-assurance-verification--testing-framework)
   - 5.1 [Sensor Calibration Protocols](#51-sensor-calibration-protocols)
   - 5.2 [Unit, Integration & Stress Test Cases](#52-unit-integration--stress-test-cases)
   - 5.3 [Quality Metrics & Acceptance Criteria](#53-quality-metrics--acceptance-criteria)
6. [Implementation & Feasibility Analysis](#6-implementation--feasibility-analysis)
   - 6.1 [Internal & External Operational Environments](#61-internal--external-operational-environments)
   - 6.2 [Technical, Operational & Economic Feasibility](#62-technical-operational--economic-feasibility)
   - 6.3 [Field Deployment Procedures](#63-field-deployment-procedures)
7. [Oral Defense Compliance & Panel Revision Action Matrix](#7-oral-defense-compliance--panel-revision-action-matrix)
8. [Bibliography & Academic References (APA 7th Edition)](#8-bibliography--academic-references-apa-7th-edition)

---

## 1. Executive Summary & Project Overview

**SolanaWatch** is an Internet of Things (IoT)-based microclimatic disease early warning and decision-support system engineered specifically for soil-grown **Solanaceae crops** (Tomato, Eggplant, Bell Pepper, and Potato) in the Philippines.

```
+---------------------------------------------------------------------------------------------------------+
|                                    SOLANAWATCH SYSTEM AT A GLANCE                                       |
+---------------------------------------------------------------------------------------------------------+
|  [ESP32 Edge Node]                                                                                      |
|   - Ambient Temp & RH (DHT22 in Stevenson Shield)                                                       |
|   - Leaf Wetness Duration (IP68 RS485 Modbus Dielectric Grid)                                           |
|   - Root-Zone Soil Temp (DS18B20 1-Wire Digital Probe @ 10cm)                                           |
|   - Soil Moisture (Capacitive v1.2 Analog Probe @ 10cm)                                                 |
|   - Power: 20W Monocrystalline PV + 12.8V 12Ah LiFePO4 Battery + MPPT Controller (47-Day Autonomy)      |
|   - Offline Logging: SPI MicroSD Buffer (JSON Lines)                                                    |
|                                                                                                         |
|                                       || 2.4 GHz Wi-Fi / HTTP REST                                      |
|                                       \/                                                                |
|                                                                                                         |
|  [Node.js Cloud Backend & Turso Distributed libSQL DB]                                                  |
|   - Transactional Ingestion & Deduplication (UNIQUE: node_id + recorded_at)                             |
|   - Disease Risk Engine:                                                                                |
|       * Late Blight: Adapted Wallin Severity Values (SV) & Leaf Wetness Duration (LWD >= 10h)           |
|       * Bacterial Wilt: Hydrothermal Risk Score R_BW = (0.50 * S_ST) + (0.50 * S_SM)                    |
|                                                                                                         |
|                                       || Real-Time Telemetry & JSON APIs                                |
|                                       \/                                                                |
|                                                                                                         |
|  [React.js Web Dashboard & Early Warning UI]                                                            |
|   - Live Environmental Gauges & Multi-Series Historical Time-Series Charts                              |
|   - Color-Coded Risk Banners (Green = Low, Yellow = Moderate, Red = High Risk Alert)                   |
|   - Actionable Agronomic Preventive Recommendations & Device Telemetry Health Indicators                |
+---------------------------------------------------------------------------------------------------------+
```

### Core Value Proposition
- **Pre-Symptomatic Early Warning:** Unlike post-symptomatic camera/computer-vision AI systems that detect disease only after visible leaf lesions and irreversible tissue damage have occurred, SolanaWatch evaluates physical microclimatic favorability in real time, alerting growers before infection develops.
- **Microclimatic Precision:** Captures canopy and root-zone parameters directly in the field, overcoming the coarse spatial inaccuracy of regional weather station forecasts.
- **Edge Resilience:** Equipped with local SPI MicroSD offline FIFO buffering, idempotent cloud batch synchronization, an ultra-low power ESP32 deep-sleep cycling routine, and a solar-assisted LiFePO₄ power subsystem ensuring continuous 24/7 operation across extended rainy/monsoon periods.
- **Economic Feasibility:** Achieved at a total prototype hardware cost of only **₱7,208.00** with open-source software stacks and zero recurrent SaaS subscriptions.

---

## 2. Chapter 1: Introduction & Project Context

### 2.1 Agricultural Background & Problem Statement

Solanaceae crops, notably tomatoes (*Solanum lycopersicum*), eggplants (*Solanum melongena*), peppers (*Capsicum annuum*), and potatoes (*Solanum tuberosum*), are high-value vegetable staples critical to Philippine food security and smallholder farmer livelihoods. According to the Philippine Statistics Authority (PSA, 2026), quarterly eggplant yields consistently surpass 100,000 metric tons, while quarterly tomato yields range between 70,000 to 93,000 metric tons.

However, Solanaceae cultivation is severely threatened by two devastating pathologies:
1. **Late Blight (*Phytophthora infestans*):** An oomycete foliar pathogen thriving in high relative humidity ($\ge 90\%$), prolonged leaf wetness ($\ge 10$ continuous hours), and moderate temperatures ($12^\circ\text{C}$ to $22^\circ\text{C}$).
2. **Bacterial Wilt (*Ralstonia pseudosolanacearum*):** A soilborne vascular bacterium proliferating under warm root-zone temperatures ($28^\circ\text{C}$ to $35^\circ\text{C}$) and saturated/waterlogged soil moisture ($\ge 75\%$ Volumetric Water Content).

Delayed detection frequently results in catastrophic crop losses ranging from **50% to 90%**, forcing smallholder farmers to resort to excessive, costly, and environmentally damaging reactive chemical applications.

#### Current Monitoring Deficiencies
- **Manual Visual Scouting:** Farmers identify infections only after visible foliar discoloration, lesions, or wilting appear, by which point internal vascular or intercellular mycelial colonization is already irreversible.
- **Commercial IoT Solutions:** Cost-prohibitive ($> \text{₱}50,000$), complex, dependent on continuous utility grid power, and reliant on proprietary subscriptions.
- **Image-Based AI Tools:** Inherent lag; purely post-symptomatic.
- **Regional Meteorological Stations:** Macro-level data fails to represent localized crop canopy microclimates and root-zone hydrothermal dynamics.

### 2.2 Purpose and Description

The primary purpose of this study is to develop **SolanaWatch**, an open-source, affordable, IoT-enabled disease early warning system that:
1. Automatically collects localized canopy microclimate and root-zone soil measurements.
2. Evaluates disease risk against validated plant pathology threshold algorithms (Wallin Severity Values and Hydrothermal Soil Indices).
3. Transmits real-time updates and color-coded visual alerts to a responsive web dashboard to guide timely cultural and preventive agronomic interventions.

### 2.3 Target Beneficiaries
- **Small-Scale & Smallholder Solanaceae Farmers:** Low-cost early warnings enable timely cultural practices (e.g., improved drainage, pruning, canopy aeration, targeted preventive bio-fungicides) prior to widespread infection.
- **Agricultural Technicians & Extension Officers (LGUs, DA):** Centralized digital records support accurate, data-driven regional advisory services.
- **Agricultural & Computing Researchers:** Empirical baseline data on tropical Solanaceae microclimate dynamics and IoT edge reliability under Philippine field conditions.

### 2.4 System Conceptual Overview

```
+---------------------------------------------------------------------------------------------------+
|                                 SOLANAWATCH CONTEXT DIAGRAM                                       |
+---------------------------------------------------------------------------------------------------+
|                                                                                                   |
|  +--------------------+                                               +------------------------+  |
|  |  ESP32 Edge Node   |   Sensor Telemetry (Air/Soil/Leaf Data)       |   SolanaWatch System   |  |
|  |  - DHT22 Temp/RH   | --------------------------------------------> |   (Node.js + libSQL    |  |
|  |  - DS18B20 Soil T  |                                               |    + React Dashboard)  |  |
|  |  - Capacitive SM   | <-------------------------------------------- |                        |  |
|  |  - RS485 Leaf Wet  |            Server ACK / Sync OK               +------------------------+  |
|  |  - MicroSD Buffer  |                                                           |     ^         |
|  +--------------------+                                                           |     |         |
|                                                        Live Alerts & Risk Trends  |     | User    |
|                                                                                   |     | Config  |
|                                                                                   v     |         |
|                                                                       +------------------------+  |
|                                                                       |   Farmer / Operator    |  |
|                                                                       |   (Web Dashboard)      |  |
|                                                                       +------------------------+  |
+---------------------------------------------------------------------------------------------------+
```

### 2.5 Project Objectives (General & Specific)

#### General Objective
To design, develop, and evaluate **SolanaWatch**, an Internet of Things (IoT)-based disease early warning system for monitoring localized environmental conditions and assessing disease risk associated with late blight and bacterial wilt in soil-grown Solanaceae crops.

#### Specific Objectives
1. **Edge Sensing:** Design an outdoor IoT sensing node monitoring ambient air temperature, relative humidity, root-zone soil temperature (10 cm), volumetric soil moisture (10 cm), and leaf wetness duration in real time.
2. **Autonomous Power & Offline Resilience:** Integrate a solar-assisted LiFePO₄ power subsystem for 24/7 continuous operation and an onboard SPI MicroSD buffer to preserve data during network dropouts.
3. **Cloud Backend & Deduplication:** Implement a cloud backend for storing, managing, and automatically synchronizing offline telemetry without record duplication.
4. **Disease Risk Engine:** Develop a literature-grounded rule-based risk module for Late Blight (*P. infestans*) and Bacterial Wilt (*R. pseudosolanacearum*).
5. **Interactive Web Dashboard:** Build a responsive web interface displaying real-time conditions, historical time-series charts, node health indicators, and color-coded alert notifications.
6. **System Evaluation:** Empirically evaluate sensor calibration accuracy, communication range, battery autonomy, and software quality based on **ISO/IEC 25010** and System Usability Scale (SUS) benchmarks.

### 2.6 Scope and Delimitations

#### Scope Comparison Matrix

| Project Dimension | In-Scope Specifications | Out-of-Scope Delimitations |
|---|---|---|
| **Target Pathologies** | Microclimatic risk assessment for Late Blight (*Phytophthora infestans*) and Bacterial Wilt (*Ralstonia pseudosolanacearum*). | Direct biological pathogen detection, DNA/PCR assays, optical spectroscopy, image-based lesion classification, viral/nematode diseases. |
| **Target Crops** | Soil-grown Solanaceae crops: Tomato (*S. lycopersicum*), Eggplant (*S. melongena*), Bell Pepper (*C. annuum*), and Potato (*S. tuberosum*). | Hydroponics, aquaponics, vertical farming, non-solanaceous crops. |
| **Environmental Sensing** | Ambient air temperature, relative humidity, leaf wetness duration, root-zone soil temperature (10 cm), volumetric soil moisture (10 cm). | Soil NPK chemical nutrient sensing, soil pH, solar irradiance flux ($\text{W/m}^2$), wind velocity / anemometry. |
| **Node Architecture** | Single stationary edge node deployed at a representative canopy location in a test plot. | Mobile rovers, autonomous ground vehicles (UGVs), drone aerial multispectral imaging, multi-node mesh networks. |
| **Power System** | Solar-assisted power system (20W Monocrystalline PV + 12.8V 12Ah LiFePO₄ + IP67 MPPT Controller) with $\ge 3$ days autonomy. | Sole reliance on AC grid electricity or unverified single-cell 18650 Li-ion batteries. |
| **Edge Storage & Sync** | SPI MicroSD local FIFO queue with transactional HTTP batch sync and database deduplication. | Unbuffered live-only transmission or cellular direct-to-satellite modems. |
| **Wireless Telemetry** | 2.4 GHz Wi-Fi (802.11 b/g/n) with experimental RSSI range and packet loss profiling. | LoRaWAN private gateways, Zigbee mesh, cellular 4G/5G SIM modems. |
| **User Platform** | Responsive web-based dashboard accessible via desktop and mobile web browsers with role-based access control. | Native downloadable mobile apps (iOS App Store / Android APKs) or desktop-only software. |
| **System Outputs** | Real-time sensor metrics, multi-series historical charts, device status telemetry, color-coded visual alerts, agronomic recommendations. | Automated physical actuation (motorized irrigation valves, automated pesticide spray boom actuators). |
| **Evaluation Framework** | Laboratory sensor calibration, 72-hour battery deprivation test, RF range profiling, ISO/IEC 25010 software evaluation, SUS survey ($N=10$). | Multi-year longitudinal agronomic yield trials or chemical reduction field audits. |

---

## 3. Chapter 2: Review of Related Literature & Technical Grounding

### 3.1 Environmental Determinants of Target Solanaceae Pathologies

```
+---------------------------------------------------------------------------------------------------------+
|                                    TARGET PATHOLOGY EPIDEMIOLOGY                                        |
+---------------------------------------------------------------------------------------------------------+
|                                                                                                         |
|  1. LATE BLIGHT (Phytophthora infestans)                                                                |
|     - Primary Drivers: Foliar Microclimate (Leaf Surface Moisture + Air Humidity + Moderate Temp)       |
|     - High-Risk Temperature Window: 12°C to 22°C (Optimal sporangia germination: 15°C–20°C)             |
|     - Relative Humidity: >= 90% RH                                                                      |
|     - Leaf Wetness Duration (LWD): >= 10 to 15 continuous hours                                         |
|     - Epidemiological Basis: Wallin Severity Values (SV) & BLITECAST (Boulton et al., 2023;             |
|       Mazumdar et al., 2021; Univ. of Florida IFAS Extension, n.d.)                                     |
|                                                                                                         |
|  2. BACTERIAL WILT (Ralstonia pseudosolanacearum)                                                       |
|     - Primary Drivers: Root-Zone Hydrothermal Dynamics (Soil Temp + Soil Moisture Saturation)           |
|     - Optimal Proliferation Soil Temperature: 28°C to 35°C                                              |
|     - Soil Volumetric Moisture: >= 75% VWC (Saturated / Waterlogged pore space)                         |
|     - Epidemiological Basis: Hydrothermal bacterial motility & root invasion (Jiang et al., 2021;       |
|       Silva et al., 2024; Subedi et al., 2024)                                                          |
|                                                                                                         |
+---------------------------------------------------------------------------------------------------------+
```

### 3.2 Comparative Analysis of Embedded Computing Platforms

To rigorously justify selecting the **Espressif ESP32 DevKit V1**, the system architecture was benchmarked against competing platforms commonly used in agricultural IoT research:

| Evaluation Metric | Arduino Leonardo | Raspberry Pi 4 Model B | Espressif ESP32 DevKit V1 | Selection Justification for SolanaWatch |
|---|---|---|---|---|
| **CPU Architecture & Clock** | 8-bit AVR RISC @ 16 MHz | 64-bit Quad-Core ARM Cortex-A72 @ 1.5 GHz | **32-bit Dual-Core Xtensa LX6 @ 240 MHz** | ESP32 provides ample speed for RS485 Modbus CRC, local JSON serialization, and cryptographic TLS. |
| **SRAM Memory** | 2.5 KB | 2 GB – 8 GB LPDDR4 | **520 KB SRAM** | ESP32 handles network TCP buffers and local SD queues without memory exhaustion. |
| **Flash Memory** | 32 KB | External MicroSD (OS-dependent) | **4 MB SPI Flash** | ESP32 stores firmware and calibration offsets reliably with zero risk of OS filesystem corruption. |
| **Integrated Wireless** | None (Requires external shield) | Dual-Band Wi-Fi (2.4/5.0 GHz) & BLE 5.0 | **Integrated 2.4 GHz Wi-Fi (802.11 b/g/n) & BLE 4.2** | Native Wi-Fi eliminates extra hardware shields, secondary wiring, and failure points. |
| **Active Power Consumption** | ~100–150 mW (20–30 mA @ 5V) | ~3.0–6.5 W (600–1300 mA @ 5V) | **~330–790 mW (100–240 mA @ 3.3V TX peak)** | Highly efficient power profile suitable for compact solar-battery field operation. |
| **Deep-Sleep Current** | ~15–25 mW (No true deep sleep) | ~1.5–2.0 W (No deep sleep mode) | **10 µA – 150 µA (ULP Deep Sleep)** | Low deep-sleep current enables multi-week battery autonomy between 15-minute polling cycles. |
| **Peripheral Interfaces** | 1x UART, 1x SPI, 1x I2C | 2x I2C, 2x SPI, 2x UART (No native ADC) | **3x UART, 3x SPI, 2x I2C, 18x 12-bit ADC** | Natively connects RS485 (UART2), MicroSD (SPI), DS18B20 (GPIO), and Capacitive sensor (ADC). |
| **Unit Hardware Cost** | ~₱450.00 (Excl. Wi-Fi shield) | ~₱3,500.00 – ₱5,200.00 | **~₱300.00 – ₱350.00** | Highly cost-effective, supporting overall economic feasibility for smallholder farmers. |

### 3.3 Sensor Selection, Operational Principles & Calibration

1. **Ambient Temperature & Relative Humidity (DHT22 / AM2302):**
   - *Operational Principle:* Capacitive polymer humidity element and high-precision NTC thermistor outputting single-wire digital data.
   - *Housing:* Enclosed within a multi-plate, louvered **Stevenson Radiation Shield** to ensure free ambient airflow while preventing solar radiation heating and direct rain impingement (Botero-Valencia et al., 2022).
2. **Root-Zone Soil Temperature (Dallas DS18B20):**
   - *Operational Principle:* Encapsulated in a waterproof 304 stainless-steel tube ($6\times50\text{ mm}$), communicating via digital 1-Wire protocol with built-in 12-bit ADC ($\pm0.5^\circ\text{C}$ accuracy from $-10^\circ\text{C}$ to $+85^\circ\text{C}$).
3. **Volumetric Soil Moisture (Capacitive Soil Moisture Sensor v1.2):**
   - *Operational Principle:* Measures soil dielectric permittivity via high-frequency capacitance. Insulated copper traces prevent electrochemical galvanic corrosion common to resistive probes (Cabia et al., 2025; Songara & Patel, 2022).
4. **Foliar Leaf Surface Wetness (Industrial Dielectric RS485 Leaf Sensor):**
   - *Operational Principle:* Measures surface dielectric changes caused by water droplets on an IP68 waterproof grid. Interfaced via MAX485 differential transceiver utilizing **RS485 Modbus-RTU protocol** for high noise immunity over field wiring.

### 3.4 Solar-Assisted Power & Battery Storage Technology

#### Reassessment of Initial 3.7V 2600 mAh Li-ion Battery
A standard 18650 3.7V 2600 mAh Li-ion cell provides a nominal capacity of only $9.62\text{ Wh}$. Under active Wi-Fi transmission bursts (up to 240 mA @ 3.3V) and powering 12V RS485 converters, a 2600 mAh cell depletes in **under 16 to 24 hours** without continuous direct sunlight. Moreover, standard Li-ion chemistry degrades rapidly under tropical field temperatures ($>40^\circ\text{C}$ enclosure temperatures) and provides only 300–500 full charge cycles before significant capacity degradation.

#### Upgraded Power Subsystem: Lithium Iron Phosphate (LiFePO₄)
- **Battery Pack:** 12.8V 12Ah ($153.6\text{ Wh}$) LiFePO₄ pack with internal 15A Battery Management System (BMS). LiFePO₄ chemistry provides superior thermal stability (operational up to $60^\circ\text{C}$), non-combustible safety, and an extended lifespan of **2,000 to 4,000 charge cycles** at 80% Depth of Discharge (DoD).
- **Solar Harvesting:** 20W Monocrystalline Photovoltaic Panel ($V_{\text{mp}} = 18.0\text{V}$, $I_{\text{mp}} = 1.11\text{A}$) paired with an IP67 waterproof MPPT charge controller ($\ge 98\%$ conversion efficiency), generating $\approx 67.5\text{ Wh/day}$ under average Philippine solar conditions ($4.5\text{ Peak Sun Hours/day}$).

### 3.5 Edge Data Buffering, Wireless Range vs. Microclimatic Footprint

A critical distinction in agricultural IoT engineering is separating radio-frequency transmission from physical sensing representativeness:
- **Sensor Microclimatic Coverage Footprint ($5\text{ m}$ to $15\text{ m}$ radial zone):** The physical area in a uniform crop canopy where point-source microclimatic measurements accurately reflect field conditions.
- **Wireless RF Communication Range ($30\text{ m}$ to $50\text{ m}$ Line-of-Sight):** The radio transmission distance over 2.4 GHz 802.11 b/g/n between the ESP32 and the farmstead Wi-Fi router.
- **MicroSD Edge FIFO Buffer:** When Wi-Fi is lost, data is queued locally as JSON Lines (`telemetry_buffer.jsonl`). Once reconnected, an idempotent batch HTTP POST synchronizes records with zero loss and server-enforced unique constraints (`node_id + recorded_at`) to eliminate duplicate logs.

### 3.6 Hardware Packaging: Custom PCB vs. Breadboards & IP Enclosure

| Packaging Feature | Solderless Breadboard Prototype | Custom Fabricated PCB Shield | Engineering Impact |
|---|---|---|---|
| **Contact Resistance** | 0.1 Ω to 0.5 Ω per connection | **< 0.01 Ω soldered joint** | Eliminates analog ADC measurement jitter and voltage drift. |
| **Vibration & Wind Resistance** | High risk of loose jumper wires | **Rigid screw terminals & soldered pins** | Field mast vibrations cannot dislodge sensor lines. |
| **Humidity & Oxidation Resistance** | Rapid spring-leaf tarnishing (> 80% RH) | **FR-4 fiberglass with solder mask & conformal coating** | Prevents intermittent open circuits and electrical shorts. |
| **Enclosure Rating** | Open/unrated plastic box | **IP65/IP66 Polycarbonate Enclosure** | Silicone rubber gasket, PG7/PG9 waterproof glands, internal silica gel desiccant. |

### 3.7 State-of-the-Art Comparative Synthesis & Research Gaps

| System Feature / Paradigm | Commercial Agronomic Suites (e.g. CropX) | Mobile Soil Rovers (e.g. Das et al., 2024) | Image AI Apps (e.g. Jafar et al., 2024) | Proposed SolanaWatch System |
|---|---|---|---|---|
| **Monitoring Target** | Deep soil salinity & irrigation | Spatial soil fertility mapping (NPK) | Foliar visible leaf lesions | **Canopy microclimate & root-zone soil (5 parameters)** |
| **Early Warning Timing** | General agronomic advisory | None (Soil classification only) | Post-symptomatic (requires visible damage) | **Pre-symptomatic rule-based risk evaluation** |
| **Target Pathologies** | None (Moisture/fertilizer only) | None | Broad foliar diseases | **Late Blight (*P. infestans*) & Bacterial Wilt (*R. pseudosolanacearum*)** |
| **Power Infrastructure** | Proprietary multi-year sealed pack | High-drain LiPo (1–2 hr runtime) | Smartphone battery / Server | **Autonomous 20W Solar PV + LiFePO₄ Battery (47-Day Autonomy)** |
| **Offline Resilience** | Cellular cloud-dependent | Local offline SD storage | Requires continuous internet | **MicroSD FIFO buffer with idempotent cloud sync** |
| **Deployment Cost** | $> \text{₱}50,000 + \text{monthly SaaS}$ | $\text{₱}25,000 - \text{₱}35,000$ | Free/low app cost, but high damage lag | **Low-cost prototype (~₱7,208) with zero recurring SaaS fees** |

---

## 4. Chapter 3: Technical Background, System Design & Architecture

### 4.1 Requirements Analysis (ISO/IEC 25010)

#### 4.1.1 Functional Requirements (FR-1 to FR-10)

| ID | Functional Requirement | Description | Target Layer |
|---|---|---|---|
| **FR-1** | User Authentication & Authorization | Securely authenticate users using hashed credentials (Argon2/Bcrypt) and restrict dashboard functions via role-based access control. | Web App / Node.js Backend |
| **FR-2** | Environmental Data Acquisition | Automatically sample air temperature, relative humidity, soil temperature, soil moisture, and leaf wetness every 15 minutes. | ESP32 Edge Node / Sensors |
| **FR-3** | Local Offline Edge Logging | Sequentially append timestamped telemetry records as JSON Lines to onboard MicroSD storage whenever Wi-Fi is unavailable. | ESP32 / MicroSD SPI |
| **FR-4** | Cloud Data Synchronization | Synchronize offline records in batches upon Wi-Fi reconnection, enforcing database deduplication constraints. | ESP32 / Backend / Turso DB |
| **FR-5** | Disease-Risk Assessment | Evaluate multi-parameter sensor data against literature-grounded threshold models for Late Blight and Bacterial Wilt. | Cloud Backend Risk Engine |
| **FR-6** | Web-Based Monitoring Dashboard | Provide a responsive UI displaying real-time sensor gauges, time-series charts, disease-risk states, and node status. | React.js / Vite / Tailwind CSS |
| **FR-7** | Early Warning Alert Generation | Trigger color-coded visual alerts (Green = Low, Yellow = Moderate, Red = High) when environmental conditions favor disease development. | Backend / Web Dashboard |
| **FR-8** | Historical Data Visualization | Render interactive multi-series time-series graphs and tabular data with customizable date filtering. | React.js / Chart.js |
| **FR-9** | Device Health Telemetry | Monitor and report edge node battery voltage, solar charging state, Wi-Fi RSSI signal strength, and heartbeat status. | ESP32 Firmware / Web UI |
| **FR-10** | Agronomic Decision Support | Deliver actionable, context-aware cultural preventive recommendations based on active risk level. | Web Dashboard |

#### 4.1.2 Non-Functional Requirements (NFR-1 to NFR-6)

| ID | Non-Functional Requirement | Description & Quality Characteristic | Quality Benchmark / Metric |
|---|---|---|---|
| **NFR-1** | **Reliability** | Ensure continuous telemetry collection and zero data loss across network or power disruptions. | $\ge 99.0\%$ data collection uptime; automatic Hardware Watchdog Timer (WDT) recovery within 5.0 s. |
| **NFR-2** | **Performance Efficiency** | Maintain low latency from sensor acquisition to cloud dashboard display. | End-to-end telemetry propagation latency $< 2.0\text{ s}$; dashboard page load time $< 1.5\text{ s}$. |
| **NFR-3** | **Usability** | Provide an intuitive, clear web dashboard requiring minimal technical training. | System Usability Scale (SUS) score $\ge 80.0 / 100$ (Grade A). |
| **NFR-4** | **Security** | Enforce secure communication and access control. | HTTPS/TLS 1.3 encryption; zero plaintext credentials; parameterized SQL queries. |
| **NFR-5** | **Environmental Resilience** | Operate reliably in outdoor tropical agricultural environments without grid electricity. | Minimum **3 Days of Zero-Sunlight Battery Autonomy**; IP65/IP66 weatherproof enclosure. |
| **NFR-6** | **Interoperability** | Ensure collision-free communication across mixed hardware buses (1-Wire, SPI, RS485 Modbus, ADC). | $100\%$ RS485 Modbus CRC checksum verification; zero bus contention errors. |

---

### 4.2 Bill of Materials (Hardware & Software Specifications)

#### Hardware Bill of Materials (BoM)

| Category | Component / Module | Qty | Exact Part Number & Technical Specifications | Unit Cost (PHP) |
|---|---|---|---|---|
| **Microcontroller** | ESP32 DevKit V1 | 1 | ESP32-WROOM-32, 32-bit Dual-Core 240MHz, 520KB SRAM, 4MB Flash, 2.4GHz Wi-Fi/BT | ₱350.00 |
| **Foliar Sensing** | DHT22 Temp & Humidity | 1 | AM2302, Amb. Temp (-40 to +80°C ±0.5°C), Rel. Humidity (0–100% ±2% RH) | ₱200.00 |
| **Sensor Shelter** | Stevenson Radiation Shield | 1 | Louvered multi-plate solar radiation shield, UV-stabilized ABS plastic | ₱350.00 |
| **Soil Temp** | DS18B20 Digital Probe | 1 | Waterproof stainless-steel probe (304 SS), 1-Wire bus, -55°C to +125°C (±0.5°C) | ₱99.00 |
| **Soil Moisture** | Capacitive Moisture v1.2 | 1 | SKU: SEN0193, corrosion-resistant insulated PCB, Analog output 0.0–3.0V DC | ₱150.00 |
| **Leaf Wetness** | Industrial Leaf Wetness Sensor | 1 | IP68 waterproof dielectric grid, Modbus-RTU protocol over RS485, 7–24V DC input | ₱2,450.00 |
| **Bus Interface** | MAX485 / SP3485 Module | 1 | TTL to RS485 differential converter transceiver module, 3.3V/5V compatible | ₱50.00 |
| **Offline Storage** | MicroSD Module + 16GB Card | 1 | SPI Interface, FAT32 filesystem support, local FIFO JSON Lines logging | ₱210.00 |
| **Solar Harvesting**| 20W 12V Solar PV Panel | 1 | Monocrystalline PV panel ($V_{\text{mp}} = 18.0\text{V}$, $I_{\text{mp}} = 1.11\text{A}$), anodized aluminum frame | ₱850.00 |
| **Charge Controller**| 12V 10A MPPT Controller | 1 | IP67 waterproof, multi-stage LiFePO₄ charging profile, MPPT efficiency $\ge 98\%$ | ₱1,250.00 |
| **Battery Storage**| 12.8V 12Ah LiFePO₄ Battery | 1 | 12.8V, 12Ah (153.6 Wh), built-in 15A BMS (Overcharge/Discharge protection) | ₱2,499.00 |
| **Power Regulators**| DC-DC Step-Down Buck Modules| 2 | LM2596 / MP1584 buck modules: 12V-to-5V (3A) and 12V-to-3.3V (2A), 88% efficiency | ₱140.00 |
| **Enclosure** | Weatherproof Enclosure Box | 1 | IP65/IP66 Polycarbonate junction box ($200 \times 150 \times 100\text{ mm}$), silicone gasket, latches | ₱280.00 |
| **Hardware Mount** | Cable Glands & Field Mast | 1 set | PG7/PG9 waterproof glands, 1.5m galvanized steel mast mounting bracket | ₱129.00 |
| **PCB Shield** | Custom Fabricated Proto-Shield| 1 | Double-sided FR-4 PCB, screw terminals, soldered pin headers, ground plane | ₱250.00 |
| **Total Hardware Cost** | | | | **₱7,208.00** |

#### Software Toolchain & Stack

| Layer / Role | Technology Stack | Role in SolanaWatch Architecture |
|---|---|---|
| **Firmware Development** | Visual Studio Code & PlatformIO | Embedded C++ development, FreeRTOS task scheduling, SPI/UART driver integration. |
| **Cloud Backend API** | Node.js & Express.js | RESTful API server, telemetry ingestion, batch deduplication, and disease-risk calculation. |
| **Cloud Database** | Turso (Distributed libSQL / SQLite) | Edge-replicated cloud database with composite unique constraints for historical records. |
| **Frontend Dashboard** | React.js & Vite | Single-page web dashboard for live monitoring and administrative management. |
| **Styling & Graphing** | Tailwind CSS & Chart.js | Responsive UI styling, dynamic gauges, and interactive multi-series time-series charts. |
| **Version Control** | Git & GitHub | Collaborative source code versioning, issue tracking, and CI/CD repository. |

---

### 4.3 Development Methodology (Prototyping Model)

SolanaWatch follows the **Prototyping Model** to facilitate continuous hardware-firmware-software iteration:

```
[Requirements Gathering & Analysis]
                |
                v
          [Quick Design]
                |
                v
        [Build Prototype] <---------------+
                |                         |
                v                         | Refinements
       [Evaluate & Test] -----------------+
                |
                v (Accepted)
    [Final Implementation & Deployment]
```

| Prototyping Phase | Core Activities | Inputs | Key Deliverables |
|---|---|---|---|
| **1. Requirements Gathering** | Stakeholder consultations, Solanaceae epidemiology review, hardware selection. | PSA crop reports, plant pathology literature. | System Requirements Specification (SRS), Scope Matrix. |
| **2. Quick Design** | Schematic design, power budget modeling, database ER drafting, UI wireframes. | Sensor datasheets, threshold models. | Circuit schematics, Turso ER schema, Figma mockups. |
| **3. Build Prototype** | PCB soldering, firmware coding (FreeRTOS, SD logging, RS485 Modbus), backend API build. | VS Code, PlatformIO, electronic modules. | Functional edge node prototype, REST backend, React UI. |
| **4. Evaluation & Testing** | Laboratory 2-point sensor calibration, RSSI range decay test, 72-hr battery stress test. | Calibrated reference meters, test cases. | Calibration lookup curves, RSSI profiles, test logs. |
| **5. Refining Prototype** | Hardware Watchdog Timer integration, debounce logic, UI responsiveness improvements. | Test logs, bug reports, expert feedback. | Hardened firmware, optimized PCB shield, refined UI. |
| **6. Final Implementation** | 7-day unattended field deployment in crop plot, operational verification. | Assembled hardware, test plot. | Validated SolanaWatch platform, complete documentation. |

---

### 4.4 System Architecture & Data Flow

```
+---------------------------------------------------------------------------------------------------------+
|                                    SOLANAWATCH SYSTEM ARCHITECTURE                                      |
+---------------------------------------------------------------------------------------------------------+
|                                                                                                         |
|  [ LAYER 1: EDGE SENSING & HARDWARE NODE ]                                                             |
|   +--------------------------------------------------------------------------------------------------+  |
|   |  - DHT22 (Air Temp & RH in Stevenson Shield)                                                     |  |
|   |  - DS18B20 (Soil Temperature @ 10cm depth via 1-Wire GPIO 4)                                     |  |
|   |  - Capacitive Soil Moisture v1.2 (Soil Moisture @ 10cm depth via ADC GPIO 34)                    |  |
|   |  - Industrial Leaf Wetness Grid (Modbus-RTU over MAX485 UART2 GPIO 16/17)                        |  |
|   |  - Power: 20W Solar PV + 12.8V LiFePO4 Battery + MPPT Controller (5V/3.3V Buck Regulators)       |  |
|   |  - ESP32 Dual-Core MCU (FreeRTOS: Sensor Sampling -> JSON Packaging -> MicroSD SPI Backup)       |  |
|   +--------------------------------------------------------------------------------------------------+  |
|                                                  |                                                      |
|                                    2.4 GHz Wi-Fi | HTTP POST /api/telemetry                             |
|                                                  v                                                      |
|  [ LAYER 2: CLOUD BACKEND & DATA MANAGEMENT ]                                                          |
|   +--------------------------------------------------------------------------------------------------+  |
|   |  - Node.js & Express.js REST API Server                                                          |  |
|   |  - Transactional Batch Ingestion & Deduplication Handler                                         |  |
|   |  - Turso Distributed libSQL Database (users, nodes, sensor_readings, disease_risk_logs, alerts)  |  |
|   |  - Disease Risk Engine:                                                                          |  |
|   |      * Late Blight Module (Wallin Severity Values & Leaf Wetness Duration)                       |  |
|   |      * Bacterial Wilt Module (Hydrothermal Soil Temperature & Moisture Scoring)                  |  |
|   +--------------------------------------------------------------------------------------------------+  |
|                                                  |                                                      |
|                                       JSON HTTPS | WebSockets / REST API                                |
|                                                  v                                                      |
|  [ LAYER 3: WEB MONITORING & DECISION SUPPORT ]                                                         |
|   +--------------------------------------------------------------------------------------------------+  |
|   |  - React.js Single Page Application (Vite + Tailwind CSS + Chart.js)                             |  |
|   |  - Real-Time Environmental Gauges & Multi-Series Historical Trend Graphs                         |  |
|   |  - Color-Coded Early Warning Alert System (Green = Low, Yellow = Moderate, Red = High)           |  |
|   |  - Actionable Agronomic Recommendations & Edge Node Telemetry Health Status                      |  |
|   +--------------------------------------------------------------------------------------------------+  |
+---------------------------------------------------------------------------------------------------------+
```

---

### 4.5 Circuit Pinout & Hardware Interfacing Schematic

```
+---------------------------------------------------------------------------------------------------------+
|                                    SOLANAWATCH CIRCUIT SCHEMATIC                                        |
+---------------------------------------------------------------------------------------------------------+
|                                                                                                         |
|  [ 20W Solar PV Panel ] ===> [ 12V 10A MPPT Solar Charge Controller ] <===> [ 12.8V 12Ah LiFePO4 Batt ] |
|                                             |                                                           |
|                     +-----------------------+-----------------------+                                   |
|                     | 12.0V DC Rail                                 | 12.0V DC Rail                     |
|                     v                                               v                                   |
|        [ Buck Step-Down (12V->5V) ]                    [ Buck Step-Down (12V->3.3V) ]                   |
|                     | 5.0V DC Rail                                  | 3.3V DC Rail                      |
|                     +-----------------------+                       +-------------------+               |
|                                             |                                           |               |
|                                             v                                           v               |
|                             +-----------------------------------+                       |               |
|                             |      ESP32 DevKit V1 (MCU)        |                       |               |
|                             |                                   |                       |               |
|  [ DHT22 Sensor ] <------- | GPIO 15 (Digital In/Out + 4.7kΩ)  | <---------------------+ (3.3V Power)  |
|                             |                                   |                                       |
|  [ DS18B20 Probe ] <------ | GPIO 4  (1-Wire Bus + 4.7kΩ Pull) | <---------------------+ (3.3V Power)  |
|                             |                                   |                                       |
|  [ Capacitive Moisture ] <- | GPIO 34 (ADC1_CH6 Analog Input)   | <---------------------+ (3.3V Power)  |
|                             |                                   |                                       |
|  [ MAX485 Converter ] <--- | GPIO 16 (RX2), GPIO 17 (TX2)      | <---------------------+ (3.3V Power)  |
|         |                   | GPIO 21 (DE/RE Flow Control)      |                                       |
|         |                   |                                   |                                       |
|         +-- (RS485 A/B) --> | [ IP68 Leaf Wetness Sensor ] <----------------------------+ (12V Power)   |
|                             |                                   |                                       |
|  [ MicroSD SPI Card ] <--- | GPIO 5 (CS), GPIO 18 (SCK)        | <---------------------+ (3.3V Power)  |
|                             | GPIO 19 (MISO), GPIO 23 (MOSI)    |                                       |
|                             |                                   |                                       |
|  [ Battery Voltage Div ] <- | GPIO 35 (ADC1_CH7 100k/22k Divider)| <-------------------+ (12V Batt Rail) |
|                             +-----------------------------------+                                       |
|                                             |                                                           |
|                                            GND (Common Continuous Ground Plane)                         |
+---------------------------------------------------------------------------------------------------------+
```

#### Detailed GPIO Interfacing Table

| Component Name | ESP32 GPIO Pin | Interface Protocol | Operating Voltage | Pull-Up / External Circuitry |
|---|---|---|---|---|
| **DHT22 Temp & Humidity** | `GPIO 15` | Single-Wire Proprietary Digital | 3.3V DC | $4.7\text{ k}\Omega$ pull-up resistor to 3.3V rail. |
| **DS18B20 Soil Temp Probe** | `GPIO 4` | Dallas 1-Wire Digital Bus | 3.3V DC | $4.7\text{ k}\Omega$ pull-up resistor between Data and 3.3V rail. |
| **Capacitive Soil Moisture**| `GPIO 34` | Analog-to-Digital Converter (ADC1_CH6) | 3.3V DC | Native analog input ($0.0\text{V} - 3.0\text{V}$ output). |
| **MAX485 Transceiver (RX)** | `GPIO 16` | Hardware Serial UART2 (RX2) | 3.3V DC | Connected to MAX485 `RO` pin. |
| **MAX485 Transceiver (TX)** | `GPIO 17` | Hardware Serial UART2 (TX2) | 3.3V DC | Connected to MAX485 `DI` pin. |
| **MAX485 Direction Control**| `GPIO 21` | Digital Output (GPIO) | 3.3V DC | Tied to `DE` and `RE` for half-duplex direction control. |
| **RS485 Leaf Wetness Sensor**| RS485 Differential | RS485 Modbus-RTU over A/B lines | 12.0V DC | $120\ \Omega$ termination resistor across A-B differential lines. |
| **MicroSD Module (CS)** | `GPIO 5` | Hardware SPI Bus (Chip Select) | 3.3V DC | Dedicated SPI chip select line. |
| **MicroSD Module (SCK)** | `GPIO 18` | Hardware SPI Bus (Clock) | 3.3V DC | SPI Clock line. |
| **MicroSD Module (MISO)** | `GPIO 19` | Hardware SPI Bus (Data In) | 3.3V DC | SPI Master In / Slave Out line. |
| **MicroSD Module (MOSI)** | `GPIO 23` | Hardware SPI Bus (Data Out) | 3.3V DC | SPI Master Out / Slave In line. |
| **Battery Voltage Monitor** | `GPIO 35` | Analog-to-Digital Converter (ADC1_CH7) | 3.3V DC | Precision resistor voltage divider ($100\text{ k}\Omega / 22\text{ k}\Omega$). |

---

### 4.6 Mathematical Power Subsystem Sizing & Verification

#### 1. Daily Energy Consumption Budget ($E_{\text{daily}}$)
The edge node operates on a **15-minute polling interval** ($96\text{ cycles/day}$):
- **Active Cycle ($t_{\text{act}}$):** $10\text{ seconds}$ (Sensor warm-up, RS485 query, SD write, Wi-Fi TX).
- **Deep Sleep Cycle ($t_{\text{sleep}}$):** $890\text{ seconds}$ ($14\text{ min } 50\text{ s}$, ULP timer active).

$$\begin{aligned}
P_{\text{act}} &= (3.3\text{V} \times 0.251\text{A}) + (12.0\text{V} \times 0.030\text{A}) = 0.828\text{W} + 0.360\text{W} = \mathbf{1.188\text{ Watts}} \\
P_{\text{sleep}} &= (3.3\text{V} \times 0.0004\text{A}) + (12.0\text{V} \times 0.005\text{A}) = 0.00132\text{W} + 0.060\text{W} = \mathbf{0.06132\text{ Watts}} \\
E_{\text{cycle}} &= \left[ 1.188\text{W} \times \frac{10\text{ s}}{3600\text{ s}} \right] + \left[ 0.06132\text{W} \times \frac{890\text{ s}}{3600\text{ s}} \right] = 0.00330\text{ Wh} + 0.01515\text{ Wh} = \mathbf{0.01845\text{ Wh/cycle}} \\
E_{\text{daily\_base}} &= 96\text{ cycles/day} \times 0.01845\text{ Wh} = \mathbf{1.7712\text{ Watt-hours/day}}
\end{aligned}$$

Applying a **30% engineering safety margin ($\times 1.30$)** to account for Wi-Fi retransmission retries and temperature variations:

$$E_{\text{daily\_design}} = 1.7712\text{ Wh/day} \times 1.30 \approx \mathbf{2.30\text{ Watt-hours per day}}$$

#### 2. Battery Capacity Sizing ($C_{\text{battery}}$)
Targeting a minimum of **3 Days of Zero-Sunlight Autonomy ($N_{\text{days}} = 3$)** at 80% Depth of Discharge ($\text{DoD} = 0.80$) and 88% DC buck efficiency ($\eta_{\text{reg}} = 0.88$):

$$C_{\text{Wh}} = \frac{E_{\text{daily\_design}} \times N_{\text{days}}}{\text{DoD} \times \eta_{\text{reg}}} = \frac{2.30\text{ Wh} \times 3}{0.80 \times 0.88} = \frac{6.90}{0.704} \approx \mathbf{9.80\text{ Watt-hours}}$$

$$C_{\text{Ah\_required}} = \frac{9.80\text{ Wh}}{12.8\text{V}} \approx \mathbf{0.766\text{ Ampere-hours (766 mAh)}}$$

**Selected Specification:** The integrated **12.8V 12Ah ($153.6\text{ Wh}$) LiFePO₄ pack** provides:

$$\text{Actual Autonomy} = \frac{153.6\text{ Wh} \times 0.80 \times 0.88}{2.30\text{ Wh/day}} \approx \mathbf{47.0\text{ Days of Continuous Autonomy}}$$

This guarantees 100% operational uptime through multi-week Philippine rainy/monsoon periods.

#### 3. Solar Photovoltaic Sizing ($P_{\text{solar}}$)
Based on the Philippine national average insolation of **4.5 Peak Sun Hours ($PSH = 4.5\text{ h/day}$)** and system efficiency of **75% ($\eta_{\text{sys}} = 0.75$):**

$$P_{\text{solar\_required}} = \frac{E_{\text{daily\_design}}}{PSH \times \eta_{\text{sys}}} = \frac{2.30\text{ Wh}}{4.5\text{ h} \times 0.75} = \frac{2.30}{3.375} \approx \mathbf{0.68\text{ Watts}}$$

**Selected Specification:** The selected **20W Monocrystalline Solar Panel** generates:

$$\text{Daily Generation} = 20\text{W} \times 4.5\text{ h} \times 0.75 = \mathbf{67.5\text{ Watt-hours per day}}$$

The 20W panel exceeds daily consumption by a factor of 29, fully replenishing daily power consumption within **15 minutes of direct sunlight** or maintaining net positive charging under overcast daylight.

---

### 4.7 Literature-Grounded Disease-Risk Algorithms & Mathematical Models

#### Multi-Parameter Disease Environmental Thresholds

| Monitored Parameter | Sensor Module | Optimal Crop Baseline | Late Blight (*P. infestans*) Conducive Conditions | Bacterial Wilt (*R. pseudosolanacearum*) Conducive Conditions | Plant Pathology Reference |
|---|---|---|---|---|---|
| **Ambient Air Temp** | DHT22 (Stevenson Shield) | 24°C – 28°C | **12°C – 22°C (Optimal sporulation: 15°C–20°C)** | 28°C – 35°C | Boulton et al. (2023); Mazumdar et al. (2021) |
| **Relative Humidity** | DHT22 (Stevenson Shield) | 60% – 80% RH | **≥ 90% RH** | ≥ 85% RH | Mazumdar et al. (2021); Tao et al. (2024) |
| **Leaf Wetness Duration**| IP68 RS485 Modbus Sensor | 0 hours (Dry) | **≥ 10 continuous hours** | Not a primary foliar driver | Boulton et al. (2023); IFAS Extension (n.d.) |
| **Soil Temperature** | DS18B20 (10 cm depth) | 18°C – 24°C | < 20°C (when humid) | **28°C – 35°C (Optimal bacterial multiplication)**| Silva et al. (2024); Subedi et al. (2024) |
| **Soil Moisture** | Capacitive v1.2 (10 cm) | 40% – 60% VWC | > 60% VWC | **≥ 75% VWC (Saturated / Waterlogged pore space)**| Jiang et al. (2021); Subedi et al. (2024) |

---

#### 4.7.1 Late Blight Severity Value Algorithm (Wallin / BLITECAST)

Late Blight infection risk is evaluated using an adapted **Wallin Severity Value (SV)** tracking cumulative consecutive hours of leaf wetness and ambient temperature:

```
IF (Leaf Wetness Duration < 6 continuous hours) THEN:
    Late_Blight_SV = 0  --> [ LOW RISK (Green) ]

ELSE IF (6 <= Leaf Wetness Duration < 10 continuous hours) AND (12°C <= Air_Temp <= 22°C) THEN:
    Late_Blight_SV = 1  --> [ MODERATE RISK (Yellow) ]

ELSE IF (10 <= Leaf Wetness Duration < 15 continuous hours) AND (12°C <= Air_Temp <= 22°C) THEN:
    Late_Blight_SV = 2  --> [ MODERATE RISK (Yellow) ]

ELSE IF (Leaf Wetness Duration >= 15 continuous hours) AND (12°C <= Air_Temp <= 22°C)
     OR (Leaf Wetness Duration >= 10 continuous hours) AND (Relative_Humidity >= 90%) THEN:
    Late_Blight_SV = 3  --> [ HIGH RISK ALERT (Red) ]
```

---

#### 4.7.2 Bacterial Wilt Hydrothermal Risk Index

Bacterial Wilt risk is calculated using a normalized composite hydrothermal score ($R_{\text{BW}}$):

$$R_{\text{BW}} = (0.50 \times S_{\text{ST}}) + (0.50 \times S_{\text{SM}})$$

Where $S_{\text{ST}}$ is the Soil Temperature Factor and $S_{\text{SM}}$ is the Soil Moisture Factor:

$$S_{\text{ST}} = \begin{cases} 
1.0, & \text{if } 28^\circ\text{C} \le \text{Soil Temp} \le 35^\circ\text{C} \quad (\text{Optimal bacterial multiplication}) \\
0.6, & \text{if } 25^\circ\text{C} \le \text{Soil Temp} < 28^\circ\text{C} \\
0.2, & \text{if } 20^\circ\text{C} \le \text{Soil Temp} < 25^\circ\text{C} \\
0.0, & \text{if } \text{Soil Temp} < 20^\circ\text{C} \text{ or } \text{Soil Temp} > 38^\circ\text{C}
\end{cases}$$

$$S_{\text{SM}} = \begin{cases} 
1.0, & \text{if } \text{Soil Moisture} \ge 75\%\text{ VWC} \quad (\text{Saturated / Waterlogged}) \\
0.6, & \text{if } 60\%\text{ VWC} \le \text{Soil Moisture} < 75\%\text{ VWC} \\
0.2, & \text{if } 40\%\text{ VWC} \le \text{Soil Moisture} < 60\%\text{ VWC} \quad (\text{Optimal Field Capacity}) \\
0.0, & \text{if } \text{Soil Moisture} < 40\%\text{ VWC} \quad (\text{Dry Soil})
\end{cases}$$

#### Risk Level Categorization & Recommendations

| Computed Risk Score | Alert Level & Color | System Display | Actionable Agronomic Recommendation |
|---|---|---|---|
| **$R_{\text{BW}} < 0.40$ / $\text{SV} = 0$** | **LOW (Green)** | Normal Status | Environmental conditions are unfavorable for disease development. Maintain routine field scouting and standard crop management. |
| **$0.40 \le R_{\text{BW}} < 0.70$ / $\text{SV} \in \{1, 2\}$** | **MODERATE (Yellow)** | Advisory Warning | Environmental conditions are moderately favorable. Enhance canopy aeration through selective weeding/pruning; inspect soil drainage channels. |
| **$R_{\text{BW}} \ge 0.70$ / $\text{SV} = 3$** | **HIGH (Red)** | Immediate Alert | Highly conducive disease microclimate. Immediately withhold overhead sprinkler irrigation, open furrow drainage, and apply preventive bio-fungicides/protective sprays. |

---

### 4.8 Database Schema & Data Architecture (Turso libSQL)

```
+------------------+         +-------------------+         +------------------------+
|    users_tbl     | 1     * |    nodes_tbl      | 1     * |  sensor_readings_tbl   |
|------------------|---------|-------------------|---------|------------------------|
| PK user_id (UUID)|         | PK node_id (UUID) |         | PK reading_id (UUID)   |
|    full_name     |         | FK user_id        |         | FK node_id             |
|    email (UQ)    |         |    node_name      |         |    air_temperature     |
|    password_hash |         |    crop_type      |         |    air_humidity        |
|    role          |         |    field_location |         |    soil_temperature    |
|    created_at    |         |    battery_voltage|         |    soil_moisture       |
+------------------+         |    last_seen_at   |         |    leaf_wetness_status |
                             +-------------------+         |    recorded_at (UQ)    |
                                       | 1                 |    synced_at           |
                                       |                   +------------------------+
                                       | *                             | 1
                             +-------------------+                     | *
                             |   disease_risk_   |         +------------------------+
                             |     logs_tbl      |         |     alerts_tbl         |
                             |-------------------|         |------------------------|
                             | PK log_id (UUID)  |         | PK alert_id (UUID)     |
                             | FK node_id        |         | FK node_id             |
                             | FK reading_id     |         | FK reading_id          |
                             |    late_blight_sv |         |    disease_target      |
                             |    bact_wilt_idx  |         |    alert_level         |
                             |    calculated_at  |         |    message             |
                             +-------------------+         |    created_at          |
                                                           +------------------------+
```

#### Database Schema DDL Specification

```sql
-- 1. Users Table
CREATE TABLE users_tbl (
    user_id TEXT PRIMARY KEY, -- UUID v4
    full_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('admin', 'technician', 'farmer')),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 2. Nodes Table
CREATE TABLE nodes_tbl (
    node_id TEXT PRIMARY KEY, -- Hardware MAC / UUID
    user_id TEXT NOT NULL,
    node_name TEXT NOT NULL,
    crop_type TEXT NOT NULL CHECK(crop_type IN ('Tomato', 'Eggplant', 'Pepper', 'Potato')),
    field_location TEXT NOT NULL,
    battery_voltage REAL DEFAULT 12.8,
    last_seen_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users_tbl(user_id) ON DELETE CASCADE
);

-- 3. Sensor Readings Table (with Composite Unique Deduplication)
CREATE TABLE sensor_readings_tbl (
    reading_id TEXT PRIMARY KEY, -- UUID v4
    node_id TEXT NOT NULL,
    air_temperature REAL NOT NULL, -- in °C
    air_humidity REAL NOT NULL,    -- in % RH
    soil_temperature REAL NOT NULL,-- in °C
    soil_moisture REAL NOT NULL,   -- in % VWC
    leaf_wetness_status INTEGER NOT NULL CHECK(leaf_wetness_status IN (0, 1)),
    leaf_wetness_val REAL DEFAULT 0.0,
    recorded_at DATETIME NOT NULL,
    synced_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (node_id) REFERENCES nodes_tbl(node_id) ON DELETE CASCADE,
    UNIQUE(node_id, recorded_at) -- Deduplication constraint
);

-- 4. Disease Risk Logs Table
CREATE TABLE disease_risk_logs_tbl (
    log_id TEXT PRIMARY KEY,
    node_id TEXT NOT NULL,
    reading_id TEXT NOT NULL,
    late_blight_sv INTEGER NOT NULL CHECK(late_blight_sv BETWEEN 0 AND 3),
    bact_wilt_idx REAL NOT NULL,
    calculated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (node_id) REFERENCES nodes_tbl(node_id) ON DELETE CASCADE,
    FOREIGN KEY (reading_id) REFERENCES sensor_readings_tbl(reading_id) ON DELETE CASCADE
);

-- 5. Alerts Table
CREATE TABLE alerts_tbl (
    alert_id TEXT PRIMARY KEY,
    node_id TEXT NOT NULL,
    reading_id TEXT NOT NULL,
    disease_target TEXT NOT NULL CHECK(disease_target IN ('Late Blight', 'Bacterial Wilt')),
    alert_level TEXT NOT NULL CHECK(alert_level IN ('Moderate', 'High')),
    message TEXT NOT NULL,
    is_resolved INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (node_id) REFERENCES nodes_tbl(node_id) ON DELETE CASCADE,
    FOREIGN KEY (reading_id) REFERENCES sensor_readings_tbl(reading_id) ON DELETE CASCADE
);
```

---

### 4.9 Offline Edge Resilient Data Synchronization Protocol

```
ESP32 Edge Node                                           Node.js Backend & Turso DB
      |                                                              |
      |--- 1. Read Sensors (DHT22, DS18B20, Soil, Leaf) ----------->|
      |                                                              |
      |--- 2. Check Wi-Fi Connection State                          |
      |    |                                                         |
      |    +-- [Wi-Fi Down] -> Append JSON line to MicroSD Card      |
      |    |                   (telemetry_buffer.jsonl)              |
      |    |                                                         |
      |    +-- [Wi-Fi Up]   -> Read MicroSD Buffer (Max 25 records)  |
      |                        HTTP POST /api/telemetry/batch ------>|
      |                                                              |--- 3. Validate Payload Format
      |                                                              |--- 4. Execute SQL INSERT OR IGNORE
      |                                                              |       (Enforce UNIQUE constraint)
      |                                                              |--- 5. Execute Disease Risk Engine
      |                                                              |--- 6. Generate Alerts if Red/Yellow
      |<-- HTTP 200/201 Success Response with Synced IDs ------------|
      |                                                              |
      |--- 7. Flush Synced Records from MicroSD Buffer               |
      |--- 8. Enter ULP Deep Sleep for 890 seconds (15-min cycle) ->|
```

---

## 5. Quality Assurance, Verification & Testing Framework

### 5.1 Sensor Calibration Protocols

1. **Capacitive Soil Moisture Sensor v1.2 (2-Point Calibration):**
   - *Step 1 (Dry Air Baseline - 0% VWC):* Suspend probe in dry ambient air ($25^\circ\text{C}$); record raw $ADC_{\text{dry}} \approx 3200$.
   - *Step 2 (Distilled Water Saturation - 100% VWC):* Submerge probe up to the maximum immersion line in distilled water; record $ADC_{\text{wet}} \approx 1450$.
   - *Calibration Equation:* $\text{Moisture (\%)} = \left[ \frac{ADC_{\text{dry}} - ADC_{\text{raw}}}{ADC_{\text{dry}} - ADC_{\text{wet}}} \right] \times 100\%$ (clamped between 0% and 100%).
2. **DS18B20 Digital Soil Temperature Probe:**
   - Verify readings across a 2-point reference bath: Ice-water slurry ($0.0^\circ\text{C} \pm 0.1^\circ\text{C}$) and warm circulating bath ($40.0^\circ\text{C} \pm 0.1^\circ\text{C}$) against a calibrated mercury laboratory thermometer ($\pm 0.5^\circ\text{C}$ acceptance band).
3. **DHT22 Ambient Air Relative Humidity:**
   - Enclose probe inside an airtight test container containing a saturated Sodium Chloride ($\text{NaCl}$) salt slurry ($75.3\%\text{ RH}$ equilibrium at $25^\circ\text{C}$) to establish factory offset verification.
4. **RS485 Leaf Wetness Sensor:**
   - Validate 0% baseline reading in dry laboratory conditions and positive wet-state transition under fine aerosol water misting.

---

### 5.2 Unit, Integration & Stress Test Cases

#### Component-Level Unit Test Cases

| Test ID | Target Component | Test Procedure & Stimulus | Expected Result | Requirement |
|---|---|---|---|---|
| **TC-HW-01** | DHT22 Sensor | Sample air temp/RH inside Stevenson shield across varying ambient diurnal cycles. | Captures ambient temp ($\pm0.5^\circ\text{C}$) and RH ($\pm3\%\text{ RH}$) accurately. | FR-2, NFR-1 |
| **TC-HW-02** | DS18B20 Probe | Monitor root-zone soil temperature at 10 cm depth under wet and dry soil conditions. | Delivers stable 1-Wire temperature data without bus dropouts. | FR-2, NFR-1 |
| **TC-HW-03** | Capacitive Moisture | Measure output across oven-dried soil, field capacity soil, and flooded saturation. | Monotonic linear voltage curve from 0% to 100% VWC. | FR-2, NFR-1 |
| **TC-HW-04** | Leaf Wetness Sensor | Query RS485 Modbus-RTU registers via MAX485 transceiver under dry and sprayed leaves. | Correctly parses Modbus response and CRC checksum. | FR-2, NFR-6 |
| **TC-HW-05** | MicroSD Storage | Disconnect Wi-Fi router; trigger 10 consecutive sensor sampling cycles. | Appends 10 valid JSON Lines to MicroSD card buffer. | FR-3, NFR-1 |
| **TC-HW-06** | MPPT Solar Charger | Connect discharged battery ($11.5\text{V}$) to 20W solar panel under sunlight. | Regulates charge current up to 1.1A; cuts off at $14.4\text{V}$ bulk limit. | NFR-1, NFR-5 |
| **TC-HW-07** | Step-Down Bucks | Sweep input voltage from $10.0\text{V}$ to $14.4\text{V}$ under active 300 mA load. | 5V buck outputs $5.0\text{V} \pm 0.1\text{V}$; 3.3V buck outputs $3.3\text{V} \pm 0.05\text{V}$. | NFR-1, NFR-5 |

#### System Integration & Software Test Cases

| Test ID | Target Module | Test Description & Action | Expected Result | Requirement |
|---|---|---|---|---|
| **TC-SW-01** | User Authentication | Attempt login with valid and invalid credentials; test role-protected routes. | Authenticates valid users; blocks invalid requests with HTTP 401/403. | FR-1, NFR-4 |
| **TC-SW-02** | Telemetry Ingestion | Transmit live multi-sensor JSON payload via HTTP POST to `/api/telemetry`. | Ingests and parses readings; returns HTTP 201 Created. | FR-2, FR-6 |
| **TC-SW-03** | Disease Risk Engine | Feed edge conditions simulating Late Blight ($\text{LWD} \ge 15\text{h}$, $18^\circ\text{C}$) and Bacterial Wilt ($32^\circ\text{C}$, $85\%$ VWC). | Computes $\text{SV}=3$ (Late Blight Red Alert) and $R_{\text{BW}}=1.0$ (Bacterial Wilt Red Alert). | FR-5, FR-7 |
| **TC-SW-04** | Deduplication & Sync | Reconnect Wi-Fi and upload batch payload containing overlapping timestamps. | Inserts new unique records; ignores duplicate records without error. | FR-4, NFR-1 |
| **TC-SW-05** | Alert Notification | Trigger Moderate/High risk threshold state in backend. | Generates visual alert banner on React web dashboard within 2.0 s. | FR-7 |
| **TC-SW-06** | Chart Visualization | Filter historical data across 24-hour, 7-day, and 30-day views. | Dynamically renders responsive time-series charts without UI freeze. | FR-8, NFR-2 |

#### Reliability, RF Range & Autonomy Stress Test Cases

| Test ID | Stress Category | Empirical Test Methodology | Expected Result | Requirement |
|---|---|---|---|---|
| **TC-REL-01** | 7-Day Field Uptime | Deploy prototype in open Solanaceae plot for 7 consecutive days ($672\text{ cycles}$). | Operates unattended with $\ge 99.0\%$ data completion rate in cloud DB. | NFR-1, NFR-5 |
| **TC-REL-02** | Wi-Fi RSSI Range | Measure ESP32 RSSI (dBm) and Packet Delivery Ratio at 5m, 10m, 20m, 30m, 50m. | $\text{RSSI} > -80\text{ dBm}$ and $\text{PDR} \ge 95\%$ at distances $\le 35\text{ m}$ Line-of-Sight. | NFR-6 |
| **TC-REL-03** | Battery Deprivation | Disconnect 20W solar PV panel; operate node on fully charged 12.8V battery. | Operates continuously on 15-minute cycles for $> 72\text{ hours}$ without shutdown. | NFR-5 |
| **TC-REL-04** | Watchdog Recovery | Force firmware into an intentional blocking infinite while-loop. | Hardware Watchdog Timer resets ESP32 within 5.0 s; resumes normal logging. | NFR-1 |
| **TC-REL-05** | Enclosure Sealing | Subject IP66 enclosure to continuous water spray simulating heavy tropical downpours. | Zero moisture ingress or condensation inside electronics compartment. | NFR-5 |
| **TC-UAT-01** | Stakeholder Usability | Conduct System Usability Scale (SUS) survey with 10 farmers and technicians. | Achieves a mean SUS score $\ge 80.0 / 100$ (Grade A usability). | NFR-3 |

---

### 5.3 Quality Metrics & Acceptance Criteria

| ISO/IEC 25010 Quality Metric | Target Acceptance Criteria | Empirical Verification Method | Literature / Standard Benchmark |
|---|---|---|---|
| **Sensor Measurement Accuracy** | **90% – 95%** | Calibration bath & reference meter validation | Cabia et al. (2025); Mane et al. (2024) |
| **Communication Reliability** | **≥ 95% Packet Delivery** | Multi-distance RSSI and packet loss profiling | Suryadevara et al. (2022); Tao et al. (2024) |
| **Continuous Device Uptime** | **≥ 99% Operational Uptime** | 7-day continuous field deployment logging | Rachakonda & Stasiewicz (2024) |
| **Disease Rule Logic Accuracy** | **≥ 95% Logical Accuracy** | Synthetic edge threshold validation test suites | Boulton et al. (2023); Silva et al. (2024) |
| **Zero-Sunlight Battery Autonomy**| **≥ 3 Days (72 Hours)** | Physical solar disconnection load testing | Gao et al. (2023) |
| **System Usability Scale (SUS)** | **≥ 80.0 / 100 (Grade A)** | Standard 10-question SUS questionnaire ($N=10$) | Turner (2022); ISO/IEC 25010 Usability |

---

## 6. Implementation & Feasibility Analysis

### 6.1 Internal & External Operational Environments

#### Internal Environment
Encompasses the integrated hardware sensing node, solar charge subsystem, custom FR-4 PCB shield, cloud backend services, distributed database, and the development team. The iterative prototyping model facilitates continuous firmware debugging, Watchdog Timer verification, and UI refinements.

#### External Environment
Encompasses the open-field and screenhouse Solanaceae cultivation plots in the Philippines, local farmers, LGU agricultural technicians, fluctuating tropical weather (heat, monsoons, high humidity), and intermittent wireless connectivity. The solar-assisted LiFePO₄ battery, IP66 weatherproof enclosure, Stevenson radiation shield, and MicroSD offline buffer ensure continuous resilience against these external environmental challenges.

### 6.2 Technical, Operational & Economic Feasibility

- **Technical Feasibility:** Validated by the dual-core ESP32 microcontroller, FreeRTOS multi-threading, low-latency Turso libSQL database, and robust RS485 Modbus/SPI hardware buses.
- **Operational Feasibility:** The system requires no specialized software installation—farmers and technicians access real-time gauges, time-series graphs, and clear color-coded alerts through standard web browsers on any mobile phone, tablet, or PC.
- **Economic Feasibility:** The entire edge hardware prototype is assembled for **₱7,208.00**, leveraging open-source software libraries and zero recurrent SaaS fees. By mitigating disease-induced harvest losses of 50%–90%, the system offers high return on investment for smallholder Solanaceae growers.

### 6.3 Field Deployment Procedures

```
1. Laboratory Sensor Calibration
   - Execute 2-point calibration on capacitive soil moisture probe (dry air vs. water).
   - Verify DS18B20 soil temp in ice bath (0.0°C) and DHT22 RH in saturated NaCl chamber (75.3% RH).

2. Mast & Solar Mounting
   - Secure 1.5m galvanized steel field mast in representative crop plot.
   - Mount IP66 enclosure box and angle 20W solar PV panel toward true South (15° tilt).

3. Canopy & Soil Sensor Placement
   - Install DHT22 inside Stevenson shield at canopy level (1.0m to 1.2m height).
   - Attach RS485 dielectric leaf wetness sensor within upper foliar canopy.
   - Insert DS18B20 digital probe and capacitive soil moisture probe into root zone (10 cm depth).

4. Electrical Commissioning & Wi-Fi Linking
   - Connect LiFePO4 battery and solar PV to MPPT charge controller.
   - Establish 2.4 GHz Wi-Fi link between ESP32 edge node and local gateway/access point.

5. Cloud Activation & Validation
   - Verify real-time telemetry ingestion on Turso cloud database and React web dashboard.
   - Simulate network disconnection to confirm local MicroSD FIFO logging.
   - Activate 24/7 automated continuous disease-risk monitoring.
```

---

## 7. Oral Defense Compliance & Panel Revision Action Matrix

The capstone proposal oral defense evaluation returned a verdict of **Major Revisions**. Below is the complete 24-point compliance matrix addressing every panel remark with exact technical actions implemented:

| # | Panel Comment / Revision Item | Target Manuscript Section | Identified Weakness in Initial Draft | Exact Technical Action Implemented |
|---|---|---|---|---|
| **1** | Comparative analysis of ESP32, Arduino Leonardo, and Raspberry Pi. | Chapter 2 (Section 2.2) | Qualitative text lacked structured tabular metrics and micro-architecture comparison. | Added Table 2 comparing Clock Speed, SRAM, Flash, Built-in Wireless, Deep-Sleep Current, Active Power, Unit Cost, and Peripheral Buses. |
| **2** | Justify selection of ESP32 based on SolanaWatch requirements. | Chapter 2 & Chapter 3.1 | Justification was generic without mapping to edge logging, RS485, and solar autonomy. | Explicitly linked ESP32 dual-core Xtensa LX6, native Wi-Fi stack, low-power deep sleep (10–150 µA), and peripheral buses (SPI, UART2, ADC) to system requirements. |
| **3** | Specify exact models and specifications of all sensors and components. | Chapter 3.1 (Table 6) | Generic sensor descriptions without part numbers, tolerances, operating voltages, or protocols. | Specified exact part numbers: DHT22/AM2302, DS18B20 (Waterproof 304 SS), Capacitive Moisture v1.2 (SEN0193), IP68 Industrial RS485 Leaf Sensor, MAX485 converter. |
| **4** | Reassess the 3.7V 2600 mAh Li-ion battery for 24/7 operation. | Chapter 2 & Chapter 3.1 | 3.7V 2600 mAh (9.62 Wh) depletes in < 16 hours with active Wi-Fi and 12V RS485 boost converters. | Performed a formal power audit proving why single 18650 cells fail 24/7 operation; upgraded to a 12.8V 12Ah LiFePO₄ battery pack. |
| **5** | Investigate solar-assisted power system for continuous operation. | Chapter 2 & Chapter 3.1 | Solar power was mentioned without engineering sizing formulas or solar irradiance analysis. | Provided solar photovoltaic sizing models based on Philippine Peak Sun Hours (PSH = 4.5 h/day), solar charging efficiency ($\eta = 0.75$), and continuous day/night cycling. |
| **6** | Conduct actual power-consumption testing of the complete prototype. | Chapter 3.4 (Table 14) | Missing physical power measurement protocol and energy dissipation profiles. | Formulated power measurement test bench capturing current draw across Active TX (180–240 mA), Sensing (30–60 mA), and Deep Sleep (15–50 µA) states. |
| **7** | Determine solar panel and battery capacity based on measured power requirements. | Chapter 3.1 & 3.3 | Hardware ratings were selected arbitrarily without mathematical sizing formulas. | Integrated formal sizing formulas: Daily Energy Budget ($E_{\text{daily}} = 2.30\text{ Wh/day}$), Battery Capacity ($C_{\text{battery}} = 153.6\text{ Wh}$), and PV Panel Wattage ($20\text{W}$). |
| **8** | Clarify sensor coverage vs. wireless communication range. | Chapter 1 & Chapter 3.1 | Conflated microclimatic sensing footprint with ESP32 Wi-Fi transmission radius. | Differentiated *Microclimatic Footprint* (5–15 m radial zone of microclimate homogeneity) vs. *RF Wireless Range* (30–50 m Wi-Fi line-of-sight). |
| **9** | Conduct experimental test to determine communication range of ESP32. | Chapter 3.4 (Table 16) | Lacked empirical RF range and signal degradation testing protocol. | Formulated experimental RSSI (dBm) and Packet Delivery Ratio (PDR %) test at 5m, 10m, 20m, 30m, 50m intervals under LOS and canopy NLOS conditions. |
| **10** | Provide RRL support for selected environmental parameters. | Chapter 2 (Section 2.1) | Need stronger plant pathology citations linking microclimate to specific Solanaceae pathogens. | Added direct peer-reviewed citations for Air Temp, RH, Leaf Wetness Duration, Soil Temp, and Soil Moisture influencing *P. infestans* and *R. pseudosolanacearum*. |
| **11** | Provide research basis for disease-risk thresholds and formulas. | Chapter 3.3 (Table 11) | Thresholds were presented as static ranges without mathematical combination logic. | Formulated Wallin's Severity Values (SV) / BLITECAST rule-base for Late Blight and hydrothermal soil infection index for Bacterial Wilt with scientific citations. |
| **12** | Clarify how multiple environmental parameters are combined. | Chapter 3.3 (Section 3.3.4) | No multi-variate formula explaining how individual sensor thresholds synthesize into a single risk index. | Defined decision tree algorithms combining air, soil, and canopy metrics over cumulative time windows ($\text{LWD} \ge 10\text{ h}$). |
| **13** | Clarify that SolanaWatch performs disease-risk assessment rather than diagnosis. | Chapter 1 (Scope & Delim.) | Ambiguous terminology implied that the system detects pathogen existence directly. | Explicitly refined all text to state that SolanaWatch evaluates **microclimatic conduciveness** (risk modeling) and does not perform biological/optical diagnosis. |
| **14** | Identify intended users of SolanaWatch. | Chapter 1 (Section 1.2) | User descriptions were broad without persona and operational context. | Defined specific target user groups: Smallholder Solanaceae farmers, agricultural technicians, extension officers, and agricultural researchers. |
| **15** | Clearly label all components and functions in circuit and system diagrams. | Chapter 3.3 (Section 3.3.2) | Circuit schematic lacked GPIO pin mappings, pull-up resistors, power lines, and level shifters. | Produced an annotated schematic showing ESP32 pinouts (`GPIO 4, 15, 16, 17, 21, 34, 35, 5, 18, 19, 23`), step-down bucks, and $4.7\text{ k}\Omega$ pull-up resistors. |
| **16** | Evaluate using a PCB instead of a breadboard for final prototype. | Chapter 2 & Chapter 3.1 | Breadboards are vulnerable to corrosion, contact bounce, and outdoor field failure. | Added comparative evaluation proving custom PCB ensures low contact resistance ($<0.01\ \Omega$), tropical humidity resistance, and anti-vibration integrity. |
| **17** | Add test cases for sensor accuracy, transmission, offline logging, and sync. | Chapter 3.4 (Section 3.4.3) | Existing test cases were vague ("Test sensor reads climate"). | Implemented structured test suites with Test ID, Description, Preconditions, Test Steps, Expected Result, and Acceptance Criteria. |
| **18** | Explain how data loss and duplication will be prevented during network outages. | Chapter 3.3 & 3.4 | Sync mechanism lacked technical description of deduplication and ACK handshaking. | Detailed the SPI MicroSD FIFO buffer, monotonic timestamping, transactional batch sync, HTTP 200/201 ACK validation, and DB `UNIQUE(node_id, recorded_at)` constraint. |
| **19** | Establish calibration procedure for all environmental sensors. | Chapter 3.4 (Section 3.4.2) | Missing sensor calibration methods prior to field deployment. | Provided standard 2-point calibration for capacitive soil moisture (air vs. water), ice-point for DS18B20, and saturated salt chamber verification for DHT22. |
| **20** | Specify Solanaceae crops and field conditions covered by the study. | Chapter 1 (Scope & Delim.) | Broad reference to Solanaceae without crop varieties and agro-ecological conditions. | Specified Tomato (*S. lycopersicum*), Eggplant (*S. melongena*), Bell Pepper (*C. annuum*), and Potato (*S. tuberosum*) in open-field/screenhouse cultivation. |
| **21** | Evaluate enclosure and components for outdoor agricultural conditions. | Chapter 2 & Chapter 3.1 | Enclosure lacked ingress protection ratings, UV considerations, and radiation shielding. | Specified IP65/IP66 weatherproof junction box with silicone gaskets, PG7/PG9 cable glands, silica desiccant packs, and a louvered Stevenson radiation shield for DHT22. |
| **22** | Add reliability testing plan for continuous operation. | Chapter 3.4 (Table 16) | Lacked continuous operational stress testing and watchdog timer fail-safe protocols. | Added a 7-day continuous unattended field testing protocol, ESP32 hardware Watchdog Timer (WDT) configuration, brown-out reset (BOR), and auto-recovery routines. |
| **23** | Provide validation procedure for solar charging and battery autonomy. | Chapter 3.4 (Table 16) | No procedure to verify if battery survives zero-sunlight conditions or charges efficiently. | Detailed a 3-day solar deprivation autonomy stress test (battery discharge curve) and a 48-hour solar harvesting profile under varying ambient solar irradiance. |
| **24** | Support all technical claims and component selections with recent RRL. | Entire Manuscript | Several claims lacked direct citations or empirical justification. | Integrated 2020–2026 high-impact journal citations (IEEE, Elsevier, Springer, MDPI), official datasheets, and derived engineering formulas across all chapters. |

---

## 8. Bibliography & Academic References (APA 7th Edition)

Aquino, A. L., Bon, S. G., Guanlao, A. P., Magnaye, A. M. A., Sta. Cruz, F. C., & Sta. Cruz, P. C. (2024). Field assessment of fertilization, nursery, and crop management practices among tomato (*Solanum lycopersicum* L.) growers in the Ilocos Provinces, Philippines. *The Philippine Agricultural Scientist*, 107(4), 354–365.

Aubriot, X., & Knapp, S. (2022). A revision of the “spiny solanums” of Tropical Asia (*Solanum*, the Leptostemonum Clade, Solanaceae). *PhytoKeys*, 198, 1–270. https://doi.org/10.3897/phytokeys.198.79514

Aumentado, H. D., & Balendres, M. A. (2024). Diseases of eggplant (*Solanum melongena* L.) and sustainable management in Asia. *Plant Pathology & Quarantine*, 14(1), 98–117. https://doi.org/10.5943/ppq/14/1/9

Benameur, R., Dahane, A., Kechar, B., & Benyamina, A. E. H. (2024). An innovative smart and sustainable low-cost irrigation system for anomaly detection using deep learning. *Sensors*, 24(4), Article 1162. https://doi.org/10.3390/s24041162

Botero-Valencia, J. S., Mejia-Herrera, M., & Pearce, J. M. (2022). Low cost climate station for smart agriculture applications with photovoltaic energy and wireless communication. *HardwareX*, 12, Article e00296. https://doi.org/10.1016/j.ohx.2022.e00296

Boulton, A., et al. (2023). Predicting daily aerobiological risk level of potato late blight using C5.0 and random forest algorithms under field conditions. *Plants*, 12(9), Article 1837. https://doi.org/10.3390/plants12091837

Cabia, C. A., Sumaria, M. C., De Padua, E., & Leorna, N. (2025). Quantifying calibration strategies for capacitive soil-moisture sensors (V1.2 SKU: FA3003-1) in automated drip irrigation for upland, rainfed farms. *Annals of Tropical Research*, 47(2), 90–105. https://doi.org/10.32945/atr4727.2025

Caldwell, T. G., Cosh, M. H., Evett, S. R., Edwards, N., Hofman, H., Illston, B. G., Meyers, T. P., Skumanich, M., & Sutcliffe, K. (2022). In situ soil moisture sensors in undisturbed soils. *Journal of Visualized Experiments*, 189, Article e64498. https://doi.org/10.3791/64498

Didi, Z., & El Azami, I. (2022). IoT, comparative study between the use of Arduino Uno, ESP32, and Raspberry Pi in greenhouses. In *Digital Technologies and Applications* (pp. 718–726). Springer. https://doi.org/10.1007/978-3-031-02447-4_74

Faqir, Y., Qayoom, A., Erasmus, E., Schutte-Smith, M., & Visser, H. G. (2024). A review on the application of advanced soil and plant sensors in the agriculture sector. *Computers and Electronics in Agriculture*, 226, Article 109385. https://doi.org/10.1016/j.compag.2024.109385

Fathima, N., B, V. K. S., & Bagali, M. U. (2026). Smart precision agriculture using IoT sensing and machine learning analytics for farming in Mysuru District. *International Journal of Electronics and Communication Engineering*, 13(4), 265–276. https://doi.org/10.14445/23488549/ijece-v13i4p122

Gao, X., et al. (2023). Energy-efficient resource scheduling and computation offloading strategy for solar-powered agriculture WSN. *Journal of Sensors*, 2023, Article 7020104. https://doi.org/10.1155/2023/7020104

Idris, F., Latiff, A. A., Buntat, M. A., Lecthmanan, Y., & Berahim, Z. (2024). IoT-based fertigation system for agriculture. *Bulletin of Electrical Engineering and Informatics*, 13(3), 1574–1581. https://doi.org/10.11591/eei.v13i3.6829

Jafar, A., Bibi, N., Naqvi, R. A., Sadeghi-Niaraki, A., & Jeong, D. (2024). Revolutionizing agriculture with artificial intelligence: Plant disease detection methods, applications, and their limitations. *Frontiers in Plant Science*, 15, Article 1356260. https://doi.org/10.3389/fpls.2024.1356260

Jiang, G., Wei, Z., Xu, J., Chen, H., Shen, Q., & Friman, V. P. (2021). Soil moisture determines the incidence of bacterial wilt through altering soil microbial diversity and community structure. *Soil Biology and Biochemistry*, 155, Article 108157. https://doi.org/10.1016/j.soilbio.2021.108157

Mane, S., Das, N. N., Singh, G., Cosh, M. H., & Dong, Y. (2024). Advancements in dielectric soil moisture sensor calibration: A comprehensive review of methods and techniques. *Computers and Electronics in Agriculture*, 218, Article 108686. https://doi.org/10.1016/j.compag.2024.108686

Mastul, A.-R. H., Awae, A., Bara, Z. J., & Yaro, Y. (2023). The use of IoT on smart agriculture in the Philippines: A narrative review. *Bincang Sains dan Teknologi (BST)*, 2(3), 98–107. https://doi.org/10.56741/bst.v2i03.416

Mazumdar, P., Singh, P., Kethiravan, D., Ramathani, I., & Ramakrishnan, N. (2021). Late blight in tomato: Insights into the pathogenesis of the aggressive pathogen *Phytophthora infestans* and future research priorities. *Planta*, 253(6), Article 119. https://doi.org/10.1007/s00425-021-03636-x

Miller, T., Mikiciuk, G., Durlik, I., Mikiciuk, M., Łobodzińska, A., & Śnieg, M. (2025). The IoT and AI in agriculture: The time is now—A systematic review of smart sensing technologies. *Sensors*, 25(12), Article 3583. https://doi.org/10.3390/s25123583

Mohd Khalid, N. K., Jamal, N., Mustafa, F., Zambri, N. A., & Abdullah, M. S. R. (2024). Solar power IoT based smart agriculture system using NodeMCU ESP32. *Progress in Engineering Application and Technology*, 5(1), 112–121.

Montzka, C., Cosh, M. H., Bayat, B., Al Bitar, A., Berg, A., Bindlish, R., Bogena, H. R., Bolton, J. D., Cabot, F., Caldwell, T., Chan, S., Colliander, A., Crow, W., Das, N., De Lannoy, G., Dorigo, W., Evett, S. R., Gruber, A., Hahn, S., ... Nickeson, J. (2020). *Soil moisture product validation good practices protocol* (Version 1.0). Committee on Earth Observation Satellites (CEOS) / NASA. https://doi.org/10.5067/DOC/CEOSWGCV/LPV/SM.001

Ndjuluwa, L. N. P., Adebisi, J. A., & Dayoub, M. (2023). Internet of Things for crop farming: A review of technologies and applications. *Commodities*, 2(4), 367–381. https://doi.org/10.3390/commodities2040021

Philippine Statistics Authority. (2026). *Major vegetables and root crops quarterly bulletin*. PSA Publications.

Rachakonda, L. (2022). ETS: A smart and enhanced topsoil health monitoring and control system at edge using IoT. In *2022 IEEE International Symposium on Smart Electronic Systems (iSES)* (pp. 689–693). IEEE. https://doi.org/10.1109/ises54909.2022.00153

Rachakonda, L., & Stasiewicz, S. (2024). SanaSolo 2.0: Edge-based monitoring and management of soil fertility using IoT. In *2024 IEEE Computer Society Annual Symposium on VLSI (ISVLSI)* (pp. 1–6). IEEE. https://doi.org/10.1109/vlsi-soc62099.2024.10767818

Silva, P. H. R., Johnson-Silva, W., Albuquerque, G. M. R., Oliveira, V. L. B., Santos, L. V. S., & Gonçalves, M. H. O. (2024). Exploring the competitive potential of *Ralstonia pseudosolanacearum* and *Ralstonia solanacearum*: Insights from a comparative adaptability study. *Plant Pathology*, 73(4), 898–914. https://doi.org/10.1111/ppa.13848

Song, W., Li, X., Zhang, J., Huang, J., Wang, J., Feng, W., Guo, Y., & Ren, L. (2026). Soil sensors in smart agriculture: Multi-type monitoring technologies and ecological development pathways. *Agriculture*, 16(3), Article 359. https://doi.org/10.3390/agriculture16030359

Songara, J. C., & Patel, J. N. (2022). Calibration and comparison of various sensors for soil moisture measurement. *Measurement*, 197, Article 111301. https://doi.org/10.1016/j.measurement.2022.111301

Subedi, N., Cowell, T., Cope-Arguello, M., Paul, P., Cellier, G., Bkayrat, H., Bonagura, N., Cadatal, A., Chen, R., Enriquez, A., Parasar, R., Repetto, L., Hernandez Rivas, A., Shahbaz, M., White, K., Lowe-Power, T. M., & Miller, S. A. (2024). Characterization of *Ralstonia pseudosolanacearum* diversity and screening tomato, pepper, and eggplant resistance to manage bacterial wilt in South Asia. *PhytoFrontiers*, 4(2), 180–195. https://doi.org/10.1094/PHYTOFR-10-23-0136-R

Suryadevara, N. K., George, B., & Kumar, K. (2022). Design and development of an IoT-enabled sensor node for agricultural and modelling applications. In *Sensing Technology: Proceedings of ICST 2022* (pp. 215–228). Springer. https://doi.org/10.1007/978-3-031-29807-3_18

Tao, X., Butcher, J., Silvestri, S., & Esposito, F. (2024). iCrop: Enabling high-precision crop disease detection via LoRa technology. In *2024 33rd International Conference on Computer Communications and Networks (ICCCN)* (pp. 1–9). IEEE. https://doi.org/10.1109/icccn61486.2024.10637527

Turner, P. (2022, June 6). The value of user acceptance testing in mission-critical applications. *F2 Strategy Insights*. https://f2strategy.com/insight/value-of-user-acceptance-testing

University of Florida IFAS Extension. (n.d.). *Late blight on potato and tomato (Plant Pathology Fact Sheet PP-13)*. University of Florida.

Yesankar, P. R., Bandre, P., Verma, P., Gudadhe, A. G., Gourshettiwar, P., & Puri, C. (2024). A review on the role of IoT in smart agriculture with reference to efficiency, sustainability and precision farming. In *2024 International Conference on Emerging Smart Computing and Informatics (ESCI)* (pp. 533–537). IEEE. https://doi.org/10.1109/icesc60852.2024.10689999
