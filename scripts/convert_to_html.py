import os
import base64
import markdown

artifact_dir = r"C:\Users\agabu\.gemini\antigravity-cli\brain\d2b1ae52-6063-4142-a38a-b997f915c996"
out_dir = r"C:\Users\agabu\Downloads\CODE PROJECTS\SOLANAWATCH\paperwork\proposal"
fig_dir = r"C:\Users\agabu\Downloads\CODE PROJECTS\SOLANAWATCH\figures"

def get_base64_img(img_name):
    p = os.path.join(fig_dir, img_name)
    if os.path.exists(p):
        with open(p, 'rb') as f:
            b64 = base64.b64encode(f.read()).decode('utf-8')
            return f'<div style="text-align:center; margin: 25px 0;"><img src="data:image/png;base64,{b64}" style="max-width:100%; border: 1px solid #ccc; border-radius: 4px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);"/></div>'
    return ""

# Read markdown files
with open(os.path.join(artifact_dir, "SolanaWatch_Chapter_1_Revised.md"), 'r', encoding='utf-8') as f:
    ch1 = f.read()
with open(os.path.join(artifact_dir, "SolanaWatch_Chapter_2_Revised.md"), 'r', encoding='utf-8') as f:
    ch2 = f.read()
with open(os.path.join(artifact_dir, "SolanaWatch_Chapter_3_Revised.md"), 'r', encoding='utf-8') as f:
    ch3 = f.read()
with open(os.path.join(artifact_dir, "SolanaWatch_Bibliography_APA7.md"), 'r', encoding='utf-8') as f:
    bib = f.read()

# Replace ASCII diagram blocks with rich image embeds
ch1 = ch1.replace("```\n+---------------------------------------------------------------------------------------------------------+\n|                                    FIGURE 1: SOLANAWATCH CONTEXT DIAGRAM                                |\n+---------------------------------------------------------------------------------------------------------+\n|                                                                                                         |\n|   +--------------------------+                         +--------------------------+                     |\n|   |                          |    Air Temperature      |                          |                     |\n|   |                          |    Relative Humidity    |                          |                     |\n|   |    Field Sensor Node     |    Soil Temperature     |       SolanaWatch        |                     |\n|   | (Sensors + Local Storage)| ----------------------> |   IoT Disease Early      |                     |\n|   |                          |    Soil Moisture        |     Warning System       |                     |\n|   |                          |    Leaf Wetness         |                          |                     |\n|   +--------------------------+                         +--------------------------+                     |\n|                                                                    ^     |                              |\n|                                                                    |     |                              |\n|                                         Login & Control Inputs     |     | Real-Time Sensor Readings    |\n|                                         Device Configurations      |     | Historical Charts & Reports  |\n|                                                                    |     | Disease-Risk Visual Alerts   |\n|                                                                    |     v                              |\n|                                                        +--------------------------+                     |\n|                                                        |                          |                     |\n|                                                        |     Farmer / Operator    |                     |\n|                                                        |     (Web Dashboard)      |                     |\n|                                                        |                          |                     |\n|                                                        +--------------------------+                     |\n|                                                                                                         |\n+---------------------------------------------------------------------------------------------------------+\n```", get_base64_img("figure1_context_diagram.png"))

