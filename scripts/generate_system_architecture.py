import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Set destination directory
out_dir = r"C:\Users\agabu\Downloads\CODE PROJECTS\SOLANAWATCH\figures"
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "figure3_system_architecture_revised.png")

# Set figure canvas (17x11 inches, 300 DPI)
fig, ax = plt.subplots(figsize=(17, 11), dpi=300)
ax.set_xlim(0, 17)
ax.set_ylim(0, 11)
ax.axis('off')

# Colors
COLOR_TITLE = "#0F172A"
COLOR_POWER = "#D97706"        # Amber
COLOR_POWER_BG = "#FFFBEB"
COLOR_EDGE = "#1E3A8A"         # Dark Navy
COLOR_EDGE_BG = "#EFF6FF"
COLOR_SENSORS = "#334155"      # Slate
COLOR_SENSORS_BG = "#F8FAFC"
COLOR_CLOUD = "#047857"        # Emerald
COLOR_CLOUD_BG = "#ECFDF5"
COLOR_WEB = "#1D4ED8"          # Blue
COLOR_WEB_BG = "#F0F9FF"
COLOR_RISK_BG = "#FEF3C7"      # Soft Gold
COLOR_RISK_BORDER = "#B45309"

# -------------------------------------------------------------
# 0. HEADER & TITLE
# -------------------------------------------------------------
ax.text(8.5, 10.6, "SOLANAWATCH: SYSTEM ARCHITECTURE & OPERATIONAL FLOW", 
        ha="center", va="center", fontsize=16, fontweight="bold", color=COLOR_TITLE)
ax.text(8.5, 10.28, "Three-Tier IoT Architecture: Field Edge Node, Cloud Analytical Engine, and Responsive Farmer Dashboard", 
        ha="center", va="center", fontsize=10.5, fontstyle="italic", color="#475569")

# -------------------------------------------------------------
# 1. COLUMN 1: HARDWARE & FIELD TIER (x: 0.5 to 5.0)
# -------------------------------------------------------------

# (1A) Power Subsystem (Top)
p_box = patches.FancyBboxPatch((0.5, 7.25), 4.6, 2.7, boxstyle="round,pad=0.1", 
                              fc=COLOR_POWER_BG, ec=COLOR_POWER, lw=1.8)
ax.add_patch(p_box)
ax.add_patch(patches.Rectangle((0.5, 9.5), 4.6, 0.45, fc=COLOR_POWER, ec=COLOR_POWER))
ax.text(2.8, 9.72, "POWER HARVESTING SUBSYSTEM", ha="center", va="center", 
        fontsize=9, fontweight="bold", color="#FFFFFF")

p_text = (
    "• 20W Monocrystalline Solar PV Panel (+1.5 m, 15° True South)\n"
    "• 12V 10A MPPT Solar Charge Controller\n"
    "• 12.8V 12Ah LiFePO4 Rechargeable Battery (+15A BMS)\n"
    "• Dual DC-DC Step-Down Buck Regulators:\n"
    "    - LM2596 (12V -> 5.0V @ 3A for ESP32 & System Rail)\n"
    "    - MP1584 (12V -> 3.3V @ 2A for Sensor Logic)\n"
    "• Operational Autonomy: ≥ 3 Days Continuous Solar Absence"
)
ax.text(0.7, 8.35, p_text, ha="left", va="center", fontsize=7.6, color="#1E293B", linespacing=1.35)

# (1B) ESP32 Edge Node (Middle)
e_box = patches.FancyBboxPatch((0.5, 3.9), 4.6, 2.9, boxstyle="round,pad=0.1", 
                              fc=COLOR_EDGE_BG, ec=COLOR_EDGE, lw=1.8)
ax.add_patch(e_box)
ax.add_patch(patches.Rectangle((0.5, 6.35), 4.6, 0.45, fc=COLOR_EDGE, ec=COLOR_EDGE))
ax.text(2.8, 6.57, "ESP32 EDGE COMPUTING NODE", ha="center", va="center", 
        fontsize=9, fontweight="bold", color="#FFFFFF")

