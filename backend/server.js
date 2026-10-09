/**
 * ==============================================================================
 * SOLANAWATCH IoT BACKEND & DISEASE EARLY WARNING REST API SERVER
 * ==============================================================================
 * University of Santo Tomas – College of Information and Computing Sciences
 * Department of Information Technology
 * 
 * Ingests live telemetry from field ESP32 edge nodes (Wi-Fi / HTTP POST),
 * executes literature-grounded plant pathology disease risk algorithms
 * (Wallin Severity Values for Late Blight & Hydrothermal Indices for Bacterial Wilt),
 * persists readings, and serves real-time data to SolanaWatch Web & Mobile Apps.
 * ==============================================================================
 */

const express = require('express');
const cors = require('cors');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 5000;
const DATA_DIR = process.env.VERCEL ? path.join('/tmp', 'solanawatch_data') : path.join(__dirname, 'data');
const DB_FILE = path.join(DATA_DIR, 'telemetry_db.json');

// Ensure data storage directory exists
if (!fs.existsSync(DATA_DIR)) {
  fs.mkdirSync(DATA_DIR, { recursive: true });
}

// Turso Distributed libSQL Cloud Database Client (Optional cloud persistence)
let tursoClient = null;
if (process.env.TURSO_DATABASE_URL && process.env.TURSO_AUTH_TOKEN) {
  try {
    const { createClient } = require('@libsql/client');
    tursoClient = createClient({
      url: process.env.TURSO_DATABASE_URL,
      authToken: process.env.TURSO_AUTH_TOKEN
    });
    console.log('[Turso] Connected to Turso Distributed Cloud Database.');
    initTursoDatabase();
  } catch (err) {
    console.warn('[Turso] Client init notice (using local store):', err.message);
  }
}

async function initTursoDatabase() {
  if (!tursoClient) return;
  try {
    await tursoClient.execute(`
      CREATE TABLE IF NOT EXISTS sensor_readings_tbl (
        reading_id TEXT PRIMARY KEY,
        node_id TEXT NOT NULL,
        recorded_at TEXT NOT NULL,
        air_temperature REAL NOT NULL,
        relative_humidity REAL NOT NULL,
        soil_temperature REAL NOT NULL,
        soil_moisture REAL NOT NULL,
        leaf_wetness_raw INTEGER,
        leaf_wetness_hours REAL,
        battery_voltage REAL,
        battery_percent INTEGER,
        solar_voltage REAL,
        wifi_rssi INTEGER,
        disease_json TEXT,
        UNIQUE(node_id, recorded_at)
      );
    `);
    console.log('[Turso] Table schema verified: sensor_readings_tbl');
    await loadTursoRecords();
  } catch (err) {
    console.error('[Turso] Table init error:', err.message);
  }
}

async function persistToTurso(record) {
  if (!tursoClient) return;
  try {
    await tursoClient.execute({
      sql: `INSERT OR REPLACE INTO sensor_readings_tbl (
        reading_id, node_id, recorded_at, air_temperature, relative_humidity,
        soil_temperature, soil_moisture, leaf_wetness_raw, leaf_wetness_hours,
        battery_voltage, battery_percent, solar_voltage, wifi_rssi, disease_json
      ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`,
      args: [
        record.reading_id,
        record.node_id,
        record.recorded_at,
        record.air_temperature,
        record.relative_humidity,
        record.soil_temperature,
        record.soil_moisture,
        record.leaf_wetness_raw,
        record.leaf_wetness_hours,
        record.battery_voltage,
        record.battery_percent,
        record.solar_voltage,
        record.wifi_rssi,
        JSON.stringify(record.disease_analysis)
      ]
    });
  } catch (err) {
    console.warn('[Turso] Insert warning:', err.message);
  }
}

async function loadTursoRecords() {
  if (!tursoClient) return;
  try {
    const res = await tursoClient.execute(`
      SELECT * FROM sensor_readings_tbl 
      ORDER BY recorded_at DESC LIMIT 300
    `);
    if (res.rows && res.rows.length > 0) {
      const loaded = res.rows.reverse().map(r => ({
        reading_id: r.reading_id,
        node_id: r.node_id,
        recorded_at: r.recorded_at,
        air_temperature: Number(r.air_temperature),
        relative_humidity: Number(r.relative_humidity),
        soil_temperature: Number(r.soil_temperature),
        soil_moisture: Number(r.soil_moisture),
        leaf_wetness_raw: Number(r.leaf_wetness_raw),
        leaf_wetness_hours: Number(r.leaf_wetness_hours),
        battery_voltage: Number(r.battery_voltage),
        battery_percent: Number(r.battery_percent),
        solar_voltage: Number(r.solar_voltage),
        wifi_rssi: Number(r.wifi_rssi),
        disease_analysis: r.disease_json ? JSON.parse(r.disease_json) : null
      }));
      telemetryReadings = loaded;
      console.log(`[Turso] Successfully loaded ${telemetryReadings.length} records from Cloud Database.`);
    }
  } catch (err) {
    console.warn('[Turso] Could not fetch initial records:', err.message);
  }
}

