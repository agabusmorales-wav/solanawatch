# SolanaWatch 🌿⚡ ESP32 Edge Firmware & Hardware Setup Guide

> **Microcontroller Firmware for Field Sensing Node**  
> *Target MCU: Espressif ESP32 DevKit V1 (32-bit Dual-Core Xtensa LX6 @ 240 MHz)*  
> *University of Santo Tomas – College of Information and Computing Sciences*

---

## 📌 Overview

The [`SolanaWatch_ESP32_Firmware.ino`](file:///C:/Users/agabu/Downloads/CODE%20PROJECTS/SOLANAWATCH/firmware/SolanaWatch_ESP32_Firmware.ino) sketch equips the ESP32 to:
1. Sample physical sensors (**DHT22**, **DS18B20**, **Capacitive Soil Moisture v1.2**, **RS485 Leaf Wetness Grid**, and **Battery Voltage Divider**).
2. Transmit real-time telemetry over 2.4 GHz Wi-Fi via `HTTP POST` JSON packets to the SolanaWatch backend (`/api/telemetry`).
3. Maintain an offline local FIFO queue on the MicroSD card (`telemetry_buffer.jsonl`) during network disconnects.
4. Serve an onboard local HTTP API directly on the ESP32 at `http://<esp32-ip>/api/telemetry`.

---

## 🔌 Hardware Interfacing & Pinout

| Sensor / Module | Physical Pin / Function | ESP32 GPIO Pin | Protocol | Operating Voltage & Notes |
| :--- | :--- | :--- | :--- | :--- |
| **DHT22 / AM2302** | Data Out | `GPIO 15` | 1-Wire Digital | 3.3V DC • Requires 4.7kΩ pull-up to 3.3V |
| **DS18B20 Soil Probe** | Data (Yellow/White) | `GPIO 4` | Dallas 1-Wire | 3.3V DC • Requires 4.7kΩ pull-up to 3.3V |
| **Capacitive Moisture v1.2**| AOUT (Analog Signal) | `GPIO 34` | ADC1_CH6 | 3.3V DC • $0.0\text{V} - 3.0\text{V}$ output |
| **MAX485 Transceiver** | RO (Receiver Output) | `GPIO 16` | UART2 RX2 | 3.3V DC |
| **MAX485 Transceiver** | DI (Driver Input) | `GPIO 17` | UART2 TX2 | 3.3V DC |
| **MAX485 Transceiver** | DE & RE (Direction) | `GPIO 21` | Digital Out | 3.3V DC (HIGH = Transmit, LOW = Receive) |
| **RS485 Leaf Wetness** | A & B Differential | To MAX485 A/B | Modbus-RTU | 12.0V DC supply • 120Ω termination across A/B |
| **MicroSD SPI Module** | CS (Chip Select) | `GPIO 5` | Hardware SPI | 3.3V DC |
| **MicroSD SPI Module** | SCK (Clock) | `GPIO 18` | Hardware SPI | 3.3V DC |
| **MicroSD SPI Module** | MISO (Data Out) | `GPIO 19` | Hardware SPI | 3.3V DC |
| **MicroSD SPI Module** | MOSI (Data In) | `GPIO 23` | Hardware SPI | 3.3V DC |
| **Battery Divider** | Midpoint ($100\text{k}\Omega / 22\text{k}\Omega$) | `GPIO 35` | ADC1_CH7 | Measures 12.8V LiFePO4 battery safely |

---

## 💻 Arduino IDE Setup Instructions

### 1. Board Installation
1. Open **Arduino IDE** (v2.x recommended).
2. Go to **File** ➔ **Preferences** ➔ **Additional boards manager URLs**, add:  
   `https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json`
3. Go to **Tools** ➔ **Board** ➔ **Boards Manager**, search for `esp32` by Espressif Systems and click **Install**.
4. Select **Tools** ➔ **Board** ➔ **esp32** ➔ **DOIT ESP32 DEVKIT V1**.

### 2. Install Required Libraries
Open **Tools** ➔ **Manage Libraries...** and search for:
1. `DHT sensor library` by Adafruit
2. `Adafruit Unified Sensor` by Adafruit
3. `OneWire` by Jim Studt, Paul Stoffregen
4. `DallasTemperature` by Miles Burton
5. `ArduinoJson` (v6 or v7) by Benoit Blanchon

### 3. Configure Wi-Fi & Backend Address
Open [`SolanaWatch_ESP32_Firmware.ino`](file:///C:/Users/agabu/Downloads/CODE%20PROJECTS/SOLANAWATCH/firmware/SolanaWatch_ESP32_Firmware.ino):
```cpp
const char* WIFI_SSID     = "YOUR_WIFI_NAME";
const char* WIFI_PASSWORD = "YOUR_WIFI_PASSWORD";

// Replace with your laptop's Wi-Fi IP address:
const char* BACKEND_API_URL = "http://192.168.1.100:5000/api/telemetry";
```

### 4. Upload & Monitor
1. Connect your ESP32 to your PC via Micro-USB cable.
2. Select the correct **Port** (e.g. `COM3` or `COM4`).
3. Click **Upload** (Ctrl + U).
4. Open **Serial Monitor** (Ctrl + Shift + M) set to **115200 baud** to see real-time sensor readings and HTTP transmission confirmations!
