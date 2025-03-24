-- Create Database
CREATE DATABASE IF NOT EXISTS medical_diagnosis_dba;
USE medical_diagnosis_dba;

-- Table Users: Lưu thông tin User
CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  first_name VARCHAR(255),
  last_name VARCHAR(255),
  email VARCHAR(255) NOT NULL UNIQUE,
  password_hash TEXT NOT NULL,
  role ENUM('doctor', 'patient', 'admin'),
  profile_picture TEXT,
  bio TEXT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table Statuses: Lưu các trạng thái của Medical Examination
CREATE TABLE IF NOT EXISTS statuses (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table Hospitals: Lưu thông tin các Bệnh Viện
CREATE TABLE IF NOT EXISTS hospitals (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL UNIQUE,
  description TEXT,
  address TEXT,
  phone VARCHAR(20),
  email VARCHAR(255),
  website VARCHAR(255),
  established DATE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table Medical Examination Form
CREATE TABLE IF NOT EXISTS medical_examination_forms (
  id INT AUTO_INCREMENT PRIMARY KEY,
  doctor_id INT,
  patient_id INT,
  hospital_id INT,
  status_id INT,

  -- Patient Information
  age INT,
  gender BOOLEAN,
  ethnicity TINYINT,
  education_level TINYINT,

  -- Lifestyle Factors
  bmi FLOAT,
  smoking BOOLEAN,
  alcohol_consumption FLOAT,
  physical_activity FLOAT,
  diet_quality FLOAT,
  sleep_quality FLOAT,

  -- Medical History
  family_history_parkinsons BOOLEAN,
  traumatic_brain_injury BOOLEAN,
  hypertension BOOLEAN,
  diabetes BOOLEAN,
  depression BOOLEAN,
  stroke BOOLEAN,

  -- Clinical Measurements
  systolic_bp INT,
  diastolic_bp INT,
  cholesterol_total FLOAT,
  cholesterol_ldl FLOAT,
  cholesterol_hdl FLOAT,
  cholesterol_triglycerides FLOAT,

  -- Cognitive and Functional Assessments
  updrs_score FLOAT,
  moca_score FLOAT,
  functional_assessment FLOAT,

  -- Symptoms
  tremor BOOLEAN,
  rigidity BOOLEAN,
  bradykinesia BOOLEAN,
  postural_instability BOOLEAN,
  speech_problems BOOLEAN,
  sleep_disorders BOOLEAN,
  constipation BOOLEAN,
  
  diagnosis BOOLEAN,

  FOREIGN KEY (doctor_id) REFERENCES users(id) ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (patient_id) REFERENCES users(id) ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (hospital_id) REFERENCES hospitals(id) ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (status_id) REFERENCES statuses(id) ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table Results (Diagnosis, SHAP, LIME, doctor_decision)
CREATE TABLE IF NOT EXISTS results (
  id INT AUTO_INCREMENT PRIMARY KEY,
  medical_examination_form_id INT NOT NULL,
  lime_result_json TEXT,

  FOREIGN KEY (medical_examination_form_id)
    REFERENCES medical_examination_forms(id)
    ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS doctor_decisions (
  id INT AUTO_INCREMENT PRIMARY KEY,
  result_id INT NOT NULL,
  doctor_decision BOOLEAN,

  FOREIGN KEY (result_id)
    REFERENCES results(id)
    ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;