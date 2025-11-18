const axios = require("axios");

const ML_SERVICE_URL = process.env.ML_SERVICE_URL || "http://localhost:8000";

async function getConvertedCompetenciesFromMl(text, topK = 10) {
    const response = await axios.post(`${ML_SERVICE_URL}/predict`, {
        text,
        top_k: topK,
    });

    const data = response.data || {};
    const results = Array.isArray(data.results) ? data.results : [];

    return results;
}

module.exports = { getConvertedCompetenciesFromMl };
