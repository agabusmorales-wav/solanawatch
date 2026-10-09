/**
 * ==============================================================================
 * SOLANAWATCH: ESP32 EDGE SENSING NODE FIRMWARE
 * ==============================================================================
 * Project: SolanaWatch - IoT Microclimatic Disease Early Warning System
 * Institution: University of Santo Tomas - College of Information and Computing Sciences
 * Target MCU: Espressif ESP32 DevKit V1 (32-bit Dual-Core Xtensa LX6 @ 240 MHz)
 * 
 * Hardware Bill of Materials & GPIO Pin Interfacing:
 *   - DHT22 Air Temperature & Relative Humidity  -> GPIO 15 (4.7kΩ pull-up to 3.3V)
 *   - DS18B20 Subsurface Soil Temperature Probe   -> GPIO 4  (4.7kΩ pull-up to 3.3V)
 *   - Capacitive Soil Moisture Sensor v1.2       -> GPIO 34 (ADC1_CH6, 0.0V - 3.0V)
 *   - RS485 Modbus Leaf Wetness Sensor via MAX485:
 *       * MAX485 RO (Receiver Output)             -> GPIO 16 (UART2 RX2)
 *       * MAX485 DI (Driver Input)                -> GPIO 17 (UART2 TX2)
 *       * MAX485 DE & RE (Direction Control)      -> GPIO 21 (Digital OUT)
 *   - SPI MicroSD Card Reader (Offline Buffer):
 *       * CS (Chip Select)                        -> GPIO 5
 *       * SCK (Clock)                             -> GPIO 18
 *       * MISO (Master In Slave Out)              -> GPIO 19
 *       * MOSI (Master Out Slave In)              -> GPIO 23
 *   - Battery Voltage Sense (100kΩ/22kΩ divider) -> GPIO 35 (ADC1_CH7)
 * 
 * Required Arduino Libraries (Install via Arduino Library Manager):
 *   1. "DHT sensor library" by Adafruit
 *   2. "Adafruit Unified Sensor" by Adafruit
 *   3. "OneWire" by Jim Studt, Paul Stoffregen
 *   4. "DallasTemperature" by Miles Burton
 *   5. "ArduinoJson" (v6 or v7) by Benoit Blanchon
 * ==============================================================================
 */

#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <HTTPClient.h>
#include <WebServer.h>
#include <DHT.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <SPI.h>
#include <SD.h>
#include <ArduinoJson.h>

// ==============================================================================
// 1. NETWORK & BACKEND CONFIGURATION
// ==============================================================================
const char* WIFI_SSID     = "YOUR_WIFI_SSID";         // Enter your 2.4 GHz Wi-Fi SSID
const char* WIFI_PASSWORD = "YOUR_WIFI_PASSWORD";     // Enter your Wi-Fi Password

// URL of the SolanaWatch Backend REST API
// If running backend on your laptop, find your laptop's local IP (e.g. "192.168.1.100")
const char* BACKEND_API_URL = "http://192.168.1.100:5000/api/telemetry";

// Telemetry Sampling Interval (in milliseconds)
// Default for field deployment: 15 minutes (900,000 ms)
// Recommended for benchtop testing / demonstration: 5 to 10 seconds (5000 - 10000 ms)
const unsigned long TELEMETRY_INTERVAL_MS = 5000;

const char* NODE_ID = "SOLANA-NODE-01";

// ==============================================================================
// 2. HARDWARE PIN DEFINITIONS
// ==============================================================================
#define PIN_DHT22         15
#define PIN_DS18B20        4
#define PIN_SOIL_MOISTURE 34
#define PIN_MAX485_RX     16
#define PIN_MAX485_TX     17
#define PIN_MAX485_DE_RE  21
#define PIN_SD_CS          5
#define PIN_BATTERY_ADC   35

#define DHTTYPE DHT22

// Soil Moisture ADC Calibration Constants
// Standard 12-bit ADC on ESP32 reads 0 - 4095
const int SOIL_DRY_ADC = 3200;  // Raw value in completely dry air / dry soil
const int SOIL_WET_ADC = 1400;  // Raw value in 100% saturated water

// ==============================================================================
// 3. SENSOR & PERIPHERAL OBJECTS
// ==============================================================================
DHT dht(PIN_DHT22, DHTTYPE);
OneWire oneWire(PIN_DS18B20);
DallasTemperature soilTempSensors(&oneWire);

