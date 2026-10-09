import os
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

OUTPUT_FILE = r"C:\Users\agabu\Downloads\CODE PROJECTS\SOLANAWATCH\paperwork\reports-and-presentations\SolanaWatch_Presentation_Editable.pptx"

# 16:9 Widescreen dimensions
SLIDE_WIDTH = Inches(13.333)
SLIDE_HEIGHT = Inches(7.5)

# Modern, clean color palette (Professional Green & Slate for AgTech)
C_WHITE = RGBColor(255, 255, 255)
C_BG_PAGE = RGBColor(248, 250, 252)       # Light slate/off-white #F8FAFC
C_CARD_BG = RGBColor(255, 255, 255)       # Pure white cards #FFFFFF
C_CARD_BORDER = RGBColor(226, 232, 240)   # Light gray border #E2E8F0
C_PRIMARY = RGBColor(16, 124, 65)         # Agritech Emerald Green #107C41
C_PRIMARY_LIGHT = RGBColor(220, 252, 231) # Mint badge #DCFCE7
C_NAVY_DARK = RGBColor(15, 23, 42)        # Deep Charcoal/Navy #0F172A
C_BODY_TEXT = RGBColor(51, 65, 85)        # Slate 700 #334155
C_MUTED_TEXT = RGBColor(100, 116, 139)    # Slate 500 #64748B
C_ACCENT_AMBER = RGBColor(217, 119, 6)    # Amber #D97706
C_ACCENT_BLUE = RGBColor(2, 132, 199)     # Sky Blue #0284C7