ch3 = ch3.replace("```\n+---------------------------------------------------------------------------------------------------------+\n|                                    FIGURE 3: PROTOTYPING DEVELOPMENT MODEL                              |\n+---------------------------------------------------------------------------------------------------------+\n|                                                                                                         |\n|   +--------------------------+                                                                          |\n|   |  Requirements Gathering   | <--------------------------------------------+                          |\n|   |        & Analysis        |                                              |                          |\n|   +--------------------------+                                              |                          |\n|                |                                                            |                          |\n|                v                                                            |                          |\n|   +--------------------------+                                              |                          |\n|   |       Quick Design       | <--------------------+                       |                          |\n|   |   (Schematic & UI/UX)    |                      |                       |                          |\n|   +--------------------------+                      |                       |                          |\n|                |                                    |                       |                          |\n|                v                                    |                       |                          |\n|   +--------------------------+                      |                       |                          |\n|   |    Build Prototype       |                      |                       |                          |\n|   | (Firmware, PCB, Backend) |                      |                       |                          |\n|   +--------------------------+                      |                       |                          |\n|                |                                    |                       |                          |\n|                v                                    |                       |                          |\n|   +--------------------------+                      |                       |                          |\n|   |   Evaluation & Testing   |                      | (Refinements Needed)  |                          |\n|   |  (Unit, Range, Autonomy) |                      |                       |                          |\n|   +--------------------------+                      |                       |                          |\n|                |                                    |                       |                          |\n|                v                                    |                       |                          |\n|         /--------------\                            |                       |                          |\n|        / System Meets   \            NO             |                       |                          |\n|       <  Acceptance      >--------------------------+                       |                          |\n|        \   Criteria?    /                                                   |                          |\n|         \--------------/                                                    |                          |\n|                | YES                                                        |                          |\n|                v                                                            |                          |\n|   +--------------------------+                                              |                          |\n|   | Final Validation & Field | ---------------------------------------------+                          |\n|   |        Deployment        | (Major Revisions Feedback Loop)                                         |\n|   +--------------------------+                                                                          |\n|                                                                                                         |\n+---------------------------------------------------------------------------------------------------------+\n```", get_base64_img("figure3_prototyping_model.png"))

ch3 = ch3.replace("```\n+---------------------------------------------------------------------------------------------------------+\n|                               FIGURE 4: SOLANAWATCH SYSTEM ARCHITECTURE DIAGRAM                         |\n+---------------------------------------------------------------------------------------------------------+\n|                                                                                                         |\n|  [ POWER SUBSYSTEM ]                                                                                    |\n|  - 20W 12V Monocrystalline Solar Panel                                                                  |\n|  - 12V 10A MPPT Solar Charge Controller (IP67)                                                          |\n|  - 12.8V 12Ah LiFePO4 Battery Pack (Built-in 15A BMS)                                                   |\n|  - High-Efficiency DC-DC Step-Down Buck Converters (12V -> 5V & 3.3V)                                   |\n|                                                                                                         |\n|                                       | (Regulated DC Power Rails)                                      |\n|                                       v                                                                 |\n|                                                                                                         |\n|  [ ESP32 EDGE NODE SUBSYSTEM ]                                                                          |\n|  - ESP32 Dual-Core Microcontroller (240MHz, 2.4GHz Wi-Fi)                                                |\n|  - Multi-Parameter Sensor Array:                                                                        |\n|      * Air Temp & Relative Humidity (DHT22 inside Stevenson Radiation Shield)                           |\n|      * Soil Temperature (Waterproof DS18B20 Stainless Probe @ 10cm Depth)                               |\n|      * Soil Moisture (Capacitive Soil Moisture Sensor v1.2 @ 10cm Depth)                                |\n|      * Leaf Surface Wetness (IP68 RS485 Modbus Sensor via MAX485 Transceiver)                           |\n|  - Local Offline Logging: SPI MicroSD Card Module (JSON-Line FIFO Queue)                                |\n|  - Custom Fabricated PCB Shield & IP65/IP66 Weatherproof Polycarbonate Enclosure                       |\n|                                                                                                         |\n|                                       | (2.4 GHz Wi-Fi / HTTP REST JSON Payload)                        |\n|                                       v                                                                 |\n|                                                                                                         |\n|  [ CLOUD BACKEND & DATA MANAGEMENT ]                                                                    |\n|  - Node.js & Express.js REST API Server                                                                 |\n|  - Distributed Cloud Database: Turso (libSQL) with UNIQUE(node_id, recorded_at) constraint              |\n|  - Multi-Parametric Disease-Risk Assessment Module:                                                     |\n|      * Late Blight Module: Adapted Wallin's Severity Values & Leaf Wetness Duration Tracking            |\n|      * Bacterial Wilt Module: Soil Hydrothermal Index (Soil Moisture + Soil Temp Matrix)                |\n|                                                                                                         |\n|                                       | (HTTPS / Real-Time JSON Stream)                                 |\n|                                       v                                                                 |\n|                                                                                                         |\n|  [ WEB DASHBOARD & USER INTERFACE ]                                                                     |\n|  - React.js + Vite Web Application (Desktop & Mobile Responsive)                                        |\n|  - Live Environmental Telemetry Gauges & Node Battery Status                                            |\n|  - Dynamic Historical Time-Series Visualizations & Tabular Exports                                      |\n|  - Tri-Level Color-Coded Early Warning Disease Risk Alerts (Low, Moderate, High)                        |\n|  - Pre-Symptomatic Agronomic Preventive Recommendations for Farmers                                     |\n|                                                                                                         |\n+---------------------------------------------------------------------------------------------------------+\n```", get_base64_img("figure4_system_architecture.png"))

