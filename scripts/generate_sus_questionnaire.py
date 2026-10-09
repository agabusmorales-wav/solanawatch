import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_table_borders(table, color="B0BEC5", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>\n'
        f'  <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>\n'
        f'  <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>\n'
        f'  <w:left w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>\n'
        f'  <w:right w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>\n'
        f'  <w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>\n'
        f'  <w:insideV w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>\n'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def set_cell_background(cell, fill_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_color}"/>')
    tcPr.append(shd)

def prevent_row_split(row):
    trPr = row._tr.get_or_add_trPr()
    trPr.append(OxmlElement('w:cantSplit'))

def set_repeat_header(row):
    trPr = row._tr.get_or_add_trPr()
    trPr.append(OxmlElement('w:tblHeader'))

def add_heading_styled(doc, text, level=1, space_before=12, space_after=4):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = 'Arial'
    run.bold = True
    if level == 1:
        run.font.size = Pt(12)
        run.font.color.rgb = RGBColor(0x00, 0x33, 0x66) # Deep Navy Blue
        # Add a subtle bottom border or rule under Heading 1
    elif level == 2:
        run.font.size = Pt(10.5)
        run.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
    else:
        run.font.size = Pt(9.5)
        run.font.color.rgb = RGBColor(0x2D, 0x37, 0x48)
    return p

def create_sus_questionnaire():
    doc = docx.Document()
    
    # 0.75-inch margins
    for section in doc.sections:
        section.top_margin = Inches(0.75)
        section.bottom_margin = Inches(0.75)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)
        
        # Header / Footer
        header = section.header
        p_hdr = header.paragraphs[0]
        p_hdr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r_hdr = p_hdr.add_run("SolanaWatch: IoT Disease Early Warning System | SUS Evaluation Instrument")
        r_hdr.font.name = 'Arial'
        r_hdr.font.size = Pt(8)
        r_hdr.font.color.rgb = RGBColor(0x7F, 0x8C, 0x8D)
        
        footer = section.footer
        p_ftr = footer.paragraphs[0]
        p_ftr.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_ftr = p_ftr.add_run("Form SUS-2026-v1.0 | UST-CICS Capstone Research Instrument (ISO/IEC 25010 Usability)")
        r_ftr.font.name = 'Arial'
        r_ftr.font.size = Pt(8)
        r_ftr.font.color.rgb = RGBColor(0x7F, 0x8C, 0x8D)

    # Styles
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Arial'
    normal_style.font.size = Pt(9.5)
    normal_style.font.color.rgb = RGBColor(0x22, 0x22, 0x22)
    
    # -------------------------------------------------------------
    # 1. INSTITUTIONAL HEADER WITH LOGOS
    # -------------------------------------------------------------
    logo_dir = r"C:\Users\agabu\Downloads\extracted_logos"
    ust_logo = os.path.join(logo_dir, "ust_logo_clean.png")
    cics_logo = os.path.join(logo_dir, "cics_logo_clean.png")
    
    header_table = doc.add_table(rows=1, cols=3)
    header_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    header_table.autofit = False
    
    col_widths = [Inches(1.0), Inches(5.0), Inches(1.0)]
    for i, col in enumerate(header_table.columns):
        col.width = col_widths[i]
        
    row = header_table.rows[0]
    prevent_row_split(row)
    
    # Left logo (UST)
    cell_left = row.cells[0]
    p_left = cell_left.paragraphs[0]
    p_left.alignment = WD_ALIGN_PARAGRAPH.LEFT
    if os.path.exists(ust_logo):
        p_left.add_run().add_picture(ust_logo, width=Inches(0.85))
        
    # Center text
    cell_center = row.cells[1]
    p_mid = cell_center.paragraphs[0]
    p_mid.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_mid.paragraph_format.space_before = Pt(0)
    p_mid.paragraph_format.space_after = Pt(0)
    p_mid.paragraph_format.line_spacing = 1.15
    
    r_u1 = p_mid.add_run("UNIVERSITY OF SANTO TOMAS\n")
    r_u1.font.name = 'Arial'
    r_u1.font.size = Pt(11)
    r_u1.font.bold = True
    r_u1.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
    
    r_u2 = p_mid.add_run("COLLEGE OF INFORMATION AND COMPUTING SCIENCES\n")
    r_u2.font.name = 'Arial'
    r_u2.font.size = Pt(9.5)
    r_u2.font.bold = True
    r_u2.font.color.rgb = RGBColor(0x00, 0x33, 0x66)
    
    r_u3 = p_mid.add_run("DEPARTMENT OF INFORMATION TECHNOLOGY\n")
    r_u3.font.name = 'Arial'
    r_u3.font.size = Pt(9)
    r_u3.font.bold = True
    
    r_u4 = p_mid.add_run("Academic Year 2025–2026 | Special Term")
    r_u4.font.name = 'Arial'
    r_u4.font.size = Pt(8.5)
    r_u4.font.italic = True
    r_u4.font.color.rgb = RGBColor(0x55, 0x55, 0x55)
    
    # Right logo (CICS)
    cell_right = row.cells[2]
    p_right = cell_right.paragraphs[0]
    p_right.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    if os.path.exists(cics_logo):
        p_right.add_run().add_picture(cics_logo, width=Inches(0.85))
        
    for cell in row.cells:
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        set_cell_margins(cell, top=0, bottom=40, left=0, right=0)

    # Decorative Line
    p_rule = doc.add_paragraph()
    p_rule.paragraph_format.space_before = Pt(4)
    p_rule.paragraph_format.space_after = Pt(8)
    p_rule.paragraph_format.line_spacing = 1.0
    r_line = p_rule.add_run("―" * 58)
    r_line.font.name = 'Arial'
    r_line.font.size = Pt(14)
    r_line.font.bold = True
    r_line.font.color.rgb = RGBColor(0x00, 0x33, 0x66)

    # -------------------------------------------------------------
    # 2. INSTRUMENT TITLE & METADATA BLOCK
    # -------------------------------------------------------------
    p_doc_title = doc.add_paragraph()
    p_doc_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_doc_title.paragraph_format.space_before = Pt(2)
    p_doc_title.paragraph_format.space_after = Pt(2)
    r_t1 = p_doc_title.add_run("SYSTEM USABILITY SCALE (SUS) EVALUATION INSTRUMENT\n")
    r_t1.font.name = 'Arial'
    r_t1.font.size = Pt(13)
    r_t1.font.bold = True
    r_t1.font.color.rgb = RGBColor(0x00, 0x33, 0x66)
    
    r_t2 = p_doc_title.add_run("ISO/IEC 25010 Usability & User Experience Quality Metric\n")
    r_t2.font.name = 'Arial'
    r_t2.font.size = Pt(9.5)
    r_t2.font.bold = True
    r_t2.font.color.rgb = RGBColor(0xC5, 0x9B, 0x27) # UST Gold tone
    
    r_t3 = p_doc_title.add_run("Project Title: SolanaWatch: An IoT-Based Disease Early Warning System for Soil-Grown Solanaceae Crops")
    r_t3.font.name = 'Arial'
    r_t3.font.size = Pt(9)
    r_t3.font.italic = True
    r_t3.font.color.rgb = RGBColor(0x33, 0x33, 0x33)

    # Project Information Card Table
    meta_table = doc.add_table(rows=2, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_table.autofit = False
    meta_widths = [Inches(3.5), Inches(3.5)]
    for i, col in enumerate(meta_table.columns):
        col.width = meta_widths[i]
    set_table_borders(meta_table, color="D0D7DE", sz="4")
    
    row0 = meta_table.rows[0]
    prevent_row_split(row0)
    set_cell_background(row0.cells[0], "F8FAFC")
    set_cell_background(row0.cells[1], "F8FAFC")
    set_cell_margins(row0.cells[0], 60, 60, 100, 100)
    set_cell_margins(row0.cells[1], 60, 60, 100, 100)
    
    p_m1 = row0.cells[0].paragraphs[0]
    p_m1.paragraph_format.space_before = Pt(0)
    p_m1.paragraph_format.space_after = Pt(0)
    p_m1.paragraph_format.line_spacing = 1.15
    r = p_m1.add_run("Proponents (3ITC - Group 1):\n")
    r.font.bold = True
    r.font.size = Pt(8.5)
    r_names = p_m1.add_run("• Morales, Simeon Agabus S.\n• Rapada, Raven M.\n• Hernandez, Andrei S.\n• Eugenio, Vince Angelo")
    r_names.font.size = Pt(8)
    
    p_m2 = row0.cells[1].paragraphs[0]
    p_m2.paragraph_format.space_before = Pt(0)
    p_m2.paragraph_format.space_after = Pt(0)
    p_m2.paragraph_format.line_spacing = 1.15
    r2 = p_m2.add_run("Academic Context & Supervision:\n")
    r2.font.bold = True
    r2.font.size = Pt(8.5)
    r_sup = p_m2.add_run("• Project Adviser: Prof. Eugenia R. Zhuo, DIT\n• Degree: B.S. in Information Technology\n• Evaluation Target: ≥ 80.0 / 100 (SUS Grade A)\n• Target Group: Farmers & Agricultural Technicians")
    r_sup.font.size = Pt(8)
    
    row1 = meta_table.rows[1]
    prevent_row_split(row1)
    set_cell_background(row1.cells[0], "FFFFFF")
    set_cell_background(row1.cells[1], "FFFFFF")
    set_cell_margins(row1.cells[0], 60, 60, 100, 100)
    set_cell_margins(row1.cells[1], 60, 60, 100, 100)
    
    p_m3 = row1.cells[0].paragraphs[0]
    p_m3.paragraph_format.space_before = Pt(0)
    p_m3.paragraph_format.space_after = Pt(0)
    r3 = p_m3.add_run("Participant ID / Code: ")
    r3.font.bold = True
    r3.font.size = Pt(8.5)
    p_m3.add_run("____________________").font.size = Pt(8.5)
    
    p_m4 = row1.cells[1].paragraphs[0]
    p_m4.paragraph_format.space_before = Pt(0)
    p_m4.paragraph_format.space_after = Pt(0)
    r4 = p_m4.add_run("Date of Evaluation: ")
    r4.font.bold = True
    r4.font.size = Pt(8.5)
    p_m4.add_run("____________________").font.size = Pt(8.5)

    # -------------------------------------------------------------
    # SECTION 1: RESEARCH PURPOSE & INFORMED CONSENT
    # -------------------------------------------------------------
    add_heading_styled(doc, "SECTION 1: PURPOSE OF EVALUATION & INFORMED CONSENT", level=1, space_before=10, space_after=3)
    
    p_intro = doc.add_paragraph()
    p_intro.paragraph_format.space_before = Pt(0)
    p_intro.paragraph_format.space_after = Pt(4)
    p_intro.paragraph_format.line_spacing = 1.15
    p_intro.add_run(
        "Dear Participant,\n\n"
        "Thank you for participating in the usability evaluation of SolanaWatch: An IoT-Based Disease Early Warning System for "
        "Soil-Grown Solanaceae Crops. SolanaWatch is a capstone research system developed at the University of Santo Tomas – "
        "College of Information and Computing Sciences (CICS). The system combines solar-powered field sensing nodes (monitoring "
        "air temperature, relative humidity, leaf wetness duration, root-zone soil temperature, and capacitive soil moisture) with a "
        "web-based decision support dashboard to deliver pre-symptomatic alerts for Late Blight (Phytophthora infestans) and Bacterial "
        "Wilt (Ralstonia pseudosolanacearum).\n\n"
        "This evaluation utilizes the standardized System Usability Scale (SUS) formulated by John Brooke (1996) to measure usability, "
        "learnability, and overall user acceptance under the ISO/IEC 25010 Software Quality Standard. Your honest feedback is vital "
        "in optimizing the system for practical agricultural deployment."
    )
    
    # Ethics & Privacy Callout Box
    ethics_table = doc.add_table(rows=1, cols=1)
    ethics_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    ethics_table.autofit = False
    ethics_table.columns[0].width = Inches(7.0)
    set_table_borders(ethics_table, color="003366", sz="6")
    cell_eth = ethics_table.rows[0].cells[0]
    set_cell_background(cell_eth, "F0F4F8")
    set_cell_margins(cell_eth, 80, 80, 120, 120)
    p_eth = cell_eth.paragraphs[0]
    p_eth.paragraph_format.space_before = Pt(0)
    p_eth.paragraph_format.space_after = Pt(0)
    p_eth.paragraph_format.line_spacing = 1.15
    r_eth_t = p_eth.add_run("Informed Consent & Data Privacy Guarantee (R.A. 10173 - Philippine Data Privacy Act of 2012):\n")
    r_eth_t.font.bold = True
    r_eth_t.font.size = Pt(8.5)
    r_eth_t.font.color.rgb = RGBColor(0x00, 0x33, 0x66)
    r_eth_b = p_eth.add_run(
        "• Participation is entirely voluntary. You may pause or withdraw from this evaluation at any time without penalty.\n"
        "• All responses and demographic information will be kept strictly confidential and anonymized using assigned Participant IDs.\n"
        "• Data gathered will be utilized exclusively for academic analysis, capstone documentation, and scientific dissemination.\n"
        "• No personally identifiable financial or commercial information will be collected or published."
    )
    r_eth_b.font.size = Pt(8)

    # -------------------------------------------------------------
    # SECTION 2: PARTICIPANT PROFILE & DEMOGRAPHICS
    # -------------------------------------------------------------
    add_heading_styled(doc, "SECTION 2: PARTICIPANT DEMOGRAPHIC & OPERATIONAL PROFILE", level=1, space_before=10, space_after=3)
    
    p_dem_inst = doc.add_paragraph()
    p_dem_inst.paragraph_format.space_before = Pt(0)
    p_dem_inst.paragraph_format.space_after = Pt(4)
    r_d = p_dem_inst.add_run("Please mark [X] or complete the information corresponding to your background:")
    r_d.font.size = Pt(8.5)
    r_d.font.italic = True
    
    dem_table = doc.add_table(rows=6, cols=2)
    dem_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    dem_table.autofit = False
    dem_widths = [Inches(3.5), Inches(3.5)]
    for i, col in enumerate(dem_table.columns):
        col.width = dem_widths[i]
    set_table_borders(dem_table, color="D0D7DE", sz="4")
    
    dem_data = [
        ("1. Primary Stakeholder Role:",
         "[  ] Smallholder Solanaceae Farmer\n[  ] Agricultural Extension Worker / LGU Technician\n[  ] Agronomist / Plant Pathologist\n[  ] Academic Researcher / IT Evaluator\n[  ] Other: ___________________________",
         "2. Gender & Age Bracket:",
         "Gender:  [  ] Male   [  ] Female   [  ] Prefer not to say\nAge:  [  ] 18–29   [  ] 30–39   [  ] 40–49\n         [  ] 50–59   [  ] 60 and above"),
        ("3. Farming / Agricultural Experience:",
         "[  ] Less than 2 years\n[  ] 2 to 5 years\n[  ] 6 to 10 years\n[  ] More than 10 years",
         "4. Solanaceae Crops Cultivated / Handled:",
         "[  ] Eggplant (Talong)\n[  ] Tomato (Kamatis)\n[  ] Pepper (Siling Haba / Bell Pepper)\n[  ] Potato (Patatas)\n[  ] Mixed / Diversified Cropping"),
        ("5. Farm / Workplace Location:",
         "Barangay: ___________________________\nMunicipality: ___________________________\nProvince: ___________________________",
         "6. Digital Device Usage in Daily Routine:",
         "[  ] Smartphone (Android / iOS)\n[  ] Tablet\n[  ] Desktop / Laptop Computer\n[  ] Basic Keypad Phone (SMS only)\n[  ] Non-User / Assistance Required"),
        ("7. Past Experience with Digital Farm Tools:",
         "[  ] None (First time using smart farm tools)\n[  ] Occasional (Weather apps, SMS advisories)\n[  ] Frequent (IoT, sensors, farm management apps)",
         "8. Preferred Language for Agricultural Advice:",
         "[  ] English\n[  ] Filipino / Tagalog\n[  ] Bilingual (English with Filipino subtitles)\n[  ] Regional Dialect: __________________"),
        ("9. Scale of Farming Operation (if applicable):",
         "[  ] Backyard / Subsistence (< 500 sqm)\n[  ] Smallholder (0.1 to 1.0 hectare)\n[  ] Medium Commercial (1.0 to 5.0 hectares)\n[  ] Institutional / Research Experimental Plot",
         "10. Previous Crop Loss Experience from Disease:",
         "[  ] Frequent severe loss (Late Blight / Wilt)\n[  ] Moderate seasonal loss\n[  ] Minimal / Well-controlled loss\n[  ] Not applicable (Non-farmer / Researcher)"),
    ]
    
    for row_idx, (col1_title, col1_val, col2_title, col2_val) in enumerate(dem_data):
        row = dem_table.rows[row_idx]
        prevent_row_split(row)
        
        c1 = row.cells[0]
        set_cell_margins(c1, 50, 50, 80, 80)
        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_before = Pt(0)
        p1.paragraph_format.space_after = Pt(0)
        p1.paragraph_format.line_spacing = 1.15
        r_t = p1.add_run(f"{col1_title}\n")
        r_t.font.bold = True
        r_t.font.size = Pt(8.5)
        r_t.font.color.rgb = RGBColor(0x00, 0x33, 0x66)
        r_v = p1.add_run(col1_val)
        r_v.font.size = Pt(8)
        
        c2 = row.cells[1]
        set_cell_margins(c2, 50, 50, 80, 80)
        p2 = c2.paragraphs[0]
        p2.paragraph_format.space_before = Pt(0)
        p2.paragraph_format.space_after = Pt(0)
        p2.paragraph_format.line_spacing = 1.15
        r_t2 = p2.add_run(f"{col2_title}\n")
        r_t2.font.bold = True
        r_t2.font.size = Pt(8.5)
        r_t2.font.color.rgb = RGBColor(0x00, 0x33, 0x66)
        r_v2 = p2.add_run(col2_val)
        r_v2.font.size = Pt(8)

    # -------------------------------------------------------------
    # SECTION 3: SYSTEM INTERACTION WALKTHROUGH CHECKLIST
    # -------------------------------------------------------------
    doc.add_page_break()
    add_heading_styled(doc, "SECTION 3: SYSTEM INTERACTION & TASK WALKTHROUGH", level=1, space_before=10, space_after=3)
    
    p_scen_inst = doc.add_paragraph()
    p_scen_inst.paragraph_format.space_before = Pt(0)
    p_scen_inst.paragraph_format.space_after = Pt(4)
    p_scen_inst.paragraph_format.line_spacing = 1.15
    p_scen_inst.add_run(
        "To ensure a realistic and grounded evaluation, participants must interact with the live or simulated SolanaWatch "
        "Web Dashboard by performing the five core operational tasks listed below before rating the system:"
    )
    
    task_table = doc.add_table(rows=6, cols=4)
    task_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    task_table.autofit = False
    task_widths = [Inches(0.7), Inches(2.3), Inches(3.0), Inches(1.0)]
    for i, col in enumerate(task_table.columns):
        col.width = task_widths[i]
    set_table_borders(task_table, color="D0D7DE", sz="4")
    
    # Header row
    th_row = task_table.rows[0]
    prevent_row_split(th_row)
    set_repeat_header(th_row)
    headers = ["Task #", "Operational Scenario", "Core User Action Performed", "Completion"]
    for i, title in enumerate(headers):
        cell = th_row.cells[i]
        set_cell_background(cell, "003366")
        set_cell_margins(cell, 60, 60, 80, 80)
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if i in [0, 3] else WD_ALIGN_PARAGRAPH.LEFT
        r = p.add_run(title)
        r.font.bold = True
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        
    tasks = [
        ("Task 1", "Real-Time Telemetry Inspection",
         "Navigated the dashboard to inspect live air temp, air RH, leaf wetness duration, root-zone soil temp, and soil moisture gauges.",
         "[  ] Done\n[  ] Partial"),
        ("Task 2", "Disease Early Warning Interpretation",
         "Observed and interpreted color-coded risk alert banners (Green = Low Risk, Yellow = Moderate Risk, Red = High Risk Alert) for Late Blight and Bacterial Wilt.",
         "[  ] Done\n[  ] Partial"),
        ("Task 3", "Historical Time-Series Trend Analysis",
         "Interacted with historical time-series charts to inspect 24-hour microclimate curves and identify prolonged leaf wetness or warm saturated soil events.",
         "[  ] Done\n[  ] Partial"),
        ("Task 4", "Actionable Agronomic Recommendations",
         "Accessed and reviewed specific farm management advisories triggered by active risk levels (e.g., canopy thinning, drainage trenching, bio-fungicide timing).",
         "[  ] Done\n[  ] Partial"),
        ("Task 5", "Hardware Health & Battery Telemetry",
         "Checked system health status indicators, including LiFePO4 battery voltage, solar MPPT charging status, and MicroSD offline sync connection state.",
         "[  ] Done\n[  ] Partial"),
    ]
    
    for row_idx, (t_no, t_name, t_desc, t_stat) in enumerate(tasks, start=1):
        row = task_table.rows[row_idx]
        prevent_row_split(row)
        bg_col = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
        for i, text in enumerate([t_no, t_name, t_desc, t_stat]):
            cell = row.cells[i]
            set_cell_background(cell, bg_col)
            set_cell_margins(cell, 50, 50, 80, 80)
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.15
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if i in [0, 3] else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(text)
            r.font.size = Pt(8)
            if i == 0:
                r.font.bold = True
                r.font.color.rgb = RGBColor(0x00, 0x33, 0x66)

    # -------------------------------------------------------------
    # SECTION 4: THE 10-ITEM SYSTEM USABILITY SCALE (SUS)
    # -------------------------------------------------------------
    add_heading_styled(doc, "SECTION 4: SYSTEM USABILITY SCALE (SUS) QUESTIONNAIRE", level=1, space_before=12, space_after=3)
    
    p_sus_inst = doc.add_paragraph()
    p_sus_inst.paragraph_format.space_before = Pt(0)
    p_sus_inst.paragraph_format.space_after = Pt(4)
    p_sus_inst.paragraph_format.line_spacing = 1.15
    p_sus_inst.add_run(
        "Instructions: For each of the 10 statements below, please mark [X] in the box that best reflects your immediate, honest reaction. "
        "Do not spend too long on any single statement; your first impression is usually the most accurate.\n\n"
        "Tagalog: Para sa bawat pahayag sa ibaba, mangyaring lagyan ng [X] ang kahon na pinakaangkop sa inyong karanasan sa paggamit ng sistema.\n\n"
        "Rating Scale:\n"
        "  1 = Strongly Disagree (SD) / Lubos na Hindi Sumasang-ayon\n"
        "  2 = Disagree (D) / Hindi Sumasang-ayon\n"
        "  3 = Neutral (N) / Walang Kinikilingan\n"
        "  4 = Agree (A) / Sumasang-ayon\n"
        "  5 = Strongly Agree (SA) / Lubos na Sumasang-ayon"
    )
    p_sus_inst.runs[0].font.size = Pt(8.5)
    
    sus_table = doc.add_table(rows=11, cols=7)
    sus_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    sus_table.autofit = False
    sus_widths = [Inches(0.5), Inches(3.7), Inches(0.55), Inches(0.55), Inches(0.55), Inches(0.55), Inches(0.55)]
    for i, col in enumerate(sus_table.columns):
        col.width = sus_widths[i]
    set_table_borders(sus_table, color="B0BEC5", sz="4")
    
    # Table Header
    sth_row = sus_table.rows[0]
    prevent_row_split(sth_row)
    set_repeat_header(sth_row)
    sus_headers = ["#", "Usability Statement (English & Filipino)", "1\nSD", "2\nD", "3\nN", "4\nA", "5\nSA"]
    for i, title in enumerate(sus_headers):
        cell = sth_row.cells[i]
        set_cell_background(cell, "003366")
        set_cell_margins(cell, 60, 60, 40, 40)
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.0
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if i != 1 else WD_ALIGN_PARAGRAPH.LEFT
        r = p.add_run(title)
        r.font.bold = True
        r.font.size = Pt(8)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        
    sus_items = [
        (1, "I think that I would like to use the SolanaWatch system frequently.",
            "Nais kong gamitin ang SolanaWatch system nang madalas sa aking pagsasaka o trabaho."),
        (2, "I found the system unnecessarily complex.",
            "Pakiramdam ko ay masyadong masalimuot o kumplikado ang sistema nang walang sapat na dahilan."),
        (3, "I thought the system was easy to use.",
            "Pakiramdam ko ay madaling gamitin at unawain ang sistema."),
        (4, "I think that I would need the support of a technical person to be able to use this system.",
            "Sa tingin ko ay kakailanganin ko ang tulong ng isang eksperto o teknikal na tao upang magamit ang sistemang ito."),
        (5, "I found the various functions in this system were well integrated.",
            "Napansin kong maayos na magkakaugnay at nagtutulungan ang iba't ibang bahagi at datos sa sistema."),
        (6, "I thought there was too much inconsistency in this system.",
            "Pakiramdam ko ay labis ang hindi pagtutugma o pabagu-bago sa mga bahagi ng sistema."),
        (7, "I would imagine that most people would learn to use this system very quickly.",
            "Tinataya kong karamihan ng mga magsasaka at gumagamit ay mabilis na matututong gumamit ng sistemang ito."),
        (8, "I found the system very cumbersome (awkward or heavy) to use.",
            "Naramdaman kong napakahirap, nakakaasiwa, o mabigat gamitin ang sistema."),
        (9, "I felt very confident using the system.",
            "Naging lubos akong tiwala at panatag sa aking sarili habang ginagamit ang sistema."),
        (10, "I needed to learn a lot of things before I could get going with this system.",
            "Kinailangan kong mag-aral at mag-alala ng napakaraming bagay bago ko nagawang gamitin ang sistema.")
    ]
    
    for row_idx, (num, eng_text, fil_text) in enumerate(sus_items, start=1):
        row = sus_table.rows[row_idx]
        prevent_row_split(row)
        bg_col = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
        
        # Item Number
        c0 = row.cells[0]
        set_cell_background(c0, bg_col)
        set_cell_margins(c0, 60, 60, 40, 40)
        p0 = c0.paragraphs[0]
        p0.paragraph_format.space_before = Pt(0)
        p0.paragraph_format.space_after = Pt(0)
        p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r0 = p0.add_run(str(num))
        r0.font.bold = True
        r0.font.size = Pt(8.5)
        r0.font.color.rgb = RGBColor(0x00, 0x33, 0x66)
        
        # Item Statement
        c1 = row.cells[1]
        set_cell_background(c1, bg_col)
        set_cell_margins(c1, 60, 60, 60, 60)
        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_before = Pt(0)
        p1.paragraph_format.space_after = Pt(0)
        p1.paragraph_format.line_spacing = 1.15
        r_eng = p1.add_run(f"{eng_text}\n")
        r_eng.font.size = Pt(8)
        r_fil = p1.add_run(fil_text)
        r_fil.font.size = Pt(7.5)
        r_fil.font.italic = True
        r_fil.font.color.rgb = RGBColor(0x55, 0x55, 0x55)
        
        # Scale Checkboxes (Cols 2-6)
        for col_i in range(2, 7):
            cell_box = row.cells[col_i]
            set_cell_background(cell_box, bg_col)
            set_cell_margins(cell_box, 60, 60, 20, 20)
            cell_box.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            p_b = cell_box.paragraphs[0]
            p_b.paragraph_format.space_before = Pt(0)
            p_b.paragraph_format.space_after = Pt(0)
            p_b.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r_b = p_b.add_run("[   ]")
            r_b.font.size = Pt(9)
            r_b.font.color.rgb = RGBColor(0x44, 0x44, 0x44)

    # -------------------------------------------------------------
    # SECTION 5: QUALITATIVE USABILITY FEEDBACK
    # -------------------------------------------------------------
    doc.add_page_break()
    add_heading_styled(doc, "SECTION 5: QUALITATIVE USABILITY & OPEN FEEDBACK", level=1, space_before=10, space_after=3)
    
    p_qual_inst = doc.add_paragraph()
    p_qual_inst.paragraph_format.space_before = Pt(0)
    p_qual_inst.paragraph_format.space_after = Pt(6)
    p_qual_inst.paragraph_format.line_spacing = 1.15
    p_qual_inst.add_run(
        "Please provide brief qualitative insights to help the research team refine the user experience, agronomic value, "
        "and physical interaction design of the SolanaWatch platform:"
    )
    p_qual_inst.runs[0].font.size = Pt(8.5)
    
    qual_table = doc.add_table(rows=3, cols=1)
    qual_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    qual_table.autofit = False
    qual_table.columns[0].width = Inches(7.0)
    set_table_borders(qual_table, color="D0D7DE", sz="4")
    
    questions = [
        ("1. What specific dashboard features, environmental charts, or alerts were the MOST HELPFUL and easiest to understand?",
         "Anong partikular na bahagi ng dashboard, grap, o babala ang pinakanakatulong at pinakamadaling maunawaan?"),
        ("2. Did you encounter any CONFUSION, difficulty, or visual clutter while navigating or reading disease risk levels?",
         "May naging kalituhan ba, kahirapan, o magulong impormasyon habang tinitingnan ang antas ng peligro ng sakit?"),
        ("3. What ENHANCEMENTS or additional features would you recommend for real-world deployment on your farm or community?",
         "Anong mga dagdag na kakayahan, pagbabago sa wika, o disenyo ang iminumungkahi ninyo para sa aktwal na sakahan?")
    ]
    
    for q_idx, (q_eng, q_fil) in enumerate(questions):
        row = qual_table.rows[q_idx]
        prevent_row_split(row)
        cell = row.cells[0]
        set_cell_background(cell, "FFFFFF")
        set_cell_margins(cell, 80, 80, 100, 100)
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        
        r_qe = p.add_run(f"{q_eng}\n")
        r_qe.font.bold = True
        r_qe.font.size = Pt(8.5)
        r_qe.font.color.rgb = RGBColor(0x00, 0x33, 0x66)
        
        r_qf = p.add_run(f"{q_fil}\n\n")
        r_qf.font.size = Pt(8)
        r_qf.font.italic = True
        r_qf.font.color.rgb = RGBColor(0x55, 0x55, 0x55)
        
        # Ruled blank lines for user response
        r_lines = p.add_run(
            "___________________________________________________________________________________________________\n\n"
            "___________________________________________________________________________________________________\n\n"
            "___________________________________________________________________________________________________"
        )
        r_lines.font.size = Pt(8)
        r_lines.font.color.rgb = RGBColor(0xBD, 0xC3, 0xC7)

    # -------------------------------------------------------------
    # SECTION 6: EVALUATOR SCORING & BENCHMARKING GUIDE
    # -------------------------------------------------------------
    add_heading_styled(doc, "SECTION 6: EVALUATOR SCORING GUIDE & USABILITY BENCHMARKS (AUDIT REFERENCE)", level=1, space_before=12, space_after=3)
    
    p_score_intro = doc.add_paragraph()
    p_score_intro.paragraph_format.space_before = Pt(0)
    p_score_intro.paragraph_format.space_after = Pt(4)
    p_score_intro.paragraph_format.line_spacing = 1.15
    p_score_intro.add_run(
        "Note for Evaluators & Capstone Panel: The System Usability Scale yields a single composite score on a scale of 0 to 100 "
        "(Brooke, 1996). It is not a percentage, but a normalized percentile ranking. Follow the standardized calculation below:"
    )
    p_score_intro.runs[0].font.size = Pt(8)
    p_score_intro.runs[0].font.italic = True
    
    calc_table = doc.add_table(rows=1, cols=2)
    calc_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    calc_table.autofit = False
    calc_widths = [Inches(4.2), Inches(2.8)]
    for i, col in enumerate(calc_table.columns):
        col.width = calc_widths[i]
    set_table_borders(calc_table, color="B0BEC5", sz="4")
    
    c_calc1 = calc_table.rows[0].cells[0]
    set_cell_background(c_calc1, "F8FAFC")
    set_cell_margins(c_calc1, 60, 60, 80, 80)
    p_c1 = c_calc1.paragraphs[0]
    p_c1.paragraph_format.space_before = Pt(0)
    p_c1.paragraph_format.space_after = Pt(0)
    p_c1.paragraph_format.line_spacing = 1.15
    r_f_t = p_c1.add_run("Standard Brooke (1996) SUS Formula:\n")
    r_f_t.font.bold = True
    r_f_t.font.size = Pt(8.5)
    r_f_t.font.color.rgb = RGBColor(0x00, 0x33, 0x66)
    
    r_f_b = p_c1.add_run(
        "1. For Odd Items (1, 3, 5, 7, 9):\n"
        "    Score Contribution = Scale Position − 1 (e.g., Rating 5 contributes 4)\n"
        "2. For Even Items (2, 4, 6, 8, 10):\n"
        "    Score Contribution = 5 − Scale Position (e.g., Rating 1 contributes 4)\n"
        "3. Composite SUS Score:\n"
        "    Total SUS = [ Sum of all 10 item contributions ] × 2.5\n"
        "    Score Range: 0 to 100 points."
    )
    r_f_b.font.size = Pt(8)
    
    c_calc2 = calc_table.rows[0].cells[1]
    set_cell_background(c_calc2, "FFFFFF")
    set_cell_margins(c_calc2, 60, 60, 80, 80)
    p_c2 = c_calc2.paragraphs[0]
    p_c2.paragraph_format.space_before = Pt(0)
    p_c2.paragraph_format.space_after = Pt(0)
    p_c2.paragraph_format.line_spacing = 1.15
    
    r_res_t = p_c2.add_run("Evaluator Official Score Card:\n")
    r_res_t.font.bold = True
    r_res_t.font.size = Pt(8.5)
    r_res_t.font.color.rgb = RGBColor(0x00, 0x33, 0x66)
    
    r_res_b = p_c2.add_run(
        "• Sum of Odd Contributions (X): ____\n"
        "• Sum of Even Contributions (Y): ____\n"
        "• Total Raw Sum (X + Y): _________\n"
        "• Calculated SUS Score: ________ / 100\n"
        "• Adjective Rating: _______________\n"
        "• ISO/IEC Usability Pass: [  ] YES  [  ] NO"
    )
    r_res_b.font.size = Pt(8)

    # Benchmarking Grading Table
    add_heading_styled(doc, "SUS Score Interpretation Scale (Bangor, Kortum, & Miller, 2008; Sauro & Lewis, 2012):", level=3, space_before=6, space_after=3)
    
    bench_table = doc.add_table(rows=5, cols=5)
    bench_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    bench_table.autofit = False
    b_widths = [Inches(1.2), Inches(1.0), Inches(1.3), Inches(1.8), Inches(1.7)]
    for i, col in enumerate(bench_table.columns):
        col.width = b_widths[i]
    set_table_borders(bench_table, color="B0BEC5", sz="4")
    
    b_th = bench_table.rows[0]
    prevent_row_split(b_th)
    b_headers = ["SUS Score Range", "Letter Grade", "Adjective Rating", "Acceptability Status", "SolanaWatch Compliance"]
    for i, title in enumerate(b_headers):
        c = b_th.cells[i]
        set_cell_background(c, "1B365D")
        set_cell_margins(c, 50, 50, 60, 60)
        p = c.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(title)
        r.font.bold = True
        r.font.size = Pt(8)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        
    bench_rows = [
        ("80.3 – 100.0", "Grade A", "Excellent / Best Imaginable", "Highly Acceptable", "★ Target Design Goal (≥ 80.0)"),
        ("68.0 – 80.2", "Grade B / C+", "Good (Above Average)", "Acceptable (Industry Mean = 68.0)", "Meets Minimum Baseline"),
        ("51.0 – 67.9", "Grade C / D", "OK / Marginal", "Marginally Acceptable", "Requires Interface Revision"),
        ("0.0 – 50.9", "Grade F", "Poor / Unacceptable", "Not Acceptable", "Critical Usability Failure")
    ]
    
    for row_idx, (r_rng, r_grd, r_adj, r_acc, r_sol) in enumerate(bench_rows, start=1):
        row = bench_table.rows[row_idx]
        prevent_row_split(row)
        bg = "E8F8F5" if row_idx == 1 else ("FFFFFF" if row_idx % 2 == 0 else "F8FAFC")
        for i, text in enumerate([r_rng, r_grd, r_adj, r_acc, r_sol]):
            c = row.cells[i]
            set_cell_background(c, bg)
            set_cell_margins(c, 40, 40, 60, 60)
            p = c.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(text)
            r.font.size = Pt(8)
            if row_idx == 1:
                r.font.bold = True
                if i == 4:
                    r.font.color.rgb = RGBColor(0x16, 0xA0, 0x85)

    # -------------------------------------------------------------
    # SECTION 7: PARTICIPANT CONSENT SIGN-OFF & ENDORSEMENT
    # -------------------------------------------------------------
    add_heading_styled(doc, "SECTION 7: PARTICIPANT ACKNOWLEDGEMENT & EVALUATOR SIGN-OFF", level=1, space_before=10, space_after=3)
    
    p_ack = doc.add_paragraph()
    p_ack.paragraph_format.space_before = Pt(0)
    p_ack.paragraph_format.space_after = Pt(6)
    p_ack.paragraph_format.line_spacing = 1.15
    p_ack.add_run(
        "Declaration of Participant: I hereby confirm that I have interacted with the SolanaWatch system prototype and have completed "
        "this questionnaire voluntarily and truthfully according to my genuine user experience."
    )
    p_ack.runs[0].font.size = Pt(8)
    p_ack.runs[0].font.italic = True
    
    sig_table = doc.add_table(rows=1, cols=2)
    sig_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    sig_table.autofit = False
    sig_widths = [Inches(3.5), Inches(3.5)]
    for i, col in enumerate(sig_table.columns):
        col.width = sig_widths[i]
    set_table_borders(sig_table, color="D0D7DE", sz="4")
    
    # Left: Participant Sign-off
    c_sig1 = sig_table.rows[0].cells[0]
    set_cell_background(c_sig1, "FFFFFF")
    set_cell_margins(c_sig1, 80, 80, 100, 100)
    p_s1 = c_sig1.paragraphs[0]
    p_s1.paragraph_format.space_before = Pt(0)
    p_s1.paragraph_format.space_after = Pt(0)
    p_s1.paragraph_format.line_spacing = 1.15
    r_s1_t = p_s1.add_run("Evaluated by (Participant):\n\n\n\n")
    r_s1_t.font.bold = True
    r_s1_t.font.size = Pt(8.5)
    r_s1_b = p_s1.add_run(
        "_________________________________________\n"
        "Signature over Printed Name\n\n"
        "Date Signed: ____________________________"
    )
    r_s1_b.font.size = Pt(8)
    
    # Right: Evaluator / Proponent Sign-off
    c_sig2 = sig_table.rows[0].cells[1]
    set_cell_background(c_sig2, "FFFFFF")
    set_cell_margins(c_sig2, 80, 80, 100, 100)
    p_s2 = c_sig2.paragraphs[0]
    p_s2.paragraph_format.space_before = Pt(0)
    p_s2.paragraph_format.space_after = Pt(0)
    p_s2.paragraph_format.line_spacing = 1.15
    r_s2_t = p_s2.add_run("Administered & Verified by (Capstone Proponent):\n\n\n\n")
    r_s2_t.font.bold = True
    r_s2_t.font.size = Pt(8.5)
    r_s2_b = p_s2.add_run(
        "_________________________________________\n"
        "Lead Usability Evaluator (UST-CICS)\n\n"
        "Date Verified: __________________________"
    )
    r_s2_b.font.size = Pt(8)

    # Save document
    output_path = r"C:\Users\agabu\Downloads\CODE PROJECTS\SOLANAWATCH\paperwork\evaluation-sus\SolanaWatch_System_Usability_Scale_Questionnaire.docx"
    doc.save(output_path)
    print(f"Successfully generated SUS Questionnaire DOCX at: {output_path}")

if __name__ == "__main__":
    create_sus_questionnaire()
