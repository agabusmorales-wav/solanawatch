# 🌿 SolanaWatch: Weekly Progress Report

> **Project Title:** SolanaWatch: An IoT-Based Disease Early Warning System for Soil-Grown Solanaceae Crops  
> **Course / Program:** Bachelor of Science in Information Technology  
> **Institution:** University of Santo Tomas – College of Information and Computing Sciences (CICS)  
> **Group / Term:** Group 1 (3ITC) – "Surfer Bros" | Special Term, A/Y 2025–2026  
> **Project Adviser:** Prof. Eugenia R. Zhuo, DIT  
> **Project Status:** **● ON TRACK**  
> **Reporting Period:** Current Week (September 24, 2026)  

---

## 📌 Executive Summary

This week, the **SolanaWatch** team achieved a major capstone milestone: **100% Complete Hardware Materials Procurement**, successfully transitioning the project from canvassing and sourcing into active physical circuit prototyping and bench bring-up. In parallel, the team finalized the working interactive frontends (PC Web Dashboard and iOS Mobile App) and completed the official UST Institutional Ethics Review documentation.

---

## 📊 Weekly Progress Matrix (3-Column Report)

| Column 1: CURRENT TASKS & ACCOMPLISHMENTS | Column 2: EXPECTED CHALLENGES & MITIGATIONS | Column 3: PLAN FOR NEXT WEEK |
| :--- | :--- | :--- |
| **1. 100% Complete Hardware Procurement:**<br>Acquired full ₱7,208 Bill of Materials with all components on-hand: ESP32 DevKit V1, DHT22 with Stevenson shield, dual DS18B20 soil temp probes, Capacitive v1.2 moisture sensor, industrial IP68 RS485 dielectric leaf wetness grid, 20W solar PV, MPPT controller, 12.8V LiFePO4 battery (47-day autonomy), and IP66 enclosure. | **1. Mixed-Bus Signal Integrity & Noise:**<br>*Challenge:* Concurrent 1-Wire, analog ADC, and RS485 lines can cause electrical noise.<br>*Mitigation:* Separated 5V logic and 3.3V sensor rails via dual buck converters; added 4.7kΩ pull-ups and line filters. | **1. Complete Physical Circuit Assembly:**<br>Finalize breadboard wiring harness connecting all 5 sensors to ESP32 and test power delivery from the 12.8V LiFePO4 battery pack. |
| **2. Physical Circuit Bring-Up Initiated:**<br>Started breadboard component layout, pin mapping, and isolated dual 5V/3.3V power rails. Verified initial 1-Wire, ADC, and RS485 communication lines. | **2. RS485 Modbus-RTU Timing:**<br>*Challenge:* Potential timing contention between MAX485 switching and ESP32 Wi-Fi routines.<br>*Mitigation:* Dedicated ESP32 Core 1 FreeRTOS task to sensor polling, isolating it from Core 0 network tasks. | **2. FreeRTOS Firmware Routines:**<br>Implement multi-sensor sampling loops and offline FIFO MicroSD buffer (`telemetry_buffer.jsonl`) for zero-loss edge storage. |
| **3. Interactive UI Dashboards Completed:**<br>Built functional PC Web Dashboard (`desktop.html`) and iOS mobile view (`index.html`) featuring live microclimate gauges, disease risk calculation, and actionable cultural alerts. | **3. Two-Point Soil Calibration:**<br>*Challenge:* ADC variance across Philippine clay-loam Solanaceae soils.<br>*Mitigation:* Calibrating in controlled oven-dry (0% VWC) and saturated (100% VWC) soil samples. | **3. Cloud Ingestion & Risk Engine:**<br>Connect Node.js/Express REST API to Turso libSQL cloud database and link Wallin SV and Hydrothermal risk models. |
| **4. Ethics Clearance Accomplished:**<br>Completed and packaged UST Ethics Review Form 4.2 (Protocol Assessment) and Form 7.2 (Application for Ethics Review) for institutional compliance. | | **4. Sensor Bench Calibration:**<br>Execute ice-point (0.0°C) and NaCl humidity chamber (75.3% RH) calibration tests. |

---

## 🛠️ Complete Hardware Inventory (100% Acquired)

| Subsystem | Components Procured | Status | Notes |
| :--- | :--- | :--- | :--- |
| **Compute & Edge Logging** | ESP32 DevKit V1 (Dual-Core 240MHz, 4MB Flash) + SPI MicroSD Module + 16GB FAT32 Card | **100% In-Hand** | Verified pinouts; ready for FreeRTOS firmware flashing |
| **Atmospheric Sensors** | DHT22 / AM2302 in Louvered Stevenson Screen + Industrial IP68 Dielectric Leaf Wetness Grid (RS485 Modbus) | **100% In-Hand** | MAX485 transceiver tested; Stevenson shield assembled |
| **Subsurface Soil Sensors** | Dallas DS18B20 Stainless Probe (1-Wire) + Capacitive Soil Moisture Sensor v1.2 (Dielectric PCB) | **100% In-Hand** | 4.7kΩ pull-up verified; ready for 2-point calibration |
| **Autonomous Power System** | 20W Monocrystalline PV Panel + 12V 10A MPPT Controller + 12.8V 12Ah LiFePO4 Battery + Dual Buck Regulators | **100% In-Hand** | 153.6 Wh capacity; 47-day zero-sunlight battery autonomy |
| **Field Packaging** | IP65/IP66 Polycarbonate Enclosure ($200 	imes 150 	imes 100\text{ mm}$) + PG7/PG9 Compression Cable Glands | **100% In-Hand** | Weatherproof sealing & cable gland drip loops ready |

---

## 💻 Software & System Highlights

1. **Working PC Dashboard (`SolanaWatch_PC_Dashboard.html`):**
   - High-density responsive interface with 5 real-time environmental gauge cards.
   - Dual Disease Risk Engine: Late Blight (Wallin Severity Values @ LWD $\ge 10	ext{ h}$) & Bacterial Wilt Hydrothermal index ($R_{	ext{BW}} = 0.50 	imes S_{	ext{ST}} + 0.50 	imes S_{	ext{SM}}$).
   - Contextual agronomic interventions and hardware telemetry monitoring.
2. **Mobile iOS App (`SolanaWatch_iOS_App.html`):**
   - Mobile-first interface designed to Apple HIG standards for field inspections.
3. **Institutional Ethics Compliance:**
   - UST Ethics Review Form 4.2 & Form 7.2 completed, covering smallholder farmer participant safety and research protocols.

---

*Compiled by Group 1 (3ITC) - Surfer Bros: Morales, Simeon Agabus S. • Rapada, Raven M. • Hernandez, Andrei S. • Eugenio, Vince Angelo*  
*Adviser: Prof. Eugenia R. Zhuo, DIT | UST College of Information and Computing Sciences*