e_text = (
    "• Weatherproof Enclosure: IP66 Polycarbonate (+0.7 m on Mast)\n"
    "• Controller: ESP32 DevKit V1 (240MHz Dual-Core Xtensa MCU)\n"
    "• Custom FR-4 PCB Proto-Shield + MAX485 Transceiver\n"
    "• Edge Firmware Tasks:\n"
    "    - 10-Minute Periodic Telemetry Sampling & CRC Checks\n"
    "    - Outlier Filtering & Analog Calibration Algorithms\n"
    "    - Wi-Fi 802.11 b/g/n Client (WPA2-PSK)\n"
    "• Offline Resilience / Local Data Logging:\n"
    "    - SPI MicroSD Module (Appends JSON lines on network drop)\n"
    "    - Automatic FIFO Batch Synchronization upon reconnection"
)
ax.text(0.7, 5.1, e_text, ha="left", va="center", fontsize=7.5, color="#1E293B", linespacing=1.32)

# (1C) Sensor Array & Target Solanaceae Crops (Bottom)
s_box = patches.FancyBboxPatch((0.5, 0.75), 4.6, 2.7, boxstyle="round,pad=0.1", 
                              fc=COLOR_SENSORS_BG, ec=COLOR_SENSORS, lw=1.8)
ax.add_patch(s_box)
ax.add_patch(patches.Rectangle((0.5, 3.0), 4.6, 0.45, fc=COLOR_SENSORS, ec=COLOR_SENSORS))
ax.text(2.8, 3.22, "FIELD SENSOR ARRAY & SOLANACEAE CROPS", ha="center", va="center", 
        fontsize=9, fontweight="bold", color="#FFFFFF")

s_text = (
    "• Target Crops: Tomato, Eggplant, Bell Pepper, Potato\n"
    "• Atmospheric / Foliage Probes:\n"
    "    - DHT22 (Air Temp & RH): Louvered Stevenson Shield @ +1.1 m\n"
    "    - RS485 Dielectric Leaf Wetness: Tilted 35° NW @ +0.9 m\n"
    "• Subsurface Rhizosphere Probes:\n"
    "    - DS18B20 Soil Temperature Probe: Horizontal @ -10 cm\n"
    "    - Capacitive Soil Moisture v1.2: Vertical @ -10 cm (15 cm from stem)\n"
    "• Representative Siting: Single Node Covers ~100–250 m² Plot"
)
ax.text(0.7, 1.85, s_text, ha="left", va="center", fontsize=7.5, color="#1E293B", linespacing=1.35)

# Connectors within Column 1
# Power -> Edge Node
ax.annotate('', xy=(2.8, 6.8), xytext=(2.8, 7.25), 
            arrowprops=dict(arrowstyle="-|>", color=COLOR_POWER, lw=2.5))
ax.text(3.75, 7.02, "12V / 5V DC Supply", ha="center", va="center", 
        fontsize=7.2, fontweight="bold", color=COLOR_POWER, backgroundcolor=COLOR_POWER_BG)

# Sensors -> Edge Node
ax.annotate('', xy=(2.8, 3.9), xytext=(2.8, 3.45), 
            arrowprops=dict(arrowstyle="-|>", color=COLOR_SENSORS, lw=2.5))
ax.text(3.75, 3.68, "Analog / 1-Wire / RS485", ha="center", va="center", 
        fontsize=7.2, fontweight="bold", color=COLOR_SENSORS, backgroundcolor=COLOR_SENSORS_BG)

# -------------------------------------------------------------
# 2. COLUMN 2: CLOUD ANALYTICAL TIER (x: 5.8 to 11.2)
# -------------------------------------------------------------
c_box = patches.FancyBboxPatch((5.8, 0.75), 5.3, 9.2, boxstyle="round,pad=0.1", 
                              fc=COLOR_CLOUD_BG, ec=COLOR_CLOUD, lw=1.8)
