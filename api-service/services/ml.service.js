const axios = require("axios");
const axiosRetry = require("axios-retry").default;

const ML_SERVICE_URL = process.env.ML_SERVICE_URL || "http://localhost:8000";

const mlClient = axios.create({
    baseURL: ML_SERVICE_URL,
});

axiosRetry(mlClient, {
    retries: 30,
    retryDelay: (retryCount) => {
        console.log(`ML service is unavailable (connection error). Please wait and try again... (Attempt ${retryCount})`);
        return retryCount * 1000;
    },
    retryCondition: (error) => {
        return axiosRetry.isNetworkOrIdempotentRequestError(error) || error.code === 'ECONNREFUSED';
    }
});

async function getConvertedCompetenciesFromMl(text, topK = 10) {
    try {
        const response = await mlClient.post('/predict', {
            text,
            top_k: topK,
        });

        const data = response.data || {};
        const results = Array.isArray(data.results) ? data.results : [];

        return results;
    } catch (error) {
        console.error("Failed to connect to ML service after all attempts.");
        throw error;
    }
}

module.exports = { getConvertedCompetenciesFromMl };
