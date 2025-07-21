
# 🔍 Web Security Scanner

A web security scanner application built with **FastAPI** and **React**. It allows users to scan websites for common vulnerabilities like SQL Injection and XSS, and download a PDF report of the scan results.

---

## 🚀 Features

- ✅ URL crawling and link extraction
- ✅ Detects common vulnerabilities:
  - SQL Injection (SQLi)
  - Cross-Site Scripting (XSS)
  - Directory Traversal
  - Missing CSRF Tokens
- ✅ PDF report generation (in-memory download)
- ✅ Simple and intuitive React frontend
- ✅ CORS enabled for frontend-backend communication

---

## 🧱 Tech Stack

| Layer     | Technology     |
|-----------|----------------|
| Backend   | FastAPI        |
| Frontend  | React          |
| PDF Report| ReportLab      |
  |

---

## 📁 Project Structure

```
web-security-scanner/
├── backend/
|   ├── Dockerfile
│   ├── scanner.py
│   ├── main.py
│   └── requirements.txt
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── App.js
│   │   └── index.js
|   ├── Dockerfile
│   └── package.json
├── docker-compose.yml
└── README.md
```

---

## ⚙️ Backend Setup (FastAPI)

### 🔧 Prerequisites

- Python 3.9+
- pip

### ▶️ Running the Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

- API will be available at: `http://localhost:8000`
- Swagger Docs: `http://localhost:8000/docs`

---

## 💻 Frontend Setup (React)

### 🔧 Prerequisites

- Node.js (v18+ recommended)
- npm or yarn

### ▶️ Running the Frontend

```bash
cd frontend
npm install
npm run dev
```

- Visit the frontend at: `http://localhost:3000`

---

## 🐳 Docker (Optional)

If you prefer to use Docker:

### 🔧 Prerequisites

- Docker & Docker Compose

### ▶️ Using Docker Compose

```bash
docker-compose up --build
```

- Frontend: [http://localhost:3000](http://localhost:3000)
- Backend: [http://localhost:8000](http://localhost:8000)

---

## 📄 Example API Request

### Endpoint

`POST /scan`

### Payload

```json
{
  "target_url": "http://testphp.vulnweb.com",
  "max_depth": 2,
  "delay": 1.0
}
```

### Response

- Returns a **PDF** file as a downloadable stream containing the scan results.

---

## 🌐 Example Frontend Output

```
Web Security Scanner
http://testphp.vulnweb.com
Start Scan

Scan complete.

Vulnerabilities Found:
- SQL Injection → /products?id=1'
- XSS → /search?q=<script>alert(1)</script>

[Download PDF Report]
```

---

## 🛡️ Disclaimer

This tool is intended **strictly for educational use or authorized penetration testing**.  
**Do not scan any website without proper permission. Unauthorized scanning may be illegal.**

---

## 🧑‍💻 Author

Made with ❤️ by [Paul Nnaji]  
GitHub: [https://github.com/paularinzee](https://github.com/paularinzee)

---

## 📜 License

MIT License – use freely and contribute!
