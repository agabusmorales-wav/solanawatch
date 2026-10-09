"""
==============================================================================
SOLANAWATCH: VIRTUAL HARDWARE TELEMETRY STREAM SIMULATOR
==============================================================================
Simulates an active ESP32 edge sensing node transmitting real-time sensor packets
over HTTP POST to the SolanaWatch backend (http://localhost:5000/api/telemetry).

Useful for benchtop verification, UI testing, and oral defense demonstrations.
==============================================================================
"""

import argparse
import time
import json
import random
import urllib.request
import urllib.error

parser = argparse.ArgumentParser(description="SolanaWatch Virtual Hardware Telemetry Stream Simulator")
parser.add_argument("--url", default="http://localhost:5000/api/telemetry", help="Target telemetry POST URL (e.g. https://your-project.vercel.app/api/telemetry)")
parser.add_argument("--interval", type=float, default=3.0, help="Transmission interval in seconds (default: 3.0)")
args = parser.parse_args()

BACKEND_URL = args.url
INTERVAL_SECONDS = args.interval

print("=" * 65)
print("🌿 SolanaWatch ESP32 Hardware Telemetry Simulator")
print(f"📡 Target Endpoint: {BACKEND_URL}")
print(f"⏱️  Transmission Rate: Every {INTERVAL_SECONDS} seconds")
print("Press Ctrl+C to terminate.")
print("=" * 65)

# Initial baseline
air_temp = 22.0
air_rh = 82.0
soil_temp = 27.0
soil_moisture = 65.0
lwd_hours = 5.0
batt_pct = 95
packet_count = 0

while True:
    packet_count += 1
    # Natural microclimatic jitter
    air_temp = round(air_temp + random.uniform(-0.3, 0.4), 1)
    air_rh = round(max(50.0, min(99.0, air_rh + random.uniform(-0.8, 1.2))), 1)
    soil_temp = round(soil_temp + random.uniform(-0.1, 0.2), 1)
    soil_moisture = round(max(30.0, min(90.0, soil_moisture + random.uniform(-0.5, 0.7))), 1)
    
    # Accumulate leaf wetness if RH > 85%
    if air_rh >= 88.0:
        lwd_hours = round(lwd_hours + 0.1, 1)
        leaf_raw = 1
    else:
        lwd_hours = round(max(0.0, lwd_hours - 0.05), 1)
        leaf_raw = 0

    payload = {
        "node_id": "SOLANA-ESP32-DEV1",
        "air_temperature": air_temp,
        "relative_humidity": air_rh,
        "soil_temperature": soil_temp,
        "soil_moisture": soil_moisture,
        "leaf_wetness_raw": leaf_raw,
        "leaf_wetness_hours": lwd_hours,
        "battery_voltage": round(12.8 + random.uniform(-0.05, 0.1), 2),
        "battery_percent": batt_pct,
        "solar_voltage": 17.8,
        "wifi_rssi": random.randint(-68, -55)
    }

    try:
        req = urllib.request.Request(
            BACKEND_URL,
            data=json.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        with urllib.request.urlopen(req, timeout=3) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            lb = data.get("disease_analysis", {}).get("late_blight", {})
            bw = data.get("disease_analysis", {}).get("bacterial_wilt", {})
            print(f"[Packet #{packet_count}] Sent -> Air: {air_temp}°C, {air_rh}% | Soil: {soil_moisture}% | LWD: {lwd_hours}h | LB: {lb.get('risk_level')} (SV {lb.get('severity_value')}) | BW: {bw.get('risk_level')}")
    except urllib.error.URLError as e:
        print(f"[Error #{packet_count}] Could not reach backend: {e.reason}. Ensure 'npm start' is running in backend/ folder.")

    time.sleep(INTERVAL_SECONDS)
