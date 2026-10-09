# 🚀 SolanaWatch Vercel Production Deployment Guide

This guide walks you through deploying **SolanaWatch** to **Vercel** so your IoT Decision Support System (DSS) can be accessed from any phone, tablet, or PC worldwide, receiving real-time microclimatic telemetry from your remote ESP32 hardware.

---

## 🏗️ Architecture at a Glance

```
  [ESP32 Hardware Node]  ──(HTTPS POST)──>  [Vercel Serverless Function]  <──>  [Turso Cloud DB]
  (Field / Remote Laptop)                   https://<app>.vercel.app/api/telemetry    (Persistent SQLite)
                                                        │
                                                        ▼
                                            [Vercel Global Edge CDN]
                                            https://<app>.vercel.app
                                            (iOS DSS & PC Dashboard)
```

- **Frontend**: Edge CDN serves [`web-app/index.html`](web-app/index.html) and [`web-app/desktop.html`](web-app/desktop.html).
- **Backend**: Serverless Express API running in [`api/index.js`](api/index.js) handling Wallin Late Blight & Bacterial Wilt disease models.
- **Database**: Optional persistent cloud storage via Turso libSQL (free tier).
- **Hardware**: ESP32 using `WiFiClientSecure` sends encrypted telemetry over port 443.

---

