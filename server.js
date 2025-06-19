// backend/server.js
const express = require("express");
const cors = require("cors");
const app = express();

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// CORS configuration
app.use(cors({
  origin: ['https://frontenduidashboard.netlify.app', 'http://localhost:3000', 'http://localhost:5173'],
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  credentials: true,
  allowedHeaders: ['Content-Type', 'Authorization']
}));

// Health check endpoint
app.get("/health", (req, res) => {
  res.json({ 
    status: "healthy", 
    timestamp: new Date().toISOString(),
    service: "Node.js Backend"
  });
});

// Root endpoint
app.get("/", (req, res) => {
  res.json({ 
    message: "GRC Compliance Monitoring API is running",
    version: "1.0.0",
    service: "Node.js Backend",
    endpoints: {
      health: "/health",
      test: "/api/test"
    }
  });
});

// Mount routes
app.use(require("./routes/test"));

// Test route (also available at /api/test via routes)
app.get("/api/test", (req, res) => {
  res.json({ 
    message: "Connected to Node.js backend!", 
    timestamp: new Date().toISOString() 
  });
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ error: "Something went wrong!" });
});

// 404 handler
app.use((req, res) => {
  res.status(404).json({ error: "Endpoint not found" });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`🚀 Node.js Server running on port ${PORT}`);
  console.log(`📚 Health Check: http://localhost:${PORT}/health`);
  console.log(`🔗 Test Endpoint: http://localhost:${PORT}/api/test`);
});



