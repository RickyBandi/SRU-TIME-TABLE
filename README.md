⭐ SRU Timetable Automation — Full Professional README.md

# SRU Timetable Automation

A modern full-stack web application designed for SR University students to upload, visualize, and manage their class timetables with clean UI, accurate Excel parsing, and free-time slot detection.

---

## 🚀 Live Demo

**Frontend:** https://sru-time-table.vercel.app/  
**Backend:** https://sru-time-table.onrender.com/

---

## 📌 Overview

SRU Timetable Automation simplifies the manual process of reading academic timetables by providing:

- Automatic Excel timetable parsing  
- Intelligent merged-cell detection  
- Free-time slot visualization  
- Export to PNG / PDF  
- Fully responsive modern UI  
- Works on any device (Mobile, Tablet, Desktop)

The application follows a client–server architecture with FastAPI-powered backend processing and a lightweight, blazing-fast frontend.

---

## ✨ Features

### 🧾 Upload & Parse Timetable
- Supports `.xlsx` Excel files  
- Handles merged cells, inconsistent formatting, and uneven structures  
- Converts Excel into clean, structured JSON  

### 🎨 Modern UI
- Clean SRU-style timetable grid
- Smooth animations & elegant spacing
- Works on all screen sizes

### 🔍 Free Time Slot Detection
- Toggle to highlight available free periods  
- Algorithm checks each day & each period automatically  

### 📤 Export Options
- Export the timetable as PNG  
- Export as PDF  

### 🌐 100% Frontend + Backend Separation
- Frontend handles UI rendering  
- Backend handles Excel parsing and returns JSON  

---

## 🏗️ Project Structure

SRU Time Table/
├── backend/
│   ├── main.py              # FastAPI backend server
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── index.html           # Frontend web app
│   ├── script.js            # Rendering & API logic
│   └── styles.css           # UI design
└── README.md

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/sru-timetable.git
cd sru-timetable


⸻

🐍 Backend Setup (FastAPI)

Install Dependencies

cd backend
pip install -r requirements.txt

Run Backend Server

uvicorn main:app --reload --port 8000

Server will be available at:

http://127.0.0.1:8000


⸻

🖥️ Frontend Setup

Start a local static server

cd frontend
npx http-server -p 8080

Frontend available at:

http://localhost:8080


⸻

🧠 How It Works (Architecture Flow)
	1.	User uploads Excel file
	2.	Frontend sends file → Backend API
	3.	Backend uses openpyxl
	•	Reads sheet
	•	Handles merged cells
	•	Extracts periods, days, subjects
	•	Builds structured JSON
	4.	Frontend renders timetable
	•	Builds grid UI
	•	Applies free-time algorithm
	5.	Export options
	•	PNG via html-to-image
	•	PDF via browser / library

⸻

🛠️ Tech Stack

Backend
	•	Python
	•	FastAPI
	•	openpyxl
	•	uvicorn

Frontend
	•	HTML
	•	CSS
	•	JavaScript
	•	html-to-image.js

Deployment
	•	Frontend: Vercel
	•	Backend: Render

⸻

🔄 API Endpoint

POST /parse-timetable

Uploads an Excel file and returns timetable JSON.

Request:
Multipart Form File (Excel)

Response (example):

{
  "days": ["Monday", "Tuesday", "Wednesday"],
  "slots": ["9-10", "10-11", "11-12"],
  "table": {
    "Monday": ["Math", "DBMS", "Free"],
    "Tuesday": ["Free", "AI", "Free"]
  }
}


⸻

📤 Exporting the Timetable

PNG Export

Uses HTML-to-image to convert DOM table → PNG.

PDF Export

Browser-native or library-based rendering enabled via frontend button.

⸻

❗ Notes
	•	Backend must be running before opening the frontend locally
	•	The Excel parsing algorithm handles:
	•	Merged cells
	•	Blank cells
	•	Irregular timetable formats
	•	CORS enabled for smooth local development

⸻

🧑‍💻 Contributing

Pull requests are welcome.
Please ensure clean code formatting and add comments for any parsing logic updates.

⸻

📜 License

This project is licensed under the MIT License.

⸻

💬 Contact

For queries or feature requests:

Developer: Ricky
Email: your email here
GitHub: your GitHub link

---