## 📋 Prerequisites
1. A free account on [Vercel](https://vercel.com).
2. Git installed on your computer.
3. Your Arduino laptop with Arduino IDE and the ESP32 connected.

---

## 🚀 Option A: Deploy via GitHub (Recommended)

This is the easiest and most reliable method because any future updates pushed to GitHub will automatically deploy to Vercel.

### Step 1: Initialize Git and Commit Your Project
Open PowerShell in your project folder (`C:\Users\agabu\Downloads\CODE PROJECTS\SOLANAWATCH`) and run:

```powershell
git init
git add .
git commit -m "feat: SolanaWatch production deployment for Vercel"
```

### Step 2: Push to a New GitHub Repository
1. Go to [GitHub.com/new](https://github.com/new) and create a new repository (name it `solanawatch`). Keep it Public or Private.
2. Link and push your local repository:
```powershell
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/solanawatch.git
git branch -M main
git push -u origin main
```

### Step 3: Import into Vercel
1. Log into your dashboard at [vercel.com](https://vercel.com).
2. Click **Add New…** > **Project**.
3. Locate `solanawatch` under your GitHub repositories and click **Import**.
4. In the configuration screen:
   - **Framework Preset**: *Other* (detected automatically).
   - **Root Directory**: `./` (leave default).
   - **Build Command**: *None* (or leave empty).
   - **Output Directory**: *None* (or leave empty).
5. Click **Deploy**.
6. Within 30 seconds, Vercel will give you a live production URL:
   `https://solanawatch-xxxx.vercel.app`

---

## ⚡ Option B: Deploy Directly via Vercel CLI

If you don't want to use GitHub, you can deploy straight from PowerShell using the Vercel CLI:

1. In your project directory, run:
```powershell
npx vercel
```
2. Follow the interactive prompts:
   - **Set up and deploy?** -> `Y`
   - **Which scope do you want to deploy to?** -> *Select your personal account*
   - **Link to existing project?** -> `N`
   - **What's your project's name?** -> `solanawatch`
   - **In which directory is your code located?** -> `./`
   - **Want to modify these settings?** -> `N`
3. To deploy directly to production domain:
```powershell
npx vercel --prod
```
4. Copy the production URL shown in your terminal (e.g., `https://solanawatch.vercel.app`).

---

## 🗄️ Optional: Add Free Cloud Database (Turso libSQL)

Vercel serverless functions have ephemeral memory (they sleep when inactive). If you want historical sensor data to be stored permanently in the cloud:

1. Sign up for free at [turso.tech](https://turso.tech).
2. Click **Create Database** and name it `solanawatch-db`.
3. In the database dashboard:
   - Copy the **Database URL** (starts with `libsql://solanawatch-db-xxx.turso.io`).
   - Click **Create Token** and copy the **Auth Token**.
4. Go to your **Vercel Project Dashboard** > **Settings** > **Environment Variables**.
5. Add the following two variables:
   - `TURSO_DATABASE_URL` = `libsql://your-database-name.turso.io`
   - `TURSO_AUTH_TOKEN` = `your_auth_token_here`
6. Redeploy or trigger a redeploy so the serverless function connects to Turso.

*(Note: If you skip Turso, the backend still works immediately using in-memory and cached store!)*

---

## 🔌 Connecting the ESP32 Hardware Remotely

Now that your backend is live on the internet, point your physical hardware to the Vercel endpoint.

### Step 1: Open the Sketch on the Arduino Laptop
1. Copy or open the firmware sketch located at:
   [`firmware/SolanaWatch_ESP32_Firmware.ino`](firmware/SolanaWatch_ESP32_Firmware.ino)
2. In the Arduino IDE, install required libraries if not yet installed:
   - `DHT sensor library` (Adafruit)
   - `OneWire` & `DallasTemperature`
   - `ArduinoJson` (v6 or v7)

### Step 2: Configure Network & Vercel URL
Locate lines 28–34 in [`firmware/SolanaWatch_ESP32_Firmware.ino`](firmware/SolanaWatch_ESP32_Firmware.ino):

```cpp
// Wi-Fi Access Point Credentials
const char* WIFI_SSID     = "YOUR_WIFI_SSID";         // e.g. Phone hotspot or local router
const char* WIFI_PASSWORD = "YOUR_WIFI_PASSWORD";

// Target Production Endpoint
// Replace with your actual Vercel domain:
const char* SERVER_URL    = "https://solanawatch.vercel.app/api/telemetry";
```

> **Why HTTPS works out-of-the-box:** The sketch uses `WiFiClientSecure` with `client.setInsecure()`, so the ESP32 automatically accepts Vercel's Let's Encrypt / Cloudflare SSL certificate without needing manual root CA cert hardcoding.

### Step 3: Flash and Verify
1. Select board **ESP32 Dev Module** and the correct COM port.
2. Click **Upload**.
3. Open **Tools > Serial Monitor** (baud rate `115200`).
4. Watch the serial log:
   ```
   [WiFi] Connected! IP: 192.168.1.104
   [HTTPS] Connecting to: https://solanawatch.vercel.app/api/telemetry
   [HTTPS] Payload: {"node_id":"SOLANA-ESP32-DEV1","air_temperature":24.5,...}
   [HTTPS] POST status code: 200
   [HTTPS] Late Blight Risk: LOW | Bacterial Wilt Risk: MODERATE
   ```

---

## 🧪 Testing Your Live Deployment

### 1. Test Health Endpoint in Browser
Visit your deployment's health route:
```
https://solanawatch.vercel.app/api/health
```
You should receive:
```json
{
  "status": "online",
  "system": "SolanaWatch Decision Support Platform",
  "version": "1.0.0",
  "database": "libSQL Cloud (or local memory)",
  "uptime_seconds": 12
}
```

### 2. Test with Virtual Telemetry Streamer
You can test your live Vercel deployment right now from your PC without touching hardware:

```powershell
python scripts/simulate_hardware.py --url https://solanawatch.vercel.app/api/telemetry
```

You will see live packets posted to your cloud server every 3 seconds!

### 3. Open the Dashboards on Any Device
- **Mobile iOS DSS**: `https://solanawatch.vercel.app`
- **PC Agronomist Dashboard**: `https://solanawatch.vercel.app/desktop.html`

Both dashboards automatically detect that they are running on Vercel and seamlessly pull real-time telemetry and disease advisories from `/api/telemetry/latest`.
