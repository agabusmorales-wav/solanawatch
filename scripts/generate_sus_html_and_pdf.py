import os
import base64
import subprocess

out_dir = r"C:\Users\agabu\Downloads\CODE PROJECTS\SOLANAWATCH\paperwork\evaluation-sus"
logo_dir = r"C:\Users\agabu\Downloads\extracted_logos"

def get_base64_image(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return ""

ust_b64 = get_base64_image(os.path.join(logo_dir, "ust_logo_clean.png"))
cics_b64 = get_base64_image(os.path.join(logo_dir, "cics_logo_clean.png"))

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>SolanaWatch: System Usability Scale (SUS) Questionnaire</title>
<style>
    @page {{
        size: A4 portrait;
        margin: 15mm 15mm 15mm 15mm;
    }}
    body {{
        font-family: Arial, Helvetica, sans-serif;
        font-size: 9.5pt;
        line-height: 1.35;
        color: #222;
        background-color: #fff;
        margin: 0;
        padding: 0;
    }}
    .page-container {{
        max-width: 800px;
        margin: 0 auto;
        padding: 20px 25px;
    }}
    .header-table {{
        width: 100%;
        border-collapse: collapse;
        margin-bottom: 8px;
    }}
    .header-table td {{
        vertical-align: middle;
        padding: 0;
    }}
    .header-logo {{
        width: 75px;
        height: 75px;
        object-fit: contain;
    }}
    .inst-text {{
        text-align: center;
    }}
    .inst-u1 {{
        font-size: 11pt;
        font-weight: bold;
        color: #000;
        letter-spacing: 0.5px;
    }}
    .inst-u2 {{
        font-size: 9.5pt;
        font-weight: bold;
        color: #003366;
    }}
    .inst-u3 {{
        font-size: 8.5pt;
        font-weight: bold;
        color: #333;
    }}
    .inst-term {{
        font-size: 8pt;
        font-style: italic;
        color: #666;
    }}
    .gold-divider {{
        height: 2.5px;
        background: linear-gradient(90deg, #003366 0%, #D4AF37 50%, #003366 100%);
        margin: 6px 0 12px 0;
        border-radius: 2px;
    }}
    .doc-title-block {{
        text-align: center;
        margin-bottom: 12px;
    }}
    .doc-title {{
        font-size: 13pt;
        font-weight: bold;
        color: #003366;
        margin-bottom: 2px;
    }}
    .doc-subtitle {{
        font-size: 9.5pt;
        font-weight: bold;
        color: #C59B27;
        margin-bottom: 3px;
    }}
    .doc-proj {{
        font-size: 8.5pt;
        font-style: italic;
        color: #444;
    }}
    .meta-box {{
        width: 100%;
        border: 1px solid #D0D7DE;
        border-collapse: collapse;
        margin-bottom: 14px;
        background: #F8FAFC;
    }}
    .meta-box td {{
        padding: 6px 10px;
        font-size: 8pt;
        border: 1px solid #D0D7DE;
        vertical-align: top;
    }}
    .sec-heading {{
        font-size: 10.5pt;
        font-weight: bold;
        color: #003366;
        border-bottom: 1.5px solid #003366;
        padding-bottom: 3px;
        margin: 14px 0 6px 0;
        text-transform: uppercase;
        letter-spacing: 0.3px;
    }}
    .desc-text {{
        font-size: 8.5pt;
        margin-bottom: 8px;
        text-align: justify;
    }}
    .callout-box {{
        background: #F0F4F8;
        border-left: 4px solid #003366;
        border: 1px solid #D0D7DE;
        border-left-width: 4px;
        padding: 8px 12px;
        font-size: 8pt;
        margin-bottom: 12px;
        border-radius: 3px;
    }}
    .dem-table, .task-table, .sus-table, .bench-table, .calc-table, .sig-table {{
        width: 100%;
        border-collapse: collapse;
        margin-bottom: 12px;
    }}
    .dem-table td {{
        border: 1px solid #D0D7DE;
        padding: 6px 10px;
        font-size: 8pt;
        vertical-align: top;
        width: 50%;
    }}
    .dem-title {{
        font-weight: bold;
        color: #003366;
        margin-bottom: 4px;
    }}
    .task-table th, .sus-table th, .bench-table th {{
        background-color: #003366;
        color: #fff;
        padding: 6px 8px;
        font-size: 8pt;
        font-weight: bold;
        border: 1px solid #002244;
        text-align: center;
    }}
    .task-table td, .sus-table td, .bench-table td {{
        border: 1px solid #D0D7DE;
        padding: 5px 8px;
        font-size: 8pt;
        vertical-align: middle;
    }}
    .task-table tr:nth-child(even), .sus-table tr:nth-child(even) {{
        background-color: #F8FAFC;
    }}
    .col-center {{
        text-align: center;
    }}
    .checkbox-bubble {{
        display: inline-block;
        width: 14px;
        height: 14px;
        border: 1.5px solid #555;
        border-radius: 2px;
        background: #FFF;
        margin: 0 auto;
    }}
    .statement-eng {{
        font-weight: 500;
        color: #111;
        margin-bottom: 2px;
    }}
    .statement-fil {{
        font-style: italic;
        color: #555;
        font-size: 7.5pt;
    }}
    .page-break {{
        page-break-before: always;
    }}
    .qual-box {{
        border: 1px solid #D0D7DE;
        padding: 8px 12px;
        margin-bottom: 10px;
        border-radius: 3px;
    }}
    .qual-prompt-eng {{
        font-weight: bold;
        font-size: 8.5pt;
        color: #003366;
        margin-bottom: 2px;
    }}
    .qual-prompt-fil {{
        font-size: 7.5pt;
        font-style: italic;
        color: #555;
        margin-bottom: 8px;
    }}
    .ruled-area {{
        border-bottom: 1px dashed #CCC;
        height: 20px;
        margin-bottom: 6px;
    }}
    .sig-table td {{
        border: 1px solid #D0D7DE;
        padding: 10px 14px;
        width: 50%;
        vertical-align: top;
        font-size: 8pt;
    }}
</style>
</head>
<body>

<div class="page-container">
    <!-- Header Table -->
    <table class="header-table">
        <tr>
            <td style="width:80px; text-align:left;">
                {'<img src="data:image/png;base64,' + ust_b64 + '" class="header-logo" alt="UST Logo"/>' if ust_b64 else ''}
            </td>
            <td class="inst-text">
                <div class="inst-u1">UNIVERSITY OF SANTO TOMAS</div>
                <div class="inst-u2">COLLEGE OF INFORMATION AND COMPUTING SCIENCES</div>
                <div class="inst-u3">DEPARTMENT OF INFORMATION TECHNOLOGY</div>
                <div class="inst-term">Academic Year 2025–2026 | Special Term</div>
            </td>
            <td style="width:80px; text-align:right;">
                {'<img src="data:image/png;base64,' + cics_b64 + '" class="header-logo" alt="CICS Logo"/>' if cics_b64 else ''}
            </td>
        </tr>
    </table>

    <div class="gold-divider"></div>

    <!-- Title Block -->
    <div class="doc-title-block">
        <div class="doc-title">SYSTEM USABILITY SCALE (SUS) EVALUATION INSTRUMENT</div>
        <div class="doc-subtitle">ISO/IEC 25010 Usability &amp; User Experience Quality Metric</div>
        <div class="doc-proj">Project Title: SolanaWatch: An IoT-Based Disease Early Warning System for Soil-Grown Solanaceae Crops</div>
    </div>

    <!-- Metadata Card -->
    <table class="meta-box">
        <tr>
            <td style="width:50%;">
                <strong>Proponents (3ITC - Group 1):</strong><br>
                • Morales, Simeon Agabus S.<br>
                • Rapada, Raven M.<br>
                • Hernandez, Andrei S.<br>
                • Eugenio, Vince Angelo
            </td>
            <td style="width:50%;">
                <strong>Academic Supervision &amp; Metric:</strong><br>
                • Project Adviser: Prof. Eugenia R. Zhuo, DIT<br>
                • Degree: B.S. in Information Technology<br>
                • Target Usability Score: ≥ 80.0 / 100 (Grade A)<br>
                • Target Users: Smallholder Farmers &amp; Technicians
            </td>
        </tr>
        <tr>
            <td>
                <strong>Participant ID / Code:</strong> ______________________
            </td>
            <td>
                <strong>Date of Evaluation:</strong> ______________________
            </td>
        </tr>
    </table>

    <!-- Section 1 -->
    <div class="sec-heading">Section 1: Purpose of Evaluation &amp; Informed Consent</div>
    <div class="desc-text">
        <strong>Dear Participant,</strong><br>
        Thank you for participating in the usability evaluation of <strong>SolanaWatch: An IoT-Based Disease Early Warning System for Soil-Grown Solanaceae Crops</strong>. 
        SolanaWatch is a capstone research system designed at the University of Santo Tomas – CICS. It combines solar-powered field sensor nodes (capturing air temp, relative humidity, leaf wetness duration, root-zone soil temp, and soil moisture) with a responsive web dashboard to provide pre-symptomatic alerts for Late Blight (<em>Phytophthora infestans</em>) and Bacterial Wilt (<em>Ralstonia pseudosolanacearum</em>).<br><br>
        This evaluation utilizes the industry-standard <strong>System Usability Scale (SUS)</strong> (Brooke, 1996) to measure usability, learnability, and overall user acceptance under ISO/IEC 25010 standards. Your honest assessment will guide final technical refinements.
    </div>

    <div class="callout-box">
        <strong style="color:#003366;">Informed Consent &amp; Data Privacy Guarantee (R.A. 10173 - Data Privacy Act of 2012):</strong><br>
        • Participation is entirely voluntary. You may pause or withdraw from this evaluation at any time without penalty.<br>
        • All responses will be anonymized and kept strictly confidential using assigned Participant IDs.<br>
        • Data collected will be used exclusively for academic research, capstone documentation, and scientific dissemination.
    </div>

    <!-- Section 2 -->
    <div class="sec-heading">Section 2: Participant Demographic &amp; Operational Profile</div>
    <div class="desc-text" style="font-style:italic; color:#555;">Please mark [X] or fill in the information that best describes your background:</div>

    <table class="dem-table">
        <tr>
            <td>
                <div class="dem-title">1. Primary Stakeholder Role:</div>
                [ &nbsp; ] Smallholder Solanaceae Farmer<br>
                [ &nbsp; ] Agricultural Extension Worker / LGU Technician<br>
                [ &nbsp; ] Agronomist / Plant Pathologist<br>
                [ &nbsp; ] Academic Researcher / IT Evaluator<br>
                [ &nbsp; ] Other: ___________________________
            </td>
            <td>
                <div class="dem-title">2. Gender &amp; Age Bracket:</div>
                Gender: [ &nbsp; ] Male &nbsp; [ &nbsp; ] Female &nbsp; [ &nbsp; ] Prefer not to say<br>
                Age: [ &nbsp; ] 18–29 &nbsp; [ &nbsp; ] 30–39 &nbsp; [ &nbsp; ] 40–49<br>
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[ &nbsp; ] 50–59 &nbsp; [ &nbsp; ] 60 and above
            </td>
        </tr>
        <tr>
            <td>
                <div class="dem-title">3. Farming / Agricultural Experience:</div>
                [ &nbsp; ] Less than 2 years<br>
                [ &nbsp; ] 2 to 5 years<br>
                [ &nbsp; ] 6 to 10 years<br>
                [ &nbsp; ] More than 10 years
            </td>
            <td>
                <div class="dem-title">4. Solanaceae Crops Cultivated / Handled:</div>
                [ &nbsp; ] Eggplant (Talong)<br>
                [ &nbsp; ] Tomato (Kamatis)<br>
                [ &nbsp; ] Pepper (Siling Haba / Bell Pepper)<br>
                [ &nbsp; ] Potato (Patatas)<br>
                [ &nbsp; ] Mixed / Diversified Cropping
            </td>
        </tr>
        <tr>
            <td>
                <div class="dem-title">5. Farm / Workplace Location:</div>
                Barangay: ___________________________<br>
                Municipality: ___________________________<br>
                Province: ___________________________
            </td>
            <td>
                <div class="dem-title">6. Digital Device Usage in Daily Routine:</div>
                [ &nbsp; ] Smartphone (Android / iOS)<br>
                [ &nbsp; ] Tablet<br>
                [ &nbsp; ] Desktop / Laptop Computer<br>
                [ &nbsp; ] Basic Keypad Phone (SMS only)<br>
                [ &nbsp; ] Non-User / Assistance Required
            </td>
        </tr>
        <tr>
            <td>
                <div class="dem-title">7. Prior Experience with Smart Farming Tools:</div>
                [ &nbsp; ] None (First time using IoT farm tools)<br>
                [ &nbsp; ] Occasional (Weather apps, SMS advisories)<br>
                [ &nbsp; ] Frequent (Sensors, telemetry dashboards)
            </td>
            <td>
                <div class="dem-title">8. Preferred Language for Farming Advice:</div>
                [ &nbsp; ] English<br>
                [ &nbsp; ] Filipino / Tagalog<br>
                [ &nbsp; ] Bilingual (English with Filipino subtitles)<br>
                [ &nbsp; ] Regional Dialect: __________________
            </td>
        </tr>
    </table>

    <div class="page-break"></div>

    <!-- Section 3 -->
    <div class="sec-heading">Section 3: System Interaction &amp; Task Walkthrough</div>
    <div class="desc-text">
        Before completing the questionnaire, please ensure you have interacted with the SolanaWatch Web Application by performing the five core user scenarios:
    </div>

    <table class="task-table">
        <tr>
            <th style="width:10%;">Task #</th>
            <th style="width:30%;">Operational Scenario</th>
            <th style="width:45%;">Core User Action Performed</th>
            <th style="width:15%;">Completion</th>
        </tr>
        <tr>
            <td class="col-center"><strong>Task 1</strong></td>
            <td><strong>Live Telemetry Inspection</strong></td>
            <td>Navigated dashboard to inspect live air temp, air RH, leaf wetness duration, root-zone soil temp, and soil moisture gauges.</td>
            <td class="col-center">[ &nbsp; ] Done<br>[ &nbsp; ] Partial</td>
        </tr>
        <tr>
            <td class="col-center"><strong>Task 2</strong></td>
            <td><strong>Disease Early Warning Alerts</strong></td>
            <td>Observed and interpreted color-coded alert banners (Green = Low, Yellow = Moderate, Red = High Risk) for Late Blight and Bacterial Wilt.</td>
            <td class="col-center">[ &nbsp; ] Done<br>[ &nbsp; ] Partial</td>
        </tr>
        <tr>
            <td class="col-center"><strong>Task 3</strong></td>
            <td><strong>Historical Trend Analysis</strong></td>
            <td>Interacted with historical time-series charts to inspect 24-hour diurnal microclimate swings and prolonged leaf wetness events.</td>
            <td class="col-center">[ &nbsp; ] Done<br>[ &nbsp; ] Partial</td>
        </tr>
        <tr>
            <td class="col-center"><strong>Task 4</strong></td>
            <td><strong>Actionable Agronomic Advice</strong></td>
            <td>Accessed and reviewed specific farm management advisories triggered by active risk levels (e.g., canopy thinning, drainage trenching).</td>
            <td class="col-center">[ &nbsp; ] Done<br>[ &nbsp; ] Partial</td>
        </tr>
        <tr>
            <td class="col-center"><strong>Task 5</strong></td>
            <td><strong>Hardware Health Telemetry</strong></td>
            <td>Checked system health telemetry, including LiFePO4 battery percentage, MPPT solar charging state, and offline MicroSD sync status.</td>
            <td class="col-center">[ &nbsp; ] Done<br>[ &nbsp; ] Partial</td>
        </tr>
    </table>

    <!-- Section 4 -->
    <div class="sec-heading">Section 4: System Usability Scale (SUS) Questionnaire</div>
    <div class="desc-text">
        <strong>Instructions:</strong> Please mark [X] in the box that corresponds to your immediate, honest rating for each statement.<br>
        <em>Tagalog: Mangyaring lagyan ng [X] ang kahon na pinakaangkop sa inyong karanasan sa paggamit ng sistema.</em><br>
        <strong>Scale:</strong> 1 = Strongly Disagree (SD) &nbsp;|&nbsp; 2 = Disagree (D) &nbsp;|&nbsp; 3 = Neutral (N) &nbsp;|&nbsp; 4 = Agree (A) &nbsp;|&nbsp; 5 = Strongly Agree (SA)
    </div>

    <table class="sus-table">
        <tr>
            <th style="width:6%;">#</th>
            <th style="width:54%;">Usability Statement (English &amp; Filipino)</th>
            <th style="width:8%;">1<br>SD</th>
            <th style="width:8%;">2<br>D</th>
            <th style="width:8%;">3<br>N</th>
            <th style="width:8%;">4<br>A</th>
            <th style="width:8%;">5<br>SA</th>
        </tr>
        <tr>
            <td class="col-center"><strong>1</strong></td>
            <td>
                <div class="statement-eng">I think that I would like to use the SolanaWatch system frequently.</div>
                <div class="statement-fil">Nais kong gamitin ang SolanaWatch system nang madalas sa aking sakahan/trabaho.</div>
            </td>
            <td class="col-center"><div class="checkbox-bubble"></div></td>
            <td class="col-center"><div class="checkbox-bubble"></div></td>
            <td class="col-center"><div class="checkbox-bubble"></div></td>
            <td class="col-center"><div class="checkbox-bubble"></div></td>
            <td class="col-center"><div class="checkbox-bubble"></div></td>
        </tr>
        <tr>
            <td class="col-center"><strong>2</strong></td>
            <td>
                <div class="statement-eng">I found the system unnecessarily complex.</div>
                <div class="statement-fil">Pakiramdam ko ay masyadong masalimuot o kumplikado ang sistema nang walang sapat na dahilan.</div>
            </td>
            <td class="col-center"><div class="checkbox-bubble"></div></td>
            <td class="col-center"><div class="checkbox-bubble"></div></td>
            <td class="col-center"><div class="checkbox-bubble"></div></td>
            <td class="col-center"><div class="checkbox-bubble"></div></td>
            <td class="col-center"><div class="checkbox-bubble"></div></td>
        </tr>
        <tr>
            <td class="col-center"><strong>3</strong></td>
            <td>
                <div class="statement-eng">I thought the system was easy to use.</div>
                <div class="statement-fil">Pakiramdam ko ay madaling gamitin at unawain ang sistema.</div>
            </td>
            <td class="col-center"><div class="checkbox-bubble"></div></td>
            <td class="col-center"><div class="checkbox-bubble"></div></td>
            <td class="col-center"><div class="checkbox-bubble"></div></td>
            <td class="col-center"><div class="checkbox-bubble"></div></td>
            <td class="col-center"><div class="checkbox-bubble"></div></td>
        </tr>
        <tr>
            <td class="col-center"><strong>4</strong></td>
            <td>
                <div class="statement-eng">I think that I would need the support of a technical person to be able to use this system.</div>
                <div class="statement-fil">Sa tingin ko ay kakailanganin ko ang tulong ng isang eksperto o teknikal na tao upang magamit ang sistemang ito.</div>
            </td>
            <td class="col-center"><div class="checkbox-bubble"></div></td>
            <td class="col-center"><div class="checkbox-bubble"></div></td>
            <td class="col-center"><div class="checkbox-bubble"></div></td>
            <td class="col-center"><div class="checkbox-bubble"></div></td>
            <td class="col-center"><div class="checkbox-bubble"></div></td>
        </tr>
        <tr>
            <td class="col-center"><strong>5</strong></td>
            <td>
                <div class="statement-eng">I found the various functions in this system were well integrated.</div>
                <div class="statement-fil">Napansin kong maayos na magkakaugnay at nagtutulungan ang iba't ibang bahagi at impormasyon sa sistema.</div>
            </td>
            <td class="col-center"><div class="checkbox-bubble"></div></td>
            <td class="col-center"><div class="checkbox-bubble"></div></td>
            <td class="col-center"><div class="checkbox-bubble"></div></td>
            <td class="col-center"><div class="checkbox-bubble"></div></td>
            <td class="col-center"><div class="checkbox-bubble"></div></td>
        </tr>
        <tr>
            <td class="col-center"><strong>6</strong></td>
            <td>
                <div class="statement-eng">I thought there was too much inconsistency in this system.</div>
                <div class="statement-fil">Pakiramdam ko ay labis ang hindi pagtutugma o pabagu-bago sa sistema.</div>
            </td>
            <td class="col-center"><div class="checkbox-bubble"></div></td>
            <td class="col-center"><div class="checkbox-bubble"></div></td>
            <td class="col-center"><div class="checkbox-bubble"></div></td>
            <td class="col-center"><div class="checkbox-bubble"></div></td>
            <td class="col-center"><div class="checkbox-bubble"></div></td>
        </tr>
        <tr>
            <td class="col-center"><strong>7</strong></td>
            <td>
                <div class="statement-eng">I would imagine that most people would learn to use this system very quickly.</div>
                <div class="statement-fil">Tinataya kong karamihan ng mga magsasaka at gumagamit ay mabilis na matututong gumamit ng sistemang ito.</div>
            </td>
            <td class="col-center"><div class="checkbox-bubble"></div></td>
            <td class="col-center"><div class="checkbox-bubble"></div></td>
            <td class="col-center"><div class="checkbox-bubble"></div></td>
            <td class="col-center"><div class="checkbox-bubble"></div></td>
            <td class="col-center"><div class="checkbox-bubble"></div></td>
        </tr>
        <tr>
            <td class="col-center"><strong>8</strong></td>
            <td>
                <div class="statement-eng">I found the system very cumbersome (awkward/heavy) to use.</div>
                <div class="statement-fil">Naramdaman kong napakahirap, nakakaasiwa, o mabigat gamitin ang sistema.</div>
            </td>
            <td class="col-center"><div class="checkbox-bubble"></div></td>
            <td class="col-center"><div class="checkbox-bubble"></div></td>
            <td class="col-center"><div class="checkbox-bubble"></div></td>
            <td class="col-center"><div class="checkbox-bubble"></div></td>
            <td class="col-center"><div class="checkbox-bubble"></div></td>
        </tr>
        <tr>
            <td class="col-center"><strong>9</strong></td>
            <td>
                <div class="statement-eng">I felt very confident using the system.</div>
                <div class="statement-fil">Naging lubos akong tiwala at panatag sa paggamit ng sistema.</div>
            </td>
            <td class="col-center"><div class="checkbox-bubble"></div></td>
            <td class="col-center"><div class="checkbox-bubble"></div></td>
            <td class="col-center"><div class="checkbox-bubble"></div></td>
            <td class="col-center"><div class="checkbox-bubble"></div></td>
            <td class="col-center"><div class="checkbox-bubble"></div></td>
        </tr>
        <tr>
            <td class="col-center"><strong>10</strong></td>
            <td>
                <div class="statement-eng">I needed to learn a lot of things before I could get going with this system.</div>
                <div class="statement-fil">Kinailangan kong mag-aral ng napakaraming bagay bago ko nagawang gamitin nang maayos ang sistema.</div>
            </td>
            <td class="col-center"><div class="checkbox-bubble"></div></td>
            <td class="col-center"><div class="checkbox-bubble"></div></td>
            <td class="col-center"><div class="checkbox-bubble"></div></td>
            <td class="col-center"><div class="checkbox-bubble"></div></td>
            <td class="col-center"><div class="checkbox-bubble"></div></td>
        </tr>
    </table>

    <div class="page-break"></div>

    <!-- Section 5 -->
    <div class="sec-heading">Section 5: Qualitative Usability Feedback &amp; Suggestions</div>
    <div class="desc-text">Please share brief qualitative remarks to guide future software and hardware enhancements:</div>

    <div class="qual-box">
        <div class="qual-prompt-eng">1. What specific dashboard features, environmental charts, or alerts were the MOST HELPFUL and easiest to understand?</div>
        <div class="qual-prompt-fil">Anong partikular na bahagi ng dashboard, grap, o babala ang pinakanakatulong at pinakamadaling maunawaan?</div>
        <div class="ruled-area"></div>
        <div class="ruled-area"></div>
        <div class="ruled-area" style="border:none;"></div>
    </div>

    <div class="qual-box">
        <div class="qual-prompt-eng">2. Did you encounter any CONFUSION, difficulty, or visual clutter while navigating or reading disease risk levels?</div>
        <div class="qual-prompt-fil">May naging kalituhan ba, kahirapan, o magulong impormasyon habang tinitingnan ang antas ng peligro ng sakit?</div>
        <div class="ruled-area"></div>
        <div class="ruled-area"></div>
        <div class="ruled-area" style="border:none;"></div>
    </div>

    <div class="qual-box">
        <div class="qual-prompt-eng">3. What ENHANCEMENTS or additional features would you recommend for real-world deployment on your farm?</div>
        <div class="qual-prompt-fil">Anong mga dagdag na kakayahan, pagbabago sa wika, o disenyo ang iminumungkahi ninyo para sa aktwal na sakahan?</div>
        <div class="ruled-area"></div>
        <div class="ruled-area"></div>
        <div class="ruled-area" style="border:none;"></div>
    </div>

    <!-- Section 6 -->
    <div class="sec-heading">Section 6: Evaluator Scoring Guide &amp; Usability Benchmarks (Audit Reference)</div>
    <div class="desc-text" style="font-style:italic; font-size:8pt; color:#555;">
        Note for Capstone Panel &amp; Evaluator: The System Usability Scale produces a composite score from 0 to 100 points (Brooke, 1996). Follow the standardized calculation below:
    </div>

    <table class="dem-table">
        <tr>
            <td style="background:#F8FAFC;">
                <strong style="color:#003366; font-size:8.5pt;">Brooke (1996) Scoring Formula:</strong><br>
                1. <strong>Odd Items (1, 3, 5, 7, 9):</strong><br>
                &nbsp;&nbsp;&nbsp;&nbsp;Contribution = Scale Position − 1<br>
                2. <strong>Even Items (2, 4, 6, 8, 10):</strong><br>
                &nbsp;&nbsp;&nbsp;&nbsp;Contribution = 5 − Scale Position<br>
                3. <strong>Composite Normalized Score:</strong><br>
                &nbsp;&nbsp;&nbsp;&nbsp;<strong>SUS Score = [ Sum of all 10 item contributions ] × 2.5</strong><br>
                &nbsp;&nbsp;&nbsp;&nbsp;Range: 0 to 100 points.
            </td>
            <td style="background:#FFFFFF;">
                <strong style="color:#003366; font-size:8.5pt;">Evaluator Official Score Card:</strong><br>
                • Sum of Odd Contributions (X): ________<br>
                • Sum of Even Contributions (Y): ________<br>
                • Total Raw Sum (X + Y): _______________<br>
                • <strong>Calculated Composite SUS: ________ / 100</strong><br>
                • Adjective Rating: ______________________<br>
                • ISO/IEC Usability Target Met: [ &nbsp; ] YES &nbsp; [ &nbsp; ] NO
            </td>
        </tr>
    </table>

    <div style="font-weight:bold; font-size:8.5pt; color:#003366; margin:6px 0 3px 0;">
        SUS Score Interpretation Scale (Bangor et al., 2008; Sauro &amp; Lewis, 2012):
    </div>
    <table class="bench-table">
        <tr>
            <th>SUS Score Range</th>
            <th>Letter Grade</th>
            <th>Adjective Rating</th>
            <th>Acceptability Status</th>
            <th>SolanaWatch Compliance</th>
        </tr>
        <tr style="background:#E8F8F5; font-weight:bold;">
            <td class="col-center">80.3 – 100.0</td>
            <td class="col-center">Grade A</td>
            <td class="col-center">Excellent / Best Imaginable</td>
            <td class="col-center">Highly Acceptable</td>
            <td class="col-center" style="color:#16A085;">★ Target Design Goal (≥ 80.0)</td>
        </tr>
        <tr>
            <td class="col-center">68.0 – 80.2</td>
            <td class="col-center">Grade B / C+</td>
            <td class="col-center">Good (Above Average)</td>
            <td class="col-center">Acceptable (Industry Avg = 68.0)</td>
            <td class="col-center">Meets Baseline Standard</td>
        </tr>
        <tr>
            <td class="col-center">51.0 – 67.9</td>
            <td class="col-center">Grade C / D</td>
            <td class="col-center">OK / Marginal</td>
            <td class="col-center">Marginally Acceptable</td>
            <td class="col-center">Requires UI Revisions</td>
        </tr>
        <tr>
            <td class="col-center">0.0 – 50.9</td>
            <td class="col-center">Grade F</td>
            <td class="col-center">Poor / Unacceptable</td>
            <td class="col-center">Not Acceptable</td>
            <td class="col-center" style="color:#C0392B;">Critical Usability Failure</td>
        </tr>
    </table>

    <!-- Section 7 -->
    <div class="sec-heading">Section 7: Participant Acknowledgement &amp; Evaluator Sign-Off</div>
    <div class="desc-text" style="font-style:italic; font-size:8pt; color:#555;">
        Declaration: I hereby confirm that I have interacted with the SolanaWatch system and completed this evaluation truthfully and voluntarily.
    </div>

    <table class="sig-table">
        <tr>
            <td>
                <strong>Evaluated by (Participant):</strong><br><br><br>
                _________________________________________<br>
                Signature over Printed Name<br><br>
                Date Signed: ____________________________
            </td>
            <td>
                <strong>Administered &amp; Verified by:</strong><br><br><br>
                _________________________________________<br>
                Lead Usability Evaluator (UST-CICS)<br><br>
                Date Verified: __________________________
            </td>
        </tr>
    </table>

</div>

</body>
</html>
"""

html_path = os.path.join(out_dir, "SolanaWatch_System_Usability_Scale_Questionnaire.html")
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)
print(f"Generated HTML at: {html_path}")

# Compile to PDF using Microsoft Edge Headless
pdf_path = os.path.join(out_dir, "SolanaWatch_System_Usability_Scale_Questionnaire.pdf")
edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

if os.path.exists(edge_path):
    cmd = [
        edge_path,
        "--headless",
        "--disable-gpu",
        "--run-all-compositor-stages-before-draw",
        f"--print-to-pdf={pdf_path}",
        html_path
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if os.path.exists(pdf_path):
        print(f"Successfully generated companion PDF at: {pdf_path} ({os.path.getsize(pdf_path):,} bytes)")
    else:
        print("PDF generation failed or timed out.")
