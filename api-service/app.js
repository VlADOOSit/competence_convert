require("dotenv").config();
const express = require("express");
const cors = require("cors");

const ErrorHandler = require("./middlewares/errorHandler");

const ConversionRouter = require("./routes/conversion.router");

const app = express();

app.use(cors());
app.use(express.json());

app.get("/health", (req, res) => {
    res.json({ status: "ok" });
});

app.use("/api/conversion", ConversionRouter);

app.use(ErrorHandler);

module.exports = app;
