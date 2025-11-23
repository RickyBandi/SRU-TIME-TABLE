SRU Timetable Automation

A modern full‑stack web app for SR University students to upload, parse, visualize, and export academic timetables.

⸻

🔗 Live (Deployed)
	•	Frontend: https://sru-time-table.vercel.app/
	•	Backend:  https://sru-time-table.onrender.com/

If the links are private or behind authentication, please replace them with the correct production URLs.

⸻

Table of contents
	1.	About￼
	2.	Features￼
	3.	Project structure￼
	4.	Quickstart (Local)￼
	5.	API￼
	6.	How parsing works￼
	7.	Frontend behavior & exports￼
	8.	Deployment notes￼
	9.	Development & Contributing￼
	10.	Troubleshooting￼
	11.	License & Contact￼

⸻

About

SRU Timetable Automation converts messy Excel timetables into a consistent, interactive schedule view. The backend reliably parses .xlsx files (including merged cells and irregular formats) and returns normalized JSON consumed by a responsive frontend that renders a clean timetable UI and allows PNG/PDF export.

This repository is intentionally separated into backend/ (FastAPI) and frontend/ (static client) so teams can develop and deploy independently.

⸻

Features
	•	✅ Upload .xlsx timetable files
	•	✅ Robust Excel parsing (merged cells, blank cells, varied formats)
	•	✅ JSON output with days, slots, and cell metadata
	•	✅ Free‑time detection and highlight toggle
	•	✅ Export timetable as PNG and as PDF
	•	✅ Responsive layout for mobile and desktop
	•	✅ CORS enabled for local development

⸻

Project structure

SRU Time Table/
├── backend/
│   ├── main.py           # FastAPI backend server (parsing + API)
│   ├── parsers.py        # Excel parsing utilities (openpyxl)
│   └── requirements.txt  # Python dependencies
├── frontend/
│   ├── index.html       # Main UI
│   ├── script.js        # Frontend logic: upload, render, exports
│   └── styles.css       # Styling and responsive layout
└── README.md            # This file

NOTE: If you maintain additional helper scripts (cli tools, tests, fixtures), add them under backend/tools/ or tests/ and update this section.

⸻

Quickstart (Local)

Prerequisites
	•	Node.js + npm (for static server if needed)
	•	Python 3.10+
	•	pip or venv

Backend — install & run

cd backend
python -m venv .venv
source .venv/bin/activate    # macOS / Linux
.venv\Scripts\activate     # Windows (PowerShell)

pip install -r requirements.txt
uvicorn main:app --reload --port 8000

By default the backend will run at http://127.0.0.1:8000.

Frontend — run locally

Open a new terminal window and run a static server in frontend/:

cd frontend
npx http-server -p 8080

Or serve using live-server, serve, or any static hosting. Frontend default: http://localhost:8080.

Using the app
	1.	Open http://localhost:8080 in your browser.
	2.	Choose an Excel file using the file input.
	3.	Click Load Timetable. The frontend uploads the file to the backend /parse-timetable endpoint.
	4.	The parsed timetable appears. Toggle Show Free Time and use Export → PNG/PDF.

⸻

API

POST /parse-timetable

Parses an uploaded Excel timetable and returns JSON.

Request
	•	Content-Type: multipart/form-data
	•	Form field: file (Excel .xlsx file)

Response (200)

{
  "days": ["Monday","Tuesday","Wednesday","Thursday","Friday"],
  "slots": ["9:00-10:00","10:00-11:00","11:00-12:00"],
  "cells": [
    {"day":"Monday","slot":"9:00-10:00","text":"DBMS","rowspan":1,"colspan":1},
    {"day":"Monday","slot":"10:00-11:00","text":"Free","rowspan":1,"colspan":1}
  ],
  "meta": {"sheetName": "Sheet1", "parsedAt": "2025-11-23T18:00:00Z"}
}

Errors
	•	400 Bad Request — invalid file type or missing file
	•	422 Unprocessable Entity — file could not be parsed (malformed)

Implementation note: the parser populates rowspan/colspan for merged cells; the frontend uses those values when rendering the grid.

⸻

How parsing works (Backend internals)

High-level steps used by parsers.py (openpyxl):
	1.	Load workbook and target sheet.
	2.	Detect table region heuristically (first non-empty rows/cols for days and slots).
	3.	Normalize day headers (e.g., “Mon”, “MONDAY”, “monday” → “Monday”).
	4.	Iterate cells capturing text and merged regions:
	•	If a cell is part of a merged region, read the master cell and compute appropriate rowspan/colspan.
	•	Trim and normalize whitespace, replace newline separators with — where appropriate.
	5.	Produce JSON with days, slots, cells[], and meta fields.

Edge cases handled:
	•	Merged header rows (e.g., a header spanning two rows)
	•	Empty cells representing free slots
	•	Irregular slot time formats (normalized to HH:MM-HH:MM when possible)

⸻

Frontend behavior & exports
	•	Renders parsed JSON into a CSS grid table. rowspan and colspan properties are respected via grid-row / grid-column spans.
	•	Free slots are determined by the absence of subject text or explicit markers like Free, -, or blank.
	•	Export to PNG uses html-to-image (or dom-to-image fallback). The export button captures the timetable node and downloads a high-DPI PNG.
	•	Export to PDF can be done via: (a) browser print-to-PDF capturing the DOM node, or (b) converting PNG → PDF programmatically using a small client-side library.

⸻

Deployment notes
	•	Frontend: Deploy as static site (Vercel recommended) — point to built frontend/.
	•	Backend: Deploy FastAPI app (Render, Fly.io, or any container-based provider). When deploying:
	•	Ensure CORS origin includes your frontend domain
	•	Increase worker/timeout for larger Excel files if needed
	•	Use HTTPS and set environment variables for any secrets

⸻

Development & Contributing

If you want to add improvements (better parsing heuristics, more export options, mobile layout tweaks):
	1.	Fork the repo and create a feature branch.
	2.	Create small, focused PRs with one change per PR.
	3.	Add tests for parsing edge cases (example Excel fixtures).

Suggested labels for PRs:
	•	enhancement — parsing logic or UI improvements
	•	bug — incorrect parsing/rendering
	•	docs — README or usage improvements

⸻

Troubleshooting

File appears unparsed / wrong cells
	•	Verify the sheet name is Sheet1 or update the backend parsing config.
	•	Check merged headers — if the sheet uses a complex header layout, send a sample fixture to reproduce.

Export images are blurry
	•	Exports use device pixel ratio. For high-quality PNG, increase capture scale in the html-to-image options.

CORS errors
	•	Confirm backend CORS_ORIGINS includes your frontend origin (e.g., https://sru-time-table.vercel.app).

⸻

Example Excel fixtures (recommended)

Include a small fixtures/ directory with these example files for tests:
	•	simple-timetable.xlsx — single header row, uniform slots
	•	merged-headers.xlsx — merged day headers and multi-row times
	•	irregular-format.xlsx — mixed time formats and stray merged cells

⸻

Changelog (high level)
	•	v1.0.0 — Initial public release: core parsing, UI rendering, PNG/PDF export
	•	(Add future notes here — keep semantic versioning)

⸻

License & Contact

License: MIT — see LICENSE file.

Maintainer: Ricky (Bujji)
	•	GitHub: https://github.com/your-username
	•	Email: your-email@example.com

If you want, I can also:
	•	produce a README.md with badges + screenshots embedded,
	•	generate a release CHANGELOG.md, or
	•	create a ready-to-commit LICENSE file.

⸻

Generated for the SRU Timetable Automation project.
