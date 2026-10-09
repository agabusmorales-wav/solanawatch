import os
import sys
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

PROJECT_DIR = r"C:\Users\agabu\Downloads\CODE PROJECTS\SOLANAWATCH"
FIGURES_DIR = os.path.join(PROJECT_DIR, "figures")
PPTX_PATH = os.path.join(PROJECT_DIR, "paperwork", "reports-and-presentations", "SolanaWatch_Weekly_Progress_Report.pptx")

# High-Contrast White Background Palette
C_WHITE_BG = RGBColor(255, 255, 255)       # #FFFFFF
C_CARD_BG = RGBColor(248, 250, 252)        # #F8FAFC
C_CARD_BORDER = RGBColor(226, 232, 240)    # #E2E8F0
C_TEXT_MAIN = RGBColor(15, 23, 42)         # #0F172A (Deep Charcoal / Black)
C_TEXT_SUB = RGBColor(71, 85, 105)         # #475569 (Slate Gray)
C_TEXT_MUTED = RGBColor(100, 116, 139)     # #64748B

# Accents
C_PRIMARY_BLUE = RGBColor(2, 132, 199)     # #0284C7
C_ACCENT_GREEN = RGBColor(22, 163, 74)     # #16A34A
C_ACCENT_AMBER = RGBColor(217, 119, 6)     # #D97706
C_BADGE_BG_GREEN = RGBColor(220, 252, 231) # #DCFCE7
C_BADGE_BG_BLUE = RGBColor(224, 242, 254)  # #E0F2FE