// Middleware
app.use(cors());
app.use(express.json({ limit: '2mb' }));

// Serve the static web-app frontend directly
const webAppPath = path.join(__dirname, '..', 'web-app');
app.use(express.static(webAppPath));

// In-Memory Telemetry Storage (persisted to disk)
let telemetryReadings = [];

function loadDatabase() {
  if (fs.existsSync(DB_FILE)) {
    try {
      const raw = fs.readFileSync(DB_FILE, 'utf8');
      telemetryReadings = JSON.parse(raw);
      console.log(`[Database] Loaded ${telemetryReadings.length} historical records.`);
    } catch (err) {
      console.error('[Database] Failed to read existing db file, initializing fresh:', err.message);
      seedInitialData();
    }
  } else {
    seedInitialData();
  }
}

function saveDatabase(newRecord) {
  try {
    if (newRecord) {
      persistToTurso(newRecord);
    }
    // Keep maximum 1000 latest records in local JSON store
    if (telemetryReadings.length > 1000) {
      telemetryReadings = telemetryReadings.slice(-1000);
    }
    fs.writeFileSync(DB_FILE, JSON.stringify(telemetryReadings, null, 2), 'utf8');
  } catch (err) {
    console.error('[Database] Error persisting telemetry:', err.message);
  }
}

// Seed initial realistic 24-hour historical records if brand new database
function seedInitialData() {
  console.log('[Database] Seeding initial baseline telemetry for demonstration...');
  const now = Date.now();
  const seeded = [];
  
  for (let i = 24; i >= 0; i--) {
    const timestamp = new Date(now - i * 3600 * 1000).toISOString();
    const progress = (24 - i) / 24;
    
    // Gradual progression into moderate microclimate
    const airT = parseFloat((23.0 - (progress * 2.5) + (Math.sin(i) * 1.2)).toFixed(1));
    const airRH = parseFloat((70.0 + (progress * 18.0) + (Math.cos(i) * 3)).toFixed(1));
    const soilT = parseFloat((25.0 + (progress * 2.0)).toFixed(1));
    const soilM = parseFloat((55.0 + (progress * 14.0)).toFixed(1));
    const lwd = parseFloat((progress * 7.5).toFixed(1));
    
    const record = processTelemetry({
      node_id: "SOLANA-NODE-01",
      recorded_at: timestamp,
      air_temperature: airT,
      relative_humidity: airRH,
      soil_temperature: soilT,
      soil_moisture: soilM,
      leaf_wetness_raw: lwd > 0 ? 1 : 0,
      leaf_wetness_hours: lwd,
      battery_voltage: 13.05,
      battery_percent: 94,
      solar_voltage: 17.8,
      wifi_rssi: -62
    });
    seeded.push(record);
  }
  
  telemetryReadings = seeded;
  saveDatabase();
}

/**
 * ==============================================================================
 * PLANT PATHOLOGY DISEASE RISK COMPUTATION ENGINE
 * ==============================================================================
 */
function evaluateLateBlightRisk(airTemp, airRH, lwdHours) {
  // Adapted Wallin Severity Values (SV) & Leaf Wetness Duration
  let sv = 0;
  let riskLevel = 'LOW';
  
  // Temperature favorability: Optimal 12°C to 22°C (especially 15°C - 20°C)
  const isTempOptimal = (airTemp >= 12.0 && airTemp <= 22.0);
  const isTempConducive = (airTemp >= 10.0 && airTemp <= 25.0);

  if (lwdHours >= 15.0 && isTempOptimal) {
    sv = 4;
    riskLevel = 'HIGH';
  } else if ((lwdHours >= 10.0 && isTempOptimal) || (lwdHours >= 12.0 && airRH >= 90.0)) {
    sv = 3;
    riskLevel = 'HIGH';
  } else if ((lwdHours >= 7.0 && isTempOptimal) || (lwdHours >= 8.0 && isTempConducive)) {
    sv = 2;
    riskLevel = 'MODERATE';
  } else if ((lwdHours >= 5.0 && isTempConducive) || (airRH >= 85.0 && lwdHours >= 4.0)) {
    sv = 1;
    riskLevel = 'MODERATE';
  } else {
    sv = 0;
    riskLevel = 'LOW';
  }

  return {
    severity_value: sv,
    risk_level: riskLevel,
    lwd_hours: lwdHours,
    air_temp: airTemp,
    air_rh: airRH
  };
}

