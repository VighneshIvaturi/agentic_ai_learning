# 🩺 PrescriptionBot

### AI-Powered Prescription Understanding Platform

PrescriptionBot is a full-stack Generative AI application that transforms complex medical prescriptions into structured, patient-friendly insights.

The platform accepts prescriptions in multiple formats—including images, PDFs, DOCX documents, and live camera captures—and leverages Google's Gemini multimodal models to extract, analyze, and explain prescription information.

---

## 🚀 Key Highlights

✅ Upload prescription images

✅ Analyze multi-page PDF prescriptions

✅ Process DOCX files with typed text

✅ Extract prescriptions from embedded DOCX images

✅ Capture prescriptions directly from webcam

✅ AI-generated medication explanations

✅ Patient and doctor information extraction

✅ Safety warnings and risk identification

✅ Structured JSON responses

✅ Modern React frontend + FastAPI backend

---

## 📸 Supported Input Types

| Input Type     | Supported |
| -------------- | --------- |
| JPG            | ✅         |
| JPEG           | ✅         |
| PNG            | ✅         |
| PDF            | ✅         |
| DOCX           | ✅         |
| Webcam Capture | ✅         |

---

## 🏗️ System Architecture

```text
User
 │
 ▼
React Frontend (Vite)
 │
 ▼
FastAPI Backend
 │
 ├── Image Processing
 ├── PDF Processing
 ├── DOCX Processing
 └── Logging Layer
 │
 ▼
Google Gemini 2.5 Flash
 │
 ▼
Structured Medical Analysis
 │
 ▼
Patient-Friendly Output
```

---

## 🎯 Core Features

### 1. Prescription Image Analysis

Upload handwritten or printed prescription images and automatically extract:

* Patient details
* Doctor details
* Medicines
* Dosage instructions
* Frequency
* Duration
* Safety notes

---

### 2. Multi-Page PDF Processing

The system:

* Detects PDF uploads
* Converts each page into images
* Analyzes every page individually
* Produces page-wise structured results

---

### 3. Intelligent DOCX Analysis

Supports both:

#### Typed Prescriptions

Extracts and analyzes structured text directly from DOCX documents.

#### Embedded Prescription Images

Automatically identifies images embedded inside DOCX files and performs image-based prescription analysis.

---

### 4. Camera Capture Mode

Users can:

* Open webcam
* Capture prescription instantly
* Analyze without uploading files

This creates a real-world workflow similar to healthcare mobile applications.

---

## 🧠 AI Capabilities

Using Gemini 2.5 Flash, PrescriptionBot generates:

### Patient Information

* Name
* Age
* Gender
* Date

### Doctor Information

* Doctor Name
* Clinic/Hospital
* Registration Information

### Medicine Extraction

* Medicine Name
* Strength
* Dosage
* Frequency
* Route
* Duration

### Clinical Insights

* Doctor Advice
* Recommended Investigations
* Warnings
* Unclear/Risky Instructions
* Safety Notes

### Simplified Explanation

Each prescription is translated into a patient-friendly explanation that is easier to understand than traditional medical prescriptions.

---

## 🛠️ Technology Stack

### Frontend

* React
* Vite
* React Webcam
* CSS3

### Backend

* FastAPI
* Python 3.10+

### AI Layer

* Google Gemini 2.5 Flash
* Multimodal Prompt Engineering

### Document Processing

* PyMuPDF
* python-docx
* Pillow

### Logging & Monitoring

* Python Logging Framework

---

## 📂 Project Structure

```text
prescription-bot
│
├── backend
│   ├── app
│   │   ├── document_service.py
│   │   ├── llm_service.py
│   │   ├── prompts.py
│   │   └── logger_config.py
│   │
│   ├── logs
│   ├── uploads
│   ├── requirements.txt
│   ├── .env
│   └── main.py
│
├── frontend
│   ├── src
│   ├── public
│   ├── package.json
│   └── vite.config.js
│
└── README.md
```

---

## ⚙️ Local Setup

### Backend Setup

```bash
cd backend

python -m venv prescriptbotenv

prescriptbotenv\Scripts\activate

pip install -r requirements.txt
```

Create:

```env
GEMINI_API_KEY=YOUR_API_KEY
```

Run backend:

```bash
uvicorn main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

---

### Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

Frontend:

```text
http://localhost:5173
```

---

## 📡 API Endpoints

### Health Check

```http
GET /health
```

### Analyze Prescription

```http
POST /analyze-prescription
```

Supported file formats:

```text
jpg
jpeg
png
pdf
docx
```

---

## 📈 Future Roadmap

### Phase 1

* Export analysis as PDF
* Download JSON reports
* Drag & Drop uploads

### Phase 2

* Drug interaction detection
* Medicine knowledge base
* Confidence scoring

### Phase 3

* Docker containerization
* AWS deployment
* CI/CD pipeline

### Phase 4

* Multi-language prescriptions
* Healthcare RAG integration
* Clinical decision support features

---

## 👨‍💻 Author

### Sai Vighnesh Ivaturi

AI / ML Engineer

Specializations:

* Generative AI
* LLM Applications
* Agentic AI Systems
* RAG Pipelines
* MLOps & Cloud Deployment

---

## ⚠️ Disclaimer

PrescriptionBot is intended for educational and research purposes.

The generated output is AI-assisted and should not be considered medical advice. Users should always consult licensed healthcare professionals before making healthcare decisions.
