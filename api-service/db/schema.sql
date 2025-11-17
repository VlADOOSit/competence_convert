-- Створення бази даних (якщо ще немає)
CREATE DATABASE IF NOT EXISTS competence_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE competence_db;
-- Таблиця Users
CREATE TABLE IF NOT EXISTS Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('user', 'admin') DEFAULT 'user',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE = InnoDB;
-- Таблиця JobProfiles
CREATE TABLE IF NOT EXISTS JobProfiles (
    profile_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    source ENUM('manual', 'work_ua', 'djinni', 'dou', 'other') NOT NULL,
    title VARCHAR(200) NOT NULL,
    parsed_data TEXT,
    parsed_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    status ENUM('pending', 'converted', 'error') DEFAULT 'pending',
    CONSTRAINT fk_jobprofiles_user FOREIGN KEY (user_id) REFERENCES Users(user_id) ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE = InnoDB;
-- Таблиця Competencies
CREATE TABLE IF NOT EXISTS Competencies (
    competency_id INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(10) NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT
) ENGINE = InnoDB;
-- Таблиця CompetencyLevels
CREATE TABLE IF NOT EXISTS CompetencyLevels (
    level_id INT AUTO_INCREMENT PRIMARY KEY,
    level_code VARCHAR(10) NOT NULL,
    level_name VARCHAR(100) NOT NULL,
    level_description TEXT
) ENGINE = InnoDB;
-- Таблиця CompetencyLevelMapping
CREATE TABLE IF NOT EXISTS CompetencyLevelMapping (
    competency_id INT NOT NULL,
    level_id INT NOT NULL,
    is_applicable BOOLEAN DEFAULT TRUE,
    PRIMARY KEY (competency_id, level_id),
    CONSTRAINT fk_clm_competency FOREIGN KEY (competency_id) REFERENCES Competencies(competency_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_clm_level FOREIGN KEY (level_id) REFERENCES CompetencyLevels(level_id) ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE = InnoDB;
-- Таблиця ConversionResults
CREATE TABLE IF NOT EXISTS ConversionResults (
    profile_id INT NOT NULL,
    competency_id INT NOT NULL,
    level_id INT NOT NULL,
    probability FLOAT,
    converted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    expert_rating FLOAT,
    PRIMARY KEY (profile_id, competency_id, level_id),
    CONSTRAINT fk_cr_profile FOREIGN KEY (profile_id) REFERENCES JobProfiles(profile_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_cr_competency FOREIGN KEY (competency_id) REFERENCES Competencies(competency_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_cr_level FOREIGN KEY (level_id) REFERENCES CompetencyLevels(level_id) ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE = InnoDB;
-- Таблиця FineTuningLogs
CREATE TABLE IF NOT EXISTS FineTuningLogs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    dataset_name VARCHAR(150) NOT NULL,
    accuracy FLOAT,
    f1_score FLOAT,
    loss FLOAT,
    date DATETIME DEFAULT CURRENT_TIMESTAMP,
    initiated_by INT,
    CONSTRAINT fk_ftl_user FOREIGN KEY (initiated_by) REFERENCES Users(user_id) ON UPDATE CASCADE ON DELETE
    SET NULL
) ENGINE = InnoDB;