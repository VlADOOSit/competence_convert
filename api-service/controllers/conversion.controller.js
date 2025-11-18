const { getConvertedCompetenciesFromMl } = require("../services/ml.service");
const { extractTextFromHtml } = require("../utils/htmlToText");

class ConversionController {
    async runConversion(req, res) {
        try {
            /*const profileId = Number(req.params.profileId);
            if (!profileId) {
                return res.status(400).json({ message: "Invalid profileId" });
            }

            // Перевіримо, що профіль існує
            const profile = await getJobProfileById(profileId);
            if (!profile) {
                return res
                    .status(404)
                    .json({ message: "Job profile not found" });
            }*/

            if (!req.file) {
                return res.status(400).json({
                    message: "HTML file is required (field name: file)",
                });
            }

            const htmlBuffer = req.file.buffer;
            const htmlContent = htmlBuffer.toString("utf8");

            // 1) Витягуємо чистий текст із HTML
            const plainText = extractTextFromHtml(htmlContent);
            if (!plainText) {
                return res
                    .status(400)
                    .json({ message: "Cannot extract text from HTML" });
            }

            // 2) Викликаємо ML-сервіс для конвертації
            const predictions = await getConvertedCompetenciesFromMl(
                plainText,
                10
            );

            //await updateJobProfileParsedData(profileId, plainText, "converted");

            //await saveConversionResults(profileId, predictions);

            return res.json({
                message: "Conversion completed",
                //profile_id: profileId,
                parsed_text_length: plainText.length,
                results_saved: predictions.length,
                predictions,
            });
        } catch (err) {
            console.error("runConversion error:", err);
            return res
                .status(500)
                .json({ message: "Internal server error", error: err.message });
        }
    }
}

module.exports = new ConversionController();
