#!/usr/bin/env python3
"""
==============================================================================
SOLANAWATCH - USB SERIAL TO CLOUD BRIDGE (RUN ON SEPARATE LAPTOP)
==============================================================================
Reads live telemetry from the ESP32 connected via USB Serial and forwards it
to the SolanaWatch Vercel Web App or local Node.js backend.

Usage:
  python serial_bridge.py
  python serial_bridge.py --port COM3 --baud 115200 --url https://your-app.vercel.app/api/telemetry
==============================================================================
"""

import sys
import time
import json
import argparse
import urllib.request
import urllib.error

try:
    import serial
    import serial.tools.list_ports
except ImportError:
    print("[ERROR] 'pyserial' library not found.")
    print("Please run:  pip install pyserial")
    sys.exit(1)

def find_esp32_port():
    """Auto-detects USB serial COM port for ESP32 / CP210x / CH340 / FTDI."""
    ports = serial.tools.list_ports.comports()
    for port, desc, hwid in ports:
        desc_lower = desc.lower()
        if any(keyword in desc_lower for keyword in ["cp210", "ch340", "ch341", "usb-serial", "ftdi", "uart", "esp32"]):
            return port
    if ports:
        return ports[0].device
    return None

def forward_to_cloud(url, payload_dict):
    """Sends JSON telemetry to the Vercel backend using Python standard library."""
    data_bytes = json.dumps(payload_dict).encode('utf-8')
    req = urllib.request.Request(
        url,
        data=data_bytes,
        headers={
            'Content-Type': 'application/json',
            'User-Agent': 'SolanaWatch-SerialBridge/1.0'
        },
        method='POST'
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            status = response.getcode()
            body = response.read().decode('utf-8')
            return status, body
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode('utf-8')
    except Exception as e:
        return 0, str(e)

def main():
    parser = argparse.ArgumentParser(description="SolanaWatch Serial to Cloud Forwarder")
    parser.add_argument("--port", type=str, default=None, help="COM port (e.g. COM3 or /dev/ttyUSB0)")
    parser.add_argument("--baud", type=int, default=115200, help="Baud rate (default: 115200)")
    parser.add_argument("--url", type=str, default="http://localhost:5000/api/telemetry", 
                        help="Backend URL (e.g. https://your-app.vercel.app/api/telemetry)")
    args = parser.parse_args()

    port = args.port or find_esp32_port()
    if not port:
        print("[!] No USB Serial COM ports detected.")
        print("    Please connect the ESP32 to this laptop and try again.")
        sys.exit(1)

    print("==================================================================")
    print("  SOLANAWATCH: USB SERIAL TO CLOUD BRIDGE")
    print("==================================================================")
    print(f"  * Serial Port : {port} @ {args.baud} baud")
    print(f"  * Cloud Target: {args.url}")
    print("==================================================================")
    print("  Connecting to ESP32...")

    try:
        ser = serial.Serial(port, args.baud, timeout=1)
        time.sleep(1.5)  # Allow ESP32 serial to stabilize
        print(f"  [CONNECTED] Listening for telemetry on {port}...\n")
    except Exception as e:
        print(f"  [ERROR] Could not open {port}: {e}")
        sys.exit(1)

    packets_forwarded = 0

    while True:
        try:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            if not line:
                continue

            # Look for JSON output from ESP32
            json_str = None
            if line.startswith("[JSON]"):
                json_str = line.replace("[JSON]", "").strip()
            elif line.startswith("{") and line.endswith("}"):
                json_str = line

            if json_str:
                try:
                    payload = json.loads(json_str)
                    print(f"[{time.strftime('%H:%M:%S')}] Telemetry Ingested:")
                    print(f"   Air Temp: {payload.get('air_temperature')}°C | RH: {payload.get('relative_humidity')}% | Soil M: {payload.get('soil_moisture')}% | Leaf Wet: {payload.get('leaf_wetness_hours')}h")
                    
                    status, resp = forward_to_cloud(args.url, payload)
                    if status == 200 or status == 201:
                        packets_forwarded += 1
                        print(f"   --> Synced to Cloud! (HTTP {status}) | Total Forwarded: {packets_forwarded}\n")
                    else:
                        print(f"   --> Cloud Sync Failed: HTTP {status} ({resp})\n")
                except json.JSONDecodeError:
                    pass
            else:
                # Echo regular monitor lines
                if "[SOLANAWATCH REPORT]" in line or "°C" in line or "Leaf Wetness" in line:
                    print(f"   {line}")

        except KeyboardInterrupt:
            print("\nBridge stopped by user.")
            break
        except Exception as e:
            print(f"[!] Serial read error: {e}")
            time.sleep(1)

    ser.close()

if __name__ == "__main__":
    main()