function evaluateBacterialWiltRisk(soilTemp, soilMoisture) {
  // Hydrothermal Soil Index R_BW = (0.50 * S_ST) + (0.50 * S_SM)
  // S_ST: Optimal bacterial multiplication at 28°C - 35°C
  let s_st = 0.2;
  if (soilTemp >= 28.0 && soilTemp <= 35.0) {
    s_st = 1.0;
  } else if ((soilTemp >= 25.0 && soilTemp < 28.0) || (soilTemp > 35.0 && soilTemp <= 38.0)) {
    s_st = 0.6;
  } else if (soilTemp >= 20.0 && soilTemp < 25.0) {
    s_st = 0.35;
  } else {
    s_st = 0.15;
  }

  // S_SM: Saturated / waterlogged root-zone at >= 75% VWC
  let s_sm = 0.2;
  if (soilMoisture >= 75.0) {
    s_sm = 1.0;
  } else if (soilMoisture >= 65.0 && soilMoisture < 75.0) {
    s_sm = 0.70;
  } else if (soilMoisture >= 50.0 && soilMoisture < 65.0) {
    s_sm = 0.40;
  } else {
    s_sm = 0.15;
  }

  const score = parseFloat(((0.50 * s_st) + (0.50 * s_sm)).toFixed(2));
  
  let riskLevel = 'LOW';
  if (score >= 0.70) {
    riskLevel = 'HIGH';
  } else if (score >= 0.40) {
    riskLevel = 'MODERATE';
  } else {
    riskLevel = 'LOW';
  }

  return {
    risk_score: score,
    risk_level: riskLevel,
    soil_temp: soilTemp,
    soil_moisture: soilMoisture,
    s_st_factor: s_st,
    s_sm_factor: s_sm
  };
}

function generateAgronomicAdvisory(lbRisk, bwRisk, lwd, soilM) {
  if (lbRisk.risk_level === 'HIGH' || bwRisk.risk_level === 'HIGH') {
    return {
      status_tier: 'danger-theme',
      badge_text: 'CRITICAL ALERT',
      headline: 'Pathogen Outbreak Imminent',
      description: `Adapted Wallin SV reached ${lbRisk.severity_value} with ${lwd}h leaf wetness. Soil hydrothermal risk is at ${bwRisk.risk_score.toFixed(2)}.`,
      advisories: [
        {
          title: "Immediate Canopy Aeration & Pruning",
          desc: "Initiate selective suckering and lower-leaf pruning to promote laminar airflow and accelerate foliar evaporation."
        },
        {
          title: "Suspend Drip & Overhead Irrigation",
          desc: `Soil moisture is at ${soilM}% VWC. Halting irrigation prevents bacterial vascular mobility in the rhizosphere.`
        },
        {
          title: "Preventive Bio-Fungicide Barrier",
          desc: "Apply copper hydroxide or Bacillus subtilis barrier spray within 12 hours before initial hyphal penetration."
        }
      ]
    };
  } else if (lbRisk.risk_level === 'MODERATE' || bwRisk.risk_level === 'MODERATE') {
    return {
      status_tier: 'warning-theme',
      badge_text: 'WARNING ADVISORY',
      headline: 'Developing Microclimate Advisory',
      description: `Foliar leaf wetness accumulating (${lwd}h). Environmental conditions are moderately favorable for zoosporangia germination.`,
      advisories: [
        {
          title: "Inspect Foliar Canopy Density",
          desc: "Check lower plant tier for dew retention; clear inter-row weeds to facilitate natural cross-ventilation."
        },
        {
          title: "Regulate Irrigation Schedules",
          desc: "Switch to early morning drip cycles only to allow bed surface drying before evening dew point."
        },
        {
          title: "Prepare Bio-Control Agents",
          desc: "Stage preventive biological agents in case leaf wetness exceeds the critical threshold."
        }
      ]
    };
  } else {
    return {
      status_tier: 'safe-theme',
      badge_text: 'OPTIMAL CONDITIONS',
      headline: 'Optimal Crop Microclimate',
      description: `Foliar surfaces are dry. Soil moisture (${soilM}%) and root-zone temperatures are well within safe physiological parameters.`,
      advisories: [
        {
          title: "Routine Crop Scouting",
          desc: "Maintain standard weekly visual inspection for insect vectors and physiological vigor."
        },
        {
          title: "Normal Balanced Irrigation",
          desc: "Proceed with standard fertigation program at 50%–60% field capacity."
        },
        {
          title: "No Chemical Action Required",
          desc: "Microclimate remains unfavorable for sporulation and bacterial proliferation."
        }
      ]
    };
  }
}

