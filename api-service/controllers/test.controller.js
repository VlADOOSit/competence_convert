const ApiError = require("../utils/ApiError");

class TestController {
    test(req, res, next) {
        try {
            const result = "test successful";
            return res.status(200).json(result);
        } catch (error) {
            next(error);
        }
    }
}

module.exports = new TestController();