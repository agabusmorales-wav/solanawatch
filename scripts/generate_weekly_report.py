import os
import sys
import subprocess
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

PROJECT_DIR = r"C:\Users\agabu\Downloads\CODE PROJECTS\SOLANAWATCH"
FIGURES_DIR = os.path.join(PROJECT_DIR, "figures")
REPORT_DIR = os.path.join(PROJECT_DIR, "paperwork", "reports-and-presentations")
PPTX_PATH = os.path.join(REPORT_DIR, "SolanaWatch_Weekly_Progress_Report.pptx")
HTML_SLIDES_PATH = os.path.join(REPORT_DIR, "SolanaWatch_Weekly_Progress_Report_Slides.html")
PDF_PATH = os.path.join(REPORT_DIR, "SolanaWatch_Weekly_Progress_Report.pdf")
MD_REPORT_PATH = os.path.join(REPORT_DIR, "WEEKLY_PROGRESS_REPORT.md")

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

def generate_pptx():
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
    print(f"[SUCCESS] 2-Slide PPTX saved to: {PPTX_PATH}")

def generate_html_and_pdf():
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>SolanaWatch - Weekly Progress Report (Week of Sept 24, 2026)</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap');

  @page {{
    size: 1920px 1080px;
    margin: 0;
  }}

  * {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }}

  body {{
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background-color: #ffffff;
    color: #0f172a;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }}

  .slide {{
    width: 1920px;
    height: 1080px;
    page-break-after: always;
    page-break-inside: avoid;
    position: relative;
    overflow: hidden;
    background: #ffffff;
    padding: 55px 75px;
    display: flex;
    flex-direction: column;
  }}

  /* Slide Header */
  .slide-header {{
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 24px;
    border-bottom: 2px solid #e2e8f0;
    padding-bottom: 18px;
  }}
  .header-left .category-pill {{
    display: inline-flex;
    align-items: center;
    gap: 8px;
    font-size: 14px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #0284c7;
    margin-bottom: 4px;
  }}
  .header-left .category-pill::before {{
    content: '';
    display: inline-block;
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: #0284c7;
  }}
  .header-left h1 {{
    font-size: 36px;
    font-weight: 800;
    color: #0f172a;
    letter-spacing: -0.5px;
  }}
  .header-left p {{
    font-size: 16px;
    font-weight: 600;
    color: #475569;
    margin-top: 4px;
  }}
  .header-badge {{
    background: #dcfce7;
    border: 2px solid #16a34a;
    padding: 10px 24px;
    border-radius: 30px;
    font-size: 15px;
    font-weight: 800;
    color: #15803d;
    letter-spacing: 0.5px;
  }}

  /* 3 Column Layout (Slide 1) */
  .three-col-grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 24px;
    flex: 1;
  }}
  .col-card {{
    background: #f8fafc;
    border: 2px solid #e2e8f0;
    border-radius: 18px;
    padding: 24px 22px;
    display: flex;
    flex-direction: column;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
  }}
  .col-card.blue {{ border-top: 6px solid #0284c7; }}
  .col-card.amber {{ border-top: 6px solid #d97706; }}
  .col-card.green {{ border-top: 6px solid #16a34a; }}

  .col-header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 16px;
    padding-bottom: 10px;
    border-bottom: 2px solid #e2e8f0;
  }}
  .col-title {{
    font-size: 20px;
    font-weight: 800;
    letter-spacing: 0.5px;
  }}
  .col-card.blue .col-title {{ color: #0284c7; }}
  .col-card.amber .col-title {{ color: #d97706; }}
  .col-card.green .col-title {{ color: #16a34a; }}

  .col-item {{
    margin-bottom: 14px;
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 14px 16px;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.02);
  }}
  .col-item:last-child {{
    margin-bottom: 0;
  }}
  .col-item h3 {{
    font-size: 16px;
    font-weight: 800;
    color: #0f172a;
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    gap: 8px;
  }}
  .col-item p {{
    font-size: 13.5px;
    font-weight: 500;
    color: #334155;
    line-height: 1.5;
  }}

  .slide-footer-bar {{
    margin-top: 16px;
    padding: 12px 24px;
    background: #f1f5f9;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 14px;
    font-weight: 600;
    color: #475569;
  }}

  /* 2 Column Layout (Slide 2) */
  .two-col-grid {{
    display: grid;
    grid-template-columns: 1.35fr 1fr;
    gap: 28px;
    flex: 1;
  }}
  .image-container {{
    border-radius: 18px;
    overflow: hidden;
    border: 2px solid #e2e8f0;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
    background: #ffffff;
    display: flex;
    align-items: center;
    justify-content: center;
  }}
  .image-container img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
  }}
  .info-panel {{
    background: #f8fafc;
    border: 2px solid #e2e8f0;
    border-radius: 18px;
    padding: 24px 24px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
  }}
  .info-title {{
    font-size: 22px;
    font-weight: 800;
    color: #0284c7;
    margin-bottom: 14px;
  }}
  .feature-list {{
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 10px;
  }}
  .feature-item {{
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 12px 16px;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.02);
  }}
  .feature-item h4 {{
    font-size: 15.5px;
    font-weight: 800;
    color: #0f172a;
    margin-bottom: 3px;
    display: flex;
    align-items: center;
    gap: 8px;
  }}
  .feature-item p {{
    font-size: 13px;
    font-weight: 500;
    color: #475569;
    line-height: 1.45;
  }}
</style>
</head>
<body>

  <!-- SLIDE 1: EXECUTIVE PROGRESS MATRIX -->
  <div class="slide">
    <div class="slide-header">
      <div class="header-left">
        <div class="category-pill">Weekly Progress Report</div>
        <h1>SOLANAWATCH  |  SURFER BROS</h1>
        <p>Group 1 (3ITC) • UST College of Information and Computing Sciences (CICS) • Special Term, A/Y 2025–2026</p>
      </div>
      <div class="header-badge">● STATUS: ON TRACK</div>
    </div>

    <div class="three-col-grid">
      <!-- Col 1: Current Tasks -->
      <div class="col-card blue">
        <div class="col-header">
          <div class="col-title">CURRENT TASKS</div>
          <span style="font-size: 13px; font-weight: 700; color: #0284c7; background: #e0f2fe; padding: 4px 10px; border-radius: 12px;">Active / Completed</span>
        </div>
        
        <div class="col-item">
          <h3>📦 100% Materials Procurement</h3>
          <p>Acquired full ₱7,208 BOM: ESP32 MCU, DHT22 with Stevenson shield, dual DS18B20 soil temp probes, Capacitive v1.2, industrial IP68 RS485 leaf wetness grid, 20W solar PV, MPPT controller, 12.8V LiFePO4 battery (47-day autonomy), and IP66 enclosure.</p>
        </div>

        <div class="col-item">
          <h3>⚡ Physical Circuit Bring-Up</h3>
          <p>Initiated breadboard layout, pin mapping, and isolated dual 5V/3.3V power rails. Verified initial 1-Wire, ADC, and RS485 communication lines.</p>
        </div>

        <div class="col-item">
          <h3>💻 Interactive UI Dashboards</h3>
          <p>Completed functional PC Web Dashboard (desktop.html) and iOS mobile view (index.html) featuring live microclimate gauges and disease risk calculation.</p>
        </div>

        <div class="col-item">
          <h3>📋 Ethics Clearance Complete</h3>
          <p>Accomplished and packaged UST Ethics Review Form 4.2 and Form 7.2 for research protocol compliance and participant safety.</p>
        </div>
      </div>

      <!-- Col 2: Expected Challenges -->
      <div class="col-card amber">
        <div class="col-header">
          <div class="col-title">EXPECTED CHALLENGES</div>
          <span style="font-size: 13px; font-weight: 700; color: #d97706; background: #fef3c7; padding: 4px 10px; border-radius: 12px;">Mitigated</span>
        </div>

        <div class="col-item">
          <h3>⚠️ Mixed-Bus Signal Integrity</h3>
          <p>Concurrent 1-Wire, analog ADC, and RS485 lines can cause electrical noise. Separated 5V logic and 3.3V sensor rails via dual buck converters; added 4.7kΩ pull-ups and line filters.</p>
        </div>

        <div class="col-item">
          <h3>⏱️ RS485 Modbus-RTU Timing</h3>
          <p>Potential timing contention between MAX485 switching and ESP32 Wi-Fi routines. Dedicated ESP32 Core 1 FreeRTOS task to sensor polling, isolating it from Core 0 network tasks.</p>
        </div>

        <div class="col-item">
          <h3>🧪 Two-Point Soil Calibration</h3>
          <p>ADC variance across Philippine clay-loam Solanaceae soils. Calibrating in controlled oven-dry (0% VWC) and saturated (100% VWC) soil samples.</p>
        </div>
      </div>

      <!-- Col 3: Plan for Next Week -->
      <div class="col-card green">
        <div class="col-header">
          <div class="col-title">PLAN FOR NEXT WEEK</div>
          <span style="font-size: 13px; font-weight: 700; color: #16a34a; background: #dcfce7; padding: 4px 10px; border-radius: 12px;">Next Sprint</span>
        </div>

        <div class="col-item">
          <h3>🔌 Complete Circuit Assembly</h3>
          <p>Finalize physical breadboard wiring harness connecting all 5 sensors to ESP32 and test power delivery from the 12.8V LiFePO4 battery pack.</p>
        </div>

        <div class="col-item">
          <h3>🔄 FreeRTOS Firmware Routines</h3>
          <p>Implement multi-sensor sampling loops and offline FIFO MicroSD buffer (telemetry_buffer.jsonl) for zero-loss edge storage.</p>
        </div>

        <div class="col-item">
          <h3>☁️ Cloud Ingestion & Risk Engine</h3>
          <p>Connect Node.js/Express REST API to Turso libSQL cloud database and link Wallin SV and Hydrothermal risk models.</p>
        </div>

        <div class="col-item">
          <h3>🌡️ Sensor Bench Calibration</h3>
          <p>Execute ice-point (0.0°C) and NaCl humidity chamber (75.3% RH) calibration tests.</p>
        </div>
      </div>
    </div>

    <div class="slide-footer-bar">
      <div><strong>Team Members:</strong> Morales, Simeon Agabus S. • Rapada, Raven M. • Hernandez, Andrei S. • Eugenio, Vince Angelo</div>
      <div><strong>Adviser:</strong> Prof. Eugenia R. Zhuo, DIT &nbsp;|&nbsp; <strong>Special Term A/Y 2025–2026</strong></div>
    </div>
  </div>

  <!-- SLIDE 2: HARDWARE MATERIALS & SOFTWARE SHOWCASE -->
  <div class="slide">
    <div class="slide-header">
      <div class="header-left">
        <div class="category-pill">Hardware Showcase & System Highlights</div>
        <h1>MATERIALS INVENTORY & WORKING APPLICATION</h1>
        <p>SolanaWatch: An IoT-Based Disease Early Warning System for Soil-Grown Solanaceae Crops</p>
      </div>
      <div class="header-badge">● 100% MATERIALS IN-HAND</div>
    </div>

    <div class="two-col-grid">
      <div class="image-container">
        <img src="../../figures/web_dashboard_mockup.jpg" alt="SolanaWatch Working Web Dashboard">
      </div>

      <div class="info-panel">
        <div class="info-title">Materials Inventory & System Highlights</div>

        <ul class="feature-list">
          <li class="feature-item">
            <h4>✔ 100% Complete Hardware Materials (₱7,208 BOM)</h4>
            <p>ESP32 DevKit V1, DHT22 in Stevenson shield, DS18B20 soil temp, Capacitive v1.2, IP68 RS485 leaf wetness grid, 20W PV + MPPT + 12.8V LiFePO4 battery (47-day autonomy), IP66 enclosure.</p>
          </li>
          <li class="feature-item">
            <h4>✔ Physical Circuit Bring-Up Underway</h4>
            <p>Breadboard component layout, pin mapping, isolated 5V & 3.3V power rails, and preliminary sensor communication checks actively progressing.</p>
          </li>
          <li class="feature-item">
            <h4>✔ Working PC & Mobile UI Dashboards</h4>
            <p>Real-time telemetry readouts for Soil Moisture (68%), Soil Temp (24°C), Air Temp (22°C), Leaf Wetness (4.2h), and Humidity (88%).</p>
          </li>
          <li class="feature-item">
            <h4>✔ Pre-Symptomatic Disease Risk Engine</h4>
            <p>Embedded algorithms for Late Blight (Wallin Severity Values @ LWD >= 10h) and Bacterial Wilt (Hydrothermal Soil Risk Index R_BW).</p>
          </li>
          <li class="feature-item">
            <h4>✔ Institutional Ethics Clearance Complete</h4>
            <p>UST Form 4.2 & Form 7.2 accomplished for research protocol compliance and participant safety.</p>
          </li>
        </ul>
      </div>
    </div>

    <div class="slide-footer-bar">
      <div><strong>Interactive Prototype:</strong> Open <code>SolanaWatch_PC_Dashboard.html</code> or <code>SolanaWatch_iOS_App.html</code></div>
      <div><strong>SolanaWatch:</strong> IoT Early Warning System for Solanaceae Crops &nbsp;|&nbsp; Group 1 (3ITC)</div>
    </div>
  </div>

</body>
</html>
"""
    with open(HTML_SLIDES_PATH, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"[SUCCESS] 2-Slide HTML saved to: {HTML_SLIDES_PATH}")

    # Compile PDF via Edge Headless
    edge_candidates = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
    ]
    edge_path = None
    for path in edge_candidates:
        if os.path.exists(path):
            edge_path = path
            break

    if edge_path:
        cmd = [
            edge_path,
            "--headless",
            "--disable-gpu",
            "--print-to-pdf-no-header",
            f"--print-to-pdf={PDF_PATH}",
            HTML_SLIDES_PATH
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0 and os.path.exists(PDF_PATH):
            print(f"[SUCCESS] 2-Slide PDF generated at: {PDF_PATH} ({os.path.getsize(PDF_PATH)} bytes)")
        else:
            print(f"[ERROR] Edge PDF generation failed: {res.stderr}")

def generate_markdown_report():
    md_content = """# 🌿 SolanaWatch: Weekly Progress Report

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
| **Field Packaging** | IP65/IP66 Polycarbonate Enclosure ($200 \times 150 \times 100\\text{ mm}$) + PG7/PG9 Compression Cable Glands | **100% In-Hand** | Weatherproof sealing & cable gland drip loops ready |

---

## 💻 Software & System Highlights

1. **Working PC Dashboard (`SolanaWatch_PC_Dashboard.html`):**
   - High-density responsive interface with 5 real-time environmental gauge cards.
   - Dual Disease Risk Engine: Late Blight (Wallin Severity Values @ LWD $\ge 10\text{ h}$) & Bacterial Wilt Hydrothermal index ($R_{\text{BW}} = 0.50 \times S_{\text{ST}} + 0.50 \times S_{\text{SM}}$).
   - Contextual agronomic interventions and hardware telemetry monitoring.
2. **Mobile iOS App (`SolanaWatch_iOS_App.html`):**
   - Mobile-first interface designed to Apple HIG standards for field inspections.
3. **Institutional Ethics Compliance:**
   - UST Ethics Review Form 4.2 & Form 7.2 completed, covering smallholder farmer participant safety and research protocols.

---

*Compiled by Group 1 (3ITC) - Surfer Bros: Morales, Simeon Agabus S. • Rapada, Raven M. • Hernandez, Andrei S. • Eugenio, Vince Angelo*  
*Adviser: Prof. Eugenia R. Zhuo, DIT | UST College of Information and Computing Sciences*
"""
    with open(MD_REPORT_PATH, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"[SUCCESS] Markdown Report saved to: {MD_REPORT_PATH}")

if __name__ == "__main__":
    generate_pptx()
    generate_html_and_pdf()
    generate_markdown_report()
