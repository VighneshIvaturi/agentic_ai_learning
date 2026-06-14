# 🛡️ ScamGuard AI

## Protecting Trust with Generative Intelligence

ScamGuard AI is an intelligent scam detection system that leverages Large Language Models (LLMs), prompt engineering techniques, threat intelligence, URL analysis, and explainable AI to identify fraudulent messages and classify them into scam categories.

The project demonstrates how modern Generative AI systems can be combined with tool-based reasoning and structured outputs to build scalable, explainable, and production-ready cybersecurity applications.

---

# 🚀 Features

### Scam Detection

Classifies messages into:

* Scam
* Not Scam
* Uncertain

---

### Intent Detection

Identifies underlying scam intent such as:

* Phishing
* OTP Fraud
* Loan Scam
* Fake Authority
* Reward Manipulation
* Fear Tactics
* Account Suspension
* Urgency

---

### Prompt Engineering Techniques

Implemented and benchmarked:

* Zero-Shot Prompting
* Few-Shot Prompting
* Chain-of-Thought (CoT)
* ReAct Prompting

---

### Threat Intelligence

Cross-checks messages against:

* Known scam domains
* Known scam keywords
* Threat database patterns

---

### URL Safety Analysis

Detects:

* Suspicious domains
* Scam URLs
* Domain impersonation patterns
* Malicious keywords

---

### Explainable AI

Provides:

* Risk Score
* Reasoning
* Recommended Safe Actions

---

### Multilingual Detection

Supports:

* English
* Hindi
* Telugu
* Tamil
* Kannada
* Malayalam

---

### Feedback Learning Loop

Stores user feedback for future improvement and dynamic few-shot generation.

---

# 🏗️ System Architecture

```text
User
 ↓
Streamlit UI
 ↓
ReAct Agent
 ↓
Language Detection
 ↓
Threat Intelligence
 ↓
URL Extraction
 ↓
URL Safety Analysis
 ↓
Gemini LLM
 ↓
Structured Validation
 ↓
Risk Engine
 ↓
Final Decision
 ↓
Feedback Collection
```

---

# 📂 Project Structure

```text
ScamGuard-AI
│
├── app.py
├── main.py
│
├── data
│   ├── dataset.csv
│   ├── threat_database.json
│   └── feedback.csv
│
├── prompts
│   ├── zero_shot.txt
│   ├── few_shot.txt
│   ├── cot_prompt.txt
│   └── react_prompt.txt
│
├── src
│   ├── scam_analyzer.py
│   ├── gemini_client.py
│   ├── language_detector.py
│   ├── url_extractor.py
│   ├── url_checker.py
│   ├── threat_intel.py
│   ├── risk_engine.py
│   ├── react_agent.py
│   ├── feedback_manager.py
│   ├── schemas.py
│   └── utils.py
│
└── evaluation
    ├── evaluate.py
    └── benchmark.py
```

---

# 📊 Benchmark Results

| Prompt Technique | Classification Accuracy | Intent Accuracy |
| ---------------- | ----------------------- | --------------- |
| Zero-Shot        | 100%                    | 75.51%          |
| Few-Shot         | 100%                    | 87.23%          |
| Chain-of-Thought | 100%                    | 74.00%          |
| ReAct            | 100%                    | 76.00%          |

### Best Performing Technique

Few-Shot Prompting achieved the highest intent detection accuracy.

---

# 🛠️ Technology Stack

### Backend

* Python 3.12
* Gemini API
* Pydantic
* Pandas

### Frontend

* Streamlit

### AI Techniques

* Prompt Engineering
* ReAct Agents
* Structured Outputs
* Threat Intelligence
* Explainable AI

---

# ▶️ Running the Project

### Clone Repository

```bash
git clone <repository-url>
cd ScamGuard-AI
```

### Create Virtual Environment

```bash
python -m venv scamenv
```

### Activate Environment

Windows:

```bash
scamenv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment

Create:

```env
GOOGLE_API_KEY=YOUR_KEY
```

### Run Application

```bash
streamlit run app.py
```

---

# Example

### Input

```text
Your SBI account will be blocked.
Verify KYC immediately at:
http://sbi-verify-now.com
```

### Output

```text
Classification: Scam

Intent:
Phishing

Risk Score:
100/100

Threat Intelligence:
Known Scam Domain Detected

Safe Action:
Do not click the link.
Contact SBI through official channels.
```

---

# Future Enhancements

* Translation-based multilingual analysis
* Real-time threat intelligence APIs
* Advanced feedback learning
* Mobile deployment
* Cloud deployment (AWS/Azure)

---

# Author

Sai Vighnesh Ivaturi

ScamGuard AI – Protecting Trust with Generative Intelligence.