ch3 = ch3.replace("```\n+---------------------------------------------------------------------------------------------------------+\n|                                    SOLANAWATCH COMPLETE CIRCUIT SCHEMATIC                               |\n+---------------------------------------------------------------------------------------------------------+\n|                                                                                                         |\n|  [20W 12V Solar Panel] ---> [12V 10A MPPT Controller] <---> [12.8V 12Ah LiFePO4 Battery + BMS]          |\n|                                      |                                                                  |\n|                                (12V DC Rail)                                                            |\n|                                /           \\                                                            |\n|                               /             \\                                                           |\n|            [12V-to-5V Buck Converter]    [RS485 Leaf Wetness Sensor (IP68)]                             |\n|                       |                             | (A / B Differential Modbus Lines)                 |\n|                 (5V DC Rail)                        v                                                   |\n|                 /          \\             [MAX485 / SP3485 Board]                                        |\n|                /            \\            - VCC: 3.3V, GND: Common Ground                                |\n|        [ESP32 DevKit V1]   [3.3V Buck]   - RO: GPIO 16 (UART2 RX2)                                      |\n|        - VIN: 5.0V                       - DI: GPIO 17 (UART2 TX2)                                      |\n|        - GND: Common GND                 - DE/RE: GPIO 22 (Direction Control)                           |\n|                                                                                                         |\n|  [ESP32 GPIO Pin Assignments]                                                                           |\n|  - GPIO 15 (Digital I/O) ---------> DHT22 Data Pin (with 4.7k ohm pull-up resistor to 3.3V)             |\n|  - GPIO 4  (Digital I/O) ---------> DS18B20 OneWire Data Pin (with 4.7k ohm pull-up resistor to 3.3V)   |\n|  - GPIO 34 (ADC1 Channel 6) ------> Capacitive Soil Moisture Sensor v1.2 Analog Output                  |\n|  - GPIO 5  (VSPI CS) -------------> MicroSD SPI Chip Select (CS)                                        |\n|  - GPIO 18 (VSPI SCK) ------------> MicroSD SPI Clock (SCK)                                             |\n|  - GPIO 19 (VSPI MISO) -----------> MicroSD SPI Master-In-Slave-Out (MISO)                              |\n|  - GPIO 23 (VSPI MOSI) -----------> MicroSD SPI Master-Out-Slave-In (MOSI)                              |\n|  - GPIO 16 (UART2 RX2) -----------> MAX485 Receiver Output (RO)                                         |\n|  - GPIO 17 (UART2 TX2) -----------> MAX485 Driver Input (DI)                                            |\n|  - GPIO 22 (Digital Out) ---------> MAX485 Driver Enable / Receiver Enable (DE / /RE)                   |\n|                                                                                                         |\n+---------------------------------------------------------------------------------------------------------+\n```", get_base64_img("figure6_circuit_schematic.png"))

