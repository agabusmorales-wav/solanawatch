import os
import subprocess

PROJECT_DIR = r"C:\Users\agabu\Downloads\CODE PROJECTS\SOLANAWATCH"
FIGURES_DIR = os.path.join(PROJECT_DIR, "figures")
HTML_SLIDES_PATH = os.path.join(PROJECT_DIR, "paperwork", "reports-and-presentations", "SolanaWatch_Weekly_Progress_Report_Slides.html")
PDF_PATH = os.path.join(PROJECT_DIR, "paperwork", "reports-and-presentations", "SolanaWatch_Weekly_Progress_Report.pdf")
WEB_MOCKUP_PATH = os.path.join(PROJECT_DIR, "web-app", "SolanaWatch_Web_Dashboard_Mockup.html")

# Create 2-Slide White Background HTML Presentation for PDF export
html_slides = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>SolanaWatch - Weekly Progress Report (White Background)</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap');

  @page {
    size: 1920px 1080px;
    margin: 0;
  }

  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }

  body {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background-color: #ffffff;
    color: #0f172a;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }

  .slide {
    width: 1920px;
    height: 1080px;
    page-break-after: always;
    page-break-inside: avoid;
    position: relative;
    overflow: hidden;
    background: #ffffff;
    padding: 60px 80px;
    display: flex;
    flex-direction: column;
  }

  /* Slide Header */
  .slide-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 28px;
    border-bottom: 2px solid #e2e8f0;
    padding-bottom: 20px;
  }
  .header-left .category-pill {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    font-size: 15px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #0284c7;
    margin-bottom: 6px;
  }
  .header-left .category-pill::before {
    content: '';
    display: inline-block;
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: #0284c7;
  }
  .header-left h1 {
    font-size: 38px;
    font-weight: 800;
    color: #0f172a;
    letter-spacing: -0.5px;
  }
  .header-left p {
    font-size: 17px;
    font-weight: 600;
    color: #475569;
    margin-top: 4px;
  }
  .header-badge {
    background: #dcfce7;
    border: 2px solid #16a34a;
    padding: 10px 24px;
    border-radius: 30px;
    font-size: 16px;
    font-weight: 800;
    color: #15803d;
    letter-spacing: 0.5px;
  }

  /* 3 Column Layout (Slide 1) */
  .three-col-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 28px;
    flex: 1;
  }
  .col-card {
    background: #f8fafc;
    border: 2px solid #e2e8f0;
    border-radius: 18px;
    padding: 28px 26px;
    display: flex;
    flex-direction: column;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
  }
  .col-card.blue { border-top: 6px solid #0284c7; }
  .col-card.amber { border-top: 6px solid #d97706; }
  .col-card.green { border-top: 6px solid #16a34a; }

  .col-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 20px;
    padding-bottom: 12px;
    border-bottom: 2px solid #e2e8f0;
  }
  .col-title {
    font-size: 22px;
    font-weight: 800;
    letter-spacing: 0.5px;
  }
  .col-card.blue .col-title { color: #0284c7; }
  .col-card.amber .col-title { color: #d97706; }
  .col-card.green .col-title { color: #16a34a; }

  .col-item {
    margin-bottom: 18px;
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 18px 20px;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.02);
  }
  .col-item h3 {
    font-size: 18px;
    font-weight: 800;
    color: #0f172a;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .col-item p {
    font-size: 15px;
    font-weight: 500;
    color: #334155;
    line-height: 1.6;
  }

  .slide-footer-bar {
    margin-top: 18px;
    padding: 14px 24px;
    background: #f1f5f9;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 15px;
    font-weight: 600;
    color: #475569;
  }

  /* 2 Column Layout (Slide 2) */
  .two-col-grid {
    display: grid;
    grid-template-columns: 1.35fr 1fr;
    gap: 32px;
    flex: 1;
  }
  .image-container {
    border-radius: 18px;
    overflow: hidden;
    border: 2px solid #e2e8f0;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
    background: #ffffff;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .image-container img {
    width: 100%;
    height: 100%;
    object-fit: contain;
    display: block;
  }
  .info-panel {
    background: #f8fafc;
    border: 2px solid #e2e8f0;
    border-radius: 18px;
    padding: 30px 28px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
  }
  .info-title {
    font-size: 24px;
    font-weight: 800;
    color: #0284c7;
    margin-bottom: 16px;
  }
  .feature-list {
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 14px;
  }
  .feature-item {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 16px 20px;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.02);
  }
  .feature-item h4 {
    font-size: 17px;
    font-weight: 800;
    color: #0f172a;
    margin-bottom: 4px;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .feature-item p {
    font-size: 14.5px;
    font-weight: 500;
    color: #475569;
    line-height: 1.5;
  }
</style>
</head>
<body>

  <!-- ==========================================
       SLIDE 1: EXECUTIVE PROGRESS REPORT (WHITE BG)
       ========================================== -->
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
      <!-- Current Tasks -->
      <div class="col-card blue">
        <div class="col-header">
          <div class="col-title">CURRENT TASKS:</div>
        </div>
        <div class="col-item">
          <h3>
            <svg width="20" height="20" fill="none" stroke="#0284c7" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg>
            Canvas for materials
          </h3>
          <p>Finalized comprehensive Bill of Materials (₱7,208 total budget). Sourced ESP32, DHT22 in Stevenson shield, DS18B20 probe, RS485 dielectric leaf wetness grid, MPPT solar controller, and 12.8V LiFePO4 battery (47-day autonomy).</p>
        </div>
        <div class="col-item">
          <h3>
            <svg width="20" height="20" fill="none" stroke="#0284c7" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg>
            Designing a Web App
          </h3>
          <p>Completed clean, simple, and elegant UI/UX mockups with plain colors. Features 5 plain metric cards, disease early warning status pills, and clean soil moisture line charts.</p>
        </div>
      </div>

      <!-- Expected Challenges -->
      <div class="col-card amber">
        <div class="col-header">
          <div class="col-title">EXPECTED CHALLENGES:</div>
        </div>
        <div class="col-item">
          <h3>
            <svg width="20" height="20" fill="none" stroke="#d97706" stroke-width="2.5" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
            Hardware sourcing &amp; availability
          </h3>
          <p>Specialized IP68 RS485 dielectric leaf wetness sensor and genuine DS18B20 digital probes have limited local retail walk-in availability in Raon/electronics stores.</p>
        </div>
        <div class="col-item">
          <h3>
            <svg width="20" height="20" fill="none" stroke="#16a34a" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="9 11 12 14 22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></svg>
            Mitigation Strategy
          </h3>
          <p>Identified verified express online suppliers with 3-5 day transit; developed an ESP32 software telemetry emulator to unblock firmware and backend testing.</p>
        </div>
      </div>

      <!-- Plan for Next Week -->
      <div class="col-card green">
        <div class="col-header">
          <div class="col-title">PLAN FOR NEXT WEEK:</div>
        </div>
        <div class="col-item">
          <h3>
            <svg width="20" height="20" fill="none" stroke="#16a34a" stroke-width="2.5" viewBox="0 0 24 24"><polygon points="5 3 19 12 5 21 5 3"/></svg>
            Start making the prototype
          </h3>
          <p>Assemble breadboard test circuit, wire all 5 sensors to ESP32 DevKit V1, perform power bench testing with MPPT + LiFePO4 battery, and verify FreeRTOS sampling loops.</p>
        </div>
        <div class="col-item">
          <h3>
            <svg width="20" height="20" fill="none" stroke="#16a34a" stroke-width="2.5" viewBox="0 0 24 24"><polygon points="5 3 19 12 5 21 5 3"/></svg>
            Web app backend
          </h3>
          <p>Build Node.js/Express REST API endpoints, configure Turso cloud database (distributed libSQL), and implement Wallin SV and Hydrothermal disease risk algorithms.</p>
        </div>
      </div>
    </div>

    <div class="slide-footer-bar">
      <div><strong>Team Members:</strong> Morales, Simeon Agabus S. • Rapada, Raven M. • Hernandez, Andrei S. • Eugenio, Vince Angelo</div>
      <div><strong>Adviser:</strong> Prof. Eugenia R. Zhuo, DIT</div>
    </div>
  </div>

  <!-- ==========================================
       SLIDE 2: SIMPLE & ELEGANT MOCKUP & ARCHITECTURE (WHITE BG)
       ========================================== -->
  <div class="slide">
    <div class="slide-header">
      <div class="header-left">
        <div class="category-pill">Deliverable &amp; Architecture</div>
        <h1>Web Application Mockup (Simple &amp; Elegant UI)</h1>
        <p>Minimalist plain-color dashboard for real-time field telemetry and pre-symptomatic disease forecasting</p>
      </div>
      <div class="header-badge" style="background:#e0f2fe; border-color:#0284c7; color:#0284c7;">PLAIN &amp; ELEGANT</div>
    </div>

    <div class="two-col-grid">
      <div class="image-container">
        <img src="figures/web_mockup_minimal.jpg" alt="SolanaWatch Simple & Elegant Web Mockup">
      </div>

      <div class="info-panel">
        <div class="info-title">System Highlights &amp; Technical Architecture</div>
        <div class="feature-list">
          <div class="feature-item">
            <h4><span style="color:#0284c7;">✔</span> Simple &amp; Plain Color Palette</h4>
            <p>Designed with clean white card surfaces, subtle borders (#E2E8F0), and dark charcoal text (#0F172A) for maximum sunlight readability in the field.</p>
          </div>
          <div class="feature-item">
            <h4><span style="color:#0284c7;">✔</span> 5 Core Microclimate Metric Cards</h4>
            <p>Direct numeric readouts: Soil Moisture (68%), Soil Temp (24°C), Air Temp (22°C), Leaf Wetness Duration (4.2h), and Relative Humidity (88%).</p>
          </div>
          <div class="feature-item">
            <h4><span style="color:#0284c7;">✔</span> Pre-Symptomatic Disease Risk Engine</h4>
            <p>Evaluates Late Blight (Wallin Severity Values @ LWD &ge; 10h) &amp; Bacterial Wilt (Hydrothermal Index R_BW = 0.50*S_ST + 0.50*S_SM) with subtle risk badges.</p>
          </div>
          <div class="feature-item">
            <h4><span style="color:#0284c7;">✔</span> Finalized BOM &amp; Autonomous Solar Power</h4>
            <p>Total cost ₱7,208.00. Powered by 20W Monocrystalline PV + 12V 10A MPPT + 12.8V 12Ah LiFePO4 battery pack (47-day zero-sunlight autonomy).</p>
          </div>
        </div>
      </div>
    </div>

    <div class="slide-footer-bar">
      <div><strong>Interactive Prototype:</strong> Open <code>SolanaWatch_Web_Dashboard_Mockup.html</code> for live scenario simulation</div>
      <div><strong>SolanaWatch:</strong> IoT Early Warning System for Solanaceae Crops</div>
    </div>
  </div>

</body>
</html>
"""

# Write HTML Slides
with open(HTML_SLIDES_PATH, "w", encoding="utf-8") as f:
    f.write(html_slides)
print(f"[SUCCESS] 2-Slide White Background HTML saved to: {HTML_SLIDES_PATH}")

# Convert HTML slides to PDF via Microsoft Edge Headless
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
    print(f"Generating 2-Slide White BG PDF with Edge: {' '.join(cmd)}")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0 and os.path.exists(PDF_PATH):
        print(f"[SUCCESS] 2-Slide Presentation PDF generated at: {PDF_PATH} ({os.path.getsize(PDF_PATH)} bytes)")
    else:
        print(f"[ERROR] Edge PDF generation failed: {res.stderr}")
