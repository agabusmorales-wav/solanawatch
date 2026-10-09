import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle, Polygon, Wedge

fig_dir = r"C:\Users\agabu\Downloads\CODE PROJECTS\SOLANAWATCH\figures"
os.makedirs(fig_dir, exist_ok=True)

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']

def create_physical_layout_diagram():
    fig, ax = plt.subplots(figsize=(14, 10), dpi=300)
    ax.set_xlim(-1, 13)
    ax.set_ylim(-3.5, 12.5)
    ax.axis('off')

    # Background canvas tint
    bg = Rectangle((-1, -3.5), 14, 16, fc="#F8FAFC", ec="none", zorder=0)
    ax.add_patch(bg)

    # Ground Level & Subsurface
    ground_y = 1.0
    soil_rect = Rectangle((-1, -3.5), 14, 4.5, fc="#EFEBE9", ec="#8D6E63", lw=1.5, zorder=1)
    ax.add_patch(soil_rect)
    
    # Ground surface line
    ax.plot([-1, 13], [ground_y, ground_y], color="#5D4037", lw=3, zorder=2)
    ax.text(0.2, ground_y + 0.2, "SOIL SURFACE (0.0 m / Baseline)", fontsize=9, fontweight="bold", color="#5D4037")

    # Soil layers texture / hatch
    ax.text(0.2, ground_y - 1.8, "SUB-SURFACE ROOT ZONE\n(Solanaceae Active Rhizosphere)", fontsize=8.5, color="#8D6E63", style="italic")

    # 1.5m Galvanized Steel Mast
    mast_x = 5.0
    mast_width = 0.25
    # Underground mast anchor
    ax.add_patch(Rectangle((mast_x - mast_width/2, -1.5), mast_width, 1.5 + 9.5, fc="#90A4AE", ec="#37474F", lw=1.8, zorder=3))
    # Concrete / anchor peg
    ax.add_patch(FancyBboxPatch((mast_x - 0.6, -1.6), 1.2, 0.8, boxstyle="round,pad=0.05", fc="#B0BEC5", ec="#455A64", lw=1.5, zorder=2))
    ax.text(mast_x, -1.2, "Ground Anchor / Base Mount", ha="center", va="center", fontsize=7.5, color="#263238", fontweight="bold")

    # Height Ruler / Elevation Axis on the Left
    ax.plot([1.2, 1.2], [-1.0, 11.0], color="#78909C", lw=1.5, ls="--", zorder=3)
    height_ticks = [
        (-1.0, "-10 cm", "Root-Zone Depth"),
        (ground_y, "0.0 m", "Ground Surface"),
        (ground_y + 3.0, "+0.6 m", "Enclosure Center"),
        (ground_y + 4.5, "+0.9 m", "Leaf Wetness Canopy"),
        (ground_y + 6.0, "+1.2 m", "Stevenson Shield"),
        (ground_y + 8.5, "+1.5 m", "Solar PV Top")
    ]
    for y_pos, label_m, desc in height_ticks:
        ax.plot([1.0, 1.4], [y_pos, y_pos], color="#455A64", lw=1.5)
        ax.text(0.9, y_pos, f"{label_m}", ha="right", va="center", fontsize=8, fontweight="bold", color="#263238")
        ax.text(1.5, y_pos, f"({desc})", ha="left", va="center", fontsize=7, color="#546E7A")

    # 1. Solar PV Panel Assembly (Top @ ~1.5m, y = 9.5)
    pv_cx, pv_cy = mast_x, ground_y + 8.2
    # Bracket
    ax.add_patch(Rectangle((pv_cx - 0.2, pv_cy - 0.3), 0.4, 0.6, fc="#455A64", ec="#263238", lw=1.2, zorder=4))
    # Tilted Solar Panel (15 deg tilt facing South)
    panel_poly = Polygon([
        [pv_cx - 1.8, pv_cy + 0.9],
        [pv_cx + 1.8, pv_cy + 0.3],
        [pv_cx + 1.8, pv_cy - 0.1],
        [pv_cx - 1.8, pv_cy + 0.5]
    ], fc="#1565C0", ec="#0D47A1", lw=2, zorder=5)
    ax.add_patch(panel_poly)
    # Solar cell grid lines
    ax.plot([pv_cx - 0.9, pv_cx - 0.9], [pv_cy + 0.7, pv_cy + 0.3], color="#90CAF9", lw=1, zorder=6)
    ax.plot([pv_cx, pv_cx], [pv_cy + 0.6, pv_cy + 0.2], color="#90CAF9", lw=1, zorder=6)
    ax.plot([pv_cx + 0.9, pv_cx + 0.9], [pv_cy + 0.5, pv_cy + 0.1], color="#90CAF9", lw=1, zorder=6)
    # Solar callout
    ax.annotate("[1] 20W Monocrystalline Solar PV Panel\n   • Dimensions: 430 × 350 × 17 mm\n   • Positioning: Top of Mast (+1.5 m)\n   • Orientation: Facing True South, 15° Tilt\n   • Role: 24/7 Zero-Grid Energy Harvesting",
                xy=(pv_cx + 1.8, pv_cy + 0.4), xytext=(8.5, 10.5),
                arrowprops=dict(arrowstyle="-|>", color="#1565C0", lw=1.8),
                bbox=dict(boxstyle="round,pad=0.4", fc="#E3F2FD", ec="#1565C0", lw=1.2),
                fontsize=8.5, color="#0D47A1", fontweight="bold")

    # 2. Stevenson Radiation Shield (Ambient Temp/RH @ ~1.2m, y = 7.0)
    stev_x, stev_y = mast_x - 1.0, ground_y + 5.8
    # Mounting arm from mast
    ax.plot([mast_x, stev_x], [stev_y + 0.4, stev_y + 0.4], color="#455A64", lw=2.5, zorder=4)
    # Louvered shield plates
    for i in range(6):
        py = stev_y + (i * 0.16)
        ax.add_patch(FancyBboxPatch((stev_x - 0.45, py), 0.9, 0.10, boxstyle="round,pad=0.02", fc="#FFFFFF", ec="#78909C", lw=1.2, zorder=5))
    # Top cap
    ax.add_patch(Wedge((stev_x, stev_y + 0.95), 0.48, 0, 180, fc="#ECEFF1", ec="#78909C", lw=1.2, zorder=5))
    ax.text(stev_x, stev_y + 0.45, "DHT22\nInside", ha="center", va="center", fontsize=6, color="#455A64", fontweight="bold")
    # Stevenson callout
    ax.annotate("[2] UV-Stabilized Louvered Stevenson Shield\n   • Sensor: DHT22 / AM2302 (Temp & RH)\n   • Positioning: Canopy Level (+1.0 m to +1.2 m)\n   • Louver Design: Free airflow, zero solar radiation bias\n   • Role: Ambient Foliar Microclimate Tracking",
                xy=(stev_x - 0.45, stev_y + 0.5), xytext=(-0.8, 7.8),
                arrowprops=dict(arrowstyle="-|>", color="#0288D1", lw=1.8),
                bbox=dict(boxstyle="round,pad=0.4", fc="#E1F5FE", ec="#0288D1", lw=1.2),
                fontsize=8.5, color="#01579B", fontweight="bold")

    # 3. Leaf Wetness Sensor Assembly (Canopy Level @ ~0.9m, y = 5.2)
    leaf_x, leaf_y = mast_x + 1.2, ground_y + 4.2
    # Extended adjustable boom arm
    ax.plot([mast_x, leaf_x - 0.2], [leaf_y + 0.2, leaf_y + 0.2], color="#455A64", lw=2.5, zorder=4)
    # Leaf sensor grid tilted at 45 degrees
    leaf_poly = Polygon([
        [leaf_x - 0.3, leaf_y + 0.4],
        [leaf_x + 0.4, leaf_y + 0.1],
        [leaf_x + 0.35, leaf_y - 0.05],
        [leaf_x - 0.35, leaf_y + 0.25]
    ], fc="#2E7D32", ec="#1B5E20", lw=1.5, zorder=5)
    ax.add_patch(leaf_poly)
    # Interdigitated grid lines
    ax.plot([leaf_x - 0.1, leaf_x + 0.2], [leaf_y + 0.3, leaf_y + 0.15], color="#A5D6A7", lw=1, zorder=6)
    # Foliage graphic around leaf sensor
    ax.add_patch(patches.Ellipse((leaf_x + 0.6, leaf_y + 0.1), 0.7, 0.4, angle=30, fc="#81C784", ec="#388E3C", alpha=0.7, zorder=3))
    ax.add_patch(patches.Ellipse((leaf_x - 0.2, leaf_y - 0.3), 0.8, 0.5, angle=-20, fc="#66BB6A", ec="#2E7D32", alpha=0.7, zorder=3))
    # Leaf callout
    ax.annotate("[3] IP68 Dielectric Leaf Wetness Sensor\n   • Interface: RS485 Modbus-RTU via MAX485\n   • Positioning: Upper Active Foliar Canopy (+0.8 to +1.0 m)\n   • Angle: 30°–45° Inclination matching crop leaves\n   • Role: Real-time Leaf Wetness Duration (LWD >= 10h)",
                xy=(leaf_x + 0.3, leaf_y + 0.2), xytext=(8.5, 6.8),
                arrowprops=dict(arrowstyle="-|>", color="#2E7D32", lw=1.8),
                bbox=dict(boxstyle="round,pad=0.4", fc="#E8F5E9", ec="#2E7D32", lw=1.2),
                fontsize=8.5, color="#1B5E20", fontweight="bold")

    # 4. Central Weatherproof Enclosure (IP66 Box @ ~0.7m, y = 3.8)
    enc_w, enc_h = 1.4, 1.8
    enc_x, enc_y = mast_x - enc_w/2, ground_y + 2.0
    # U-bolt mounting brackets
    ax.add_patch(Rectangle((enc_x - 0.15, enc_y + 0.3), enc_w + 0.3, 0.15, fc="#37474F", ec="#263238", zorder=3))
    ax.add_patch(Rectangle((enc_x - 0.15, enc_y + 1.3), enc_w + 0.3, 0.15, fc="#37474F", ec="#263238", zorder=3))
    # Outer Polycarbonate Enclosure
    ax.add_patch(FancyBboxPatch((enc_x, enc_y), enc_w, enc_h, boxstyle="round,pad=0.08", fc="#ECEFF1", ec="#37474F", lw=2, zorder=4))
    # Transparent / Inner window
    ax.add_patch(Rectangle((enc_x + 0.15, enc_y + 0.2), enc_w - 0.3, enc_h - 0.4, fc="#CFD8DC", ec="#90A4AE", lw=1, zorder=5))
    ax.text(mast_x, enc_y + 1.2, "SolanaWatch IoT Node\n[IP65/IP66 Enclosure]", ha="center", va="center", fontsize=7.5, fontweight="bold", color="#263238", zorder=6)
    ax.text(mast_x, enc_y + 0.7, "• ESP32 MCU + Custom PCB\n• 12V MPPT Controller\n• 12.8V 12Ah LiFePO4 Pack\n• MicroSD Edge FIFO Buffer", ha="center", va="center", fontsize=6.5, color="#37474F", zorder=6)

    # PG7/PG9 Cable Glands at bottom
    gland_positions = [mast_x - 0.4, mast_x - 0.15, mast_x + 0.15, mast_x + 0.4]
    for gx in gland_positions:
        ax.add_patch(Rectangle((gx - 0.06, enc_y - 0.18), 0.12, 0.18, fc="#263238", ec="#000000", lw=1, zorder=5))

    # Enclosure Callout
    ax.annotate("[4] IP65/IP66 Weatherproof Enclosure (200×150×100 mm)\n   • Positioning: Middle of Mast (+0.6 m to +0.8 m)\n   • Components: ESP32 MCU, MPPT Charger, LiFePO4 Battery, MicroSD\n   • Weatherproofing: Silicone gasket, PG7/PG9 glands, Silica desiccant\n   • Role: Autonomous Control, Power Regulation & Cloud Sync",
                xy=(enc_x, enc_y + 0.9), xytext=(-0.8, 3.8),
                arrowprops=dict(arrowstyle="-|>", color="#37474F", lw=1.8),
                bbox=dict(boxstyle="round,pad=0.4", fc="#F5F5F5", ec="#424242", lw=1.2),
                fontsize=8.5, color="#212121", fontweight="bold")

    # Cable Routing Lines with Drip Loops
    # Solar Cable: PV -> Enclosure
    ax.plot([pv_cx - 0.1, mast_x - 0.18, mast_x - 0.18, mast_x - 0.4, mast_x - 0.4],
            [pv_cy - 0.2, pv_cy - 0.5, enc_y + 0.5, enc_y - 0.3, enc_y - 0.18], color="#F57F17", lw=1.5, ls="--", zorder=4)
    # Stevenson Cable: Shield -> Enclosure
    ax.plot([stev_x, stev_x + 0.3, mast_x - 0.15, mast_x - 0.15],
            [stev_y, enc_y + 0.2, enc_y - 0.3, enc_y - 0.18], color="#0288D1", lw=1.5, ls="--", zorder=4)
    # Leaf Cable: Sensor -> Enclosure
    ax.plot([leaf_x - 0.2, leaf_x - 0.4, mast_x + 0.15, mast_x + 0.15],
            [leaf_y, enc_y + 0.2, enc_y - 0.3, enc_y - 0.18], color="#2E7D32", lw=1.5, ls="--", zorder=4)

    # 5. Soil Probes Assembly (Subsurface @ 10cm depth, y = 0.0)
    # Soil conduit running down mast
    ax.plot([mast_x + 0.4, mast_x + 0.4, mast_x + 0.6, mast_x + 0.6],
            [enc_y - 0.18, ground_y - 0.2, ground_y - 0.5, -0.6], color="#3E2723", lw=2, zorder=3)
    
    # 5a. Capacitive Soil Moisture Sensor v1.2
    sm_x, sm_y = mast_x - 1.2, -0.8
    ax.plot([mast_x + 0.4, sm_x, sm_x], [ground_y - 0.2, ground_y - 0.3, sm_y + 0.4], color="#5D4037", lw=1.5, zorder=3)
    # Capacitive Sensor Board
    sm_poly = Polygon([
        [sm_x - 0.18, sm_y + 0.4],
        [sm_x + 0.18, sm_y + 0.4],
        [sm_x + 0.18, sm_y - 0.5],
        [sm_x, sm_y - 0.8],
        [sm_x - 0.18, sm_y - 0.5]
    ], fc="#2E7D32", ec="#1B5E20", lw=1.2, zorder=4)
    ax.add_patch(sm_poly)
    ax.plot([sm_x - 0.15, sm_x + 0.15], [sm_y + 0.1, sm_y + 0.1], color="#FFFFFF", lw=1.5, zorder=5) # Max immersion line
    ax.text(sm_x, sm_y, "Capacitive\nMoisture", ha="center", va="center", fontsize=5.5, color="#FFFFFF", fontweight="bold")

    # 5b. DS18B20 Soil Temperature Probe
    st_x, st_y = mast_x + 1.2, -0.8
    ax.plot([mast_x + 0.6, st_x, st_x], [-0.6, -0.6, st_y + 0.4], color="#455A64", lw=1.5, zorder=3)
    # Stainless Steel probe
    ax.add_patch(FancyBboxPatch((st_x - 0.12, st_y - 0.6), 0.24, 0.9, boxstyle="round,pad=0.03", fc="#B0BEC5", ec="#37474F", lw=1.5, zorder=4))
    ax.text(st_x, st_y - 0.15, "DS18B20\nProbe", ha="center", va="center", fontsize=5.5, color="#263238", fontweight="bold")

    # Soil Sensor Callout Left (Capacitive Moisture)
    ax.annotate("[5] Capacitive Soil Moisture Sensor v1.2\n   • Sensor Model: SKU SEN0193 (Corrosion-Proof)\n   • Positioning: Soil Subsurface @ 10 cm Depth\n   • Location: 15–20 cm away from crop base\n   • Role: Volumetric Water Content (VWC %) for Bacterial Wilt",
                xy=(sm_x - 0.18, sm_y), xytext=(-0.8, -2.4),
                arrowprops=dict(arrowstyle="-|>", color="#2E7D32", lw=1.8),
                bbox=dict(boxstyle="round,pad=0.4", fc="#E8F5E9", ec="#2E7D32", lw=1.2),
                fontsize=8.5, color="#1B5E20", fontweight="bold")

    # Soil Sensor Callout Right (DS18B20 Soil Temp)
    ax.annotate("[6] DS18B20 Stainless Steel Soil Temp Probe\n   • Sensor Model: Waterproof 304 SS (1-Wire Bus)\n   • Positioning: Root-Zone Core @ 10 cm Depth\n   • Proximity: Adjacent to Moisture Probe\n   • Role: Root-Zone Hydrothermal Risk Index (R_BW)",
                xy=(st_x + 0.12, st_y), xytext=(7.5, -2.4),
                arrowprops=dict(arrowstyle="-|>", color="#D84315", lw=1.8),
                bbox=dict(boxstyle="round,pad=0.4", fc="#FBE9E7", ec="#D84315", lw=1.2),
                fontsize=8.5, color="#BF360C", fontweight="bold")

    # Title Block Header
    plt.title("Figure 7. SolanaWatch Edge Node: Complete Physical Prototype Layout & Component Positioning", fontsize=12, fontweight="bold", pad=15, y=0.98)
    
    # Save diagram
    plt.tight_layout()
    out_path = os.path.join(fig_dir, "figure7_prototype_physical_layout.png")
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Created: {out_path}")

