require("dotenv").config();
const express = require("express");
const cors = require("cors");

const ErrorHandler = require("./middlewares/errorHandler");

const TestRouter = require("./routes/test.router");


const app = express();

app.use(cors());
app.use(express.json());

app.use("/api/test", TestRouter);


app.use(ErrorHandler);

module.exports = app;