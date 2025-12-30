# 🛡️ AI-Powered Scam URL Detection System
Real-Time Browser Extension + AI Risk Engine + Web-Based Scanner

A real-time, AI-assisted **browser-level fraud prevention system** that detects phishing, scam, and fake financial websites **before users enter sensitive information**.

Built with a **security-first architecture** combining:
- Rule-based detection
- Semantic HTML analysis
- AI intent analysis (Gemini, fallback-safe)
- Trusted infrastructure overrides
- Browser automation via Chrome Extension

---

## 🚀 Project Overview

This project proactively protects users from online financial fraud by:

- Detecting scam websites in real time
- Analyzing URLs, HTML structure, and page intent
- Preventing false positives on legitimate banking domains
- Running fully on the **client + local backend**
- Working even when AI services fail or are rate-limited

The system is designed to **alert users before entering UPI PINs, OTPs, passwords, or personal data**, addressing a major gap in current fraud detection systems.

---

## 🧱 Tech Stack

| Technology | Purpose |
|----------|--------|
| **Python 3** | Backend core |
| **FastAPI** | High-performance API |
| **Chrome Extension (JavaScript)** | Client-side real-time scanning |
| **BeautifulSoup + lxml** | HTML structure & intent analysis |
| **Gemini REST API** | AI semantic scam detection |
| **Requests** | HTTP & API communication |
| **In-Memory Cache (TTL)** | Performance & stability |
| **JSON-based testing** | Offline phishing simulation |

---

## 🏛️ System Architecture
Browser (Chrome Extension)
↓
Background Auto-Scan Listener
↓
FastAPI Backend
↓
URL Checks + HTML Analysis
↓
AI Semantic Analysis (Optional)
↓
Risk Scoring Engine
↓
Verdict → SAFE / SUSPICIOUS / SCAM


---

## 🔍 Detection Pipeline

### 1️⃣ URL Analysis
- HTTPS enforcement
- IP-based URLs
- Suspicious TLDs (`.xyz`, `.tk`, `.zip`, etc.)
- **Trusted TLD override** (`.bank.in`, `.gov.in`, `.edu.in`)

### 2️⃣ HTML & Intent Analysis
- Sensitive input fields (PIN, OTP, PAN, Card)
- Social-engineering phrases
- Urgency-based buttons
- Suspicious form actions
- Title-based deception detection

### 3️⃣ AI Semantic Analysis
- Detects phishing & scam intent
- Evaluates legitimacy conservatively
- **Never overrides trusted infrastructure**
- Safe fallback when AI is unavailable

### 4️⃣ Risk Scoring Engine
- Rule-based scoring (low confidence)
- AI-assisted escalation
- Final verdict computation

---

## 🔒 Security-First Design Principles

- AI is **advisory**, not authoritative
- Trusted financial domains cannot be downgraded
- Fallback logic prevents AI hallucination errors
- Zero trust for unknown infrastructure
- No sensitive user data is stored or logged

---

## ⚙️ Caching & Performance

### ✔ TTL-Based In-Memory Cache
- Cache duration: **12 hours**
- Prevents repeated analysis
- Reduces API calls
- Improves demo stability
Cache Key → URL  
Value → (analysis result, timestamp)

Expired entries are automatically invalidated.

---

## 🧪 Testing Framework

### Offline HTML Test Suite
- Legitimate websites
- Fake phishing pages
- SBI / Paytm clones
- OTP & UPI scam simulations

### Batch Test Runner
- Categorized results (LEGIT / FAKE)
- Automated verdict comparison
- False-positive detection
- Mismatch reporting
- Judge-friendly console output

---

## 📡 API Endpoint

### Analyze URL / HTML

POST /analyze

**Request Payload**
```json
{
  "type": "url | html",
  "data": "https://example.com",
  "html": "<optional html>"
}

Response

{
  "verdict": "SAFE | SUSPICIOUS | SCAM",
  "final_score": 42,
  "ai_explanation": "Explanation text"
}

## 🧩 Chrome Extension Features

- Automatic scan on page load  
- Manual scan option  
- Visual risk indicators  
- Color-coded results  
- No user interaction required  
- Instant feedback  

---

## ▶️ How to Run

### Backend
```bash
cd backend
uvicorn app.main:app --reload

Server:  
http://127.0.0.1:8000

### Chrome Extension
1. Open `chrome://extensions`
2. Enable **Developer Mode**
3. Click **Load unpacked**
4. Select the `chrome-extension/` folder

---

# 👥 Team: Java Wizards

| Member | Contribution                      |
|--------|-----------------------------------|
| Amballa Pardhiv | Backend Dev + AI Dev + Integration  |
| Thummala Hemanth Reddy | Frontend Dev + Tester                 |
| Chevuru V R Dinesh Karthik |Backend Dev + Documentation |
| Parimi Venkata Krishna | Frontend Dev + Documentation + Tester       |
| R Anish Reddy | AI Dev + Integration + Tester         |
| Pidela Yashwanth Reddy | All Rounder + Demo Presenter         |

---

## ⚠️ System Limitations

- AI availability depends on external API  
- In-memory cache only  
- Chrome-only support  
- Limited offline scanning  
- Single-machine scalability  

---

## 🚀 Future Enhancements

- Android support  
- Domain reputation feeds  
- JWT authentication  
- Cloud deployment  
- Bank-level integrations  

---

## 📄 License

For academic and research use.
