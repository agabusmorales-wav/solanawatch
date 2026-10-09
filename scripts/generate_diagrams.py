import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig_dir = r"C:\Users\agabu\Downloads\CODE PROJECTS\SOLANAWATCH\figures"
os.makedirs(fig_dir, exist_ok=True)

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif']

def create_context_diagram():
    fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.axis('off')

    # Sensor Node Box
    node_box = patches.FancyBboxPatch((0.5, 1.5), 2.2, 2.0, boxstyle="round,pad=0.1", fc="#EBF3FB", ec="#003366", lw=2)
    ax.add_patch(node_box)
    ax.text(1.6, 2.8, "ESP32 Sensor Node\n(Edge Hardware)", ha="center", va="center", fontsize=11, fontweight="bold", color="#003366")
    ax.text(1.6, 2.0, "• DHT22 (Air Temp/RH)\n• DS18B20 (Soil Temp)\n• Capacitive Moisture\n• RS485 Leaf Wetness\n• MicroSD Storage", ha="center", va="center", fontsize=8.5, color="#333333")

    # Central SolanaWatch System Circle
    system_circle = patches.Ellipse((5.0, 2.5), 3.0, 2.4, fc="#003366", ec="#001F3F", lw=2)
    ax.add_patch(system_circle)
    ax.text(5.0, 2.7, "SolanaWatch System", ha="center", va="center", fontsize=12, fontweight="bold", color="#FFFFFF")
    ax.text(5.0, 2.1, "IoT Disease Early Warning\n& Decision Support Platform\n(Node.js + Turso DB + React)", ha="center", va="center", fontsize=8.5, color="#E0E8F0")

    # Farmer / Operator Box
    user_box = patches.FancyBboxPatch((7.3, 1.5), 2.2, 2.0, boxstyle="round,pad=0.1", fc="#EBF3FB", ec="#003366", lw=2)
    ax.add_patch(user_box)
    ax.text(8.4, 2.8, "Farmer / Operator\n(End User)", ha="center", va="center", fontsize=11, fontweight="bold", color="#003366")
    ax.text(8.4, 2.0, "• Smallholder Growers\n• Agricultural Techs\n• Web Dashboard\n• Smartphone / PC", ha="center", va="center", fontsize=8.5, color="#333333")

    # Arrows Node -> System
    ax.annotate('', xy=(3.5, 2.7), xytext=(2.7, 2.7), arrowprops=dict(arrowstyle="-|>", color="#003366", lw=2))
    ax.text(3.1, 2.9, "Sensor Telemetry\n(Air/Soil/Leaf Data)", ha="center", va="bottom", fontsize=8, fontweight="bold", color="#003366")

    # Arrows System <-> User
    ax.annotate('', xy=(7.3, 2.8), xytext=(6.5, 2.8), arrowprops=dict(arrowstyle="-|>", color="#D9534F", lw=2))
    ax.text(6.9, 3.0, "Live Alerts &\nRisk Trends", ha="center", va="bottom", fontsize=8, fontweight="bold", color="#D9534F")

    ax.annotate('', xy=(6.5, 2.2), xytext=(7.3, 2.2), arrowprops=dict(arrowstyle="-|>", color="#003366", lw=2))
    ax.text(6.9, 1.8, "Login & Device\nConfiguration", ha="center", va="top", fontsize=8, color="#003366")

    plt.title("Figure 1. SolanaWatch Context Diagram", fontsize=12, fontweight="bold", pad=15, y=-0.05)
    plt.tight_layout()
    out_path = os.path.join(fig_dir, "figure1_context_diagram.png")
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Created: {out_path}")

