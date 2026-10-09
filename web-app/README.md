# SolanaWatch 🌿📱 Web Application Suite

> **Interactive Decision Support & Microclimatic Monitoring Frontends**  
> *SolanaWatch: IoT-Based Disease Early Warning System for Soil-Grown Solanaceae Crops*  
> *University of Santo Tomas – College of Information and Computing Sciences*

---

## 📂 Web Application Files

| File | Interface | Description | Recommended Device / Viewport |
| :--- | :--- | :--- | :--- |
| **[`index.html`](file:///C:/Users/agabu/Downloads/CODE%20PROJECTS/SOLANAWATCH/web-app/index.html)** | **iOS Mobile DSS** | Native-feeling iOS 18 web app with Apple HIG design tokens, glassmorphism cards, dynamic island status, interactive disease risk gauges, real-time sensor metrics, agronomic recommendations, live hardware connectivity, and quick switch to PC view. | Mobile Devices, iPhone Viewport (390×844) or Mobile Browser |
| **[`desktop.html`](file:///C:/Users/agabu/Downloads/CODE%20PROJECTS/SOLANAWATCH/web-app/desktop.html)** | **macOS / PC Dashboard** | High-density desktop command center with collapsible sidebar, real-time telemetry grid, dual disease vulnerability radar (Late Blight Wallin SV + Bacterial Wilt Hydrothermal), historical multi-series Chart.js analytics, live hardware link, and hardware health monitors. | PC / Mac Laptops & Desktop Monitors (1280×720 or higher) |
| **[`hardware-bridge.js`](file:///C:/Users/agabu/Downloads/CODE%20PROJECTS/SOLANAWATCH/web-app/hardware-bridge.js)** | **Hardware Link Engine** | Client-side real-time bridge connecting both interfaces to the Node.js backend (`/api/telemetry`) or directly to the ESP32 IP over Wi-Fi. | Shared Library |
| **[`SolanaWatch_Web_Dashboard_Mockup.html`](file:///C:/Users/agabu/Downloads/CODE%20PROJECTS/SOLANAWATCH/web-app/SolanaWatch_Web_Dashboard_Mockup.html)** | **Standalone Dashboard Mockup** | Lightweight dark-mode responsive dashboard demonstrating live chart streaming, battery health, and disease alert threshold triggers. | Any Desktop or Tablet Browser |
| **`SolanaWatch_iOS_App.html`** | *iOS App Alternate* | Direct copy/alias of `index.html` preserved for file name compatibility. | Mobile / Responsive Browser |
| **`SolanaWatch_PC_Dashboard.html`** | *PC Dashboard Alternate* | Direct copy/alias of `desktop.html` preserved for file name compatibility. | Desktop Browser |

---

## 📡 Live Hardware Connectivity

Both web applications are equipped with the **SolanaWatch Hardware Link**:

1. **Live Hardware Mode (Active by Default):**
   - Automatically polls the backend REST API (`http://localhost:5000/api/telemetry/latest`) or your ESP32's IP every 3 seconds.
   - Updates all live gauges, disease risk scores, dynamic island, and graphs when real sensor packets are received.
   - Shows a pulsing green status indicator (`🟢 Live Hardware`).

2. **Hardware Configuration Modal (Tap `📡 HW Link` in toolbar):**
   - Enter your laptop's local IP or your ESP32's direct Wi-Fi IP address.
   - Test Ping latency with real-time feedback.
   - Adjust polling rates (1.5s benchtop test to 10s power saver).
   - Inject test packets directly (`🚨 Send High Risk`, `⚠️ Send Moderate`, `🟢 Send Safe`).

3. **Presentation / Demo Mode:**
   - Click any scenario button (`High Risk`, `Moderate`, `Safe`) in the header toolbar to switch to simulated presentation mode during evaluations or defense without needing the physical sensors active.

---

## 🚀 How to Run the System

### Step 1: Start the Backend Server
Double-click [`start_server.bat`](file:///C:/Users/agabu/Downloads/CODE%20PROJECTS/SOLANAWATCH/start_server.bat) in the project root, or run in PowerShell:

```powershell
cd "C:\Users\agabu\Downloads\CODE PROJECTS\SOLANAWATCH\backend"
npm start
```
*The server will start on port 5000 and automatically serve the web app at `http://localhost:5000/`.*

### Step 2: Open the Web Application
Open your browser to:
- **Mobile View:** [`http://localhost:5000/`](http://localhost:5000/) or double-click [`web-app/index.html`](file:///C:/Users/agabu/Downloads/CODE%20PROJECTS/SOLANAWATCH/web-app/index.html)
- **PC Desktop View:** [`http://localhost:5000/desktop.html`](http://localhost:5000/desktop.html) or double-click [`web-app/desktop.html`](file:///C:/Users/agabu/Downloads/CODE%20PROJECTS/SOLANAWATCH/web-app/desktop.html)

### Step 3: Connect Physical ESP32 Hardware
1. Flash your ESP32 with [`firmware/SolanaWatch_ESP32_Firmware.ino`](file:///C:/Users/agabu/Downloads/CODE%20PROJECTS/SOLANAWATCH/firmware/SolanaWatch_ESP32_Firmware.ino).
2. Configure your Wi-Fi SSID and password in the `.ino` file.
3. Set `BACKEND_API_URL` in the `.ino` file to your laptop's IP (e.g. `http://192.168.1.100:5000/api/telemetry`).
4. Once powered on, the ESP32 will transmit sensor readings directly to your backend, and the web app will update in real-time!

### Optional: Test Without Physical Hardware (Virtual Stream)
If your hardware is currently powered off, simulate a live ESP32 by running:

```powershell
python "C:\Users\agabu\Downloads\CODE PROJECTS\SOLANAWATCH\scripts\simulate_hardware.py"
```
*This streams real-time microclimate packets to the backend every 3 seconds, letting you watch the web app react live!*