ax.add_patch(c_box)
ax.add_patch(patches.Rectangle((5.8, 9.5), 5.3, 0.45, fc=COLOR_CLOUD, ec=COLOR_CLOUD))
ax.text(8.45, 9.72, "CLOUD COMPUTING & ANALYTICAL TIER", ha="center", va="center", 
        fontsize=9.5, fontweight="bold", color="#FFFFFF")

# 2A: REST API Backend
api_box = patches.FancyBboxPatch((6.0, 7.45), 4.9, 1.85, boxstyle="round,pad=0.08", 
                                fc="#FFFFFF", ec=COLOR_CLOUD, lw=1.2)
ax.add_patch(api_box)
ax.text(8.45, 9.05, "Node.js & Express.js RESTful API Server", ha="center", va="center", 
        fontsize=8.5, fontweight="bold", color=COLOR_CLOUD)
api_text = (
    "• Ingests HTTP POST JSON Telemetry Streams from ESP32\n"
    "• Bearer Token Authentication & Edge Device Validation\n"
    "• Idempotent Ingestion Engine: UUID-based deduplication\n"
    "• REST Endpoints for Real-Time & Historical Data Retrieval\n"
    "• Automatic Risk Assessment Trigger upon New Reading"
)
ax.text(6.2, 8.15, api_text, ha="left", va="center", fontsize=7.4, color="#1E293B", linespacing=1.3)

# 2B: Cloud Database (Turso libSQL)
db_box = patches.FancyBboxPatch((6.0, 5.15), 4.9, 2.05, boxstyle="round,pad=0.08", 
                               fc="#FFFFFF", ec=COLOR_CLOUD, lw=1.2)
ax.add_patch(db_box)
ax.text(8.45, 6.95, "Cloud Database: Turso (Distributed libSQL / SQLite)", ha="center", va="center", 
        fontsize=8.5, fontweight="bold", color=COLOR_CLOUD)
db_text = (
    "• Distributed Edge SQLite Engine with Zero-Latency Caching\n"
    "• Schema Deduplication: UNIQUE(`node_id`, `timestamp_utc`)\n"
    "• Core Relational Tables:\n"
    "    - `sensor_readings`: Calibrated multi-sensor telemetry\n"
    "    - `disease_evaluations`: Evaluated severity scores & flags\n"
    "    - `system_alerts`: Active, historic, & acknowledged notifications\n"
    "    - `nodes_tbl` & `users_tbl`: Edge node and user account entities"
)
ax.text(6.2, 5.95, db_text, ha="left", va="center", fontsize=7.3, color="#1E293B", linespacing=1.25)

# 2C: Rule-Based Disease-Risk Engine
risk_box = patches.FancyBboxPatch((6.0, 0.95), 4.9, 3.95, boxstyle="round,pad=0.08", 
                                 fc=COLOR_RISK_BG, ec=COLOR_RISK_BORDER, lw=1.4)
ax.add_patch(risk_box)
ax.text(8.45, 4.65, "Rule-Based Disease-Risk Assessment Engine", ha="center", va="center", 
        fontsize=8.5, fontweight="bold", color=COLOR_RISK_BORDER)

risk_text = (
    "[ Epidemiological Models & Decision Rules ]\n\n"
    "• Module A: Late Blight (Phytophthora infestans)\n"
    "    - Evaluates Adapted Wallin Severity Values (SV) & LWD\n"
    "    - Critical Trigger: Air Temp 12–22°C, RH ≥ 90%, LWD ≥ 10 hrs\n"
    "    - Accumulates Daily Severity Values over Rolling Multi-Day Windows\n\n"
    "• Module B: Bacterial Wilt (Ralstonia pseudosolanacearum)\n"
    "    - Hydrothermal Soil Conduciveness Index (R_BW)\n"
    "    - Critical Trigger: Soil Temp 28–35°C & Soil Moisture (VWC) ≥ 75%\n\n"
    "[ Decision Classification State Machine ]\n"
    "    - LOW RISK (Green): Microclimate within safe agronomic baseline\n"
    "    - MODERATE RISK (Yellow): Partial disease criteria detected\n"
    "    - HIGH RISK (Red): Disease-favorable conditions fully satisfied"
)
ax.text(6.2, 2.7, risk_text, ha="left", va="center", fontsize=7.2, color="#1E293B", linespacing=1.2)