def create_2_slide_white_pptx():
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    def set_white_bg(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = C_WHITE_BG
        bg.line.fill.background()
        return bg

    # ==========================================
    # SLIDE 1: EXECUTIVE PROGRESS REPORT
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    set_white_bg(s1)

    # Super Header
    tb_sup = s1.shapes.add_textbox(Inches(0.8), Inches(0.35), Inches(10.0), Inches(0.35))
    tf_sup = tb_sup.text_frame
    p = tf_sup.paragraphs[0]
    p.text = "SOLANAWATCH • IOT-BASED DISEASE EARLY WARNING SYSTEM"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_PRIMARY_BLUE
    p.font.name = "Arial"

    # Main Title Header
    tb_t = s1.shapes.add_textbox(Inches(0.8), Inches(0.68), Inches(9.2), Inches(0.95))
    tf_t = tb_t.text_frame
    tf_t.word_wrap = True
    p = tf_t.paragraphs[0]
    p.text = "SOLANAWATCH  |  WEEKLY PROGRESS REPORT"
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = C_TEXT_MAIN
    p.font.name = "Arial"

    p2 = tf_t.add_paragraph()
    p2.text = "SURFER BROS  •  Group 1 (3ITC)  •  Special Term, A/Y 2025–2026"
    p2.font.size = Pt(14)
    p2.font.bold = True
    p2.font.color.rgb = C_TEXT_SUB
    p2.font.name = "Arial"

    # Top Right Status Badge
    badge = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(10.5), Inches(0.65), Inches(2.0), Inches(0.55))
    badge.fill.solid()
    badge.fill.fore_color.rgb = C_BADGE_BG_GREEN
    badge.line.color.rgb = C_ACCENT_GREEN
    badge.line.width = Pt(1.5)
    tf_b = badge.text_frame
    p_b = tf_b.paragraphs[0]
    p_b.text = "● STATUS: ON TRACK"
    p_b.alignment = PP_ALIGN.CENTER
    p_b.font.size = Pt(12)
    p_b.font.bold = True
    p_b.font.color.rgb = C_ACCENT_GREEN
    p_b.font.name = "Arial"

    # Subtle Divider Line
    line = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.68), Inches(11.733), Inches(0.02))
    line.fill.solid()
    line.fill.fore_color.rgb = C_CARD_BORDER
    line.line.fill.background()

    # 3 Main Column Cards
    col_w = Inches(3.72)
    gap = Inches(0.28)
    top_pos = Inches(1.85)
    card_h = Inches(4.75)

    cards_data = [
        {
            "title": "CURRENT TASKS:",
            "accent": C_PRIMARY_BLUE,
            "badge_bg": C_BADGE_BG_BLUE,
            "items": [
                ("100% Complete Materials Procurement", "Acquired full ₱7,208 Bill of Materials with all components on-hand: ESP32 DevKit V1, DHT22 with Stevenson shield, dual DS18B20 soil temp probes, Capacitive v1.2 moisture sensor, industrial IP68 RS485 dielectric leaf wetness grid, 20W solar PV, MPPT controller, 12.8V LiFePO4 battery (47-day autonomy), and IP66 enclosure."),
                ("Physical Circuit Bring-Up", "Started breadboard layout, pin mapping, and isolated dual 5V/3.3V power rails. Verified initial 1-Wire, ADC, and RS485 communication lines."),
                ("Interactive UI Dashboards", "Completed functional PC Web Dashboard and iOS mobile views featuring live microclimate gauges, disease risk calculation, and actionable cultural alerts."),
                ("Ethics Clearance Accomplished", "Completed UST Ethics Review Form 4.2 (Protocol Assessment) and Form 7.2 (Application for Ethics Review) for institutional compliance.")
            ]
        },
        {
            "title": "EXPECTED CHALLENGES:",
            "accent": C_ACCENT_AMBER,
            "badge_bg": RGBColor(254, 243, 199),
            "items": [
                ("Mixed-Bus Signal Integrity", "Concurrent 1-Wire, analog ADC, and RS485 lines can cause electrical noise. Separated 5V logic and 3.3V sensor rails via dual buck converters; added 4.7kΩ pull-ups and line filters."),
                ("RS485 Modbus-RTU Timing", "Potential timing contention between MAX485 switching and ESP32 Wi-Fi routines. Dedicated ESP32 Core 1 FreeRTOS task to sensor polling, isolating it from Core 0 network tasks."),
                ("Two-Point Soil Calibration", "ADC variance across Philippine clay-loam Solanaceae soils. Calibrating in controlled oven-dry (0% VWC) and saturated (100% VWC) soil samples.")
            ]
        },
        {
            "title": "PLAN FOR NEXT WEEK:",
            "accent": C_ACCENT_GREEN,
            "badge_bg": C_BADGE_BG_GREEN,
            "items": [
                ("Complete Circuit Assembly", "Finalize physical breadboard wiring harness connecting all 5 sensors to ESP32 and test power delivery from the 12.8V LiFePO4 battery pack."),
                ("FreeRTOS Firmware Routines", "Implement multi-sensor sampling loops and offline FIFO MicroSD buffer (telemetry_buffer.jsonl) for zero-loss edge storage."),
                ("Cloud Ingestion & Risk Engine", "Connect Node.js/Express REST API to Turso libSQL cloud database and link Wallin SV and Hydrothermal risk models."),
                ("Sensor Bench Calibration", "Execute ice-point (0.0°C) and NaCl humidity chamber (75.3% RH) calibration tests.")
            ]
        }
    ]

    for i, cdata in enumerate(cards_data):
        left_pos = Inches(0.8) + i * (col_w + gap)
        
        # Outer Card
        card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_pos, top_pos, col_w, card_h)
        card.fill.solid()
        card.fill.fore_color.rgb = C_CARD_BG
        card.line.color.rgb = cdata["accent"]
        card.line.width = Pt(2.0)

        # Header Box inside card
        header_box = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_pos + Inches(0.18), top_pos + Inches(0.18), col_w - Inches(0.36), Inches(0.55))
        header_box.fill.solid()
        header_box.fill.fore_color.rgb = cdata["badge_bg"]
        header_box.line.color.rgb = cdata["accent"]
        header_box.line.width = Pt(1.5)
        tf_h = header_box.text_frame
        p_h = tf_h.paragraphs[0]
        p_h.text = cdata["title"]
        p_h.alignment = PP_ALIGN.CENTER
        p_h.font.size = Pt(14)
        p_h.font.bold = True
        p_h.font.color.rgb = cdata["accent"]
        p_h.font.name = "Arial"

        # Content Text Box
        tb = s1.shapes.add_textbox(left_pos + Inches(0.18), top_pos + Inches(0.8), col_w - Inches(0.36), card_h - Inches(0.9))
        tf = tb.text_frame
        tf.word_wrap = True
        for j, (head, desc) in enumerate(cdata["items"]):
            p = tf.paragraphs[0] if j == 0 else tf.add_paragraph()
            p.text = f"• {head}"
            p.font.size = Pt(11.5)
            p.font.bold = True
            p.font.color.rgb = C_TEXT_MAIN
            p.font.name = "Arial"
            p.space_after = Pt(1)

            p_desc = tf.add_paragraph()
            p_desc.text = desc
            p_desc.font.size = Pt(9.8)
            p_desc.font.color.rgb = C_TEXT_SUB
            p_desc.font.name = "Arial"
            p_desc.space_after = Pt(7)

    # Footer Team Pill
    footer_box = s1.shapes.add_textbox(Inches(0.8), Inches(6.75), Inches(11.733), Inches(0.45))
    tf_f = footer_box.text_frame
    p_f = tf_f.paragraphs[0]
    p_f.text = "Team Members: Morales, Simeon Agabus S. • Rapada, Raven M. • Hernandez, Andrei S. • Eugenio, Vince Angelo  |  Adviser: Prof. Eugenia R. Zhuo, DIT"
    p_f.font.size = Pt(11.5)
    p_f.font.bold = True
    p_f.font.color.rgb = C_TEXT_MUTED
    p_f.font.name = "Arial"

    # ==========================================
    # SLIDE 2: HARDWARE MATERIALS & SOFTWARE SHOWCASE
    # ==========================================
    s2 = prs.slides.add_slide(blank_layout)
    set_white_bg(s2)

    # Super Header
    tb_sup2 = s2.shapes.add_textbox(Inches(0.8), Inches(0.35), Inches(10.0), Inches(0.35))
    tf_sup2 = tb_sup2.text_frame
    p = tf_sup2.paragraphs[0]
    p.text = "SOLANAWATCH • HARDWARE SHOWCASE & SYSTEM HIGHLIGHTS"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_PRIMARY_BLUE
    p.font.name = "Arial"

    # Title Header
    tb_t2 = s2.shapes.add_textbox(Inches(0.8), Inches(0.68), Inches(9.2), Inches(0.65))
    tf_t2 = tb_t2.text_frame
    p = tf_t2.paragraphs[0]
    p.text = "Hardware Materials Inventory & Working Application"
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = C_TEXT_MAIN
    p.font.name = "Arial"

    # Top Right Badge
    badge2 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(10.2), Inches(0.6), Inches(2.3), Inches(0.55))
    badge2.fill.solid()
    badge2.fill.fore_color.rgb = C_BADGE_BG_GREEN
    badge2.line.color.rgb = C_ACCENT_GREEN
    badge2.line.width = Pt(1.5)
    tf_b2 = badge2.text_frame
    p_b2 = tf_b2.paragraphs[0]
    p_b2.text = "● 100% MATERIALS IN-HAND"
    p_b2.alignment = PP_ALIGN.CENTER
    p_b2.font.size = Pt(11.5)
    p_b2.font.bold = True
    p_b2.font.color.rgb = C_ACCENT_GREEN
    p_b2.font.name = "Arial"

    # Divider Line
    line2 = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.4), Inches(11.733), Inches(0.02))
    line2.fill.solid()
    line2.fill.fore_color.rgb = C_CARD_BORDER
    line2.line.fill.background()

    # Left: Web Dashboard Mockup Image Embed
    mockup_img_path = os.path.join(FIGURES_DIR, "web_dashboard_mockup.jpg")
    if not os.path.exists(mockup_img_path):
        mockup_img_path = os.path.join(FIGURES_DIR, "web_mockup_minimal.jpg")
    if os.path.exists(mockup_img_path):
        s2.shapes.add_picture(mockup_img_path, Inches(0.8), Inches(1.6), Inches(7.1), Inches(4.9))

    # Right: Structured Technical Information Box
    right_card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.15), Inches(1.6), Inches(4.383), Inches(4.9))
    right_card.fill.solid()
    right_card.fill.fore_color.rgb = C_CARD_BG
    right_card.line.color.rgb = C_CARD_BORDER
    right_card.line.width = Pt(1.5)

    tb_r = s2.shapes.add_textbox(Inches(8.35), Inches(1.72), Inches(3.983), Inches(4.65))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True

    p = tf_r.paragraphs[0]
    p.text = "Materials Inventory & System Highlights"
    p.font.size = Pt(15.5)
    p.font.bold = True
    p.font.color.rgb = C_PRIMARY_BLUE
    p.font.name = "Arial"
    p.space_after = Pt(6)

    points = [
        ("100% Complete Hardware Materials", "All components on-hand: ESP32 MCU, DHT22 in Stevenson shield, DS18B20 soil temp, Capacitive v1.2, IP68 RS485 leaf wetness grid, 20W PV, MPPT controller, and 12.8V LiFePO4 battery (47-day autonomy)."),
        ("Physical Circuit Bring-Up Initiated", "Breadboard layout, pin mapping, isolated 5V & 3.3V power rails, and preliminary sensor communication checks actively progressing."),
        ("Working Decision Support Dashboards", "Functional PC Web Dashboard (desktop.html) and iOS mobile view (index.html) featuring live 5-sensor gauges and disease alerts."),
        ("Pre-Symptomatic Disease Risk Engine", "Embedded algorithms for Late Blight (Wallin Severity Values @ LWD >= 10h) and Bacterial Wilt (Hydrothermal Soil Risk Index R_BW)."),
        ("Institutional Ethics Clearance Complete", "UST Form 4.2 & Form 7.2 accomplished for research protocol compliance and participant safety.")
    ]

    for h, desc in points:
        p = tf_r.add_paragraph()
        p.text = f"✔ {h}"
        p.font.size = Pt(11.5)
        p.font.bold = True
        p.font.color.rgb = C_TEXT_MAIN
        p.font.name = "Arial"
        p.space_after = Pt(1)

        p2 = tf_r.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = C_TEXT_SUB
        p2.font.name = "Arial"
        p2.space_after = Pt(6)

    # Footer
    footer_box2 = s2.shapes.add_textbox(Inches(0.8), Inches(6.75), Inches(11.733), Inches(0.45))
    tf_f2 = footer_box2.text_frame
    p_f2 = tf_f2.paragraphs[0]
    p_f2.text = "SolanaWatch: An IoT-Based Disease Early Warning System for Soil-Grown Solanaceae Crops  |  Interactive Prototype: SolanaWatch_PC_Dashboard.html"
    p_f2.font.size = Pt(11.5)
    p_f2.font.bold = True
    p_f2.font.color.rgb = C_TEXT_MUTED
    p_f2.font.name = "Arial"

    # Save presentation
    prs.save(PPTX_PATH)
    print(f"[SUCCESS] White background 2-Slide PPTX saved to: {PPTX_PATH}")

if __name__ == "__main__":
    create_2_slide_white_pptx()