function processTelemetry(raw) {
  const recordedAt = raw.recorded_at || new Date().toISOString();
  const airT = parseFloat(raw.air_temperature ?? 24.0);
  const airRH = parseFloat(raw.relative_humidity ?? 70.0);
  const soilT = parseFloat(raw.soil_temperature ?? 24.0);
  const soilM = parseFloat(raw.soil_moisture ?? 55.0);
  const lwd = parseFloat(raw.leaf_wetness_hours ?? 0.0);
  
  const lbAnalysis = evaluateLateBlightRisk(airT, airRH, lwd);
  const bwAnalysis = evaluateBacterialWiltRisk(soilT, soilM);
  const advisory = generateAgronomicAdvisory(lbAnalysis, bwAnalysis, lwd, soilM);

  return {
    reading_id: `RDG-${Date.now()}-${Math.floor(Math.random() * 1000)}`,
    node_id: raw.node_id || "SOLANA-NODE-01",
    recorded_at: recordedAt,
    air_temperature: airT,
    relative_humidity: airRH,
    soil_temperature: soilT,
    soil_moisture: soilM,
    leaf_wetness_raw: raw.leaf_wetness_raw ?? (lwd > 0 ? 1 : 0),
    leaf_wetness_hours: lwd,
    battery_voltage: parseFloat(raw.battery_voltage ?? 12.8),
    battery_percent: parseInt(raw.battery_percent ?? 90),
    solar_voltage: parseFloat(raw.solar_voltage ?? 17.5),
    wifi_rssi: parseInt(raw.wifi_rssi ?? -65),
    disease_analysis: {
      late_blight: lbAnalysis,
      bacterial_wilt: bwAnalysis,
      overall_risk: advisory.status_tier === 'danger-theme' ? 'HIGH' : advisory.status_tier === 'warning-theme' ? 'MODERATE' : 'LOW',
      advisory: advisory
    }
  };
}

/**
 * ==============================================================================
 * API ENDPOINTS
 * ==============================================================================
 */

// 1. Ingest Telemetry from ESP32 Edge Node
app.post('/api/telemetry', (req, res) => {
  const payload = req.body;
  
  if (!payload) {
    return res.status(400).json({ error: "Empty telemetry payload." });
  }

  // Handle batch buffer upload from MicroSD card
  if (Array.isArray(payload)) {
    console.log(`[Ingestion] Received batch of ${payload.length} buffered readings from ESP32.`);
    const processed = payload.map(item => processTelemetry(item));
    telemetryReadings.push(...processed);
    processed.forEach(p => persistToTurso(p));
    saveDatabase();
    return res.status(201).json({
      status: "success",
      count: processed.length,
      message: "Batch telemetry synced successfully."
    });
  }

  // Handle single reading
  const record = processTelemetry(payload);
  telemetryReadings.push(record);
  saveDatabase(record);

  console.log(`[Ingestion] Received reading from ${record.node_id} @ ${record.recorded_at} | Air: ${record.air_temperature}°C, ${record.relative_humidity}% | Soil: ${record.soil_moisture}% | LB: ${record.disease_analysis.late_blight.risk_level}`);

  res.status(201).json({
    status: "success",
    reading_id: record.reading_id,
    recorded_at: record.recorded_at,
    disease_analysis: record.disease_analysis
  });
});

// 2. Fetch Latest Telemetry & Disease Analysis (Used by Web App)
app.get('/api/telemetry/latest', (req, res) => {
  if (telemetryReadings.length === 0) {
    seedInitialData();
  }

  const latest = telemetryReadings[telemetryReadings.length - 1];
  res.json({
    status: "success",
    node_id: latest.node_id,
    timestamp: latest.recorded_at,
    telemetry: latest
  });
});

// 3. Fetch Historical Series for Charts
app.get('/api/telemetry/history', (req, res) => {
  const limit = parseInt(req.query.limit) || 48;
  const history = telemetryReadings.slice(-limit);
  
  res.json({
    status: "success",
    count: history.length,
    data: history
  });
});

