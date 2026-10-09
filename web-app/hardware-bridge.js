/**
 * ==============================================================================
 * SOLANAWATCH: LIVE HARDWARE & BACKEND BRIDGE
 * ==============================================================================
 * Connects the SolanaWatch Web & Mobile Interfaces to:
 *   1. SolanaWatch Node.js REST API Backend (http://localhost:5000)
 *   2. Directly to ESP32 Edge Node IP (http://192.168.x.x)
 * 
 * Provides automated polling, real-time telemetry extraction, disease risk
 * synchronization, connection diagnostics, and interactive hardware modal.
 * ==============================================================================
 */

(function (window) {
  'use strict';

  // Default Backend URL
  // If served via any HTTP/HTTPS host (e.g. Vercel or local server), use window.location.origin;
  // otherwise fallback to stored URL or default http://localhost:5000
  const defaultUrl = window.location.protocol.startsWith('http')
    ? window.location.origin
    : 'https://solanawatch-roan.vercel.app';

  const HardwareBridge = {
    apiUrl: localStorage.getItem('solanawatch_api_url') || defaultUrl,
    pollIntervalMs: parseInt(localStorage.getItem('solanawatch_poll_interval')) || 3000,
    isLive: false,
    isConnected: false,
    timer: null,
    lastReading: null,
    lastLatencyMs: null,
    lastPacketTime: null,
    nodeId: 'SOLANA-NODE-01',
    listeners: {
      telemetry: [],
      status: []
    },

    init: function () {
      console.log(`[HardwareBridge] Initialized with API target: ${this.apiUrl}`);
      this.attachModalStyles();
      this.createHardwareModal();

      // Check URL params for auto-connect
      const params = new URLSearchParams(window.location.search);
      if (params.get('api')) {
        this.apiUrl = params.get('api');
        localStorage.setItem('solanawatch_api_url', this.apiUrl);
      }

      // Check initial connection
      this.testConnection().then(online => {
        if (online) {
          console.log('[HardwareBridge] Backend detected. Activating Live Hardware mode.');
          this.startLiveMode();
        } else {
          console.log('[HardwareBridge] Backend offline. Ready in Demo Mode (toggle Live anytime).');
        }
      });
    },

    onTelemetry: function (fn) {
      this.listeners.telemetry.push(fn);
    },

    onStatusChange: function (fn) {
      this.listeners.status.push(fn);
    },

    notifyStatus: function (status, details) {
      this.listeners.status.forEach(fn => fn(status, details));
      this.updateBadges(status);
      this.updateModalStatus(status, details);
    },

    startLiveMode: function () {
      this.isLive = true;
      if (this.timer) clearInterval(this.timer);
      this.fetchLatest();
      this.timer = setInterval(() => this.fetchLatest(), this.pollIntervalMs);
      this.notifyStatus('connecting', { message: 'Connecting to hardware...' });
    },

    stopLiveMode: function () {
      this.isLive = false;
      this.isConnected = false;
      if (this.timer) {
        clearInterval(this.timer);
        this.timer = null;
      }
      this.notifyStatus('standby', { message: 'Demo / Standby Mode' });
    },

    toggleLive: function () {
      if (this.isLive) {
        this.stopLiveMode();
        return false;
      } else {
        this.startLiveMode();
        return true;
      }
    },

    testConnection: async function () {
      const start = performance.now();
      try {
        const controller = new AbortController();
        const timeout = setTimeout(() => controller.abort(), 2500);
        
        // Try health endpoint first
        const resp = await fetch(`${this.apiUrl}/api/health`, { signal: controller.signal });
        clearTimeout(timeout);
        
        if (resp.ok) {
          const data = await resp.json();
          this.lastLatencyMs = Math.round(performance.now() - start);
          this.isConnected = true;
          return true;
        }
      } catch (e) {
        // Fallback: try /api/telemetry directly (e.g. when connecting directly to ESP32 local server)
        try {
          const controller2 = new AbortController();
          const timeout2 = setTimeout(() => controller2.abort(), 2000);
          const resp2 = await fetch(`${this.apiUrl}/api/telemetry`, { signal: controller2.signal });
          clearTimeout(timeout2);
          if (resp2.ok) {
            this.lastLatencyMs = Math.round(performance.now() - start);
            this.isConnected = true;
            return true;
          }
        } catch (e2) {}
      }

      this.isConnected = false;
      this.lastLatencyMs = null;
      return false;
    },

    fetchLatest: async function () {
      const start = performance.now();
      try {
        const controller = new AbortController();
        const timeout = setTimeout(() => controller.abort(), 3000);

        // Fetch from backend endpoint
        let endpoint = `${this.apiUrl}/api/telemetry/latest`;
        let resp = await fetch(endpoint, { signal: controller.signal });
        clearTimeout(timeout);

        if (!resp.ok && resp.status === 404) {
          // Direct ESP32 endpoint fallback
          resp = await fetch(`${this.apiUrl}/api/telemetry`);
        }

        if (resp.ok) {
          const json = await resp.json();
          this.lastLatencyMs = Math.round(performance.now() - start);
          this.isConnected = true;
          this.lastPacketTime = new Date();

          const record = json.telemetry || json;
          this.lastReading = record;
          this.nodeId = record.node_id || this.nodeId;

          // Dispatch to UI listeners
          this.listeners.telemetry.forEach(fn => fn(record));
          this.notifyStatus('connected', {
            nodeId: this.nodeId,
            latencyMs: this.lastLatencyMs,
            timestamp: this.lastPacketTime
          });
          return record;
        } else {
          throw new Error(`Server returned HTTP ${resp.status}`);
        }
      } catch (err) {
        this.isConnected = false;
        this.notifyStatus('error', {
          error: err.message,
          message: 'Hardware backend unreachable'
        });
        return null;
      }
    },

    simulateScenario: async function (scenarioName) {
      try {
        const resp = await fetch(`${this.apiUrl}/api/telemetry/simulate`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ scenario: scenarioName })
        });
        if (resp.ok) {
          this.fetchLatest();
          return true;
        }
      } catch (e) {
        console.warn('[HardwareBridge] Backend simulate failed, applying local fallback.');
      }
      return false;
    },

    fetchForecast: async function (lat, lon) {
      try {
        const url = `${this.apiUrl}/api/forecast?lat=${lat || '16.4550'}&lon=${lon || '120.5985'}`;
        const resp = await fetch(url);
        if (resp.ok) {
          return await resp.json();
        }
      } catch (e) {
        console.warn('[HardwareBridge] Forecast fetch failed:', e.message);
      }
      return null;
    },

    sendTestAlert: async function (msg) {
      try {
        const resp = await fetch(`${this.apiUrl}/api/alerts/test`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message: msg })
        });
        return await resp.json();
      } catch (e) {
        return { status: "error", message: e.message };
      }
    },

    getAlertStatus: async function () {
      try {
        const resp = await fetch(`${this.apiUrl}/api/alerts/status`);
        return await resp.json();
      } catch (e) {
        return null;
      }
    },

    saveSettings: function (newUrl, newInterval) {
      if (newUrl) {
        this.apiUrl = newUrl.trim().replace(/\/$/, '');
        localStorage.setItem('solanawatch_api_url', this.apiUrl);
      }
      if (newInterval) {
        this.pollIntervalMs = parseInt(newInterval);
        localStorage.setItem('solanawatch_poll_interval', this.pollIntervalMs);
      }
      this.testConnection().then(() => {
        if (this.isLive) {
          this.startLiveMode();
        }
      });
    },

    updateBadges: function (status) {
      // Update Toolbar buttons / indicators
      const liveBtn = document.getElementById('liveHwBtn');
      const liveDot = document.getElementById('liveDot');
      const liveText = document.getElementById('liveBtnText');
      const hwBadge = document.getElementById('hwToolbarBadge');

      if (status === 'connected') {
        if (liveBtn) {
          liveBtn.classList.add('active');
          liveBtn.style.borderColor = 'rgba(52, 199, 89, 0.8)';
        }
        if (liveDot) {
          liveDot.style.background = '#34c759';
          liveDot.style.boxShadow = '0 0 10px #34c759';
        }
        if (liveText) liveText.innerText = 'Live Hardware';
        if (hwBadge) {
          hwBadge.innerText = `${this.lastLatencyMs || 25}ms`;
          hwBadge.style.color = '#34c759';
        }
      } else if (status === 'connecting') {
        if (liveBtn) liveBtn.classList.add('active');
        if (liveDot) {
          liveDot.style.background = '#ff9500';
          liveDot.style.boxShadow = '0 0 8px #ff9500';
        }
        if (liveText) liveText.innerText = 'Connecting...';
        if (hwBadge) {
          hwBadge.innerText = 'Connecting';
          hwBadge.style.color = '#ff9500';
        }
      } else if (status === 'error') {
        if (liveDot) {
          liveDot.style.background = '#ff3b30';
          liveDot.style.boxShadow = '0 0 8px #ff3b30';
        }
        if (liveText) liveText.innerText = 'Offline (Click Setup)';
        if (hwBadge) {
          hwBadge.innerText = 'Offline';
          hwBadge.style.color = '#ff3b30';
        }
      } else {
        if (liveBtn) liveBtn.classList.remove('active');
        if (liveDot) {
          liveDot.style.background = '#8e8e93';
          liveDot.style.boxShadow = 'none';
        }
        if (liveText) liveText.innerText = 'Demo Mode';
        if (hwBadge) {
          hwBadge.innerText = 'HW Link';
          hwBadge.style.color = 'inherit';
        }
      }
    },

    updateModalStatus: function (status, details) {
      const statusPill = document.getElementById('hwModalStatusPill');
      const latencyVal = document.getElementById('hwModalLatency');
      const lastSeenVal = document.getElementById('hwModalLastSeen');
      const nodeVal = document.getElementById('hwModalNode');

      if (!statusPill) return;

      if (status === 'connected') {
        statusPill.innerHTML = '<span style="color:#34c759;">●</span> CONNECTED (ONLINE)';
        statusPill.className = 'hw-status-pill online';
        if (latencyVal) latencyVal.innerText = `${details.latencyMs || 20} ms`;
        if (lastSeenVal) lastSeenVal.innerText = new Date().toLocaleTimeString();
        if (nodeVal) nodeVal.innerText = details.nodeId || this.nodeId;
      } else if (status === 'connecting') {
        statusPill.innerHTML = '<span style="color:#ff9500;">●</span> CONNECTING...';
        statusPill.className = 'hw-status-pill connecting';
      } else if (status === 'error') {
        statusPill.innerHTML = '<span style="color:#ff3b30;">●</span> DISCONNECTED / OFFLINE';
        statusPill.className = 'hw-status-pill offline';
        if (latencyVal) latencyVal.innerText = 'Timeout';
      } else {
        statusPill.innerHTML = '<span style="color:#8e8e93;">●</span> STANDBY / DEMO';
        statusPill.className = 'hw-status-pill standby';
      }
    },

    openModal: function () {
      const modal = document.getElementById('solanaHardwareModal');
      const urlInput = document.getElementById('hwApiUrlInput');
      const intervalInput = document.getElementById('hwPollIntervalInput');

      if (urlInput) urlInput.value = this.apiUrl;
      if (intervalInput) intervalInput.value = this.pollIntervalMs;

      this.testConnection().then(() => {
        this.updateModalStatus(this.isConnected ? 'connected' : 'error', {
          latencyMs: this.lastLatencyMs,
          nodeId: this.nodeId
        });
      });

      if (modal) modal.style.display = 'flex';
    },

    closeModal: function () {
      const modal = document.getElementById('solanaHardwareModal');
      if (modal) modal.style.display = 'none';
    },

    createHardwareModal: function () {
      if (document.getElementById('solanaHardwareModal')) return;

      const modalHtml = `
        <div id="solanaHardwareModal" class="hw-modal-backdrop" onclick="if(event.target===this) window.SolanaHardware.closeModal()">
          <div class="hw-modal-dialog">
            <div class="hw-modal-header">
              <div style="display:flex; align-items:center; gap:8px;">
                <span style="font-size:20px;">📡</span>
                <h3 style="margin:0; font-size:17px; font-weight:700;">Hardware & Backend Link</h3>
              </div>
              <button class="hw-modal-close" onclick="window.SolanaHardware.closeModal()">✕</button>
            </div>

            <div class="hw-modal-body">
              <div class="hw-status-banner">
                <div>
                  <div style="font-size:11px; text-transform:uppercase; letter-spacing:0.5px; opacity:0.7;">Network Status</div>
                  <div id="hwModalStatusPill" class="hw-status-pill standby">● STANDBY</div>
                </div>
                <div style="text-align:right;">
                  <div style="font-size:11px; text-transform:uppercase; letter-spacing:0.5px; opacity:0.7;">Node ID</div>
                  <div id="hwModalNode" style="font-size:14px; font-weight:700;">SOLANA-NODE-01</div>
                </div>
              </div>

              <div class="hw-metrics-mini-grid">
                <div class="hw-metric-mini">
                  <span class="label">Ping Latency</span>
                  <strong id="hwModalLatency">--</strong>
                </div>
                <div class="hw-metric-mini">
                  <span class="label">Last Packet</span>
                  <strong id="hwModalLastSeen">--</strong>
                </div>
                <div class="hw-metric-mini">
                  <span class="label">Wi-Fi RSSI</span>
                  <strong id="hwModalRssi">-60 dBm</strong>
                </div>
              </div>

              <div class="hw-form-group">
                <label for="hwApiUrlInput">Backend API / ESP32 IP Address:</label>
                <div style="display:flex; gap:8px;">
                  <input type="text" id="hwApiUrlInput" placeholder="http://localhost:5000" style="flex:1;">
                  <button class="hw-btn-test" onclick="window.SolanaHardware.handleTestBtn()">Test Ping</button>
                </div>
                <small style="opacity:0.6; display:block; margin-top:4px;">
                  Use <code>http://localhost:5000</code> when running Node.js server, or <code>http://192.168.x.x</code> for direct ESP32 Wi-Fi.
                </small>
              </div>

              <div class="hw-form-group">
                <label for="hwPollIntervalInput">Live Polling Rate (ms):</label>
                <select id="hwPollIntervalInput">
                  <option value="1500">1.5 seconds (Ultra Fast / Benchtop)</option>
                  <option value="3000" selected>3.0 seconds (Recommended Live)</option>
                  <option value="5000">5.0 seconds (Standard)</option>
                  <option value="10000">10.0 seconds (Power Saver)</option>
                </select>
              </div>

              <div class="hw-simulator-section">
                <div style="font-size:12px; font-weight:700; margin-bottom:6px; opacity:0.8;">Inject Test Telemetry Packet:</div>
                <div style="display:flex; gap:6px;">
                  <button class="hw-sim-btn danger" onclick="window.SolanaHardware.simulateScenario('high')">🚨 Send High Risk</button>
                  <button class="hw-sim-btn warning" onclick="window.SolanaHardware.simulateScenario('moderate')">⚠️ Send Moderate</button>
                  <button class="hw-sim-btn safe" onclick="window.SolanaHardware.simulateScenario('safe')">🟢 Send Safe</button>
                </div>
              </div>

              <div class="hw-quick-guide">
                <strong>⚡ Quick Start Steps:</strong>
                <ol style="margin:4px 0 0 16px; padding:0; font-size:11.5px; line-height:1.5;">
                  <li>Start Backend: Run <code>npm start</code> in the <code>backend/</code> folder.</li>
                  <li>Flash ESP32: Open <code>firmware/SolanaWatch_ESP32_Firmware.ino</code> in Arduino IDE and upload.</li>
                  <li>Both ESP32 and this laptop should be on the same 2.4 GHz Wi-Fi network.</li>
                </ol>
              </div>
            </div>

            <div class="hw-modal-footer">
              <button class="hw-btn-secondary" onclick="window.SolanaHardware.closeModal()">Close</button>
              <button class="hw-btn-primary" onclick="window.SolanaHardware.handleSaveBtn()">Save & Connect</button>
            </div>
          </div>
        </div>
      `;

      const wrapper = document.createElement('div');
      wrapper.innerHTML = modalHtml;
      document.body.appendChild(wrapper.firstElementChild);
    },

    handleSaveBtn: function () {
      const url = document.getElementById('hwApiUrlInput').value;
      const interval = document.getElementById('hwPollIntervalInput').value;
      this.saveSettings(url, interval);
      this.startLiveMode();
      this.closeModal();
    },

    handleTestBtn: async function () {
      const url = document.getElementById('hwApiUrlInput').value;
      this.apiUrl = url.trim().replace(/\/$/, '');
      const btn = event.target;
      btn.innerText = 'Pinging...';
      const ok = await this.testConnection();
      btn.innerText = ok ? '✓ Online' : '✕ Offline';
      setTimeout(() => { btn.innerText = 'Test Ping'; }, 2000);
      this.updateModalStatus(ok ? 'connected' : 'error', {
        latencyMs: this.lastLatencyMs,
        nodeId: this.nodeId
      });
    },

    attachModalStyles: function () {
      if (document.getElementById('solanaHwStyles')) return;
      const style = document.createElement('style');
      style.id = 'solanaHwStyles';
      style.innerHTML = `
        .hw-modal-backdrop {
          position: fixed;
          inset: 0;
          background: rgba(0, 0, 0, 0.65);
          backdrop-filter: blur(10px);
          -webkit-backdrop-filter: blur(10px);
          display: none;
          align-items: center;
          justify-content: center;
          z-index: 99999;
          padding: 16px;
        }
        .hw-modal-dialog {
          background: #1c1c1e;
          color: #f2f2f7;
          border-radius: 20px;
          border: 1px solid rgba(255, 255, 255, 0.12);
          width: 100%;
          max-width: 480px;
          box-shadow: 0 25px 60px rgba(0, 0, 0, 0.6);
          overflow: hidden;
          font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Plus Jakarta Sans", sans-serif;
          animation: hwModalFadeIn 0.25s cubic-bezier(0.25, 1, 0.5, 1);
        }
        @keyframes hwModalFadeIn {
          from { opacity: 0; transform: scale(0.95); }
          to { opacity: 1; transform: scale(1); }
        }
        .hw-modal-header {
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding: 16px 20px;
          border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        }
        .hw-modal-close {
          background: rgba(255, 255, 255, 0.1);
          border: none;
          color: #fff;
          width: 28px;
          height: 28px;
          border-radius: 50%;
          cursor: pointer;
          font-size: 13px;
        }
        .hw-modal-body {
          padding: 20px;
          display: flex;
          flex-direction: column;
          gap: 16px;
          max-height: 75vh;
          overflow-y: auto;
        }
        .hw-status-banner {
          display: flex;
          justify-content: space-between;
          align-items: center;
          background: rgba(255, 255, 255, 0.04);
          padding: 12px 16px;
          border-radius: 12px;
          border: 1px solid rgba(255, 255, 255, 0.08);
        }
        .hw-status-pill {
          font-size: 12px;
          font-weight: 700;
          margin-top: 3px;
        }
        .hw-status-pill.online { color: #34c759; }
        .hw-status-pill.connecting { color: #ff9500; }
        .hw-status-pill.offline { color: #ff3b30; }
        .hw-status-pill.standby { color: #8e8e93; }
        .hw-metrics-mini-grid {
          display: grid;
          grid-template-columns: repeat(3, 1fr);
          gap: 8px;
        }
        .hw-metric-mini {
          background: rgba(255, 255, 255, 0.03);
          border: 1px solid rgba(255, 255, 255, 0.06);
          border-radius: 10px;
          padding: 8px;
          text-align: center;
        }
        .hw-metric-mini .label {
          display: block;
          font-size: 10px;
          opacity: 0.6;
          text-transform: uppercase;
        }
        .hw-metric-mini strong {
          display: block;
          font-size: 13px;
          margin-top: 2px;
        }
        .hw-form-group {
          display: flex;
          flex-direction: column;
          gap: 6px;
        }
        .hw-form-group label {
          font-size: 12px;
          font-weight: 600;
          opacity: 0.8;
        }
        .hw-form-group input, .hw-form-group select {
          background: rgba(255, 255, 255, 0.07);
          border: 1px solid rgba(255, 255, 255, 0.15);
          color: #fff;
          border-radius: 10px;
          padding: 9px 12px;
          font-size: 13px;
          font-family: monospace;
          outline: none;
        }
        .hw-form-group input:focus, .hw-form-group select:focus {
          border-color: #34c759;
          box-shadow: 0 0 0 3px rgba(52, 199, 89, 0.25);
        }
        .hw-btn-test {
          background: rgba(255, 255, 255, 0.12);
          border: none;
          color: #fff;
          font-size: 12px;
          font-weight: 600;
          border-radius: 10px;
          padding: 0 14px;
          cursor: pointer;
        }
        .hw-simulator-section {
          background: rgba(255, 255, 255, 0.03);
          border: 1px dashed rgba(255, 255, 255, 0.12);
          border-radius: 12px;
          padding: 10px 12px;
        }
        .hw-sim-btn {
          flex: 1;
          border: none;
          padding: 6px 8px;
          border-radius: 8px;
          font-size: 11px;
          font-weight: 600;
          cursor: pointer;
        }
        .hw-sim-btn.danger { background: rgba(255, 59, 48, 0.15); color: #ff3b30; }
        .hw-sim-btn.warning { background: rgba(255, 149, 0, 0.15); color: #ff9500; }
        .hw-sim-btn.safe { background: rgba(52, 199, 89, 0.15); color: #34c759; }
        .hw-quick-guide {
          background: rgba(10, 132, 255, 0.08);
          border: 1px solid rgba(10, 132, 255, 0.2);
          border-radius: 12px;
          padding: 10px 14px;
          color: #82b9ff;
        }
        .hw-quick-guide code {
          background: rgba(0, 0, 0, 0.3);
          padding: 1px 4px;
          border-radius: 4px;
          font-size: 11px;
          color: #fff;
        }
        .hw-modal-footer {
          display: flex;
          justify-content: flex-end;
          gap: 10px;
          padding: 14px 20px;
          border-top: 1px solid rgba(255, 255, 255, 0.08);
        }
        .hw-btn-primary {
          background: #34c759;
          color: #000;
          font-weight: 700;
          font-size: 13px;
          padding: 9px 18px;
          border-radius: 10px;
          border: none;
          cursor: pointer;
        }
        .hw-btn-secondary {
          background: rgba(255, 255, 255, 0.08);
          color: #fff;
          font-weight: 600;
          font-size: 13px;
          padding: 9px 16px;
          border-radius: 10px;
          border: none;
          cursor: pointer;
        }
      `;
      document.head.appendChild(style);
    }
  };

  window.SolanaHardware = HardwareBridge;

  // Initialize once DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => HardwareBridge.init());
  } else {
    HardwareBridge.init();
  }

})(window);
