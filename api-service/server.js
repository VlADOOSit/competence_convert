require("dotenv").config();
const app = require("./app");

const PORT = process.env.PORT || 3001;
const HOST = process.env.HOST || "localhost";

(async () => {
    try {
        app.listen(PORT, HOST, () => {
            console.log(`Server start on https://${HOST}:${PORT}`);
        });
    } catch (err) {
        console.error("error:", err);
    }
})();