def create_enclosure_internal_diagram():
    fig, ax = plt.subplots(figsize=(13, 9), dpi=300)
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 9)
    ax.axis('off')

    # Background canvas
    bg = Rectangle((0, 0), 13, 9, fc="#F8FAFC", ec="none")
    ax.add_patch(bg)

    # 1. Main Enclosure Outline (200 x 150 mm internal base)
    box_x, box_y, box_w, box_h = 1.0, 1.2, 11.0, 7.0
    # Outer Polycarbonate Flange with mounting ears
    ax.add_patch(FancyBboxPatch((box_x - 0.4, box_y - 0.4), box_w + 0.8, box_h + 0.8, boxstyle="round,pad=0.15", fc="#B0BEC5", ec="#37474F", lw=2.5))
    # Silicone Gasket Channel
    ax.add_patch(FancyBboxPatch((box_x - 0.1, box_y - 0.1), box_w + 0.2, box_h + 0.2, boxstyle="round,pad=0.08", fc="#CFD8DC", ec="#0288D1", lw=1.8, ls="--"))
    # Interior Cavity
    ax.add_patch(FancyBboxPatch((box_x, box_y), box_w, box_h, boxstyle="round,pad=0.05", fc="#ECEFF1", ec="#455A64", lw=2))

    # Corner mounting standoffs
    for cx, cy in [(box_x + 0.4, box_y + 0.4), (box_x + box_w - 0.4, box_y + 0.4), (box_x + 0.4, box_y + box_h - 0.4), (box_x + box_w - 0.4, box_y + box_h - 0.4)]:
        ax.add_patch(Circle((cx, cy), 0.22, fc="#78909C", ec="#263238", lw=1.5))
        ax.plot([cx - 0.1, cx + 0.1], [cy, cy], color="#ECEFF1", lw=1.5)
        ax.plot([cx, cx], [cy - 0.1, cy + 0.1], color="#ECEFF1", lw=1.5)

    # TOP SECTION: 12V 10A MPPT Solar Charge Controller
    mppt_x, mppt_y, mppt_w, mppt_h = box_x + 0.6, box_y + 4.6, 5.0, 2.0
    ax.add_patch(FancyBboxPatch((mppt_x, mppt_y), mppt_w, mppt_h, boxstyle="round,pad=0.05", fc="#1E88E5", ec="#0D47A1", lw=1.8))
    ax.text(mppt_x + mppt_w/2, mppt_y + 1.6, "12V 10A IP67 MPPT Solar Charge Controller", ha="center", va="center", color="#FFFFFF", fontweight="bold", fontsize=9)
    ax.text(mppt_x + mppt_w/2, mppt_y + 1.1, "• Multi-stage LiFePO4 Charging Profile (14.4V Bulk / 13.6V Float)\n• High Tracking Efficiency (>= 98% MPPT)\n• Terminals: Solar PV In (+/-), Battery (+/-), 12V Load Out (+/-)", ha="center", va="center", color="#E3F2FD", fontsize=7.2)
    # Screw Terminals on MPPT
    for i, t_name in enumerate(["PV+", "PV-", "BAT+", "BAT-", "LOAD+", "LOAD-"]):
        tx = mppt_x + 0.5 + (i * 0.75)
        ax.add_patch(Rectangle((tx - 0.25, mppt_y + 0.1), 0.5, 0.4, fc="#37474F", ec="#212121", lw=1))
        ax.text(tx, mppt_y + 0.3, t_name, ha="center", va="center", color="#FFFFFF", fontsize=6, fontweight="bold")

    # TOP RIGHT SECTION: DC-DC Step-Down Buck Converters (12V -> 5V & 12V -> 3.3V)
    buck_x, buck_y, buck_w, buck_h = box_x + 6.0, box_y + 4.6, 4.4, 2.0
    ax.add_patch(FancyBboxPatch((buck_x, buck_y), buck_w, buck_h, boxstyle="round,pad=0.05", fc="#455A64", ec="#263238", lw=1.8))
    ax.text(buck_x + buck_w/2, buck_y + 1.6, "Dual DC-DC Step-Down Buck Regulators", ha="center", va="center", color="#FFFFFF", fontweight="bold", fontsize=9)
    # Buck 1 (5V)
    ax.add_patch(Rectangle((buck_x + 0.3, buck_y + 0.2), 1.7, 1.1, fc="#546E7A", ec="#263238", lw=1.2))
    ax.text(buck_x + 1.15, buck_y + 0.9, "LM2596 (5.0V 3A)", ha="center", va="center", color="#FFFFFF", fontsize=7, fontweight="bold")
    ax.text(buck_x + 1.15, buck_y + 0.5, "ESP32 VIN Rail", ha="center", va="center", color="#B0BEC5", fontsize=6.5)
    # Buck 2 (3.3V)
    ax.add_patch(Rectangle((buck_x + 2.4, buck_y + 0.2), 1.7, 1.1, fc="#546E7A", ec="#263238", lw=1.2))
    ax.text(buck_x + 3.25, buck_y + 0.9, "MP1584 (3.3V 2A)", ha="center", va="center", color="#FFFFFF", fontsize=7, fontweight="bold")
    ax.text(buck_x + 3.25, buck_y + 0.5, "Sensors & Bus Rail", ha="center", va="center", color="#B0BEC5", fontsize=6.5)

    # MIDDLE LEFT: Custom FR-4 Proto-Shield PCB (ESP32 DevKit V1 + Buses)
    pcb_x, pcb_y, pcb_w, pcb_h = box_x + 0.6, box_y + 1.6, 5.8, 2.7
    ax.add_patch(FancyBboxPatch((pcb_x, pcb_y), pcb_w, pcb_h, boxstyle="round,pad=0.05", fc="#1B5E20", ec="#0A3B10", lw=2))
    ax.text(pcb_x + pcb_w/2, pcb_y + 2.45, "Custom FR-4 Prototype PCB Shield (SolanaWatch Motherboard)", ha="center", va="center", color="#FFFFFF", fontweight="bold", fontsize=8.5)

    # ESP32 DevKit V1 module on PCB
    esp_x, esp_y, esp_w, esp_h = pcb_x + 0.3, pcb_y + 0.3, 2.6, 1.8
    ax.add_patch(Rectangle((esp_x, esp_y), esp_w, esp_h, fc="#212121", ec="#616161", lw=1.2))
    # Metal RF can on ESP32
    ax.add_patch(Rectangle((esp_x + 0.4, esp_y + 0.7), 1.8, 0.9, fc="#9E9E9E", ec="#E0E0E0", lw=1))
    ax.text(esp_x + 1.3, esp_y + 1.15, "ESP32-WROOM-32", ha="center", va="center", color="#212121", fontsize=6.5, fontweight="bold")
    ax.text(esp_x + 1.3, esp_y + 0.4, "Dual-Core 240MHz\n2.4GHz Wi-Fi Antenna", ha="center", va="center", color="#FFFFFF", fontsize=5.8)

    # MAX485 Transceiver Module on PCB
    max_x, max_y, max_w, max_h = pcb_x + 3.1, pcb_y + 1.2, 2.4, 0.9
    ax.add_patch(Rectangle((max_x, max_y), max_w, max_h, fc="#37474F", ec="#78909C", lw=1))
    ax.text(max_x + max_w/2, max_y + 0.6, "MAX485 Module", ha="center", va="center", color="#FFFFFF", fontsize=6.8, fontweight="bold")
    ax.text(max_x + max_w/2, max_y + 0.25, "UART2 (GPIO 16/17/22)", ha="center", va="center", color="#B0BEC5", fontsize=5.8)

    # MicroSD SPI Module on PCB
    sd_x, sd_y, sd_w, sd_h = pcb_x + 3.1, pcb_y + 0.2, 2.4, 0.85
    ax.add_patch(Rectangle((sd_x, sd_y), sd_w, sd_h, fc="#424242", ec="#78909C", lw=1))
    ax.text(sd_x + sd_w/2, sd_y + 0.55, "SPI MicroSD Module", ha="center", va="center", color="#FFFFFF", fontsize=6.8, fontweight="bold")
    ax.text(sd_x + sd_w/2, sd_y + 0.25, "16GB FAT32 Card Buffer", ha="center", va="center", color="#FFD54F", fontsize=5.8)

    # MIDDLE RIGHT: 12.8V 12Ah LiFePO4 Battery Pack
    bat_x, bat_y, bat_w, bat_h = box_x + 6.8, box_y + 1.6, 3.6, 2.7
    ax.add_patch(FancyBboxPatch((bat_x, bat_y), bat_w, bat_h, boxstyle="round,pad=0.05", fc="#2E7D32", ec="#1B5E20", lw=2))
    ax.text(bat_x + bat_w/2, bat_y + 2.3, "12.8V 12Ah LiFePO4 Pack", ha="center", va="center", color="#FFFFFF", fontweight="bold", fontsize=9)
    ax.text(bat_x + bat_w/2, bat_y + 1.5, "• 153.6 Wh Energy Capacity\n• Integrated 15A BMS Circuit\n• 47.0 Days Zero-Sunlight Autonomy\n• Overcharge & Discharge Protection", ha="center", va="center", color="#C8E6C9", fontsize=6.8)
    # Battery Terminals
    ax.add_patch(Circle((bat_x + 0.8, bat_y + 0.5), 0.2, fc="#D32F2F", ec="#B71C1C", lw=1)) # Positive
    ax.text(bat_x + 0.8, bat_y + 0.5, "+", ha="center", va="center", color="#FFFFFF", fontsize=8, fontweight="bold")
    ax.add_patch(Circle((bat_x + 2.8, bat_y + 0.5), 0.2, fc="#212121", ec="#000000", lw=1)) # Negative
    ax.text(bat_x + 2.8, bat_y + 0.5, "-", ha="center", va="center", color="#FFFFFF", fontsize=8, fontweight="bold")

    # BOTTOM RIGHT: Silica Gel Desiccant Pack
    des_x, des_y, des_w, des_h = box_x + 6.8, box_y + 0.3, 3.6, 1.0
    ax.add_patch(FancyBboxPatch((des_x, des_y), des_w, des_h, boxstyle="round,pad=0.04", fc="#FFF9C4", ec="#FBC02D", lw=1.2))
    ax.text(des_x + des_w/2, des_y + 0.65, "SILICA GEL DESICCANT POUCH", ha="center", va="center", color="#F57F17", fontweight="bold", fontsize=7.5)
    ax.text(des_x + des_w/2, des_y + 0.3, "Absorbs internal moisture & prevents condensation", ha="center", va="center", color="#795548", fontsize=6.2)

    # BOTTOM CABLE GLANDS & WIRING ROUTING
    glands = [
        (box_x + 1.8, "PG9 (Solar PV In)"),
        (box_x + 3.2, "PG7 (DHT22 / Stevenson)"),
        (box_x + 4.6, "PG7 (RS485 Leaf Sensor)"),
        (box_x + 6.0, "PG7 (Soil Moisture & Temp)")
    ]
    for gx, g_label in glands:
        ax.add_patch(Rectangle((gx - 0.3, box_y - 0.6), 0.6, 0.6, fc="#263238", ec="#000000", lw=1.5))
        ax.text(gx, box_y - 0.9, g_label, ha="center", va="top", fontsize=6.8, fontweight="bold", color="#263238")

    # Title Header
    plt.title("Figure 8. SolanaWatch Weatherproof Enclosure (IP66): Internal Component & PCB Shield Layout", fontsize=12, fontweight="bold", pad=15, y=0.98)
    
    plt.tight_layout()
    out_path = os.path.join(fig_dir, "figure8_enclosure_internal_layout.png")
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Created: {out_path}")

if __name__ == "__main__":
    create_physical_layout_diagram()
    create_enclosure_internal_diagram()
