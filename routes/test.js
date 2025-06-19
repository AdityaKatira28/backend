// backend/routes/test.js
const express = require("express");
const router = express.Router();

router.get("/api/test", (req, res) => {
  res.json({ message: "Connected!" });
});

module.exports = router;