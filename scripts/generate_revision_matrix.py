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

def set_table_borders(table, color="000000", sz="4", val="single"):
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

def create_revision_matrix_docx(output_path):
    doc = docx.Document()
    
    # 0.75-inch margins
    for section in doc.sections:
        section.top_margin = Inches(0.75)
        section.bottom_margin = Inches(0.75)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)
        
    # Styles
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Arial'
    normal_style.font.size = Pt(9.5)
    normal_style.font.color.rgb = RGBColor(0x11, 0x11, 0x11)
    
    # Logos and Header
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
    p_mid1 = cell_center.paragraphs[0]
    p_mid1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_mid1.paragraph_format.space_before = Pt(0)
    p_mid1.paragraph_format.space_after = Pt(0)
    p_mid1.paragraph_format.line_spacing = 1.15
    
    r_ust = p_mid1.add_run("UNIVERSITY OF SANTO TOMAS\n")
    r_ust.font.name = 'Arial'
    r_ust.font.size = Pt(11.5)
    r_ust.font.bold = True
    
    r_cics = p_mid1.add_run("COLLEGE OF INFORMATION AND COMPUTING SCIENCES\nDEPARTMENT OF INFORMATION TECHNOLOGY")
    r_cics.font.name = 'Arial'
    r_cics.font.size = Pt(10)
    r_cics.font.bold = True
    
    # Right logo (CICS)
    cell_right = row.cells[2]
    p_right = cell_right.paragraphs[0]
    p_right.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    if os.path.exists(cics_logo):
        p_right.add_run().add_picture(cics_logo, width=Inches(0.85))
        
    for cell in row.cells:
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        set_cell_margins(cell, top=0, bottom=40, left=0, right=0)
        
    # Title
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(10)
    p_title.paragraph_format.space_after = Pt(10)
    r_mat = p_title.add_run("REVISION MATRIX")
    r_mat.font.name = 'Arial'
    r_mat.font.size = Pt(12.5)
    r_mat.font.bold = True

    # Metadata Table
    meta_table = doc.add_table(rows=5, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(meta_table, color="000000", sz="4", val="single")
    
    meta_widths = [Inches(1.8), Inches(5.2)]
    for row in meta_table.rows:
        prevent_row_split(row)
        for i, cell in enumerate(row.cells):
            cell.width = meta_widths[i]
            set_cell_margins(cell, top=70, bottom=70, left=110, right=110)
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            
    meta_data = [
        ("PROGRAM:", "Bachelor of Science in Information Technology"),
        ("DEFENSE DATE:", "July 20, 2026"),
        ("TITLE:", "SolanaWatch: An IoT-Based Disease Early Warning System for Soil-Grown Solanaceae Crops"),
        ("MEMBERS:", "1.  Morales, Simeon Agabus S.\n2.  Rapada, Raven M.\n3.  Hernandez, Andrei S.\n4.  Eugenio, Vince Angelo"),
        ("ADVISER:", "PROF. EUGENIA R. ZHUO, DIT")
    ]
    
    for i, (label, val) in enumerate(meta_data):
        c0 = meta_table.rows[i].cells[0]
        c1 = meta_table.rows[i].cells[1]
        
        p0 = c0.paragraphs[0]
        p0.paragraph_format.space_before = Pt(0)
        p0.paragraph_format.space_after = Pt(0)
        p0.paragraph_format.line_spacing = 1.15
        r0 = p0.add_run(label)
        r0.font.name = 'Arial'
        r0.font.size = Pt(9.5)
        r0.font.bold = True
        
        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_before = Pt(0)
        p1.paragraph_format.space_after = Pt(0)
        p1.paragraph_format.line_spacing = 1.15
        r1 = p1.add_run(val)
        r1.font.name = 'Arial'
        r1.font.size = Pt(9.5)
        if label == "ADVISER:":
            r1.font.bold = True
            
    doc.add_paragraph().paragraph_format.space_after = Pt(4)
    
    # 24-point Revision Matrix Data (Simple, Clear & Direct Words)
    revisions = [
        (
            "Add a comparative analysis of ESP32, Arduino Leonardo, and Raspberry Pi in Chapter 2.",
            "Added a comparison of ESP32, Arduino Leonardo, and Raspberry Pi 4 in Chapter 2, evaluating their processor speed, memory, power consumption, and outdoor field suitability.",
            "Page 21, Page 22, Pages 88–90"
        ),
        (
            "Justify the selection of the ESP32 based on SolanaWatch's requirements.",
            "Explained why ESP32 was chosen based on its dual-core processor, built-in Wi-Fi, low-power deep sleep mode, low cost, and support for multiple sensor pins.",
            "Page 22, Page 32, Page 41, Page 57"
        ),
        (
            "Specify the exact models and specifications of all sensors and components.",
            "Updated the hardware list and Chapter 2 with exact part models: DHT22 (air temp/RH), DS18B20 (soil temp), Capacitive Soil Moisture v1.2, RS485 Leaf Wetness sensor, MicroSD module, 20W solar panel, MPPT controller, and 12.8V LiFePO4 battery.",
            "Pages 22–26, Pages 41–49"
        ),
        (
            "Reassess the 3.7 V 2600 mAh Li-ion battery for 24/7 operation.",
            "Replaced the 3.7V 2600 mAh battery with a 12.8V 12Ah LiFePO4 battery pack after a power calculation showed the single cell cannot support 24/7 continuous operation.",
            "Pages 25–26, Page 44, Page 68"
        ),
        (
            "Investigate the use of a solar-assisted power system for continuous operation.",
            "Added a solar-assisted power system using a 20W solar panel and an MPPT charge controller to allow continuous 24/7 field operation without grid power.",
            "Pages 25–26, Page 44, Pages 57–58, Page 68"
        ),
        (
            "Conduct actual power-consumption testing of the complete prototype.",
            "Included power measurement test cases in the test plan to test the current draw of the ESP32 during active Wi-Fi sending, sensor reading, and deep sleep.",
            "Page 26, Page 68, Pages 78–80"
        ),
        (
            "Determine the appropriate solar panel and battery capacity based on the measured power requirement.",
            "Calculated the solar panel size (20W) and battery size (12.8V 12Ah / 153.6 Wh) using Philippine sunlight hours and the system's estimated daily power use of 2.30 Wh/day.",
            "Page 26, Page 68"
        ),
        (
            "Clarify the difference between sensor coverage and wireless communication range.",
            "Clarified that sensor coverage is the localized area around the sensors (5 to 15 meters), while wireless range is the Wi-Fi distance between the ESP32 and the router (30 to 50 meters).",
            "Pages 27–28"
        ),
        (
            "Conduct an experimental test to determine the actual communication range of the ESP32.",
            "Added a test case in Chapter 3 to test Wi-Fi signal strength (RSSI) and packet delivery at 5m, 10m, 20m, 30m, and 50m distances.",
            "Page 28, Page 79, Page 81"
        ),
        (
            "Provide RRL support for the selected environmental parameters.",
            "Added research citations showing how air temperature, humidity, leaf wetness, soil temperature, and soil moisture affect Late Blight and Bacterial Wilt.",
            "Pages 5–6, Pages 18–21, Pages 23–24, Pages 31–32"
        ),
        (
            "Provide the research basis for all disease-risk thresholds and formulas.",
            "Added research references for the disease thresholds, using Wallin's Severity Values for Late Blight and a hydrothermal soil formula for Bacterial Wilt.",
            "Pages 19–20, Pages 30–31, Pages 61–63, Page 65"
        ),
        (
            "Clarify how multiple environmental parameters are combined to determine disease risk.",
            "Explained how sensor readings are combined into decision rules to classify disease risk into Low, Moderate, and High alert levels.",
            "Pages 30–31, Page 57, Pages 61–63, Page 65, Page 72"
        ),
        (
            "Clarify that SolanaWatch performs disease-risk assessment rather than direct disease diagnosis.",
            "Clarified throughout the paper that SolanaWatch assesses environmental disease risk and favorable weather conditions, rather than diagnosing actual plant infection.",
            "Page 8, Page 14, Page 15, Pages 30–31"
        ),
        (
            "Identify the intended users of SolanaWatch.",
            "Identified smallholder farmers as primary users, and agricultural technicians, extension workers, and researchers as secondary users.",
            "Pages 12–14, Page 51, Pages 85–87"
        ),
        (
            "Clearly label all components and functions in the circuit and system diagrams.",
            "Updated and labeled all system diagrams and circuit schematics with component names, GPIO pin numbers, and power connections.",
            "Page 13, Page 58, Page 64, Page 66, Page 71, Page 74"
        ),
        (
            "Evaluate using a PCB instead of a breadboard for the final prototype.",
            "Added an explanation for using a custom PCB instead of a breadboard to ensure durable, secure connections and prevent loose wires outdoors.",
            "Page 28, Page 32, Page 49"
        ),
        (
            "Add test cases for sensor accuracy, data transmission, offline logging, and data synchronization.",
            "Added a complete test cases table in Chapter 3 covering sensor accuracy, Wi-Fi sending, offline SD card logging, and cloud data sync.",
            "Pages 76–82"
        ),
        (
            "Explain how data loss and duplication will be prevented during network interruptions.",
            "Explained that data is saved to a MicroSD card during network loss, uploaded in batches upon reconnecting, and deduplicated in the database using unique timestamps.",
            "Pages 26–27, Page 39, Pages 58–59, Pages 66–67"
        ),
        (
            "Establish a calibration procedure for all environmental sensors.",
            "Added calibration steps for sensors, including dry/wet calibration for soil moisture, ice-water testing for soil temperature, and salt chamber testing for humidity.",
            "Pages 24–25, Pages 76–77"
        ),
        (
            "Specify the Solanaceae crops and field conditions covered by the study.",
            "Specified four Solanaceae crops (tomato, eggplant, pepper, and potato) under open-field and screenhouse soil conditions in the Philippines.",
            "Pages 5–6, Page 15, Pages 17–19"
        ),
        (
            "Evaluate the enclosure and components for outdoor agricultural conditions.",
            "Selected an IP65/IP66 weatherproof enclosure box with rubber gaskets, cable glands, desiccant packs, and a Stevenson shield for outdoor protection.",
            "Page 28, Page 42, Page 45, Page 70, Page 74"
        ),
        (
            "Add a reliability testing plan for continuous operation.",
            "Added a 7-day continuous field test plan, hardware watchdog timer auto-reset, and water spray testing to ensure system reliability.",
            "Page 39, Pages 77–78, Pages 81–82"
        ),
        (
            "Provide a validation procedure for solar charging and battery autonomy.",
            "Added a 3-day (72-hour) battery test without sunlight and a solar charging test under daylight to verify battery life and charging performance.",
            "Page 68, Page 77, Page 80"
        ),
        (
            "Support all technical claims and component selections with recent RRL, datasheets, calculations, or experimental results.",
            "Supported all hardware choices, formulas, and technical details with 2020–2026 research papers, official datasheets, and calculations in APA 7th format.",
            "Pages 5–33, Pages 41–50, Pages 57–68, Pages 93–101"
        )
    ]
    
    # Main Matrix Table
    matrix_table = doc.add_table(rows=len(revisions) + 1, cols=3)
    matrix_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(matrix_table, color="000000", sz="4", val="single")
    
    # Set repeat header row on every page
    header_tr = matrix_table.rows[0]._tr.get_or_add_trPr()
    header_tr.append(OxmlElement('w:tblHeader'))
    
    col_widths = [Inches(2.0), Inches(3.8), Inches(1.2)]
    for row in matrix_table.rows:
        prevent_row_split(row)
        for i, cell in enumerate(row.cells):
            cell.width = col_widths[i]
            
    # Table Header Row
    headers = ["COMMENTS /\nRECOMMENDATIONS", "ACTION TAKEN", "PAGE\nREFLECTED"]
    for i, h in enumerate(headers):
        cell = matrix_table.rows[0].cells[i]
        set_cell_margins(cell, top=90, bottom=90, left=90, right=90)
        set_cell_background(cell, "F0F0F0")
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(h)
        r.font.name = 'Arial'
        r.font.size = Pt(9.5)
        r.font.bold = True

    # Fill Table Rows
    for idx, (comm, act, pgs) in enumerate(revisions):
        row = matrix_table.rows[idx + 1]
        prevent_row_split(row)
        
        # Col 1: Comments
        c0 = row.cells[0]
        set_cell_margins(c0, top=70, bottom=70, left=90, right=90)
        c0.vertical_alignment = WD_ALIGN_VERTICAL.TOP
        p0 = c0.paragraphs[0]
        p0.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p0.paragraph_format.space_before = Pt(0)
        p0.paragraph_format.space_after = Pt(0)
        p0.paragraph_format.line_spacing = 1.15
        r0 = p0.add_run(comm)
        r0.font.name = 'Arial'
        r0.font.size = Pt(9)
        
        # Col 2: Action Taken
        c1 = row.cells[1]
        set_cell_margins(c1, top=70, bottom=70, left=90, right=90)
        c1.vertical_alignment = WD_ALIGN_VERTICAL.TOP
        p1 = c1.paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p1.paragraph_format.space_before = Pt(0)
        p1.paragraph_format.space_after = Pt(0)
        p1.paragraph_format.line_spacing = 1.15
        r1 = p1.add_run(act)
        r1.font.name = 'Arial'
        r1.font.size = Pt(9)
        
        # Col 3: Page Reflected
        c2 = row.cells[2]
        set_cell_margins(c2, top=70, bottom=70, left=90, right=90)
        c2.vertical_alignment = WD_ALIGN_VERTICAL.TOP
        p2 = c2.paragraphs[0]
        p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p2.paragraph_format.space_before = Pt(0)
        p2.paragraph_format.space_after = Pt(0)
        p2.paragraph_format.line_spacing = 1.15
        r2 = p2.add_run(pgs)
        r2.font.name = 'Arial'
        r2.font.size = Pt(9)

    doc.add_paragraph().paragraph_format.space_after = Pt(10)
    
    # Panel Approval Table (3 columns)
    panel_table = doc.add_table(rows=3, cols=3)
    panel_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(panel_table, color="000000", sz="4", val="single")
    
    panel_widths = [Inches(2.33), Inches(2.33), Inches(2.34)]
    for row in panel_table.rows:
        prevent_row_split(row)
        for i, cell in enumerate(row.cells):
            cell.width = panel_widths[i]
            
    # Row 1: Merged Header
    r0 = panel_table.rows[0]
    r0.cells[0].merge(r0.cells[1]).merge(r0.cells[2])
    c_hdr = r0.cells[0]
    set_cell_margins(c_hdr, top=70, bottom=70, left=90, right=90)
    set_cell_background(c_hdr, "F0F0F0")
    p_hdr = c_hdr.paragraphs[0]
    p_hdr.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_hdr = p_hdr.add_run("PANEL MEMBERS")
    r_hdr.font.name = 'Arial'
    r_hdr.font.size = Pt(9.5)
    r_hdr.font.bold = True
    
    # Row 2: Panel Names
    panel_names = [
        "INST. GABRIEL EMANUEL D. MONTANO",
        "PROF. NOEL E. ESTRELLA",
        "MR. KARLO ANGELO TINO"
    ]
    r1 = panel_table.rows[1]
    for i, name in enumerate(panel_names):
        cell = r1.cells[i]
        set_cell_margins(cell, top=140, bottom=50, left=50, right=50)
        cell.vertical_alignment = WD_ALIGN_VERTICAL.BOTTOM
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(name)
        r.font.name = 'Arial'
        r.font.size = Pt(9)
        r.font.bold = True

    # Row 3: Designations / Signature Labels
    panel_labels = [
        "NAME AND SIGN OF LEAD PANEL",
        "NAME AND SIGN OF MEMBER PANEL 1",
        "NAME AND SIGN OF MEMBER PANEL 2"
    ]
    r2 = panel_table.rows[2]
    for i, label in enumerate(panel_labels):
        cell = r2.cells[i]
        set_cell_margins(cell, top=50, bottom=90, left=50, right=50)
        cell.vertical_alignment = WD_ALIGN_VERTICAL.TOP
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(label)
        r.font.name = 'Arial'
        r.font.size = Pt(8)
        
    doc.save(output_path)
    print(f"Revision Matrix successfully created at: {output_path}")

if __name__ == "__main__":
    out = r"C:\Users\agabu\Downloads\CODE PROJECTS\SOLANAWATCH\paperwork\defense-and-revisions\SolanaWatch_Revision_Matrix_Official.docx"
    create_revision_matrix_docx(out)
    out_dl = r"C:\Users\agabu\Downloads\SolanaWatch_Revision_Matrix_Official.docx"
    create_revision_matrix_docx(out_dl)
