# SolanaWatch 🌿⚙️ Build & Generator Scripts

> **Python Automation Utilities for Diagrams, Manuscripts, Forms, and Slide Decks**  
> *SolanaWatch: IoT-Based Disease Early Warning System for Soil-Grown Solanaceae Crops*  
> *University of Santo Tomas – College of Information and Computing Sciences*

---

## 🛠️ Script Inventory

| Script | Output Artifact | Description |
| :--- | :--- | :--- |
| **`generate_diagrams.py`** | `figures/figure[1-6]*.png` | Generates all 6 core 300 DPI system diagrams (Context Diagram, Activity Diagram, Prototyping Cycle, System Architecture, ER Schema, Circuit Schematic) using Matplotlib. |
| **`generate_system_architecture.py`** | `figures/figure3_system_architecture_revised.png` | Renders the high-definition revised 4-tier system architecture diagram. |
| **`generate_prototype_drawings.py`** | `figures/figure[7-8]*.png` | Renders technical layout drawings for the IP66 hardware enclosure and internal DIN rail configuration. |
| **`convert_to_docx.py`** | `paperwork/proposal/SolanaWatch_Proposal_Chapters_1-3_REVISED.docx` | Compiles Markdown proposal chapters into a formatted Microsoft Word (.docx) manuscript adhering to APA 7th edition formatting. |
| **`convert_to_html.py`** | `paperwork/proposal/SolanaWatch_Proposal_Chapters_1-3_REVISED.html` | Compiles Markdown chapters into a standalone, styled HTML manuscript with base64 embedded diagrams. |
| **`generate_accomplished_ethics_forms.py`** | `paperwork/ethics-review/FORM 4.2 & 7.2` | Generates accomplished RERC ethics submission forms in Microsoft Word format. |
| **`generate_revision_matrix.py`** | `paperwork/defense-and-revisions/SolanaWatch_Revision_Matrix_Official.docx` | Generates the official defense evaluation revision compliance matrix. |
| **`generate_sus_questionnaire.py`** | `paperwork/evaluation-sus/SolanaWatch_System_Usability_Scale_Questionnaire.docx` | Generates the official 10-item System Usability Scale (SUS) questionnaire document in Word format. |
| **`generate_sus_html_and_pdf.py`** | `paperwork/evaluation-sus/*.html`, `*.pdf` | Generates print-ready HTML and PDF editions of the SUS evaluation instrument. |
| **`generate_weekly_report.py`** | `paperwork/reports-and-presentations/*` | Compiles weekly milestone reports into styled PDF, PPTX, and HTML formats. |
| **`generate_editable_slides.py`** | `paperwork/reports-and-presentations/SolanaWatch_Presentation_Editable.pptx` | Generates the master editable PowerPoint presentation slide deck. |
| **`generate_pptx_report.py`** | `paperwork/reports-and-presentations/SolanaWatch_Weekly_Progress_Report.pptx` | Generates milestone slide presentations using python-pptx. |
| **`generate_pdf_and_web_mockup.py`** | `web-app/SolanaWatch_Web_Dashboard_Mockup.html` | Generates standalone dashboard mockup templates and captures render previews. |

---

## 📦 Prerequisites & Environment Setup

Install required Python packages:

```powershell
pip install matplotlib python-docx python-pptx markdown
```

---

## 🚀 Execution Instructions

Run any utility directly from PowerShell or Command Prompt:

```powershell
# Navigate to the project root directory
cd "C:\Users\agabu\Downloads\CODE PROJECTS\SOLANAWATCH"

# Generate system diagrams
python scripts/generate_diagrams.py

# Compile DOCX proposal manuscript
python scripts/convert_to_docx.py

# Compile HTML proposal preview
python scripts/convert_to_html.py

# Generate SUS questionnaire documents
python scripts/generate_sus_questionnaire.py

# Generate weekly progress presentation slides
python scripts/generate_editable_slides.py
```
