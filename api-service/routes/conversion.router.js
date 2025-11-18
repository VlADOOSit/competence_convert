// src/routes/conversion.js
const Router = require("express").Router;
const multer = require("multer");
const ConversionController = require("../controllers/conversion.controller.js");

const router = Router();
const upload = multer({ storage: multer.memoryStorage() });

// POST /api/conversion/:profileId/run
// form-data: file = HTML вакансії
router.post("/run", upload.single("file"), ConversionController.runConversion);

module.exports = router;