def create_activity_diagram():
    fig, ax = plt.subplots(figsize=(11, 7), dpi=300)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 7)
    ax.axis('off')

    # Swimlane Headers
    ax.add_patch(patches.Rectangle((0.2, 6.2), 3.4, 0.6, fc="#003366", ec="#333333"))
    ax.text(1.9, 6.5, "ESP32 Edge Node (Hardware)", ha="center", va="center", color="#FFFFFF", fontweight="bold", fontsize=10.5)

    ax.add_patch(patches.Rectangle((3.8, 6.2), 3.4, 0.6, fc="#1B4F72", ec="#333333"))
    ax.text(5.5, 6.5, "Node.js Cloud Backend & DB", ha="center", va="center", color="#FFFFFF", fontweight="bold", fontsize=10.5)

    ax.add_patch(patches.Rectangle((7.4, 6.2), 3.4, 0.6, fc="#2874A6", ec="#333333"))
    ax.text(9.1, 6.5, "React.js Web Dashboard", ha="center", va="center", color="#FFFFFF", fontweight="bold", fontsize=10.5)

    # Step 1: Start & Read Sensors
    ax.add_patch(patches.FancyBboxPatch((0.8, 5.0), 2.2, 0.8, boxstyle="round,pad=0.05", fc="#EBF5FB", ec="#003366", lw=1.5))
    ax.text(1.9, 5.4, "Read Sensor Array\n(DHT22, DS18B20, Soil, Leaf)", ha="center", va="center", fontsize=8.5)

    # Step 2: Check Wi-Fi
    ax.add_patch(patches.Polygon([[1.9, 4.4], [2.8, 3.8], [1.9, 3.2], [1.0, 3.8]], fc="#FEF9E7", ec="#B7950B", lw=1.5))
    ax.text(1.9, 3.8, "Wi-Fi\nAvailable?", ha="center", va="center", fontsize=8, fontweight="bold")

    # Step 3: Offline Buffer
    ax.add_patch(patches.FancyBboxPatch((0.4, 2.0), 1.5, 0.8, boxstyle="round,pad=0.05", fc="#FDEDEC", ec="#C0392B", lw=1.5))
    ax.text(1.15, 2.4, "Append JSON Line\nto MicroSD Buffer", ha="center", va="center", fontsize=8)

    # Step 4: Transmit Telemetry
    ax.add_patch(patches.FancyBboxPatch((2.2, 2.0), 1.4, 0.8, boxstyle="round,pad=0.05", fc="#E8F8F5", ec="#16A085", lw=1.5))
    ax.text(2.9, 2.4, "HTTP POST\nBatch Sync", ha="center", va="center", fontsize=8)

    # Step 5: Backend Process & Disease Engine
    ax.add_patch(patches.FancyBboxPatch((4.2, 4.6), 2.6, 0.9, boxstyle="round,pad=0.05", fc="#EBF5FB", ec="#1B4F72", lw=1.5))
    ax.text(5.5, 5.05, "Validate & Store Telemetry\nin Turso DB (libSQL)", ha="center", va="center", fontsize=8.5)

    ax.add_patch(patches.FancyBboxPatch((4.2, 3.0), 2.6, 1.1, boxstyle="round,pad=0.05", fc="#FEF5E7", ec="#D35400", lw=1.5))
    ax.text(5.5, 3.55, "Execute Disease Risk Engine\n• Late Blight (Wallin SV / LWD)\n• Bacterial Wilt (Soil Index)", ha="center", va="center", fontsize=8.5)

    # Step 6: Web Dashboard Render & Alerts
    ax.add_patch(patches.FancyBboxPatch((7.8, 4.6), 2.6, 0.9, boxstyle="round,pad=0.05", fc="#EBF5FB", ec="#2874A6", lw=1.5))
    ax.text(9.1, 5.05, "Update Real-Time Telemetry\n& Historical Time-Series", ha="center", va="center", fontsize=8.5)

    ax.add_patch(patches.FancyBboxPatch((7.8, 3.0), 2.6, 1.1, boxstyle="round,pad=0.05", fc="#FDEDEC", ec="#C0392B", lw=1.5))
    ax.text(9.1, 3.55, "Dispatch Visual Warning\n• Green = Low Risk\n• Yellow = Moderate Risk\n• Red = High Risk Alert", ha="center", va="center", fontsize=8.5)

    # Deep Sleep Loop
    ax.add_patch(patches.FancyBboxPatch((0.8, 0.6), 2.2, 0.7, boxstyle="round,pad=0.05", fc="#EAEDED", ec="#7F8C8D", lw=1.5))
    ax.text(1.9, 0.95, "Enter Deep Sleep (15 Min)\nConserve LiFePO4 Power", ha="center", va="center", fontsize=8)

    # Connectors
    ax.annotate('', xy=(1.9, 4.4), xytext=(1.9, 5.0), arrowprops=dict(arrowstyle="-|>", color="#333333", lw=1.2))
    ax.annotate('', xy=(1.15, 2.8), xytext=(1.45, 3.5), arrowprops=dict(arrowstyle="-|>", color="#C0392B", lw=1.2))
    ax.text(1.0, 3.3, "NO", fontsize=7.5, fontweight="bold", color="#C0392B")

    ax.annotate('', xy=(2.9, 2.8), xytext=(2.35, 3.5), arrowprops=dict(arrowstyle="-|>", color="#16A085", lw=1.2))
    ax.text(2.7, 3.3, "YES", fontsize=7.5, fontweight="bold", color="#16A085")

    ax.annotate('', xy=(4.2, 5.05), xytext=(3.6, 2.4), arrowprops=dict(arrowstyle="-|>", color="#1B4F72", lw=1.2))
    ax.annotate('', xy=(5.5, 4.1), xytext=(5.5, 4.6), arrowprops=dict(arrowstyle="-|>", color="#1B4F72", lw=1.2))
    ax.annotate('', xy=(7.8, 5.05), xytext=(6.8, 5.05), arrowprops=dict(arrowstyle="-|>", color="#2874A6", lw=1.2))
    ax.annotate('', xy=(7.8, 3.55), xytext=(6.8, 3.55), arrowprops=dict(arrowstyle="-|>", color="#C0392B", lw=1.2))

    ax.annotate('', xy=(1.15, 1.3), xytext=(1.15, 2.0), arrowprops=dict(arrowstyle="-|>", color="#333333", lw=1.2))
    ax.annotate('', xy=(2.9, 1.3), xytext=(2.9, 2.0), arrowprops=dict(arrowstyle="-|>", color="#333333", lw=1.2))
    ax.annotate('', xy=(0.8, 5.4), xytext=(0.8, 0.95), arrowprops=dict(arrowstyle="-|>", color="#333333", lw=1.2, connectionstyle="arc3,rad=-0.4"))

    plt.title("Figure 2. SolanaWatch System Activity and Synchronization Diagram", fontsize=12, fontweight="bold", pad=10, y=-0.05)
    plt.tight_layout()
    out_path = os.path.join(fig_dir, "figure2_activity_diagram.png")
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Created: {out_path}")