def build_presentation():
    prs = pptx.Presentation()
    prs.slide_width = SLIDE_WIDTH
    prs.slide_height = SLIDE_HEIGHT
    blank_layout = prs.slide_layouts[6]

    def add_page_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SLIDE_WIDTH, SLIDE_HEIGHT)
        bg.fill.solid()
        bg.fill.fore_color.rgb = C_BG_PAGE
        bg.line.fill.background()
        return bg

    def add_header(slide, section_tag, main_title, subtitle, time_badge=""):
        # Section Tag / Time
        tb_tag = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(8.0), Inches(0.3))
        p_tag = tb_tag.text_frame.paragraphs[0]
        p_tag.text = section_tag.upper()
        p_tag.font.name = "Arial"
        p_tag.font.size = Pt(11)
        p_tag.font.bold = True
        p_tag.font.color.rgb = C_PRIMARY

        # Main Title
        tb_title = slide.shapes.add_textbox(Inches(0.8), Inches(0.68), Inches(9.5), Inches(0.55))
        p_title = tb_title.text_frame.paragraphs[0]
        p_title.text = main_title
        p_title.font.name = "Arial"
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = C_NAVY_DARK

        # Subtitle
        if subtitle:
            tb_sub = slide.shapes.add_textbox(Inches(0.8), Inches(1.22), Inches(9.5), Inches(0.35))
            p_sub = tb_sub.text_frame.paragraphs[0]
            p_sub.text = subtitle
            p_sub.font.name = "Arial"
            p_sub.font.size = Pt(12)
            p_sub.font.color.rgb = C_MUTED_TEXT

        # Time Badge (Top Right)
        if time_badge:
            badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(11.0), Inches(0.5), Inches(1.5), Inches(0.42))
            badge.fill.solid()
            badge.fill.fore_color.rgb = C_PRIMARY_LIGHT
            badge.line.color.rgb = C_PRIMARY
            badge.line.width = Pt(1)
            tf_b = badge.text_frame
            tf_b.vertical_anchor = MSO_ANCHOR.MIDDLE
            p_b = tf_b.paragraphs[0]
            p_b.text = time_badge
            p_b.alignment = PP_ALIGN.CENTER
            p_b.font.name = "Arial"
            p_b.font.size = Pt(11)
            p_b.font.bold = True
            p_b.font.color.rgb = C_PRIMARY

    def add_content_card(slide, left, top, width, height, title, title_color=C_NAVY_DARK):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = C_CARD_BG
        card.line.color.rgb = C_CARD_BORDER
        card.line.width = Pt(1)
        
        # Title text box inside card
        tb = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.18), width - Inches(0.4), Inches(0.45))
        p = tb.text_frame.paragraphs[0]
        p.text = title
        p.font.name = "Arial"
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = title_color
        
        # Body text box inside card
        tb_body = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.65), width - Inches(0.4), height - Inches(0.8))
        tf_body = tb_body.text_frame
        tf_body.word_wrap = True
        tf_body.margin_left = tf_body.margin_right = tf_body.margin_top = tf_body.margin_bottom = 0
        return tf_body

    # =========================================================================
    # SLIDE 1: TITLE SLIDE
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    add_page_background(s1)

    # Decorative top bar
    bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SLIDE_WIDTH, Inches(0.15))
    bar.fill.solid()
    bar.fill.fore_color.rgb = C_PRIMARY
    bar.line.fill.background()

    # Main Title Card
    c_title = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(1.2), Inches(10.933), Inches(5.1))
    c_title.fill.solid()
    c_title.fill.fore_color.rgb = C_CARD_BG
    c_title.line.color.rgb = C_CARD_BORDER
    c_title.line.width = Pt(1)

    tf1 = c_title.text_frame
    tf1.word_wrap = True
    tf1.vertical_anchor = MSO_ANCHOR.MIDDLE

    p = tf1.paragraphs[0]
    p.text = "SOLANAWATCH"
    p.alignment = PP_ALIGN.CENTER
    p.font.name = "Arial"
    p.font.size = Pt(40)
    p.font.bold = True
    p.font.color.rgb = C_PRIMARY

    p2 = tf1.add_paragraph()
    p2.text = "An IoT-Based Disease Early Warning System for Soil-Grown Solanaceae Crops"
    p2.alignment = PP_ALIGN.CENTER
    p2.font.name = "Arial"
    p2.font.size = Pt(18)
    p2.font.color.rgb = C_NAVY_DARK

    p_space = tf1.add_paragraph()
    p_space.text = ""
    p_space.font.size = Pt(14)

    p3 = tf1.add_paragraph()
    p3.text = "Capstone 5-Minute Progress & Technical Briefing"
    p3.alignment = PP_ALIGN.CENTER
    p3.font.name = "Arial"
    p3.font.size = Pt(13)
    p3.font.bold = True
    p3.font.color.rgb = C_ACCENT_BLUE

    p4 = tf1.add_paragraph()
    p4.text = "Team: Simeon Agabus S. Morales • Raven M. Rapada • Andrei S. Hernandez • Vince Angelo Eugenio"
    p4.alignment = PP_ALIGN.CENTER
    p4.font.name = "Arial"
    p4.font.size = Pt(12)
    p4.font.color.rgb = C_BODY_TEXT

    p5 = tf1.add_paragraph()
    p5.text = "Project Adviser: Prof. Eugenia R. Zhuo, DIT | UST College of Information and Computing Sciences"
    p5.alignment = PP_ALIGN.CENTER
    p5.font.name = "Arial"
    p5.font.size = Pt(11)
    p5.font.color.rgb = C_MUTED_TEXT

    # =========================================================================
    # SLIDE 2: 1. PROJECT OVERVIEW (1 MINUTE)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_page_background(s2)
    add_header(s2, "Section 1 • Foundation", "1. Project Overview", "Problem formulation with literature citations, proposed IoT solution, and core objectives.", "⏱️ 1 MINUTE")

    card_w = Inches(3.64)
    card_h = Inches(5.35)
    card_top = Inches(1.65)

    # Card 1: Problem (with literature citations)
    tf = add_content_card(s2, Inches(0.8), card_top, card_w, card_h, "1. The Problem (Sources)", C_NAVY_DARK)
    items_c1 = [
        ("High Economic Stakes (PSA, 2026; Aquino et al., 2024):", True),
        ("• Solanaceae crops (Eggplant >100,000 MT/quarter; Tomato 70k-93k MT) are crucial to Philippine food security.", False),
        ("Devastating Yield Losses (50%–90%):", True),
        ("• Aumentado & Balendres (2024); Subedi et al. (2024): Caused by Late Blight (P. infestans) and Bacterial Wilt (R. pseudosolanacearum).", False),
        ("Microclimatic Infection Drivers:", True),
        ("• Late Blight: RH ≥90%, leaf wetness ≥10h, 12°C–22°C (Mazumdar et al., 2021; Boulton et al., 2023).", False),
        ("• Bacterial Wilt: Warm soil 28°C–35°C & moisture ≥75% VWC (Silva et al., 2024; Jiang et al., 2021).", False),
        ("Current Gap (Jafar et al., 2024):", True),
        ("• Computer vision AI only detects diseases POST-SYMPTOMATICALLY after irreversible tissue necrosis has occurred.", False),
    ]
    for text, bold in items_c1:
        p = tf.add_paragraph() if tf.paragraphs[0].text else tf.paragraphs[0]
        p.text = text
        p.font.name = "Arial"
        p.font.size = Pt(10)
        p.font.bold = bold
        p.font.color.rgb = C_NAVY_DARK if bold else C_BODY_TEXT
        p.space_after = Pt(2)

    # Card 2: Proposed Solution
    tf = add_content_card(s2, Inches(4.84), card_top, card_w, card_h, "2. Proposed Solution", C_PRIMARY)
    items_c2 = [
        ("Autonomous Solar IoT Edge Node:", True),
        ("• Field-deployed station monitoring real-time atmospheric, foliar, and root-zone microclimate data continuously.", False),
        ("Pre-Symptomatic Early Warning:", True),
        ("• Unlike reactive camera AI, SolanaWatch analyzes physical environmental risk drivers BEFORE symptoms physically manifest.", False),
        ("Dual Validated Pathogen Modeling:", True),
        ("• Evaluates Late Blight Wallin Severity Values (SV) & Bacterial Wilt Hydrothermal Soil Risk Index.", False),
        ("Smallholder Farmer Accessibility:", True),
        ("• Built on low-cost open hardware (₱7,208 BOM) with offline MicroSD buffering to survive frequent field power/Wi-Fi outages.", False),
    ]
    for text, bold in items_c2:
        p = tf.add_paragraph() if tf.paragraphs[0].text else tf.paragraphs[0]
        p.text = text
        p.font.name = "Arial"
        p.font.size = Pt(11)
        p.font.bold = bold
        p.font.color.rgb = C_NAVY_DARK if bold else C_BODY_TEXT
        p.space_after = Pt(4)

    # Card 3: Objectives
    tf = add_content_card(s2, Inches(8.88), card_top, card_w, card_h, "3. Project Objectives", C_ACCENT_BLUE)
    items_c3 = [
        ("General Objective:", True),
        ("• Design and develop SolanaWatch, an IoT-based disease early warning system for soil-grown Solanaceae crops.", False),
        ("Specific Objective 1:", True),
        ("• Deploy a multi-sensor edge node capturing air temp/RH, root-zone temp/moisture, and dielectric leaf wetness duration.", False),
        ("Specific Objective 2:", True),
        ("• Implement dual pathology-grounded disease risk scoring algorithms on a centralized cloud backend.", False),
        ("Specific Objective 3:", True),
        ("• Deliver responsive PC/mobile dashboards with actionable agronomic recommendations and offline data protection.", False),
    ]
    for text, bold in items_c3:
        p = tf.add_paragraph() if tf.paragraphs[0].text else tf.paragraphs[0]
        p.text = text
        p.font.name = "Arial"
        p.font.size = Pt(11)
        p.font.bold = bold
        p.font.color.rgb = C_NAVY_DARK if bold else C_BODY_TEXT
        p.space_after = Pt(4)

    # =========================================================================
    # SLIDE 3: 2. DEVELOPMENT PROGRESS (2 MINUTES)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_page_background(s3)
    add_header(s3, "Section 2 • Implementation Status", "2. Development Progress", "Original planned features, completed deliverables, and quantified workstream status.", "⏱️ 2 MINUTES")

    # Card 1: Planned Scope vs Deliverables
    tf = add_content_card(s3, Inches(0.8), card_top, Inches(4.3), card_h, "1. Planned Features & Scope", C_NAVY_DARK)
    items_s3_c1 = [
        ("Multi-Sensor Edge Telemetry:", True),
        ("• Ambient (DHT22), Subsurface (DS18B20 + Capacitive v1.2), Foliar (RS485 Dielectric Leaf Grid).", False),
        ("Autonomous Solar-Battery Power:", True),
        ("• 20W Solar PV + MPPT controller + 12.8V LiFePO4 battery providing 47 days of zero-sunlight runtime.", False),
        ("Offline Fail-Safe Edge Storage:", True),
        ("• Local MicroSD FIFO JSON Lines buffer for zero telemetry loss during rural network dropouts.", False),
        ("Cloud Ingestion & Analytics API:", True),
        ("• Node.js REST API with Turso libSQL database and automated disease risk classification engine.", False),
        ("Bilingual Decision Support Dashboards:", True),
        ("• Web PC and mobile interfaces with real-time gauges, time-series charts, and preventive recommendations.", False),
    ]
    for text, bold in items_s3_c1:
        p = tf.add_paragraph() if tf.paragraphs[0].text else tf.paragraphs[0]
        p.text = text
        p.font.name = "Arial"
        p.font.size = Pt(10.5)
        p.font.bold = bold
        p.font.color.rgb = C_NAVY_DARK if bold else C_BODY_TEXT
        p.space_after = Pt(3)

    # Card 2: Completed Deliverables
    tf = add_content_card(s3, Inches(5.3), card_top, Inches(4.3), card_h, "2. Completed Deliverables", C_PRIMARY)
    items_s3_c2 = [
        ("✅ 100% Hardware Procurement (₱7,208 BOM):", True),
        ("• Full bill of materials acquired and in-hand: ESP32, all 5 sensors, solar PV, MPPT, battery, and IP66 box.", False),
        ("✅ Physical Circuit Bench Bring-Up Active:", True),
        ("• Breadboard harness wired; dual 5V/3.3V isolated power rails verified; initial 1-Wire & ADC signals logged.", False),
        ("✅ Functional Frontend Dashboards Built:", True),
        ("• PC Dashboard (desktop.html) & iOS Mobile App (index.html) completed with live gauges and risk banners.", False),
        ("✅ UST Institutional Ethics Review Accomplished:", True),
        ("• Forms 4.2 & 7.2 submitted, establishing human & biological pathogen safety exemptions.", False),
        ("✅ Proposal Manuscript Alignment Completed:", True),
        ("• Addressed all 24 panel defense evaluation comments across Chapters 1, 2, and 3.", False),
    ]
    for text, bold in items_s3_c2:
        p = tf.add_paragraph() if tf.paragraphs[0].text else tf.paragraphs[0]
        p.text = text
        p.font.name = "Arial"
        p.font.size = Pt(10.5)
        p.font.bold = bold
        p.font.color.rgb = C_NAVY_DARK if bold else C_BODY_TEXT
        p.space_after = Pt(3)

    # Card 3: Status Matrix (% Completion)
    tf = add_content_card(s3, Inches(9.8), card_top, Inches(2.733), card_h, "3. Status Matrix", C_ACCENT_AMBER)
    items_s3_c3 = [
        ("Hardware Procurement:", True),
        ("100% COMPLETE (In-Hand)", False),
        ("Research & Ethics:", True),
        ("100% COMPLETE", False),
        ("UI Dashboards (Web/App):", True),
        ("90% ADVANCED", False),
        ("Cloud API & Database:", True),
        ("65% IN-PROGRESS", False),
        ("Firmware & Circuit Assembly:", True),
        ("60% BENCH BRING-UP", False),
        ("Bench Calibration & Field Tests:", True),
        ("30% SCHEDULED NEXT", False),
        ("OVERALL PROJECT STATUS:", True),
        ("● ~75% (ON TRACK)", False),
    ]
    for text, bold in items_s3_c3:
        p = tf.add_paragraph() if tf.paragraphs[0].text else tf.paragraphs[0]
        p.text = text
        p.font.name = "Arial"
        p.font.size = Pt(10)
        p.font.bold = bold
        p.font.color.rgb = C_PRIMARY if "COMPLETE" in text or "TRACK" in text else (C_NAVY_DARK if bold else C_BODY_TEXT)
        p.space_after = Pt(2)

    # =========================================================================
    # SLIDE 4: 3. PROTOTYPE ARCHITECTURE & DESIGN (2 MINUTES)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_page_background(s4)
    add_header(s4, "Section 3 • Technical Architecture", "3. Prototype Architecture & Design", "3-Tier system topology, sensor hardware integration, and end-to-end data pipeline.", "⏱️ 2 MINUTES")

    # Card 1: 3-Tier System Architecture
    tf = add_content_card(s4, Inches(0.8), card_top, card_w, card_h, "1. 3-Tier System Architecture", C_NAVY_DARK)
    items_s4_c1 = [
        ("Tier 1: Sensing & Edge Node", True),
        ("• ESP32 DevKit V1 (Xtensa Dual-Core 240MHz, 4MB Flash).", False),
        ("• FreeRTOS Core 1 dedicated to sensor polling.", False),
        ("• Local SPI MicroSD FIFO buffer (telemetry_buffer.jsonl).", False),
        ("• 20W Solar PV + MPPT + 12.8V LiFePO4 battery (47-day autonomy).", False),
        ("Tier 2: Cloud Ingestion & Analytics", True),
        ("• Node.js & Express REST API receiving JSON payloads.", False),
        ("• Turso Cloud Database (Distributed libSQL / SQLite).", False),
        ("• Deduplication via composite UNIQUE(node_id, recorded_at).", False),
        ("Tier 3: Presentation & Decision Support", True),
        ("• High-density PC Dashboard & iOS Mobile Interface.", False),
        ("• Color-coded alert banners (Green / Yellow / Red).", False),
        ("• Contextual agronomic recommendations (drainage, aeration).", False),
    ]
    for text, bold in items_s4_c1:
        p = tf.add_paragraph() if tf.paragraphs[0].text else tf.paragraphs[0]
        p.text = text
        p.font.name = "Arial"
        p.font.size = Pt(10)
        p.font.bold = bold
        p.font.color.rgb = C_NAVY_DARK if bold else C_BODY_TEXT
        p.space_after = Pt(2)

    # Card 2: Hardware & Software Components
    tf = add_content_card(s4, Inches(4.84), card_top, card_w, card_h, "2. Hardware / Software Spec", C_PRIMARY)
    items_s4_c2 = [
        ("Atmospheric Sensing:", True),
        ("• DHT22 / AM2302 placed inside a UV-stabilized louvered Stevenson Radiation Screen (measures ambient temp & RH).", False),
        ("Root-Zone Subsurface Sensing:", True),
        ("• Dallas DS18B20 stainless waterproof probe (1-Wire bus) @ 10 cm depth for root temperature.", False),
        ("• Capacitive v1.2 corrosion-resistant probe (analog ADC) @ 10 cm depth for volumetric soil moisture.", False),
        ("Foliar Surface Sensing:", True),
        ("• Industrial IP68 dielectric leaf wetness grid over RS485 Modbus-RTU via MAX485 transceiver.", False),
        ("Software Stack:", True),
        ("• Firmware: C++ / FreeRTOS on PlatformIO.", False),
        ("• Backend: Node.js, Express, Turso libSQL.", False),
        ("• Frontend: HTML5, Tailwind CSS, Chart.js.", False),
    ]
    for text, bold in items_s4_c2:
        p = tf.add_paragraph() if tf.paragraphs[0].text else tf.paragraphs[0]
        p.text = text
        p.font.name = "Arial"
        p.font.size = Pt(10)
        p.font.bold = bold
        p.font.color.rgb = C_NAVY_DARK if bold else C_BODY_TEXT
        p.space_after = Pt(2)

    # Card 3: Data & Process Flow
    tf = add_content_card(s4, Inches(8.88), card_top, card_w, card_h, "3. End-to-End Data Flow", C_ACCENT_BLUE)
    items_s4_c3 = [
        ("Step 1: Multi-Sensor Sampling", True),
        ("• FreeRTOS Core 1 wakes every 15 min; samples all 5 sensors across 1-Wire, ADC, and Modbus buses.", False),
        ("Step 2: Local Edge Buffering", True),
        ("• Immediately appends telemetry JSON to MicroSD card to guarantee zero data loss if Wi-Fi fails.", False),
        ("Step 3: Secure Wi-Fi Transmission", True),
        ("• FreeRTOS Core 0 enables 2.4GHz Wi-Fi; dispatches HTTP POST /api/telemetry to cloud API.", False),
        ("Step 4: Cloud Disease Risk Scoring", True),
        ("• Late Blight: Evaluates Wallin Severity Values (SV) at Leaf Wetness Duration ≥ 10h and 12°C–22°C.", False),
        ("• Bacterial Wilt: Calculates Hydrothermal Index: R_BW = 0.50*S_ST + 0.50*S_SM (temp 28–35°C, moisture ≥75%).", False),
        ("Step 5: Alert Delivery & Action", True),
        ("• Pushes immediate status and cultural interventions directly to farmers' dashboards.", False),
    ]
    for text, bold in items_s4_c3:
        p = tf.add_paragraph() if tf.paragraphs[0].text else tf.paragraphs[0]
        p.text = text
        p.font.name = "Arial"
        p.font.size = Pt(9.8)
        p.font.bold = bold
        p.font.color.rgb = C_NAVY_DARK if bold else C_BODY_TEXT
        p.space_after = Pt(2)

    # =========================================================================
    # SLIDE 5: SUMMARY & IMMEDIATE NEXT STEPS (CONCLUSION / Q&A)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_page_background(s5)
    add_header(s5, "Section 4 • Road Ahead", "Summary & Next Milestones", "Current accomplishments, target sprint deliverables, and panel defense readiness.", "Q & A")

    tf = add_content_card(s5, Inches(0.8), card_top, Inches(3.64), card_h, "Current Standing", C_PRIMARY)
    items_s5_c1 = [
        ("Hardware Foundation Solid:", True),
        ("• 100% of physical parts procured under budget (₱7,208 total).", False),
        ("Software Readiness:", True),
        ("• Interactive dashboards built and ready for telemetry ingestion.", False),
        ("Institutional Compliance:", True),
        ("• UST Ethics Review accomplished and manuscript fully coordinated with adviser directives.", False),
    ]
    for text, bold in items_s5_c1:
        p = tf.add_paragraph() if tf.paragraphs[0].text else tf.paragraphs[0]
        p.text = text
        p.font.name = "Arial"
        p.font.size = Pt(11)
        p.font.bold = bold
        p.font.color.rgb = C_NAVY_DARK if bold else C_BODY_TEXT
        p.space_after = Pt(4)

    tf = add_content_card(s5, Inches(4.84), card_top, Inches(3.64), card_h, "Immediate Next Steps", C_ACCENT_AMBER)
    items_s5_c2 = [
        ("1. Multi-Sensor Bench Calibration:", True),
        ("• Ice-point (0.0°C), NaCl salt chamber (75.3% RH), and 2-point soil calibration (0% and 100% VWC).", False),
        ("2. FreeRTOS Dual-Core Firmware:", True),
        ("• Finalize non-blocking sensor sampling routines and automatic MicroSD buffer catch-up sync.", False),
        ("3. Enclosure Packaging:", True),
        ("• Assemble IP66 weatherproof box with cable gland drip loops and field test power draw.", False),
    ]
    for text, bold in items_s5_c2:
        p = tf.add_paragraph() if tf.paragraphs[0].text else tf.paragraphs[0]
        p.text = text
        p.font.name = "Arial"
        p.font.size = Pt(11)
        p.font.bold = bold
        p.font.color.rgb = C_NAVY_DARK if bold else C_BODY_TEXT
        p.space_after = Pt(4)

    tf = add_content_card(s5, Inches(8.88), card_top, Inches(3.64), card_h, "Defense Readiness", C_ACCENT_BLUE)
    items_s5_c3 = [
        ("Thank You!", True),
        ("SolanaWatch is on track to deliver an affordable, pre-symptomatic disease early warning system for Filipino Solanaceae farmers.", False),
        ("Adviser:", True),
        ("Prof. Eugenia R. Zhuo, DIT", False),
        ("Panelists:", True),
        ("Inst. Gabriel Emanuel D. Montano\nProf. Noel E. Estrella\nMr. Karlo Angelo Tino", False),
        ("Now Open for Panel Q & A", True),
    ]
    for text, bold in items_s5_c3:
        p = tf.add_paragraph() if tf.paragraphs[0].text else tf.paragraphs[0]
        p.text = text
        p.font.name = "Arial"
        p.font.size = Pt(11)
        p.font.bold = bold
        p.font.color.rgb = C_NAVY_DARK if bold else C_BODY_TEXT
        p.space_after = Pt(4)

    prs.save(OUTPUT_FILE)
    print(f"Successfully generated: {OUTPUT_FILE}")

if __name__ == "__main__":
    build_presentation()
