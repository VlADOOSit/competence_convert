require("dotenv").config();
const app = require("./app");

const PORT = process.env.PORT || 3001;
const HOST = process.env.HOST || "localhost";

(async () => {
    try {
        app.listen(PORT, "0.0.0.0", () => {
            console.log(`Server start on http://${HOST}:${PORT}`);
        });
    } catch (err) {
        console.error("error:", err);
    }
})();