def create_prototyping_model():
    fig, ax = plt.subplots(figsize=(10, 4.5), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4.5)
    ax.axis('off')

    phases = [
        ("Requirements\nGathering & Analysis", 1.2, 3.2),
        ("Quick Design\n(Schematics & UI)", 3.8, 3.2),
        ("Build Prototype\n(PCB, Firmware, App)", 6.4, 3.2),
        ("Evaluation &\nTesting (Field/QA)", 8.8, 3.2),
        ("Refining Prototype\n(Bug Fixes & Hardening)", 5.1, 1.2),
        ("Final Validation &\nField Deployment", 8.8, 1.2),
    ]

    for title, x, y in phases:
        fc = "#003366" if "Deployment" in title else "#EBF3FB"
        tc = "#FFFFFF" if "Deployment" in title else "#003366"
        ec = "#001F3F" if "Deployment" in title else "#003366"
        box = patches.FancyBboxPatch((x-0.9, y-0.5), 1.8, 1.0, boxstyle="round,pad=0.08", fc=fc, ec=ec, lw=1.8)
        ax.add_patch(box)
        ax.text(x, y, title, ha="center", va="center", fontsize=8.5, fontweight="bold", color=tc)

    # Forward arrows top row
    ax.annotate('', xy=(2.8, 3.2), xytext=(2.2, 3.2), arrowprops=dict(arrowstyle="-|>", color="#003366", lw=1.8))
    ax.annotate('', xy=(5.4, 3.2), xytext=(4.8, 3.2), arrowprops=dict(arrowstyle="-|>", color="#003366", lw=1.8))
    ax.annotate('', xy=(7.8, 3.2), xytext=(7.4, 3.2), arrowprops=dict(arrowstyle="-|>", color="#003366", lw=1.8))

    # Testing -> Refining (Needs iteration)
    ax.annotate('', xy=(6.1, 1.2), xytext=(8.8, 2.6), arrowprops=dict(arrowstyle="-|>", color="#D9534F", lw=1.8, connectionstyle="arc3,rad=0.2"))
    ax.text(7.6, 1.7, "Issues Identified\n(Iterative Cycle)", fontsize=8, color="#D9534F", ha="center")

    # Refining -> Quick Design
    ax.annotate('', xy=(3.8, 2.6), xytext=(4.2, 1.2), arrowprops=dict(arrowstyle="-|>", color="#D9534F", lw=1.8, connectionstyle="arc3,rad=0.2"))

    # Testing -> Final Deployment (Passed)
    ax.annotate('', xy=(8.8, 1.8), xytext=(8.8, 2.6), arrowprops=dict(arrowstyle="-|>", color="#27AE60", lw=2.0))
    ax.text(9.4, 2.2, "Passed QA\nCriteria", fontsize=8, fontweight="bold", color="#27AE60", ha="left")

    plt.title("Figure 3. Prototyping Development Methodology Model", fontsize=12, fontweight="bold", pad=10, y=-0.05)
    plt.tight_layout()
    out_path = os.path.join(fig_dir, "figure3_prototyping_model.png")
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Created: {out_path}")

