const db = require("../db/db");

class JobProfile {
    getJobProfileById(profileId) {
        return db.query(
            `SELECT profile_id, user_id, source, title, parsed_data, parsed_date, status FROM JobProfiles WHERE profile_id = ?`,
            [profileId]
        );
    }

    updateJobProfileParsedData(profileId, parsedData, status = "converted") {
        return db.query(
            `UPDATE JobProfiles SET parsed_data = ?, status = ? WHERE profile_id = ?`,
            [parsedData, status, profileId]
        );
    }
}

module.exports = new JobProfile();