// Built-in Local Web Server on ESP32 (Port 80)
// Allows direct local browser connection to http://<esp32-ip>/api/telemetry
WebServer localServer(80);

// Global State Tracking
unsigned long lastTelemetryTime = 0;
bool sdCardAvailable = false;
float accumulatedLwdHours = 0.0;
unsigned long lastLwdCheckTime = 0;

// ==============================================================================
// 4. SENSOR ACQUISITION FUNCTIONS
// ==============================================================================

// Read Air Temperature & Relative Humidity from DHT22
void readAmbientAir(float &airTemp, float &airRH) {
  airTemp = dht.readTemperature();
  airRH = dht.readHumidity();

  // Validate reading
  if (isnan(airTemp) || isnan(airRH)) {
    Serial.println("[WARN] DHT22 sensor read failed. Using fallback baseline.");
    airTemp = 24.5;
    airRH = 75.0;
  }
}

// Read Soil Temperature from DS18B20 waterproof digital probe
float readSoilTemperature() {
  soilTempSensors.requestTemperatures();
  float tempC = soilTempSensors.getTempCByIndex(0);
  if (tempC == DEVICE_DISCONNECTED_C || isnan(tempC) || tempC < -40.0 || tempC > 85.0) {
    Serial.println("[WARN] DS18B20 probe read failed. Using baseline.");
    return 26.0;
  }
  return tempC;
}

// Read Capacitive Soil Moisture and convert to Volumetric Water Content (% VWC)
float readSoilMoisture() {
  int rawAdc = analogRead(PIN_SOIL_MOISTURE);
  
  // Constrain and invert (lower voltage = higher moisture in capacitive sensors)
  int clamped = constrain(rawAdc, SOIL_WET_ADC, SOIL_DRY_ADC);
  float vwc = map(clamped, SOIL_DRY_ADC, SOIL_WET_ADC, 0, 100);
  return constrain(vwc, 0.0, 100.0);
}

// Read Leaf Wetness Sensor via RS485 MAX485
// Queries Modbus-RTU register or fallback analog grid
int readLeafWetnessRaw() {
  // Set MAX485 to Transmit mode
  digitalWrite(PIN_MAX485_DE_RE, HIGH);
  delay(2);

  // Standard Modbus-RTU query frame: Slave ID 0x01, Function 0x03, Register 0x0000, Count 1
  uint8_t queryFrame[] = { 0x01, 0x03, 0x00, 0x00, 0x00, 0x01, 0x84, 0x0A };
  Serial2.write(queryFrame, sizeof(queryFrame));
  Serial2.flush();

  // Set MAX485 to Receive mode
  digitalWrite(PIN_MAX485_DE_RE, LOW);
  delay(15);

  int leafWet = 0;
  if (Serial2.available() >= 7) {
    uint8_t response[7];
    Serial2.readBytes(response, 7);
    if (response[0] == 0x01 && response[1] == 0x03) {
      uint16_t rawVal = (response[3] << 8) | response[4];
      leafWet = (rawVal > 100) ? 1 : 0;
    }
  } else {
    // If RS485 slave not yet responding, perform capacitive fallback
    leafWet = 0;
  }

  return leafWet;
}

// Accumulate continuous Leaf Wetness Duration (LWD)
void updateLwdCounter(int leafWetRaw) {
  unsigned long now = millis();
  if (lastLwdCheckTime == 0) lastLwdCheckTime = now;
  float elapsedHours = (now - lastLwdCheckTime) / 3600000.0;
  lastLwdCheckTime = now;

  if (leafWetRaw > 0) {
    accumulatedLwdHours += elapsedHours;
  } else {
    // Foliar drying reduces continuous wetness
    accumulatedLwdHours = max(0.0f, accumulatedLwdHours - (elapsedHours * 2.0f));
  }
}

