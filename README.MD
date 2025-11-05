# 🏛️ PredictiveMinds - Maharashtra Governance AI Platform

AI-driven Governance Platform that transforms raw government data into predictive, actionable intelligence for the Government of Maharashtra.

---

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Backend Setup (FastAPI)](#backend-setup-fastapi)
- [Frontend Setup (React + Vite)](#frontend-setup-react--vite)
- [Running the Application](#running-the-application)
- [Deployment](#deployment)
- [API Documentation](#api-documentation)
- [Features](#features)

---

## 🎯 Project Overview

PredictiveMinds is a secure, AI-driven platform that:

- **Predicts** future service demand using historical data
- **Detects** potential crises before they escalate
- **Prioritizes** citizen service requests automatically
- **Visualizes** real-time insights for decision-makers
- **Ensures** data privacy and compliance (GDPR, IT Act 2000, DPDP Act 2023)

---

## 🛠️ Tech Stack

### Backend

- **Python 3.11.9** (FastAPI)
- **Google Vertex AI** for ML models
- **BigQuery** for data warehousing
- **Cloud IAM/VPC** for security

### Frontend

- **React 18** with TypeScript
- **Vite** for build tooling
- **Tailwind CSS** for styling
- **shadcn/ui** component library
- **React Router** for navigation

---

## 📁 Project Structure

```
PredictiveMinds/
├── Backend/
│   └── api/
│       ├── main.py              # FastAPI application
│       ├── requirements.txt     # Python dependencies
│       ├── models/              # ML models
│       └── postman_collection.json
│
├── Frontend/  # Frontend
│   ├── src/
│   │   ├── pages/              # React pages
│   │   ├── components/         # Reusable components
│   │   └── App.tsx             # Main app component
│   ├── public/                 # Static assets
│   ├── package.json
│   └── vite.config.ts
│
└── README.md                   # This file
```

---

## ✅ Prerequisites

### System Requirements

- **Python 3.11.9** (exact version required)
- **Node.js 18+** and **npm 9+**
- **Git**

### Installation

```bash
# Install Python 3.11.9
https://www.python.org/downloads/release/python-3119/

# Verify installation
python --version  # Should show: Python 3.11.9

# Install Node.js (v18 or higher)
https://nodejs.org/

# Verify installation
node --version    # Should show: v18.x.x or higher
npm --version     # Should show: v9.x.x or higher
```

---

## 🐍 Backend Setup (FastAPI)

### Step 1: Navigate to Backend Directory

```bash
cd Backend/api
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment with Python 3.11.9
python -m venv venv
```

### Step 3: Activate Virtual Environment

**Windows (PowerShell):**

```powershell
.\venv\Scripts\Activate.ps1
```

**Windows (CMD):**

```cmd
venv\Scripts\activate.bat
```

**Linux/Mac:**

```bash
source venv/bin/activate
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Run Backend Server

```bash
# Development mode with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Or production mode
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

### Backend will be running at:

- **Local:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs (Swagger UI)
- **Health Check:** http://localhost:8000/health

---

## ⚛️ Frontend Setup (React + Vite)

### Step 1: Navigate to Frontend Directory

```bash
cd Frontend
```

### Step 2: Install Dependencies

```bash
npm install
```

### Step 3: Configure API Endpoint (if needed)

The frontend is already configured to use: `https://api.predictivminds.shop`

To change this for local development, update API URLs in:

- `src/pages/Dashboard.tsx`
- `src/pages/DemandForecasting.tsx`
- `src/pages/CrisisPrediction.tsx`
- `src/pages/PriorityScoring.tsx`
- `src/pages/DataUpload.tsx`
- `src/pages/PrivacyCompliance.tsx`

Replace `https://api.predictivminds.shop` with `http://localhost:8000`

### Step 4: Run Development Server

```bash
npm run dev
```

### Frontend will be running at:

- **Local:** http://localhost:8080

### Step 5: Build for Production

```bash
npm run build
# Creates 'dist' folder with optimized files
```

---

## 🚀 Running the Application

### Full Stack Development

**Terminal 1 - Backend:**

```bash
cd Backend/api
.\venv\Scripts\Activate.ps1  # Windows
uvicorn main:app --reload --port 8000
```

**Terminal 2 - Frontend:**

```bash
cd Frontend
npm run dev
```

**Access Application:**

- Frontend: http://localhost:8080
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

---

## 🎉 Quick Start Commands

```bash
# Backend
cd Backend/api
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# Frontend (new terminal)
cd Frontend
npm install
npm run dev

# Access at: http://localhost:8080
```

---

**Built with ❤️ for the Government of Maharashtra**
