import os
import re
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def set_cell_background(cell, fill_color="F2F2F2"):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)

def add_formatted_runs(p, text, default_font_size=12, is_bold=False):
    tokens = re.split(r'(\*\*.*?\*\*|`.*?`|\*.*?\*)', text)
    for token in tokens:
        if not token:
            continue
        if token.startswith('**') and token.endswith('**'):
            run = p.add_run(token[2:-2])
            run.bold = True
            run.font.name = 'Times New Roman'
            run.font.size = Pt(default_font_size)
            run.font.color.rgb = RGBColor(0, 0, 0)
        elif token.startswith('*') and token.endswith('*'):
            run = p.add_run(token[1:-1])
            run.italic = True
            run.font.name = 'Times New Roman'
            run.font.size = Pt(default_font_size)
            run.font.color.rgb = RGBColor(0, 0, 0)
        elif token.startswith('`') and token.endswith('`'):
            run = p.add_run(token[1:-1])
            run.font.name = 'Times New Roman'
            run.font.size = Pt(default_font_size)
            run.font.bold = True
            run.font.color.rgb = RGBColor(0, 0, 0)
        else:
            run = p.add_run(token)
            run.bold = is_bold
            run.font.name = 'Times New Roman'
            run.font.size = Pt(default_font_size)
            run.font.color.rgb = RGBColor(0, 0, 0)

def add_body_paragraph(doc, text, is_bib=False):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.5
    
    if is_bib:
        # APA 7th Hanging Indent
        p.paragraph_format.left_indent = Inches(0.5)
        p.paragraph_format.first_line_indent = Inches(-0.5)
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    else:
        # Standard Academic Research Paper First-Line Indent
        p.paragraph_format.first_line_indent = Inches(0.5)
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        
    add_formatted_runs(p, text, default_font_size=12)
    return p

def render_table(doc, table_rows):
    if not table_rows:
        return
    num_rows = len(table_rows)
    num_cols = max(len(r) for r in table_rows)
    table = doc.add_table(rows=num_rows, cols=num_cols)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.style = 'Table Grid'
    
    for row_idx, row_data in enumerate(table_rows):
        row = table.rows[row_idx]
        is_header = (row_idx == 0)
        for col_idx in range(num_cols):
            cell = row.cells[col_idx]
            text = row_data[col_idx] if col_idx < len(row_data) else ""
            cell.text = ""
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(3)
            p.paragraph_format.space_after = Pt(3)
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
            
            add_formatted_runs(p, text, default_font_size=10.5 if num_cols > 4 else 11.5)
            
            if is_header:
                set_cell_background(cell, "EAEAEA")
                for r in p.runs:
                    r.font.bold = True
                    r.font.name = 'Times New Roman'
                    r.font.color.rgb = RGBColor(0, 0, 0)
            else:
                set_cell_background(cell, "FFFFFF")
                for r in p.runs:
                    r.font.name = 'Times New Roman'
                    r.font.color.rgb = RGBColor(0, 0, 0)
            set_cell_margins(cell, top=80, bottom=80, left=120, right=120)

    p_spacer = doc.add_paragraph()
    p_spacer.paragraph_format.space_after = Pt(6)

