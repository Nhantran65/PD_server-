from sqlalchemy import Column, Integer, String, Text, ForeignKey, Enum,  Float, Boolean, JSON
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    role = Column(Enum("doctor", "patient", "admin"), nullable=False)
    profile_picture = Column(Text)
    bio = Column(Text)

class Hospital(Base):
    __tablename__ = "hospitals"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    description = Column(Text)
    address = Column(Text)
    phone = Column(String(20))
    email = Column(String(255))
    website = Column(String(255))
    established = Column(String(255))

class Status(Base):
    __tablename__ = "statuses"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)

class MedicalExaminationForm(Base):
    __tablename__ = "medical_examination_forms"

    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    patient_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    hospital_id = Column(Integer, ForeignKey("hospitals.id", ondelete="CASCADE"), nullable=False)
    status_id = Column(Integer, ForeignKey("statuses.id", ondelete="CASCADE"), nullable=False)

    # 🔽 Patient Information
    age = Column(Integer, nullable=False)
    gender = Column(Boolean, nullable=False)
    ethnicity = Column(Integer, nullable=False)
    education_level = Column(Integer, nullable=False)

    # 🔽 Lifestyle Factors
    bmi = Column(Float, nullable=False)
    smoking = Column(Boolean, nullable=False)
    alcohol_consumption = Column(Float, nullable=False)
    physical_activity = Column(Float, nullable=False)
    diet_quality = Column(Float, nullable=False)
    sleep_quality = Column(Float, nullable=False)

    # 🔽 Medical History
    family_history_parkinsons = Column(Boolean, nullable=False)
    traumatic_brain_injury = Column(Boolean, nullable=False)
    hypertension = Column(Boolean, nullable=False)
    diabetes = Column(Boolean, nullable=False)
    depression = Column(Boolean, nullable=False)
    stroke = Column(Boolean, nullable=False)

    # 🔽 Clinical Measurements
    systolic_bp = Column(Integer, nullable=False)
    diastolic_bp = Column(Integer, nullable=False)
    cholesterol_total = Column(Float, nullable=False)
    cholesterol_ldl = Column(Float, nullable=False)
    cholesterol_hdl = Column(Float, nullable=False)
    cholesterol_triglycerides = Column(Float, nullable=False)

    # 🔽 Cognitive and Functional Assessments
    updrs_score = Column(Float, nullable=False)
    moca_score = Column(Float, nullable=False)
    functional_assessment = Column(Float, nullable=False)

    # 🔽 Symptoms
    tremor = Column(Boolean, nullable=False)
    rigidity = Column(Boolean, nullable=False)
    bradykinesia = Column(Boolean, nullable=False)
    postural_instability = Column(Boolean, nullable=False)
    speech_problems = Column(Boolean, nullable=False)
    sleep_disorders = Column(Boolean, nullable=False)
    constipation = Column(Boolean, nullable=False)

    # targeted feature
    diagnosis = Column(Boolean, nullable=False)


class Result(Base):
    __tablename__ = "results"
    id = Column(Integer, primary_key=True, index=True)
    medical_examination_form_id = Column(Integer, ForeignKey("medical_examination_forms.id"), nullable=False)
    lime_result_html = Column(JSON, nullable=True)  # ⬅ dùng JSON thay vì TEXT nếu dùng SQLAlchemy

    # Optional: Relationship nếu bạn muốn truy cập result.medical_examination
    medical_examination = relationship("MedicalExaminationForm", backref="result")