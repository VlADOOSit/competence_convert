const mysql = require("mysql2");
const configPath = "./db/config.json";

dotenv.config();

const pool = mysql.createPool({
    host: process.env.DB_HOST || "localhost",
    port: process.env.DB_PORT ? Number(process.env.DB_PORT) : 3306,
    user: process.env.DB_USER || configPath.user,
    password: process.env.DB_PASSWORD || configPath.password,
    database: process.env.DB_NAME || "competence_db",
    waitForConnections: true,
    connectionLimit: 10,
    queueLimit: 0,
});

module.exports = pool.promise();
