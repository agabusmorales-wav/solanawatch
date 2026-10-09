# SolanaWatch 🌿📡

> **An IoT-Based Disease Early Warning and Decision Support System for Soil-Grown Solanaceae Crops**  
> *University of Santo Tomas – College of Information and Computing Sciences*  
> *Department of Information Technology*

---

## 📌 Project Summary

**SolanaWatch** is an open-source, solar-assisted IoT microclimatic monitoring and disease early warning system designed specifically for smallholder Solanaceae farmers (Tomato, Eggplant, Pepper, and Potato) in the Philippines.

By continuously acquiring canopy microclimatic data and root-zone soil dynamics directly in the field, SolanaWatch evaluates physical disease favorability for **Late Blight (*Phytophthora infestans*)** and **Bacterial Wilt (*Ralstonia pseudosolanacearum*)** using literature-grounded plant pathology algorithms (adapted Wallin Severity Values and Hydrothermal Soil Indices), enabling pre-symptomatic preventive crop management.

```
+---------------------------------------------------------------------------------------------------------+
|                                    SOLANAWATCH SYSTEM ARCHITECTURE                                      |
+---------------------------------------------------------------------------------------------------------+
|                                                                                                         |
|  [ SENSING NODE (ESP32) ]                                                                               |
|   ├── DHT22 (Ambient Air Temperature & Relative Humidity inside Stevenson Shield)                      |
|   ├── DS18B20 (Subsurface Root-Zone Soil Temperature at 10cm depth)                                     |
|   ├── Capacitive Soil Moisture v1.2 (Volumetric Water Content at 10cm depth)                            |
|   ├── Industrial Dielectric Leaf Wetness Grid (RS485 Modbus-RTU over MAX485)                            |
|   ├── SPI MicroSD Module (Offline FIFO JSON Lines buffer: telemetry_buffer.jsonl)                       |
|   └── Autonomous Power (20W Solar PV + 12.8V 12Ah LiFePO4 Battery + MPPT Controller = 47-Day Autonomy)  |
|                                                  │                                                      |
|                                    2.4 GHz Wi-Fi │ HTTP POST /api/telemetry (JSON)                      |
|                                                  ▼                                                      |
|  [ CLOUD BACKEND & DATABASE ]                                                                           |
|   ├── Node.js & Express.js REST API Server                                                              |
|   ├── Turso Cloud Database (Distributed libSQL / SQLite with UNIQUE(node_id, recorded_at))              |
|   └── Disease Risk Engine:                                                                              |
|       ├── Late Blight: Adapted Wallin Severity Values (SV) & Leaf Wetness Duration (LWD)               |
|       └── Bacterial Wilt: Hydrothermal Risk Score R_BW = (0.50 * S_ST) + (0.50 * S_SM)                  |
|                                                  │                                                      |
|                                       JSON HTTPS │ WebSockets / REST API                                |
|                                                  ▼                                                      |
|  [ USER DASHBOARD & DECISION SUPPORT ]                                                                  |
|   ├── React.js + Vite + Tailwind CSS + Chart.js                                                         |
|   ├── Live Environmental Gauges & Multi-Series Historical Time-Series Charts                            |
|   ├── Color-Coded Early Warning Banners (Green = Low, Yellow = Moderate, Red = High Risk Alert)         |
|   └── Contextual Agronomic Recommendations & Hardware Health Telemetry (Battery / RSSI / Solar)         |
+---------------------------------------------------------------------------------------------------------+
```

---

## 📂 Repository File Structure

