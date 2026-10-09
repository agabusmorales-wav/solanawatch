# 🌿 SolanaWatch: Physical Prototype Layout, Component Labeling & Positioning Specification

> **Project Title:** SolanaWatch: An IoT-Based Disease Early Warning System for Soil-Grown Solanaceae Crops  
> **Academic Institution:** University of Santo Tomas – College of Information and Computing Sciences (CICS)  
> **Department:** Department of Information Technology  
> **Academic Term:** Special Term, A/Y 2025–2026  

---

## 📌 1. Physical Prototype Overview

The **SolanaWatch Edge Sensing Node** is designed as a self-sustaining, pole-mounted agro-meteorological station engineered for tropical open-field and screenhouse Solanaceae crop plots (Tomato, Eggplant, Bell Pepper, and Potato).

The complete assembly is mounted on a **1.5-meter galvanized steel mast** and integrates:
1. **Top Power Harvesting Tier (+1.5 m):** 20W Monocrystalline Solar PV Panel tilted at $15^\circ$ True South.
2. **Canopy Microclimate Sensing Tier (+0.8 m to +1.2 m):**
   - Louvered Stevenson Radiation Shield housing the **DHT22 / AM2302 Ambient Temp & RH sensor**.
   - Adjustable extension arm holding the **IP68 Dielectric Leaf Wetness Sensor** tilted at $35^\circ$ inside the foliar canopy.
3. **Control & Energy Core Tier (+0.6 m to +0.8 m):**
   - **IP65/IP66 Weatherproof Polycarbonate Enclosure** ($200 \times 150 \times 100\text{ mm}$) containing the ESP32 DevKit V1 MCU, Custom FR-4 PCB Shield, 12V 10A MPPT Controller, 12.8V 12Ah $\text{LiFePO}_4$ Battery Pack (47-day autonomy), SPI MicroSD Module, and dual DC-DC Buck converters.
4. **Subsurface Root-Zone Soil Tier (-10 cm depth):**
   - **Capacitive Soil Moisture Sensor v1.2** (corrosion-resistant PCB).
   - **DS18B20 Stainless Steel Waterproof Soil Temperature Probe** (1-Wire bus).

---

## 📐 2. Structural Elevation & Positioning Diagram

```
Elevation (m)
   +1.50 m ───► [ 20W SOLAR PHOTOVOLTAIC PANEL ]  (True South @ 15° Tilt Angle)
                │
   +1.20 m ───► ├── [ LOUVERED STEVENSON SHIELD ] ──► DHT22 / AM2302 (Air Temp & RH)
                │
   +0.90 m ───► ├── [ CANOPY BOOM ARM ] ────────────► IP68 Dielectric Leaf Wetness Grid (35° Tilt)
                │
   +0.70 m ───► ├── [ IP66 WEATHERPROOF ENCLOSURE ] (200 x 150 x 100 mm)
                │   ├── ESP32 MCU + Custom FR-4 PCB Shield + MicroSD
                │   ├── 12V 10A MPPT Solar Charge Controller
                │   ├── 12.8V 12Ah LiFePO4 Battery Pack (153.6 Wh)
                │   └── Bottom PG7 / PG9 Compression Cable Glands (Drip Loops)
                │
   0.00 m  ═════╪══════════════════════════════════ [ Soil Surface Baseline ]
                │
   -0.10 m ───► ├── [ CAPACITIVE SOIL MOISTURE v1.2 ] (15–20 cm from crop stem base)
   (-10 cm)     └── [ DS18B20 STAINLESS SOIL TEMP ]   (10 cm Subsurface Rhizosphere)
                │
   -0.30 m ───► └── [ GALVANIZED MAST SUB-SURFACE BASE ANCHOR ]
```

---

## 🏷️ 3. Bill of Components & Positioning Specifications

