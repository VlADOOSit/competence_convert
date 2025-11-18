const Router = require("express").Router;
const multer = require("multer");
const ConversionController = require("../controllers/conversion.controller.js");

const router = Router();
const upload = multer({ storage: multer.memoryStorage() });

router.post("/run", upload.single("file"), ConversionController.runConversion);

module.exports = router;