```
SOLANAWATCH/
├── backend/                                              # Node.js REST API Server & Pathology Engine
│   ├── server.js                                         # Express server with disease algorithms & DB
│   ├── package.json                                      # Node.js dependencies (express, cors)
│   └── data/telemetry_db.json                            # Local persistent telemetry store
├── firmware/                                             # Edge Hardware ESP32 C++ Arduino Firmware
│   ├── SolanaWatch_ESP32_Firmware.ino                    # Complete production-ready firmware sketch
│   └── README.md                                         # Pinout diagram & Arduino IDE flashing guide
├── web-app/                                              # Interactive Web & Mobile Applications
│   ├── index.html                                        # iOS Mobile Decision Support Web Application
│   ├── desktop.html                                      # macOS / PC Agronomic Decision Support Dashboard
│   ├── hardware-bridge.js                                # Live telemetry & hardware link client engine
│   ├── SolanaWatch_Web_Dashboard_Mockup.html             # Standalone web dashboard mockup
│   └── README.md                                         # Web application documentation & run guide
├── paperwork/                                            # Capstone Paperwork, Manuscripts & Filings
│   ├── proposal/                                         # Chapters 1-3 revised manuscripts & specs
│   ├── defense-and-revisions/                            # 24-point defense compliance & revision matrices
│   ├── ethics-review/                                    # UST RERC Form 4.2 & 7.2 ethics filings & downloader
│   ├── evaluation-sus/                                   # System Usability Scale (SUS) instruments (DOCX/PDF/HTML)
│   ├── reports-and-presentations/                        # Milestone progress reports & PPTX presentation slides
│   └── README.md                                         # Comprehensive paperwork catalog & descriptions
├── figures/                                              # High-resolution 300 DPI system diagrams & renders
│   ├── figure1_context_diagram.png                       # High-level operational boundary & context
│   ├── figure2_activity_diagram.png                      # 3-swimlane activity flow diagram
│   ├── figure3_prototyping_model.png                     # Iterative prototyping development cycle
│   ├── figure3_system_architecture_revised.png           # Multi-tier hardware-cloud-frontend architecture
│   ├── figure5_er_diagram.png                            # Relational Turso libSQL database schema
│   └── figure6_circuit_schematic.png                     # Comprehensive circuit pinout & wiring schematic
├── scripts/                                              # Automated Python build & simulation tools
│   ├── simulate_hardware.py                              # Live telemetry stream simulator for testing
│   ├── generate_diagrams.py                              # Matplotlib generator for system diagrams
│   ├── convert_to_docx.py                                # Python script compiling MD chapters to styled DOCX
│   ├── convert_to_html.py                                # Python script compiling MD chapters to styled HTML
│   └── README.md                                         # Script usage guide & execution instructions
├── start_server.bat                                      # One-click Windows launcher for backend server
└── README.md                                             # Repository overview & quick-start guide
```

---

## 🔬 Core System Specifications

### 1. Hardware Bill of Materials (₱7,208.00 Total)
- **Microcontroller:** Espressif ESP32 DevKit V1 (32-bit Dual-Core Xtensa LX6 @ 240 MHz, 520 KB SRAM, 4 MB Flash)
- **Air Temp & Relative Humidity:** DHT22 / AM2302 housed inside a louvered Stevenson Radiation Shield
- **Soil Temperature:** Dallas DS18B20 waterproof stainless-steel digital probe (1-Wire bus @ 10 cm depth)
- **Soil Moisture:** Capacitive Soil Moisture Sensor v1.2 (Dielectric insulated PCB @ 10 cm depth)
- **Leaf Surface Wetness:** Industrial IP68 dielectric leaf grid (RS485 Modbus-RTU over MAX485 transceiver)
- **Offline Storage:** SPI MicroSD card module + 16GB MicroSD card (FAT32 filesystem)
- **Solar Harvesting & Storage:** 20W 12V Monocrystalline PV Panel + 12V 10A IP67 MPPT Controller + 12.8V 12Ah ($153.6\text{ Wh}$) LiFePO₄ Battery pack (built-in 15A BMS)
- **Power Autonomy:** **47.0 Days of Continuous Zero-Sunlight Autonomy** ($2.30\text{ Wh/day}$ design budget)
- **Hardware Packaging:** Custom FR-4 PCB Shield inside an IP65/IP66 Polycarbonate Enclosure with PG7/PG9 glands

### 2. Literature-Grounded Disease-Risk Algorithms
- **Late Blight (*P. infestans*):**
  - High Risk (Red Alert): Cumulative Leaf Wetness Duration $\ge 15\text{ h}$ at $12^\circ\text{C} - 22^\circ\text{C}$ OR $\text{LWD} \ge 10\text{ h}$ with $\text{RH} \ge 90\%$.
