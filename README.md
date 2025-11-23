<h1 align="center">🎓 SRU Timetable Automation — Unofficial</h1>

<p align="center">
  A clean, smart and fully automated timetable viewer for SR University students.<br>
  Upload Excel → Get a beautifully formatted timetable → View free hours → Export everything.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Status-Active-success?style=flat-square">
  <img src="https://img.shields.io/badge/Backend-FastAPI-blue?style=flat-square">
  <img src="https://img.shields.io/badge/Frontend-Vanilla%20JS-orange?style=flat-square">
  <img src="https://img.shields.io/badge/Excel-Parser-green?style=flat-square">
</p>

---

## 🌐 Live Demo  
👉 **https://sru-time-table.vercel.app/**  

---

## 📸 Screenshots

### 🏠 Homepage – Upload UI
> *The main screen where students upload their timetable Excel file.*
<br>

### 🗓️ Timetable Output
> *The timetable converted into a clean, readable layout.*
<br>

### ✔ Free-Time Table
> *Each hour marked as ❌ Class or ✔ Free for better clarity.*
<br>

---

## ✨ Overview

Every semester, students receive their timetable as a messy Excel file with merged cells, inconsistent formats, and unreadable layouts.  
This project solves that.

Upload an Excel timetable → The system parses it → Generates a clean, modern timetable → Lets you export or check free hours.

This tool works for **all years and all batches**, and is built independently as a student solution — not affiliated with SR University.

---

## 🚀 Features

### 📥 Upload & Parse Excel
- Handles merged cells  
- Handles different day/time formats  
- Works for any SRU batch or year  

### 🗓️ Clean Timetable Viewer
- University-like styling  
- Fully responsive  
- No manual formatting needed  

### ✔ Free-Time Table (Single Batch)
- Marks class hours as ❌  
- Marks free hours as ✔  
- Very helpful for daily planning  

### 🔍 Common Free Hours (Two Batches)
- Compare two timetables  
- Detect shared free hours  
- Helps with group projects & meetings  

### 📤 Export Options
- PNG  
- PDF  
- HTML (editable version)  

---

## 🛠️ Tech Stack

### **Frontend**
- HTML  
- CSS  
- Vanilla JavaScript  
- html-to-image.js  

### **Backend**
- Python  
- FastAPI  
- openpyxl  
- Uvicorn  

### **Deployment**
- Frontend → **Vercel**  
- Backend → **Render**  

---

## 🧱 Architecture

[Frontend Upload UI]
↓
[FastAPI Backend]
— Parses Excel
— Expands merged cells
— Extracts class entries
— Normalizes day/time
↓
[JSON Response]
↓
[Frontend Renderer → Timetable + Free-Time + Comparison]

---

## 📂 Project Structure

SRU-Time-Table/
├── backend/
│   ├── main.py
│   └── requirements.txt
├── frontend/
│   └── index.html
└── README.md

---

## ⚙️ Local Setup

### 1️⃣ Install backend dependencies
```bash
cd backend
pip install -r requirements.txt

2️⃣ Start backend server

uvicorn main:app --reload --port 8000

Runs at → http://127.0.0.1:8000

3️⃣ Start frontend server

cd frontend
npx http-server -p 8080


⸻

📝 Notes
	•	This is an independent student project, not an official SRU tool
	•	Some Excel files may take a bit longer during the first backend load
	•	No timetable data is stored; everything happens live and temporary

⸻

👤 Developer

Built with ❤️ by BATMAN (Rithwik Bandi)
3rd Year B.Tech — SR University

🔗 LinkedIn:
https://www.linkedin.com/in/rithwik-bandi-33b794295/

📧 Email:
ricky_bandi@yahoo.com

💻 GitHub Repo:
https://github.com/RickyBandi/SRU-TIME-TABLE

---