def create_system_architecture():
    fig, ax = plt.subplots(figsize=(11, 7.5), dpi=300)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 7.5)
    ax.axis('off')

    # Subsystem 1: Power
    ax.add_patch(patches.FancyBboxPatch((0.5, 4.5), 3.0, 2.6, boxstyle="round,pad=0.1", fc="#FCF3CF", ec="#B7950B", lw=2))
    ax.text(2.0, 6.8, "Power Subsystem", ha="center", va="center", fontsize=11, fontweight="bold", color="#7D6608")
    ax.text(2.0, 5.6, "• 20W 12V Monocrystalline PV Panel\n• 12V 10A MPPT Solar Charge Controller\n• 12.8V 12Ah LiFePO4 Battery (+15A BMS)\n• LM2596 Step-Down Buck (12V->5V/3.3V)\n• Provides >= 3 Days Full Autonomy", ha="center", va="center", fontsize=8.5)

    # Subsystem 2: Edge Node
    ax.add_patch(patches.FancyBboxPatch((0.5, 0.6), 3.0, 3.4, boxstyle="round,pad=0.1", fc="#EBF5FB", ec="#1B4F72", lw=2))
    ax.text(2.0, 3.7, "ESP32 Edge Node", ha="center", va="center", fontsize=11, fontweight="bold", color="#1B4F72")
    ax.text(2.0, 2.1, "• ESP32 DevKit V1 (240MHz, 2.4GHz Wi-Fi)\n• DHT22 in Stevenson Radiation Shield\n• DS18B20 Waterproof Stainless Probe\n• Capacitive Soil Moisture Sensor v1.2\n• RS485 Leaf Wetness Sensor + MAX485\n• SPI MicroSD Offline FIFO Buffer\n• Custom PCB Shield in IP66 Enclosure", ha="center", va="center", fontsize=8.5)

    # Subsystem 3: Cloud Backend & DB
    ax.add_patch(patches.FancyBboxPatch((4.2, 1.5), 3.0, 4.8, boxstyle="round,pad=0.1", fc="#E8F8F5", ec="#117864", lw=2))
    ax.text(5.7, 5.9, "Cloud Backend & Database", ha="center", va="center", fontsize=11, fontweight="bold", color="#117864")
    ax.text(5.7, 3.6, "• Node.js & Express.js REST API\n• Turso Database (Distributed libSQL)\n• Idempotent Sync with UUIDs\n• Composite Unique Key Deduplication\n\n[ Disease Risk Engine ]\n• Late Blight Module:\n  Adapted Wallin SV & LWD Tracking\n• Bacterial Wilt Module:\n  Soil Hydrothermal Index Matrix", ha="center", va="center", fontsize=8.5)

    # Subsystem 4: Web Dashboard
    ax.add_patch(patches.FancyBboxPatch((7.8, 1.5), 2.7, 4.8, boxstyle="round,pad=0.1", fc="#EBF3FB", ec="#003366", lw=2))
    ax.text(9.15, 5.9, "React.js Web Dashboard", ha="center", va="center", fontsize=11, fontweight="bold", color="#003366")
    ax.text(9.15, 3.6, "• React.js + Vite Architecture\n• Live Telemetry Gauges\n• Interactive Time-Series Charts\n• Node Battery & Wi-Fi Health\n• Color-Coded Risk Notifications:\n  (Green, Yellow, Red)\n• Agronomic Decision Recommendations\n• Responsive Mobile & Desktop UI", ha="center", va="center", fontsize=8.5)

    # Connectors
    ax.annotate('', xy=(2.0, 4.1), xytext=(2.0, 4.5), arrowprops=dict(arrowstyle="-|>", color="#B7950B", lw=2.5))
    ax.text(2.0, 4.3, "12V & 5V/3.3V DC", ha="center", va="center", fontsize=7.5, fontweight="bold", color="#B7950B", backgroundcolor="#FFFFFF")

    ax.annotate('', xy=(4.2, 3.0), xytext=(3.6, 2.5), arrowprops=dict(arrowstyle="-|>", color="#1B4F72", lw=2.5))
    ax.text(3.9, 2.9, "2.4GHz Wi-Fi\nHTTP JSON", ha="center", va="center", fontsize=7.5, fontweight="bold", color="#1B4F72", backgroundcolor="#FFFFFF")

    ax.annotate('', xy=(7.8, 3.9), xytext=(7.3, 3.9), arrowprops=dict(arrowstyle="<|-|>", color="#003366", lw=2.5))
    ax.text(7.55, 4.2, "HTTPS /\nREST API", ha="center", va="center", fontsize=7.5, fontweight="bold", color="#003366", backgroundcolor="#FFFFFF")

    plt.title("Figure 4. SolanaWatch System Architecture Diagram", fontsize=12, fontweight="bold", pad=10, y=-0.05)
    plt.tight_layout()
    out_path = os.path.join(fig_dir, "figure4_system_architecture.png")
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Created: {out_path}")

