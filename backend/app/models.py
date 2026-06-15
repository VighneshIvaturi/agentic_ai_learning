from typing import List
from pydantic import BaseModel


class PatientInformation(BaseModel):
    patient_name: str = ""
    age: str = ""
    gender: str = ""
    date: str = ""


class DoctorInformation(BaseModel):
    doctor_name: str = ""
    clinic_or_hospital: str = ""
    registration_number: str = ""


class Medicine(BaseModel):
    medicine_name: str = ""
    strength: str = ""
    form: str = ""
    dosage: str = ""
    frequency: str = ""
    timing: str = ""
    duration: str = ""
    route: str = ""
    confidence: str = ""
    low_confidence_reason: str = ""
    simple_explanation: str = ""


class PrescriptionAnalysis(BaseModel):
    patient_information: PatientInformation
    doctor_information: DoctorInformation
    medicines: List[Medicine]
    tests_or_investigations: List[str] = []
    doctor_advice: List[str] = []
    unclear_or_risky_items: List[str] = []
    overall_simple_explanation: str = ""
    safety_note: str = ""


class AnalyzePrescriptionResponse(BaseModel):
    filename: str
    analysis: PrescriptionAnalysis