// 4. Simulator Ingestion (Allows injecting safe, warning, or critical states for testing)
app.post('/api/telemetry/simulate', (req, res) => {
  const scenario = req.body.scenario || 'safe';
  let sample = {};

  if (scenario === 'high' || scenario === 'critical') {
    sample = {
      air_temperature: 21.4,
      relative_humidity: 94.2,
      soil_temperature: 29.8,
      soil_moisture: 78.4,
      leaf_wetness_hours: 11.8,
      battery_voltage: 12.6,
      battery_percent: 82,
      solar_voltage: 14.2
    };
  } else if (scenario === 'moderate' || scenario === 'warning') {
    sample = {
      air_temperature: 19.8,
      relative_humidity: 88.5,
      soil_temperature: 26.5,
      soil_moisture: 64.2,
      leaf_wetness_hours: 7.4,
      battery_voltage: 12.9,
      battery_percent: 88,
      solar_voltage: 16.5
    };
  } else {
    sample = {
      air_temperature: 26.8,
      relative_humidity: 64.0,
      soil_temperature: 23.4,
      soil_moisture: 52.0,
      leaf_wetness_hours: 1.2,
      battery_voltage: 13.2,
      battery_percent: 96,
      solar_voltage: 18.4
    };
  }

  // Merge any custom overrides passed in body
  const merged = { ...sample, ...req.body, recorded_at: new Date().toISOString() };
  const record = processTelemetry(merged);
  telemetryReadings.push(record);
  saveDatabase();

  res.json({
    status: "success",
    scenario_injected: scenario,
    reading: record
  });
});

// 5. System Health & Edge Node Heartbeat Status
app.get('/api/health', (req, res) => {
  const latest = telemetryReadings.length > 0 ? telemetryReadings[telemetryReadings.length - 1] : null;
  const lastSeenMs = latest ? Date.now() - new Date(latest.recorded_at).getTime() : null;
  const isHardwareOnline = lastSeenMs !== null && lastSeenMs < 15 * 60 * 1000; // seen within 15 mins

  res.json({
    status: "online",
    server_time: new Date().toISOString(),
    records_count: telemetryReadings.length,
    hardware_status: {
      node_id: latest ? latest.node_id : "UNKNOWN",
      online: isHardwareOnline,
      last_reading_time: latest ? latest.recorded_at : null,
      seconds_since_last_packet: lastSeenMs ? Math.round(lastSeenMs / 1000) : null
    }
  });
});

// 6. CSV Historical Telemetry Export (for Thesis Defense, SPSS, Excel)
app.get('/api/telemetry/export-csv', (req, res) => {
  if (telemetryReadings.length === 0) {
    seedInitialData();
  }

  const headers = [
    'Timestamp',
    'Node_ID',
    'Air_Temp_C',
    'Air_RH_Pct',
    'Soil_Temp_C',
    'Soil_Moisture_Pct',
    'Leaf_Wetness_Raw',
    'Leaf_Wetness_Hours',
    'Battery_V',
    'Battery_Pct',
    'Solar_V',
    'WiFi_RSSI_dBm',
    'Late_Blight_Risk',
    'Late_Blight_SV',
    'Bacterial_Wilt_Risk',
    'Bacterial_Wilt_Score'
  ];

  const rows = telemetryReadings.map(r => {
    const lb = r.disease_analysis?.late_blight || {};
    const bw = r.disease_analysis?.bacterial_wilt || {};
    return [
      `"${r.recorded_at}"`,
      `"${r.node_id}"`,
      r.air_temperature,
      r.relative_humidity,
      r.soil_temperature,
      r.soil_moisture,
      r.leaf_wetness_raw,
      r.leaf_wetness_hours,
      r.battery_voltage,
      r.battery_percent,
      r.solar_voltage,
      r.wifi_rssi,
      `"${lb.risk_level || 'LOW'}"`,
      lb.severity_value ?? 0,
      `"${bw.risk_level || 'LOW'}"`,
      bw.risk_score ?? 0.0
    ].join(',');
  });

  const csvContent = [headers.join(','), ...rows].join('\r\n');
  res.setHeader('Content-Type', 'text/csv');
  res.setHeader('Content-Disposition', `attachment; filename="SolanaWatch_Telemetry_${Date.now()}.csv"`);
  res.send(csvContent);
});

// Initialize database
loadDatabase();

// Export express app for Vercel Serverless Function deployment
module.exports = app;

// If run directly (local development or standalone node server), start HTTP listener
if (require.main === module || !process.env.VERCEL) {
  app.listen(PORT, '0.0.0.0', () => {
    console.log('================================================================');
    console.log(`🌿 SolanaWatch IoT REST API Server running on port ${PORT}`);
    console.log(`📡 Local API:     http://localhost:${PORT}/api/telemetry`);
    console.log(`💻 Web Dashboard: http://localhost:${PORT}/`);
    console.log('================================================================');
  });
}