def create_er_diagram():
    fig, ax = plt.subplots(figsize=(11, 6.5), dpi=300)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 6.5)
    ax.axis('off')

    # Table 1: users_tbl
    ax.add_patch(patches.Rectangle((0.5, 4.0), 2.6, 2.0, fc="#EBF5FB", ec="#003366", lw=1.5))
    ax.add_patch(patches.Rectangle((0.5, 5.5), 2.6, 0.5, fc="#003366", ec="#003366"))
    ax.text(1.8, 5.75, "users_tbl", ha="center", va="center", color="#FFFFFF", fontweight="bold", fontsize=10)
    ax.text(0.6, 4.75, "PK user_id : TEXT (UUID)\n   full_name : TEXT\n   email : TEXT (UNIQUE)\n   password_hash : TEXT\n   role : TEXT\n   created_at : TIMESTAMP", fontsize=8)

    # Table 2: nodes_tbl
    ax.add_patch(patches.Rectangle((4.2, 4.0), 2.7, 2.1, fc="#EBF5FB", ec="#003366", lw=1.5))
    ax.add_patch(patches.Rectangle((4.2, 5.6), 2.7, 0.5, fc="#003366", ec="#003366"))
    ax.text(5.55, 5.85, "nodes_tbl", ha="center", va="center", color="#FFFFFF", fontweight="bold", fontsize=10)
    ax.text(4.3, 4.75, "PK node_id : TEXT (UUID)\nFK user_id : TEXT\n   node_name : TEXT\n   crop_type : TEXT\n   field_location : TEXT\n   battery_voltage : REAL\n   last_seen_at : TIMESTAMP", fontsize=8)

    # Table 3: sensor_readings_tbl
    ax.add_patch(patches.Rectangle((8.0, 3.6), 2.6, 2.5, fc="#EBF5FB", ec="#003366", lw=1.5))
    ax.add_patch(patches.Rectangle((8.0, 5.6), 2.6, 0.5, fc="#003366", ec="#003366"))
    ax.text(9.3, 5.85, "sensor_readings_tbl", ha="center", va="center", color="#FFFFFF", fontweight="bold", fontsize=10)
    ax.text(8.1, 4.55, "PK reading_id : TEXT (UUID)\nFK node_id : TEXT\n   air_temp : REAL\n   air_humidity : REAL\n   soil_temp : REAL\n   soil_moisture : REAL\n   leaf_wetness : INTEGER\n   recorded_at : TIMESTAMP\n   synced_at : TIMESTAMP\n   UQ(node_id, recorded_at)", fontsize=7.5)

    # Table 4: disease_risk_logs_tbl
    ax.add_patch(patches.Rectangle((4.2, 0.8), 2.7, 2.2, fc="#EBF5FB", ec="#003366", lw=1.5))
    ax.add_patch(patches.Rectangle((4.2, 2.5), 2.7, 0.5, fc="#003366", ec="#003366"))
    ax.text(5.55, 2.75, "disease_risk_logs_tbl", ha="center", va="center", color="#FFFFFF", fontweight="bold", fontsize=10)
    ax.text(4.3, 1.6, "PK log_id : TEXT (UUID)\nFK node_id : TEXT\nFK reading_id : TEXT\n   late_blight_sv : INTEGER\n   bact_wilt_idx : REAL\n   risk_level : TEXT\n   calculated_at : TIMESTAMP", fontsize=8)

    # Table 5: alerts_tbl
    ax.add_patch(patches.Rectangle((8.0, 0.8), 2.6, 2.2, fc="#FDEDEC", ec="#C0392B", lw=1.5))
    ax.add_patch(patches.Rectangle((8.0, 2.5), 2.6, 0.5, fc="#C0392B", ec="#C0392B"))
    ax.text(9.3, 2.75, "alerts_tbl", ha="center", va="center", color="#FFFFFF", fontweight="bold", fontsize=10)
    ax.text(8.1, 1.6, "PK alert_id : TEXT (UUID)\nFK node_id : TEXT\nFK reading_id : TEXT\n   disease_target : TEXT\n   alert_level : TEXT\n   message : TEXT\n   is_read : BOOLEAN\n   created_at : TIMESTAMP", fontsize=8)

    # Relationships
    ax.annotate('', xy=(4.2, 5.0), xytext=(3.1, 5.0), arrowprops=dict(arrowstyle="-|>", color="#003366", lw=1.8))
    ax.text(3.6, 5.2, "1 : N", fontsize=8, fontweight="bold", ha="center")

    ax.annotate('', xy=(8.0, 5.0), xytext=(6.9, 5.0), arrowprops=dict(arrowstyle="-|>", color="#003366", lw=1.8))
    ax.text(7.45, 5.2, "1 : N", fontsize=8, fontweight="bold", ha="center")

    ax.annotate('', xy=(5.55, 3.0), xytext=(5.55, 4.0), arrowprops=dict(arrowstyle="-|>", color="#003366", lw=1.8))
    ax.text(5.8, 3.5, "1 : N", fontsize=8, fontweight="bold", ha="left")

    ax.annotate('', xy=(9.3, 3.0), xytext=(9.3, 3.6), arrowprops=dict(arrowstyle="-|>", color="#C0392B", lw=1.8))
    ax.text(9.55, 3.3, "1 : N", fontsize=8, fontweight="bold", ha="left", color="#C0392B")

    plt.title("Figure 5. SolanaWatch Database Entity-Relationship Diagram (ERD)", fontsize=12, fontweight="bold", pad=10, y=-0.05)
    plt.tight_layout()
    out_path = os.path.join(fig_dir, "figure5_er_diagram.png")
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Created: {out_path}")