ch3 = ch3.replace("```\n+------------------+         +-------------------+         +------------------------+\n|    users_tbl     | 1     * |    nodes_tbl      | 1     * |  sensor_readings_tbl   |\n|------------------|---------|-------------------|---------|------------------------|\n| PK user_id (UUID)|         | PK node_id (UUID) |         | PK reading_id (UUID)   |\n|    full_name     |         | FK user_id        |         | FK node_id             |\n|    email (UQ)    |         |    node_name      |         |    air_temperature     |\n|    password_hash |         |    crop_type      |         |    air_humidity        |\n|    role          |         |    field_location |         |    soil_temperature    |\n|    created_at    |         |    battery_voltage|         |    soil_moisture       |\n+------------------+         |    last_seen_at   |         |    leaf_wetness_status |\n                             +-------------------+         |    recorded_at (UQ)    |\n                                       | 1                 |    synced_at           |\n                                       |                   +------------------------+\n                                       | *                             | 1\n                             +-------------------+                     | *\n                             |   disease_risk_   |         +------------------------+\n                             |     logs_tbl      |         |     alerts_tbl         |\n                             |-------------------|         |------------------------|\n                             | PK log_id (UUID)  |         | PK alert_id (UUID)     |\n                             | FK node_id        |         | FK node_id             |\n                             | FK reading_id     |         | FK reading_id          |\n                             |    late_blight_sv |         |    disease_target      |\n                             |    bact_wilt_idx  |         |    alert_level         |\n                             |    calculated_at  |         |    message             |\n                             +-------------------+         |    created_at          |\n                                                           +------------------------+\n```", get_base64_img("figure5_er_diagram.png"))

combined_md = f"{ch1}\n\n<hr style='border: 1px solid #000; margin: 35px 0;'/>\n\n{ch2}\n\n<hr style='border: 1px solid #000; margin: 35px 0;'/>\n\n{ch3}\n\n<hr style='border: 1px solid #000; margin: 35px 0;'/>\n\n{bib}"

html_body = markdown.markdown(combined_md, extensions=['tables', 'fenced_code'])

full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>SolanaWatch: Capstone Proposal Chapters 1-3 (Revised)</title>
<style>
    body {{
        font-family: "Times New Roman", Times, serif;
        font-size: 12pt;
        line-height: 1.5;
        color: #000000;
        max-width: 850px;
        margin: 40px auto;
        padding: 40px 60px;
        background-color: #FFFFFF;
    }}
    p {{
        font-family: "Times New Roman", Times, serif;
        font-size: 12pt;
        line-height: 1.5;
        text-align: justify;
        text-indent: 0.5in;
        margin-top: 0;
        margin-bottom: 8px;
    }}
    /* Do not indent lists, headings, and captions */
    li p, ul, ol, table, pre, h1, h2, h3, h4, .no-indent {{
        text-indent: 0 !important;
    }}
    h1 {{
        font-family: "Times New Roman", Times, serif;
        font-size: 14pt;
        font-weight: bold;
        text-align: center;
        margin-top: 36px;
        margin-bottom: 16px;
    }}
    h2 {{
        font-family: "Times New Roman", Times, serif;
        font-size: 13pt;
        font-weight: bold;
        text-align: left;
        margin-top: 26px;
        margin-bottom: 10px;
    }}
    h3, h4 {{
        font-family: "Times New Roman", Times, serif;
        font-size: 12pt;
        font-weight: bold;
        text-align: left;
        margin-top: 18px;
        margin-bottom: 6px;
    }}
    table {{
        border-collapse: collapse;
        width: 100%;
        margin: 20px auto;
        font-family: "Times New Roman", Times, serif;
        font-size: 11pt;
    }}
    th, td {{
        border: 1px solid #333333;
        padding: 6px 10px;
        text-align: left;
    }}
    th {{
        background-color: #EAEAEA;
        color: #000000;
        font-weight: bold;
    }}
    tr:nth-child(even) {{
        background-color: #FFFFFF;
    }}
    ul, ol {{
        margin-left: 0.5in;
        margin-bottom: 12px;
        text-align: justify;
    }}
    li {{
        margin-bottom: 4px;
    }}
    pre {{
        background-color: #F8F9FA;
        border: 1px solid #CCCCCC;
        padding: 12px;
        font-family: "Times New Roman", Times, serif;
        font-size: 11pt;
        white-space: pre-wrap;
        margin: 15px 0;
    }}
    code {{
        font-family: "Times New Roman", Times, serif;
        font-weight: bold;
    }}
</style>
</head>
<body>
{html_body}
</body>
</html>
"""

html_out = os.path.join(out_dir, "SolanaWatch_Proposal_Chapters_1-3_REVISED.html")
with open(html_out, 'w', encoding='utf-8') as f:
    f.write(full_html)

print(f"Generated formatted HTML with embedded figures: {html_out}")