# Connectors inside Column 2
ax.annotate('', xy=(8.45, 7.2), xytext=(8.45, 7.45), 
            arrowprops=dict(arrowstyle="<|-|>", color=COLOR_CLOUD, lw=1.8))
ax.annotate('', xy=(8.45, 4.9), xytext=(8.45, 5.15), 
            arrowprops=dict(arrowstyle="<|-|>", color=COLOR_RISK_BORDER, lw=1.8))

# -------------------------------------------------------------
# 3. COLUMN 3: PRESENTATION & USER TIER (x: 11.8 to 16.5)
# -------------------------------------------------------------
w_box = patches.FancyBboxPatch((11.8, 3.45), 4.7, 6.5, boxstyle="round,pad=0.1", 
                              fc=COLOR_WEB_BG, ec=COLOR_WEB, lw=1.8)
ax.add_patch(w_box)
ax.add_patch(patches.Rectangle((11.8, 9.5), 4.7, 0.45, fc=COLOR_WEB, ec=COLOR_WEB))
ax.text(14.15, 9.72, "WEB DASHBOARD PRESENTATION LAYER", ha="center", va="center", 
        fontsize=9.5, fontweight="bold", color="#FFFFFF")

dash_text = (
    "• Architecture: Single Page Application (React.js + Vite)\n"
    "• Visual UI / UX: Tailwind CSS + Chart.js\n"
    "• Security: Role-Based Authorization (Admin / Field Farmer)\n"
    "• Core Dashboard Capabilities:\n\n"
    "  1. Real-Time Telemetry Gauges\n"
    "     - Live Air Temp, RH, Soil Temp, Moisture, & Leaf Wetness\n"
    "     - Hardware Diagnostics: Battery Voltage & Wi-Fi RSSI\n\n"
    "  2. Disease Early Warning Visual Alerts\n"
    "     - Color-Coded Risk Status Cards (Green / Yellow / Red)\n"
    "     - Severity Progress Bars & Conduciveness Indexes\n"
    "     - Agronomic Preventive Action Guidelines\n\n"
    "  3. Interactive Historical Analytics\n"
    "     - Multi-Series Synchronized Time-Series Graphs\n"
    "     - Historical Trend Review & Date Range Filtering\n\n"
    "  4. Responsive Client Compatibility\n"
    "     - Fully responsive across Desktop, Tablet, and Mobile"
)
ax.text(12.0, 6.4, dash_text, ha="left", va="center", fontsize=7.4, color="#1E293B", linespacing=1.3)

# End-User Subsystem (Bottom Right)
u_box = patches.FancyBboxPatch((11.8, 0.75), 4.7, 2.45, boxstyle="round,pad=0.1", 
                              fc="#FFFFFF", ec=COLOR_WEB, lw=1.5)
ax.add_patch(u_box)
ax.add_patch(patches.Rectangle((11.8, 2.75), 4.7, 0.45, fc="#2563EB", ec="#2563EB"))
ax.text(14.15, 2.97, "AGRICULTURAL END USERS", ha="center", va="center", 
        fontsize=9, fontweight="bold", color="#FFFFFF")

u_text = (
    "• User Profile: Smallholder Solanaceae Farmers & Technicians\n"
    "• Client Hardware: Smartphone / Tablet / Laptop / PC\n"
    "• Browser Support: HTML5 / ES6 (Chrome, Safari, Edge, Firefox)\n"
    "• Primary Goal: Timely crop management & early disease prevention\n"
    "  prior to irreversible physical pathogen damage"
)
ax.text(12.0, 1.75, u_text, ha="left", va="center", fontsize=7.4, color="#1E293B", linespacing=1.3)

# Connector Dashboard <-> User
ax.annotate('', xy=(14.15, 3.2), xytext=(14.15, 3.45), 
            arrowprops=dict(arrowstyle="<|-|>", color=COLOR_WEB, lw=2.0))

