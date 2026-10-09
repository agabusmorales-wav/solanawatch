/**
 * ==============================================================================
 * VERCEL SERVERLESS FUNCTION ENTRY POINT
 * ==============================================================================
 * Forwards incoming Vercel HTTP requests to the SolanaWatch Express REST API.
 * Handles both /api/telemetry, /api/telemetry/latest, /api/health, etc.
 * ==============================================================================
 */

const app = require('../backend/server.js');

module.exports = app;
