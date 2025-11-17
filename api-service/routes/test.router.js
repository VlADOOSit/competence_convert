const Router = require("express").Router;
const TestController = require("../controllers/test.controller");

const router = Router();

router.get("/", TestController.test);

module.exports = router;