- **Bacterial Wilt (*R. pseudosolanacearum*):**
  - High Risk (Red Alert): Hydrothermal Score $R_{\text{BW}} = (0.50 \times S_{\text{ST}}) + (0.50 \times S_{\text{SM}}) \ge 0.70$ (Optimal proliferation at soil temperature $28^\circ\text{C} - 35^\circ\text{C}$ and soil moisture $\ge 75\%\text{ VWC}$).

---

## 🚀 Execution & Quick-Start Guide

### 1. Start the Backend Server
Double-click [`start_server.bat`](file:///C:/Users/agabu/Downloads/CODE%20PROJECTS/SOLANAWATCH/start_server.bat) or run in terminal:
```powershell
cd "C:\Users\agabu\Downloads\CODE PROJECTS\SOLANAWATCH\backend"
npm start
```
*Starts the REST API on port 5000 and serves the web application at `http://localhost:5000/`.*

### 2. Open the Web Application
Open in any browser:
- **iOS Mobile View:** [`http://localhost:5000/`](http://localhost:5000/) or open [`web-app/index.html`](file:///C:/Users/agabu/Downloads/CODE%20PROJECTS/SOLANAWATCH/web-app/index.html)
- **PC / macOS View:** [`http://localhost:5000/desktop.html`](http://localhost:5000/desktop.html) or open [`web-app/desktop.html`](file:///C:/Users/agabu/Downloads/CODE%20PROJECTS/SOLANAWATCH/web-app/desktop.html)

### 3. Connect Physical ESP32 Hardware
1. Open [`firmware/SolanaWatch_ESP32_Firmware.ino`](file:///C:/Users/agabu/Downloads/CODE%20PROJECTS/SOLANAWATCH/firmware/SolanaWatch_ESP32_Firmware.ino) in Arduino IDE.
2. Enter your Wi-Fi SSID, Password, and your laptop's local IP address (`http://<laptop-ip>:5000/api/telemetry`).
3. Upload to your ESP32 DevKit V1 board.
4. For wiring and library details, see [`firmware/README.md`](file:///C:/Users/agabu/Downloads/CODE%20PROJECTS/SOLANAWATCH/firmware/README.md).

### 4. Deploy to Vercel (Production Cloud Hosting)
Deploy the full stack (Web App + Serverless Disease Engine) with global HTTPS access:
👉 **See the complete guide: [`DEPLOYMENT_GUIDE_VERCEL.md`](file:///C:/Users/agabu/Downloads/CODE%20PROJECTS/SOLANAWATCH/DEPLOYMENT_GUIDE_VERCEL.md)**

```powershell
# Fast CLI deployment
npx vercel --prod
```

### 5. Test Without Physical Hardware (Virtual Stream)
Stream simulated live sensor telemetry into local or remote Vercel backend:
```powershell
# Test local server
python scripts/simulate_hardware.py

# Test live Vercel production deployment
python scripts/simulate_hardware.py --url https://your-project.vercel.app/api/telemetry
```

### 6. Regenerate Academic Artifacts
```powershell
# Regenerate all 6 system diagrams
python scripts/generate_diagrams.py

# Compile Formatted DOCX Proposal Manuscript
python scripts/convert_to_docx.py

# Compile Standalone HTML Proposal Preview
python scripts/convert_to_html.py
```

---

## 📖 Complete Documentation & Paperwork

For the exhaustive technical specification, mathematical models, ISO/IEC 25010 testing matrix, defense revision action plan, and APA 7th bibliography, refer to:  
👉 **[`SolanaWatch_Project_Documentation.md`](file:///C:/Users/agabu/Downloads/CODE%20PROJECTS/SOLANAWATCH/paperwork/proposal/SolanaWatch_Project_Documentation.md)**  
👉 **[`paperwork/README.md`](file:///C:/Users/agabu/Downloads/CODE%20PROJECTS/SOLANAWATCH/paperwork/README.md)** (Full catalog of academic proposals, ethics filings, evaluation instruments, and compliance matrices)