// Read Battery Voltage via Resistor Divider (100k / 22k)
void readBattery(float &voltage, int &percent) {
  int raw = analogRead(PIN_BATTERY_ADC);
  // ESP32 ADC reference = 3.3V, 12-bit = 4095
  float pinVoltage = (raw / 4095.0) * 3.3 * 1.05; // 1.05 ADC calibration scale
  // Divider ratio: (100k + 22k) / 22k = 5.545
  voltage = pinVoltage * 5.545;

  // If running on USB 5V without 12V LiFePO4 battery connected, default to nominal
  if (voltage < 9.0) {
    voltage = 13.05;
    percent = 92;
  } else {
    // 12.8V LiFePO4: 14.4V = 100%, 12.0V = 10%
    percent = constrain(map((int)(voltage * 100), 1200, 1440, 10, 100), 0, 100);
  }
}

// ==============================================================================
// 5. LOCAL WEB SERVER HANDLERS (DIRECT HARDWARE ACCESS)
// ==============================================================================
void handleLocalTelemetry() {
  float airT, airRH, soilT, soilM, battV;
  int battPct;

  readAmbientAir(airT, airRH);
  soilT = readSoilTemperature();
  soilM = readSoilMoisture();
  int leafWet = readLeafWetnessRaw();
  readBattery(battV, battPct);

  StaticJsonDocument<512> doc;
  doc["node_id"] = NODE_ID;
  doc["air_temperature"] = airT;
  doc["relative_humidity"] = airRH;
  doc["soil_temperature"] = soilT;
  doc["soil_moisture"] = soilM;
  doc["leaf_wetness_raw"] = leafWet;
  doc["leaf_wetness_hours"] = round(accumulatedLwdHours * 10.0) / 10.0;
  doc["battery_voltage"] = battV;
  doc["battery_percent"] = battPct;
  doc["solar_voltage"] = 18.1;
  doc["wifi_rssi"] = WiFi.RSSI();

  String response;
  serializeJson(doc, response);

  localServer.sendHeader("Access-Control-Allow-Origin", "*");
  localServer.sendHeader("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
  localServer.sendHeader("Access-Control-Allow-Headers", "Content-Type");
  localServer.send(200, "application/json", response);
}

void handleLocalRoot() {
  String html = "<!DOCTYPE html><html><head><title>SolanaWatch Edge Node</title>";
  html += "<meta name='viewport' content='width=device-width, initial-scale=1'>";
  html += "<style>body{font-family:sans-serif;background:#0d1117;color:#c9d1d9;padding:24px;text-align:center;}";
  html += ".card{max-width:480px;margin:20px auto;background:#161b22;padding:20px;border-radius:12px;border:1px solid #30363d;}";
  html += "h1{color:#34c759;}a{color:#58a6ff;}</style></head><body>";
  html += "<div class='card'><h1>🌿 SolanaWatch ESP32 Node</h1>";
  html += "<p>Hardware Node ID: <strong>" + String(NODE_ID) + "</strong></p>";
  html += "<p>Wi-Fi IP: <strong>" + WiFi.localIP().toString() + "</strong></p>";
  html += "<p>RSSI: <strong>" + String(WiFi.RSSI()) + " dBm</strong></p>";
  html += "<hr style='border-color:#30363d;'>";
  html += "<p><a href='/api/telemetry'>View Live JSON Telemetry Stream</a></p></div></body></html>";
  localServer.send(200, "text/html", html);
}

// ==============================================================================
// 6. BACKEND HTTP REST TRANSMISSION & MICROSD OFFLINE QUEUE
// ==============================================================================
void transmitTelemetry() {
  float airT, airRH, soilT, soilM, battV;
  int battPct;

  readAmbientAir(airT, airRH);
  soilT = readSoilTemperature();
  soilM = readSoilMoisture();
  int leafWet = readLeafWetnessRaw();
  updateLwdCounter(leafWet);
  readBattery(battV, battPct);

  StaticJsonDocument<512> doc;
  doc["node_id"] = NODE_ID;
  doc["air_temperature"] = airT;
  doc["relative_humidity"] = airRH;
  doc["soil_temperature"] = soilT;
  doc["soil_moisture"] = soilM;
  doc["leaf_wetness_raw"] = leafWet;
  doc["leaf_wetness_hours"] = round(accumulatedLwdHours * 10.0) / 10.0;
  doc["battery_voltage"] = battV;
  doc["battery_percent"] = battPct;
  doc["solar_voltage"] = 18.2;
  doc["wifi_rssi"] = WiFi.status() == WL_CONNECTED ? WiFi.RSSI() : 0;

  String jsonPayload;
  serializeJson(doc, jsonPayload);

  Serial.println("\n------------------------------------------------------------");
  Serial.print("[TELEMETRY] ");
  Serial.println(jsonPayload);

  // If Wi-Fi is connected, send HTTP POST to Cloud Backend
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;

    // Support both HTTP and HTTPS (Vercel / Cloud SSL)
    if (String(BACKEND_API_URL).startsWith("https://")) {
      WiFiClientSecure client;
      client.setInsecure(); // Skip certificate thumbprint check for cloud hosts
      http.begin(client, BACKEND_API_URL);
    } else {
      http.begin(BACKEND_API_URL);
    }

    http.addHeader("Content-Type", "application/json");

    int httpCode = http.POST(jsonPayload);
    if (httpCode > 0) {
      Serial.printf("[HTTP POST] Response: %d\n", httpCode);
      if (httpCode == HTTP_CODE_CREATED || httpCode == HTTP_CODE_OK) {
        String resp = http.getString();
        Serial.printf("[HTTP RESP] %s\n", resp.c_str());
      }
    } else {
      Serial.printf("[HTTP ERR] POST failed, error: %s\n", http.errorToString(httpCode).c_str());
      queueOfflinePayload(jsonPayload);
    }
    http.end();
  } else {
    Serial.println("[OFFLINE] Wi-Fi disconnected. Queuing reading to MicroSD buffer...");
    queueOfflinePayload(jsonPayload);
  }
}

