// backend/server.js
const express = require("express");
const cors = require("cors");
const app = express();

// CORS configuration - ADD THIS CODE
app.use(cors({
  origin: ['https://frontenduidashboard.netlify.app', 'http://localhost:3000'],
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  credentials: true
}));

// Rest of your server code continues here...

// Test route
app.get("/api/test", (req, res) => {
  res.json({ message: "Connected to backend!" });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));

app.use(require("./routes/test"));