def create_circuit_schematic():
    fig, ax = plt.subplots(figsize=(11, 7.5), dpi=300)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 7.5)
    ax.axis('off')

    # Central ESP32 Box
    ax.add_patch(patches.FancyBboxPatch((4.0, 2.0), 3.0, 3.8, boxstyle="round,pad=0.1", fc="#1B4F72", ec="#001F3F", lw=2))
    ax.text(5.5, 5.4, "ESP32 DevKit V1\n(Main Controller)", ha="center", va="center", color="#FFFFFF", fontweight="bold", fontsize=11)
    ax.text(5.5, 3.5, "[ GPIO Pin Mappings ]\n• GPIO 15 : DHT22 Data (4.7k Pull-up)\n• GPIO 4  : DS18B20 OneWire (4.7k Pull-up)\n• GPIO 34 : Capacitive Soil (ADC1_CH6)\n• GPIO 16 : MAX485 RO (UART2 RX2)\n• GPIO 17 : MAX485 DI (UART2 TX2)\n• GPIO 22 : MAX485 DE / /RE Control\n• GPIO 5  : MicroSD CS (VSPI)\n• GPIO 18 : MicroSD SCK\n• GPIO 19 : MicroSD MISO\n• GPIO 23 : MicroSD MOSI", ha="center", va="center", color="#EAECEE", fontsize=8)

    # Power Circuit (Top Left)
    ax.add_patch(patches.FancyBboxPatch((0.4, 4.8), 2.8, 2.2, boxstyle="round,pad=0.08", fc="#FEF9E7", ec="#B7950B", lw=1.8))
    ax.text(1.8, 6.6, "Solar Power Network", ha="center", va="center", color="#7D6608", fontweight="bold", fontsize=9.5)
    ax.text(1.8, 5.6, "• 20W 12V Monocrystalline PV Panel\n  (Voc = 21.6V, Vmp = 18.0V)\n• 12V 10A MPPT Charge Controller\n• 12.8V 12Ah LiFePO4 Battery (+15A BMS)\n• LM2596 Buck -> 5.0V / 3.3V Rails", ha="center", va="center", fontsize=7.5)

    # Sensor 1: DHT22 in Stevenson
    ax.add_patch(patches.FancyBboxPatch((0.4, 2.8), 2.8, 1.6, boxstyle="round,pad=0.08", fc="#EBF5FB", ec="#2980B9", lw=1.5))
    ax.text(1.8, 4.0, "DHT22 in Stevenson Screen", ha="center", va="center", color="#1B4F72", fontweight="bold", fontsize=9)
    ax.text(1.8, 3.3, "• VCC: 3.3V, GND: Common GND\n• Data -> GPIO 15\n• 4.7k ohm pull-up to 3.3V\n• Air Temp (-40..80°C) & RH (0..100%)", ha="center", va="center", fontsize=7.5)

    # Sensor 2: DS18B20
    ax.add_patch(patches.FancyBboxPatch((0.4, 0.8), 2.8, 1.6, boxstyle="round,pad=0.08", fc="#EBF5FB", ec="#2980B9", lw=1.5))
    ax.text(1.8, 2.0, "DS18B20 Soil Temp Probe", ha="center", va="center", color="#1B4F72", fontweight="bold", fontsize=9)
    ax.text(1.8, 1.3, "• VCC: 3.3V, GND: Common GND\n• Data -> GPIO 4 (1-Wire Bus)\n• 4.7k ohm pull-up to 3.3V\n• Stainless probe @ 10cm depth", ha="center", va="center", fontsize=7.5)

    # Sensor 3: Capacitive Soil Moisture
    ax.add_patch(patches.FancyBboxPatch((7.8, 5.0), 2.8, 1.6, boxstyle="round,pad=0.08", fc="#EBF5FB", ec="#2980B9", lw=1.5))
    ax.text(9.2, 6.2, "Capacitive Moisture v1.2", ha="center", va="center", color="#1B4F72", fontweight="bold", fontsize=9)
    ax.text(9.2, 5.5, "• VCC: 3.3V, GND: Common GND\n• AOUT -> GPIO 34 (12-bit ADC)\n• Insulated PCB probe @ 10cm depth\n• 2-point calibrated (0..100% VWC)", ha="center", va="center", fontsize=7.5)

    # Sensor 4: RS485 Leaf Wetness + MAX485
    ax.add_patch(patches.FancyBboxPatch((7.8, 2.9), 2.8, 1.8, boxstyle="round,pad=0.08", fc="#FDEDEC", ec="#C0392B", lw=1.5))
    ax.text(9.2, 4.3, "RS485 Leaf Wetness + MAX485", ha="center", va="center", color="#C0392B", fontweight="bold", fontsize=9)
    ax.text(9.2, 3.4, "• Leaf Sensor: 12V DC, IP68\n• MAX485 Board: VCC 3.3V\n• RO -> GPIO 16, DI -> GPIO 17\n• DE / /RE -> GPIO 22\n• Modbus-RTU Protocol", ha="center", va="center", fontsize=7.5)

    # MicroSD Module
    ax.add_patch(patches.FancyBboxPatch((7.8, 0.8), 2.8, 1.8, boxstyle="round,pad=0.08", fc="#EAEDED", ec="#7F8C8D", lw=1.5))
    ax.text(9.2, 2.2, "SPI MicroSD Card Module", ha="center", va="center", color="#333333", fontweight="bold", fontsize=9)
    ax.text(9.2, 1.3, "• VCC: 3.3V, GND: Common GND\n• CS: GPIO 5, SCK: GPIO 18\n• MISO: GPIO 19, MOSI: GPIO 23\n• SanDisk 16GB FAT32 Offline Queue", ha="center", va="center", fontsize=7.5)

    # Connector lines to ESP32
    ax.annotate('', xy=(4.0, 5.6), xytext=(3.2, 5.6), arrowprops=dict(arrowstyle="-|>", color="#B7950B", lw=2))
    ax.annotate('', xy=(4.0, 3.6), xytext=(3.2, 3.6), arrowprops=dict(arrowstyle="-|>", color="#2980B9", lw=1.5))
    ax.annotate('', xy=(4.0, 1.6), xytext=(3.2, 1.6), arrowprops=dict(arrowstyle="-|>", color="#2980B9", lw=1.5))

    ax.annotate('', xy=(7.0, 5.5), xytext=(7.8, 5.5), arrowprops=dict(arrowstyle="<|-", color="#2980B9", lw=1.5))
    ax.annotate('', xy=(7.0, 3.6), xytext=(7.8, 3.6), arrowprops=dict(arrowstyle="<|-", color="#C0392B", lw=1.5))
    ax.annotate('', xy=(7.0, 1.6), xytext=(7.8, 1.6), arrowprops=dict(arrowstyle="<|-", color="#333333", lw=1.5))

    plt.title("Figure 6. Complete Circuit Pinout and Hardware Interfacing Schematic", fontsize=12, fontweight="bold", pad=10, y=-0.05)
    plt.tight_layout()
    out_path = os.path.join(fig_dir, "figure6_circuit_schematic.png")
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Created: {out_path}")

if __name__ == "__main__":
    create_context_diagram()
    create_activity_diagram()
    create_prototyping_model()
    create_system_architecture()
    create_er_diagram()
    create_circuit_schematic()
    print("All 6 high-resolution diagrams successfully generated.")