| Component / Subsystem | Exact Part Number / Specification | Exact Height / Depth & Location | Mounting & Orientation Details | Purpose / Epidemiological Target |
| :--- | :--- | :--- | :--- | :--- |
| **Solar PV Panel** | 20W 12V Monocrystalline ($V_{\text{mp}} = 18.0\text{V}$, $I_{\text{mp}} = 1.11\text{A}$) | **Top of Mast (+1.5 m elevation)** | Faced **True South ($180^\circ$)**, tilted at **$15^\circ$** with U-bolt mast clamp. | Maximum year-round solar energy harvesting in the Philippines ($4.5\text{ PSH/day}$). |
| **Ambient Air Temp & RH** | DHT22 / AM2302 in Louvered Stevenson Screen | **Canopy Level (+1.0 m to +1.2 m)** | Suspended inside multi-plate UV-stabilized shield on a 15 cm mast offset arm. | Tracks relative humidity ($RH \ge 90\%$) and air temp ($12^\circ\text{C}-22^\circ\text{C}$) for Late Blight. |
| **Leaf Wetness Sensor** | Industrial IP68 Dielectric Grid (RS485 Modbus-RTU) | **Upper Foliage (+0.8 m to +1.0 m)** | Mounted on adjustable boom; tilted at **$30^\circ\text{ to }45^\circ$** matching crop leaves. | Quantifies continuous Leaf Wetness Duration ($\text{LWD} \ge 10\text{ h}$) for Wallin SV calculation. |
| **Weatherproof Enclosure** | IP65/IP66 Polycarbonate Junction Box ($200 \times 150 \times 100\text{ mm}$) | **Middle Mast (+0.6 m to +0.8 m)** | Attached via dual stainless U-clamps. Silicone gasket + bottom PG7/PG9 glands. | Houses and shields all computing, power regulation, battery storage, and edge logging hardware. |
| **Capacitive Soil Moisture** | Capacitive Moisture v1.2 (Insulated PCB, SEN0193) | **Subsurface Soil (-10 cm depth)** | Inserted vertically into firm soil, **15–20 cm away from crop main stem**. | Measures root-zone Volumetric Water Content ($\ge 75\%\text{ VWC}$) for Bacterial Wilt. |
| **Soil Temperature Probe** | DS18B20 1-Wire Waterproof Digital Probe (304 SS) | **Subsurface Soil (-10 cm depth)** | Inserted horizontally at 10 cm depth in undisturbed rhizosphere soil. | Measures soil temperature ($28^\circ\text{C}-35^\circ\text{C}$) for Hydrothermal Soil Risk ($R_{\text{BW}}$). |
| **Galvanized Steel Mast** | 1.5 m $\times$ 1.25" Galvanized Steel Pipe | **Vertical Axis (-0.3 m to +1.5 m)** | Driven 30 cm into soil bed; anchored with concrete peg or ground stake. | Rigid structural support resistant to tropical monsoon winds and vibrations. |

---

## ⚡ 4. Internal Enclosure & PCB Shield Layout

```
+-----------------------------------------------------------------------------------------+
|                IP65/IP66 POLYCARBONATE WEATHERPROOF ENCLOSURE (200 x 150 x 100 mm)       |
+-----------------------------------------------------------------------------------------+
|                                                                                         |
|  [ 12V 10A MPPT CHARGE CONTROLLER ]              [ DUAL STEP-DOWN BUCK REGULATORS ]     |
|   - Multi-stage LiFePO4 Profile                   - LM2596 (12V -> 5.0V @ 3A for MCU)   |
|   - Terminals: PV In, Battery, 12V Load           - MP1584 (12V -> 3.3V @ 2A for Bus)   |
|                                                                                         |
|  -------------------------------------------------------------------------------------  |
|                                                                                         |
|  [ CUSTOM FR-4 PROTO-SHIELD PCB ]                [ 12.8V 12Ah LiFePO4 BATTERY PACK ]    |
|   - ESP32 DevKit V1 (Dual-Core MCU)               - 153.6 Wh High-Density Capacity      |
|   - MAX485 Transceiver Module (UART2)             - Built-in 15A BMS Protection Circuit |
|   - SPI MicroSD Module (16GB FAT32)               - 47.0 Days Zero-Sunlight Autonomy    |
|   - 4.7kΩ Pull-up Resistors & Terminal Blocks                                           |
|                                                  [ SILICA GEL DESICCANT POUCH ]         |
|                                                   - Absorbs internal condensation       |
|                                                                                         |
|  -------------------------------------------------------------------------------------  |
|      ||                       ||                       ||                       ||      |
|  [PG9 Gland]              [PG7 Gland]              [PG7 Gland]              [PG7 Gland] |
|  Solar PV In              DHT22 Shield             RS485 Leaf Grid          Soil Probes |
|  (Drip Loop)              (Drip Loop)              (Drip Loop)              (Drip Loop) |
+-----------------------------------------------------------------------------------------+
```

---

## 💧 5. Ingress Protection & Field Reliability Engineering

1. **Downward Compression Cable Glands:**
   - All cable penetrations are drilled strictly into the **bottom face** of the enclosure box using rubber-sealed PG7 and PG9 glands.
2. **Mandatory Cable Drip Loops:**
   - Every external wire is routed with a downward U-curve before entering the gland. Rainwater flowing down cables drips off the curve apex rather than pooling at the gland threads.
3. **Internal Condensation Mitigation:**
   - Sealed enclosure includes rechargeable silica gel desiccant packs to prevent high relative humidity from causing internal micro-condensation during temperature drops.
4. **Vibration-Proof Screw Terminals:**
   - Sensor signal wires and power leads are terminated using soldered screw terminal blocks on the custom FR-4 PCB shield rather than friction jumper wires, eliminating loose connections caused by wind buffet.

---

*Diagrams generated and archived in `figures/figure7_prototype_physical_layout.png` and `figures/figure8_enclosure_internal_layout.png`.*
