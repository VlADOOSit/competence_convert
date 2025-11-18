const { htmlToText } = require("html-to-text");

function extractTextFromHtml(html) {
    if (!html) return "";
    return htmlToText(html, {
        wordwrap: false,
    }).trim();
}

module.exports = { extractTextFromHtml };
