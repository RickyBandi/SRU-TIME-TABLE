# SRU Timetable Automation

A streamlined, high-performance web application built for SR University students to upload, parse, visualize, and export college timetables with precision. The system intelligently processes Excel files — including merged cells, irregular formats, and multi-row structures — and transforms them into a clean timetable UI with modern styling, free-time highlighting, and export tools.

🔗 **Live Frontend**: https://sru-time-table.vercel.app/  
🔗 **Live Backend**: https://sru-time-table.onrender.com/

---

## 🏆 Project Highlights

- 📥 **Excel Upload & Processing** — Handles merged cells, irregular layouts, and formatting variations  
- 🗂️ **Clean Timetable Rendering** — Structured grid view replicating SRU-style layout  
- 🕒 **Free-Time Slot Detection** — Toggle to highlight available periods  
- 🖼️ **PNG / PDF Export** — Download high-quality timetable images  
- 📱 **Fully Responsive Design** — Optimized for desktop, tablet, and mobile  
- ⚡ **FastAPI Backend + Static Frontend** — Quick load-time, low overhead  
- 🧱 **Clean Modular Architecture** — Server parses, frontend renders  

Designed for simplicity, reliability, and speed using modern development standards.

---

## ⚙️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **FastAPI** | Lightning-fast backend API |
| **openpyxl** | Excel parsing and merged-cell detection |
| **Uvicorn** | ASGI server for FastAPI |
| **HTML + CSS + JavaScript** | Lightweight frontend |
| **html-to-image.js** | PNG export functionality |
| **Vercel** | Frontend deployment |
| **Render** | Backend deployment |

---

## 📁 Project Structure

```
SRU Time Table/
├── backend/
│   ├── main.py              # FastAPI backend: upload + parse logic
├── frontend/
│   ├── index.html           # UI structure
└── README.md                # Project documentation
```

---

## 📦 Getting Started

### Prerequisites
- Python 3.10+
- Node.js (optional for local static server)

### Backend Setup

1. Navigate to backend:
```bash
cd backend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Start the FastAPI backend:
```bash
uvicorn main:app --reload --port 8000
```

Backend runs at:
```
http://127.0.0.1:8000
```

---

### Frontend Setup

1. Navigate to frontend:
```bash
cd frontend
```

2. Start a static server:
```bash
npx http-server -p 8080
```

Frontend available at:
```
http://localhost:8080
```

---

## 🧠 How It Works

### 1️⃣ User uploads an Excel file  
The frontend sends the file to the backend via `POST /parse-timetable`.

### 2️⃣ Backend parses Excel using openpyxl  
- Detects merged cells  
- Normalizes days & time slots  
- Handles missing/empty cells  
- Builds structured JSON  

### 3️⃣ Frontend renders the timetable  
Using CSS Grid with automatic row/col spanning for merged cells.

### 4️⃣ Optional: Free-Time Mode  
Calculates empty/available periods and highlights them.

### 5️⃣ Export Tools  
- PNG exporting through html-to-image.js  
- PDF via browser print or PNG conversion  

---

## 🔌 API Endpoint

### `POST /parse-timetable`

Upload an Excel file and receive structured timetable JSON.

**Request:**  
`multipart/form-data` with key `file`

**Response Example:**
```json
{
  "days": ["Monday", "Tuesday", "Wednesday"],
  "slots": ["9-10", "10-11", "11-12"],
  "table": {
    "Monday": ["DBMS", "Maths", "Free"],
    "Tuesday": ["Free", "AI", "OS"],
    "Wednesday": ["COA", "Free", "Free"]
  }
}
```

---

## 🧩 Customization & Extensibility

- Add new parsing logic in `backend/parsers.py`
- Modify style via `frontend/styles.css`
- Extend UI interactions in `frontend/script.js`
- Add new export formats or themes easily
- Plug additional analytics or timetable features

---

## 📤 Building for Production

### Backend
Hosted on **Render** using production FastAPI server.

### Frontend
Built & deployed on **Vercel** as a static site.

To rebuild:
```bash
npm run build
```

---

## 👨‍💼 Author

**Rithwik (Ricky)**  
Developer passionate about building automation tools, student utilities, and clean UI systems.  
This project reflects a focus on solving real problems with smart automation and clean design.

- Frontend Live: https://sru-time-table.vercel.app/
- Backend Live: https://sru-time-table.onrender.com/

---

## 📝 License

MIT License.  
Free to modify, fork, and enhance.
