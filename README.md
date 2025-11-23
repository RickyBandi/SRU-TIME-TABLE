# SRU Timetable Automation

A high-performance web application built for SR University students to upload, parse, visualize, and export their class timetables with precision.  
The system intelligently processes messy Excel files — merged cells, irregular layouts, inconsistent formats — and converts them into a clean, modern, interactive timetable UI.

🔗 **Live Frontend**: https://sru-time-table.vercel.app/  
🔗 **Live Backend**: https://sru-time-table.onrender.com/

---

## 🏆 Project Highlights

- 📥 **Excel Upload & Parsing** — Automatically detects merged cells & irregular structures  
- 🗂️ **Clean Timetable Rendering** — Matches SRU style and structure  
- 🕒 **Free-Time Slot Highlighting** — Toggle mode to view available periods  
- 🖼️ **Export Tools** — Download timetable as PNG or PDF  
- 📱 **Fully Responsive UI**  
- ⚡ **FastAPI Backend + Lightweight Frontend**  
- 🔄 **Zero dependencies other than FastAPI & openpyxl (built-in in your backend code)**  

---

## ⚙️ Tech Stack

| Technology | Usage |
|-----------|--------|
| **FastAPI** | Backend API for Excel processing |
| **openpyxl** | Excel parsing engine |
| **Uvicorn** | Local dev server |
| **HTML + CSS + JS** | Frontend UI |
| **html-to-image.js** | PNG export |
| **Vercel** | Frontend hosting |
| **Render** | Backend hosting |

---

## 📁 Project Structure

```
SRU Time Table/
├── backend/
│   ├── main.py             # FastAPI backend (Excel parsing + API)
│   ├── start_backend.sh    # Script to run the backend
├── frontend/
│   ├── index.html          # UI + JS + styles in one file
│   ├── start_frontend.sh   # Script to run local frontend server
├── images.png              # Screenshot / preview asset
└── README.md               # Project documentation
```

---

## 📦 Getting Started

### Prerequisites
- Python 3.10+
- Node.js (optional, if running a static dev server)

---

## 🐍 Backend Setup (FastAPI)

1. Navigate to the backend folder:
```bash
cd backend
```

2. Install required libraries:
```bash
pip install fastapi uvicorn python-multipart openpyxl
```

3. Start the backend:
```bash
uvicorn main:app --reload --port 8000
```

Backend runs at:
```
http://127.0.0.1:8000
```

OR simply run:

```bash
./start_backend.sh
```

*(Make sure it’s executable: `chmod +x start_backend.sh`)*

---

## 🖥️ Frontend Setup

Inside the `frontend/` folder:

If you have `http-server`:
```bash
npx http-server -p 8080
```

Or run your provided script:

```bash
./start_frontend.sh
```

Frontend available at:
```
http://localhost:8080
```

---

## 🧠 How It Works

### 1️⃣ Upload  
User uploads an Excel timetable file.

### 2️⃣ Backend Parses  
FastAPI receives the file → openpyxl reads cells → merged cells handled → cleaned JSON returned.

### 3️⃣ Frontend Renders  
Your custom JavaScript builds a beautiful grid-style timetable UI.

### 4️⃣ Free-Time Mode  
Frontend algorithm highlights empty/unassigned slots.

### 5️⃣ Export  
User can export the schedule as:
- PNG  
- PDF  

---

## 🔌 API Endpoint

### `POST /parse-timetable`

**Request Type:**  
`multipart/form-data` with key: `file`

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

- Improve parsing rules inside `backend/main.py`
- Customize UI styles inside the single-file `index.html`
- Add animations or themes directly in JS/CSS
- Add new export modes (SVG, HD PNG, multi-page PDF)
- Add timetable saving/sharing features

---

## 📤 Deployment

### Frontend (Vercel)
- Deploy the `frontend/` directory  
- Select **Static Site**

### Backend (Render)
- Deploy the FastAPI service  
- Build command: `pip install fastapi uvicorn python-multipart openpyxl`  
- Start command: `uvicorn main:app --host 0.0.0.0 --port 10000`

---

## 👨‍💼 Author

**Rithwik (Ricky)**  
Passionate developer building automation tools for students & real-world utility apps.

- Frontend: https://sru-time-table.vercel.app/  
- Backend: https://sru-time-table.onrender.com/

---

## 📝 License

MIT License.  
Free to use, modify, and distribute.