def convert_manuscript(md_filepaths, output_docx_path, doc_title, fig_dir):
    doc = Document()
    
    # 1.0 inch margins all around
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
    
    # Base Normal Style: Times New Roman, 12pt, 1.5 line spacing
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(12)
    normal_style.font.color.rgb = RGBColor(0, 0, 0)

    # Document Header Title
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(12)
    title_p.paragraph_format.space_after = Pt(18)
    title_p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_run = title_p.add_run(doc_title)
    title_run.bold = True
    title_run.font.size = Pt(14)
    title_run.font.name = 'Times New Roman'

    figure_map = {
        "context diagram": os.path.join(fig_dir, "figure1_context_diagram.png"),
        "activity diagram": os.path.join(fig_dir, "figure2_activity_diagram.png"),
        "prototyping": os.path.join(fig_dir, "figure3_prototyping_model.png"),
        "architecture diagram": os.path.join(fig_dir, "figure4_system_architecture.png"),
        "entity relation": os.path.join(fig_dir, "figure5_er_diagram.png"),
        "circuit schematic": os.path.join(fig_dir, "figure6_circuit_schematic.png"),
    }

    for md_path in md_filepaths:
        if not os.path.exists(md_path):
            continue
        
        is_bibliography_file = "Bibliography" in md_path
        
        with open(md_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        in_table = False
        table_rows = []
        in_code_block = False
        code_lines = []

        for line in lines:
            raw_line = line.rstrip('\r\n')
            stripped = raw_line.strip()

            # Handle Code Blocks & Diagrams
            if stripped.startswith('```') or stripped.startswith('++++'):
                if in_code_block:
                    # Check if code block contains ASCII diagram keywords that map to real images
                    full_code_text = '\n'.join(code_lines).lower()
                    matched_fig = None
                    for key, img_path in figure_map.items():
                        if key in full_code_text and os.path.exists(img_path):
                            matched_fig = img_path
                            break
                    
                    if matched_fig:
                        # Insert actual diagram image
                        p_img = doc.add_paragraph()
                        p_img.paragraph_format.space_before = Pt(8)
                        p_img.paragraph_format.space_after = Pt(6)
                        p_img.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
                        p_img.add_run().add_picture(matched_fig, width=Inches(6.0))
                    else:
                        # Standard code/formula block
                        p = doc.add_paragraph()
                        p.paragraph_format.space_before = Pt(4)
                        p.paragraph_format.space_after = Pt(6)
                        p.paragraph_format.left_indent = Inches(0.4)
                        run = p.add_run('\n'.join(code_lines))
                        run.font.name = 'Times New Roman'
                        run.font.size = Pt(11)
                    
                    code_lines = []
                    in_code_block = False
                else:
                    if in_table and table_rows:
                        render_table(doc, table_rows)
                        table_rows = []
                        in_table = False
                    in_code_block = True
                    code_lines = []
                continue

            if in_code_block:
                code_lines.append(raw_line)
                continue

            # Handle Tables
            if stripped.startswith('|') and stripped.endswith('|'):
                if re.match(r'^\|(\s*:?-+:?\s*\|)+$', stripped):
                    continue
                in_table = True
                cols = [c.strip() for c in stripped[1:-1].split('|')]
                table_rows.append(cols)
                continue
            else:
                if in_table and table_rows:
                    render_table(doc, table_rows)
                    table_rows = []
                    in_table = False

            if not stripped:
                continue

            # Headings (Times New Roman, Bold, No first-line indent)
            if stripped.startswith('# '):
                h = doc.add_paragraph()
                h.paragraph_format.space_before = Pt(18)
                h.paragraph_format.space_after = Pt(8)
                h.paragraph_format.keep_with_next = True
                h.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
                run = h.add_run(stripped[2:])
                run.bold = True
                run.font.size = Pt(14)
                run.font.name = 'Times New Roman'
            elif stripped.startswith('## '):
                h = doc.add_paragraph()
                h.paragraph_format.space_before = Pt(14)
                h.paragraph_format.space_after = Pt(6)
                h.paragraph_format.keep_with_next = True
                h.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
                run = h.add_run(stripped[3:])
                run.bold = True
                run.font.size = Pt(13)
                run.font.name = 'Times New Roman'
            elif stripped.startswith('### '):
                h = doc.add_paragraph()
                h.paragraph_format.space_before = Pt(10)
                h.paragraph_format.space_after = Pt(4)
                h.paragraph_format.keep_with_next = True
                h.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
                run = h.add_run(stripped[4:])
                run.bold = True
                run.font.size = Pt(12)
                run.font.name = 'Times New Roman'
            elif stripped.startswith('#### '):
                h = doc.add_paragraph()
                h.paragraph_format.space_before = Pt(8)
                h.paragraph_format.space_after = Pt(3)
                h.paragraph_format.keep_with_next = True
                run = h.add_run(stripped[5:])
                run.bold = True
                run.font.size = Pt(12)
                run.font.name = 'Times New Roman'
            elif stripped.startswith('**Table ') or stripped.startswith('Table '):
                # Table Caption (Above table, bold, no indent)
                p = doc.add_paragraph()
                p.paragraph_format.space_before = Pt(12)
                p.paragraph_format.space_after = Pt(4)
                p.paragraph_format.keep_with_next = True
                p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
                add_formatted_runs(p, stripped, default_font_size=12, is_bold=True)
            elif stripped.startswith('**Figure ') or stripped.startswith('Figure '):
                # Figure Caption (Below figure, center aligned, bold, no indent)
                p = doc.add_paragraph()
                p.paragraph_format.space_before = Pt(4)
                p.paragraph_format.space_after = Pt(10)
                p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
                add_formatted_runs(p, stripped, default_font_size=12, is_bold=True)
            elif stripped.startswith('- ') or stripped.startswith('* '):
                # Bullet list: left indent 0.5 in, no first line indent
                p = doc.add_paragraph(style='List Bullet')
                p.paragraph_format.space_after = Pt(3)
                p.paragraph_format.line_spacing = 1.5
                add_formatted_runs(p, stripped[2:], default_font_size=12)
            elif re.match(r'^\d+\.\s', stripped):
                # Numbered list: left indent 0.5 in, no first line indent
                p = doc.add_paragraph(style='List Number')
                p.paragraph_format.space_after = Pt(3)
                p.paragraph_format.line_spacing = 1.5
                match = re.match(r'^\d+\.\s(.*)$', stripped)
                add_formatted_runs(p, match.group(1), default_font_size=12)
            elif stripped.startswith('---'):
                continue
            else:
                # Regular body paragraph with 0.5-inch first-line indent and justified alignment
                add_body_paragraph(doc, stripped, is_bib=is_bibliography_file)

        if in_table and table_rows:
            render_table(doc, table_rows)
            table_rows = []
        if in_code_block and code_lines:
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Inches(0.4)
            run = p.add_run('\n'.join(code_lines))
            run.font.name = 'Times New Roman'
            run.font.size = Pt(11)
            code_lines = []

    doc.save(output_docx_path)
    print(f"Successfully generated formatted DOCX with embedded diagrams: {output_docx_path}")

if __name__ == "__main__":
    artifact_dir = r"C:\Users\agabu\.gemini\antigravity-cli\brain\d2b1ae52-6063-4142-a38a-b997f915c996"
    out_dir = r"C:\Users\agabu\Downloads\CODE PROJECTS\SOLANAWATCH\paperwork"
    fig_dir = r"C:\Users\agabu\Downloads\CODE PROJECTS\SOLANAWATCH\figures"
    
    # 1. Main Manuscript DOCX (Chapters 1 to 3 + Bibliography)
    manuscript_files = [
        os.path.join(artifact_dir, "SolanaWatch_Chapter_1_Revised.md"),
        os.path.join(artifact_dir, "SolanaWatch_Chapter_2_Revised.md"),
        os.path.join(artifact_dir, "SolanaWatch_Chapter_3_Revised.md"),
        os.path.join(artifact_dir, "SolanaWatch_Bibliography_APA7.md"),
    ]
    manuscript_out = os.path.join(out_dir, "proposal", "SolanaWatch_Proposal_Chapters_1-3_REVISED.docx")
    convert_manuscript(manuscript_files, manuscript_out, "SolanaWatch: Capstone Project Proposal (Chapters 1–3)", fig_dir)

    # 2. Defense Compliance Matrix DOCX
    matrix_files = [
        os.path.join(artifact_dir, "SolanaWatch_Revision_Matrix_and_Action_Plan.md")
    ]
    matrix_out = os.path.join(out_dir, "defense-and-revisions", "SolanaWatch_Defense_Evaluation_Compliance_Matrix.docx")
    convert_manuscript(matrix_files, matrix_out, "SolanaWatch: Oral Defense Evaluation Compliance Matrix", fig_dir)
