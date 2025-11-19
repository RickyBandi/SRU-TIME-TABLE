# SRU Timetable Automation Web App

A professional web application for SR University students to upload, view, and manage their timetables.

## Features

- ✅ Upload Excel timetable files
- ✅ Clean, modern UI matching the original design
- ✅ Automatic parsing of Excel files (handles merged cells, various formats)
- ✅ Free-time slot visualization
- ✅ Export to PNG and PDF
- ✅ Responsive design for all devices

## Project Structure

```
SRU TIme Table/
├── backend/
│   ├── main.py           # FastAPI backend server
│   └── requirements.txt  # Python dependencies
├── frontend/
│   └── index.html        # Frontend web application
└── README.md             # This file
```

## Setup Instructions

### 1. Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Start the Backend Server

```bash
cd backend
uvicorn main:app --reload --port 8000
```

The backend will run on `http://127.0.0.1:8000`

### 3. Start the Frontend Server

Open a new terminal window:

```bash
cd frontend
npx http-server -p 8080
```

Or use any other static file server. The frontend will be available at `http://localhost:8080`

### 4. Use the Application

1. Open your browser and go to `http://localhost:8080`
2. Click "Choose Excel File" and select your timetable Excel file
3. Click "Load Timetable"
4. View your timetable with the same beautiful styling as the original
5. Toggle "Show Free Time" to see available slots
6. Export as PNG or PDF

## How It Works

1. **Frontend**: User uploads Excel file → sends to backend API
2. **Backend**: Parses Excel using openpyxl → returns clean JSON
3. **Frontend**: Renders JSON as beautiful HTML table
4. **Features**: Free-time toggle, export functionality

## Technology Stack

- **Backend**: Python, FastAPI, openpyxl, uvicorn
- **Frontend**: HTML, CSS, JavaScript, html-to-image.js
- **Architecture**: Client-server with REST API

## Notes

- The backend must be running before using the frontend
- Excel files are parsed server-side for reliability
- The system handles merged cells, various day formats, and time slot formats automatically
- CORS is enabled for local development