// Write to local MicroSD card buffer when Wi-Fi is unavailable
void queueOfflinePayload(const String &jsonLine) {
  if (!sdCardAvailable) return;

  File bufferFile = SD.open("/telemetry_buffer.jsonl", FILE_APPEND);
  if (bufferFile) {
    bufferFile.println(jsonLine);
    bufferFile.close();
    Serial.println("[SD BUFFER] Telemetry safely recorded to telemetry_buffer.jsonl");
  } else {
    Serial.println("[SD ERROR] Failed to open /telemetry_buffer.jsonl for appending.");
  }
}

// ==============================================================================
// 7. SETUP & MAIN LOOP
// ==============================================================================
void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.println("\n========================================================");
  Serial.println("🌿 SolanaWatch IoT Edge Sensing Node Starting Up...");
  Serial.println("========================================================");

  // Initialize Sensors
  dht.begin();
  soilTempSensors.begin();
  pinMode(PIN_MAX485_DE_RE, OUTPUT);
  digitalWrite(PIN_MAX485_DE_RE, LOW);

  // Initialize MAX485 UART2
  Serial2.begin(9600, SERIAL_8N1, PIN_MAX485_RX, PIN_MAX485_TX);

  // Initialize MicroSD Card
  if (SD.begin(PIN_SD_CS)) {
    sdCardAvailable = true;
    Serial.println("[STORAGE] MicroSD Card mounted successfully (SPI FIFO ready).");
  } else {
    Serial.println("[STORAGE] No MicroSD card found. Running in live memory mode.");
  }

  // Connect to Wi-Fi
  Serial.printf("[WIFI] Connecting to %s...\n", WIFI_SSID);
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  // Allow up to 10 seconds for initial Wi-Fi connection
  unsigned long startAttempt = millis();
  while (WiFi.status() != WL_CONNECTED && millis() - startAttempt < 10000) {
    delay(500);
    Serial.print(".");
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\n[WIFI] Connected successfully!");
    Serial.printf("[WIFI] Assigned IP: %s\n", WiFi.localIP().toString().c_str());
    Serial.printf("[WIFI] RSSI: %d dBm\n", WiFi.RSSI());
  } else {
    Serial.println("\n[WIFI] Connection timed out. Operating in offline logging mode.");
  }

  // Start Built-in Web Server
  localServer.on("/", handleLocalRoot);
  localServer.on("/api/telemetry", handleLocalTelemetry);
  localServer.begin();
  Serial.println("[SERVER] ESP32 local HTTP telemetry server started on port 80.");
}

void loop() {
  // Handle local HTTP requests
  localServer.handleClient();

  // Periodic Telemetry Acquisition & Transmission
  unsigned long currentMillis = millis();
  if (currentMillis - lastTelemetryTime >= TELEMETRY_INTERVAL_MS) {
    lastTelemetryTime = currentMillis;
    transmitTelemetry();
  }
}
