require("dotenv").config();
const express = require("express");
const cors = require("cors");

//const ErrorHandler = require("./middlewares/errorHandler");

//const ProfileRouter = require("./routes/profile.router");
//const SearchRouter = require("./routes/search.router");

const app = express();

app.use(cors());
app.use(express.json());

//app.use("/api/profiles", ProfileRouter);
//app.use("/api/search", SearchRouter);

//app.use(ErrorHandler);

module.exports = app;