# -------------------------------------------------------------
# 4. CROSS-TIER CONNECTORS & DATA FLOW LABELS
# -------------------------------------------------------------

# (A) Edge Node -> Cloud API (Normal Online Wi-Fi Flow)
ax.annotate('', xy=(6.0, 8.4), xytext=(5.1, 5.7), 
            arrowprops=dict(arrowstyle="-|>", color="#047857", lw=2.4, linestyle='solid'))
ax.text(5.45, 7.3, "Normal Mode:\n2.4GHz Wi-Fi\n(HTTP POST JSON)", 
        ha="center", va="center", fontsize=7.2, fontweight="bold", color="#047857", 
        bbox=dict(boxstyle="round,pad=0.25", fc="#FFFFFF", ec="#047857", lw=1))

# (B) Edge Node -> Cloud API (Offline MicroSD Reconnection Sync Flow)
ax.annotate('', xy=(6.0, 7.7), xytext=(5.1, 4.6), 
            arrowprops=dict(arrowstyle="-|>", color="#D97706", lw=2.2, linestyle='dashed'))
ax.text(5.45, 4.9, "Network Recovery:\nMicroSD Batch Sync\n(Bulk HTTP POST)", 
        ha="center", va="center", fontsize=7.0, fontweight="bold", color="#D97706", 
        bbox=dict(boxstyle="round,pad=0.25", fc="#FFFFFF", ec="#D97706", lw=1))

# (C) Cloud API <-> Web Dashboard (HTTPS REST API)
ax.annotate('', xy=(11.8, 7.8), xytext=(10.9, 8.2), 
            arrowprops=dict(arrowstyle="<|-|>", color=COLOR_WEB, lw=2.4))
ax.text(11.35, 8.6, "HTTPS / REST API\n(JSON Telemetry &\nEarly Warning Alerts)", 
        ha="center", va="center", fontsize=7.2, fontweight="bold", color=COLOR_WEB, 
        bbox=dict(boxstyle="round,pad=0.25", fc="#FFFFFF", ec=COLOR_WEB, lw=1))

# -------------------------------------------------------------
# 5. BOTTOM FLOW LEGEND (Drawn using precise coordinates)
# -------------------------------------------------------------
legend_box = patches.FancyBboxPatch((0.5, 0.08), 16.0, 0.52, boxstyle="round,pad=0.06", 
                                    fc="#F8FAFC", ec="#CBD5E1", lw=1)
ax.add_patch(legend_box)

# Legend item 1: Power
ax.plot([0.8, 1.3], [0.34, 0.34], color=COLOR_POWER, lw=3)
ax.text(1.4, 0.34, "Power Supply Flow", va="center", fontsize=7.8, color="#1E293B", fontweight="bold")

# Legend item 2: Sensor
ax.plot([3.9, 4.4], [0.34, 0.34], color=COLOR_SENSORS, lw=3)
ax.text(4.5, 0.34, "Hardware Sensor Acquisition", va="center", fontsize=7.8, color="#1E293B", fontweight="bold")

# Legend item 3: Wi-Fi Online
ax.plot([7.4, 7.9], [0.34, 0.34], color="#047857", lw=3)
ax.text(8.0, 0.34, "Online 2.4GHz Wi-Fi (HTTP)", va="center", fontsize=7.8, color="#1E293B", fontweight="bold")

# Legend item 4: Batch Sync
ax.plot([10.7, 11.2], [0.34, 0.34], color="#D97706", lw=2.5, linestyle='dashed')
ax.text(11.3, 0.34, "Offline MicroSD Batch Sync", va="center", fontsize=7.8, color="#1E293B", fontweight="bold")

# Legend item 5: HTTPS REST
ax.plot([14.1, 14.6], [0.34, 0.34], color=COLOR_WEB, lw=3)
ax.text(14.7, 0.34, "Client/Server HTTPS REST API", va="center", fontsize=7.8, color="#1E293B", fontweight="bold")

plt.tight_layout()
plt.savefig(out_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"Successfully generated revised System Architecture: {out_path}")
