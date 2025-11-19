from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import openpyxl
from openpyxl.utils import get_column_letter
from typing import Dict, List, Optional, Tuple
import re
import json
import io

app = FastAPI(title="SRU Timetable Parser API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Day name variations
DAY_NAMES = {
    'monday': 'Monday', 'mon': 'Monday',
    'tuesday': 'Tuesday', 'tue': 'Tuesday',
    'wednesday': 'Wednesday', 'wed': 'Wednesday',
    'thursday': 'Thursday', 'thu': 'Thursday',
    'friday': 'Friday', 'fri': 'Friday',
    'saturday': 'Saturday', 'sat': 'Saturday',
    'sunday': 'Sunday', 'sun': 'Sunday'
}

def normalize_day(day_str: str) -> Optional[str]:
    """Normalize day name to standard format"""
    if not day_str:
        return None
    day_lower = day_str.strip().lower()
    return DAY_NAMES.get(day_lower)

def is_day_name(cell_value: str) -> bool:
    """Check if cell value is a day name"""
    if not cell_value:
        return False
    return normalize_day(str(cell_value)) is not None

def extract_time_slot(time_str: str) -> Optional[str]:
    """Extract time slot from various formats"""
    if not time_str:
        return None
    
    time_str = str(time_str).strip()
    
    # Pattern: 09:00-10:00 or 9:00-10:00 or 09:00–10:00
    pattern = r'(\d{1,2}):(\d{2})\s*[-–]\s*(\d{1,2}):(\d{2})'
    match = re.search(pattern, time_str)
    if match:
        start_hour = int(match.group(1))
        start_min = int(match.group(2))
        return f"{start_hour:02d}:{start_min:02d}"
    
    # Pattern: 09:00 or 9:00
    pattern = r'(\d{1,2}):(\d{2})'
    match = re.search(pattern, time_str)
    if match:
        hour = int(match.group(1))
        minute = int(match.group(2))
        return f"{hour:02d}:{minute:02d}"
    
    return None

def is_time_slot(cell_value: str) -> bool:
    """Check if cell value is a time slot"""
    return extract_time_slot(str(cell_value)) is not None

def expand_merged_cells(ws):
    """Expand merged cells to fill all cells in the merge range"""
    # First, unmerge all cells to make them writable
    merged_ranges = list(ws.merged_cells.ranges)
    
    for merged_range in merged_ranges:
        min_col, min_row, max_col, max_row = merged_range.bounds
        master_cell = ws.cell(min_row, min_col)
        master_value = master_cell.value
        
        # Unmerge the cells first
        ws.unmerge_cells(str(merged_range))
        
        # Fill all cells in the merged range with the master value
        for row in range(min_row, max_row + 1):
            for col in range(min_col, max_col + 1):
                cell = ws.cell(row, col)
                if cell.value is None or cell.value == '':
                    cell.value = master_value

def find_header_row(ws) -> Optional[int]:
    """Find the row that contains day names (header row)"""
    # Look for row with day names in columns (after first column)
    max_day_matches = 0
    header_row = None
    
    for row_idx in range(1, min(10, ws.max_row + 1)):
        day_count = 0
        for col_idx in range(2, ws.max_column + 1):
            cell_value = ws.cell(row_idx, col_idx).value
            if cell_value and is_day_name(str(cell_value)):
                day_count += 1
        
        if day_count > max_day_matches:
            max_day_matches = day_count
            header_row = row_idx
    
    return header_row if max_day_matches >= 3 else None

def find_day_columns(ws, header_row: int) -> Dict[str, int]:
    """Find which columns contain day names (in header row)"""
    day_columns = {}
    
    # Check header row for day names (skip first column which is usually "Time")
    for col_idx in range(2, ws.max_column + 1):
        cell_value = ws.cell(header_row, col_idx).value
        if cell_value:
            normalized_day = normalize_day(str(cell_value))
            if normalized_day:
                day_columns[normalized_day] = col_idx
    
    return day_columns

def find_time_slot_rows(ws, header_row: int) -> List[Tuple[int, str]]:
    """Find which rows contain time slots (in first column)"""
    time_slots = []
    
    # Check first column for time slots (after header row)
    for row_idx in range(header_row + 1, ws.max_row + 1):
        cell_value = ws.cell(row_idx, 1).value
        if cell_value:
            time_str = extract_time_slot(str(cell_value))
            if time_str:
                # Exclude 17:00 and later (college ends at 17:00/5:00pm)
                # Only include time slots up to 16:00
                hour = int(time_str.split(':')[0])
                if hour < 17:
                    time_slots.append((row_idx, time_str))
    
    # Sort by time
    time_slots.sort(key=lambda x: x[1])
    return time_slots

def extract_all_classes(cell_value: str) -> List[Dict[str, str]]:
    """Extract ALL classes from a cell (dynamic - works for any courses)"""
    if not cell_value:
        return []
    
    value = str(cell_value).strip()
    
    # Split by multiple spaces to get individual class entries
    # Classes are separated by many spaces (typically 50+)
    class_entries = re.split(r'\s{50,}', value)
    
    classes = []
    for entry in class_entries:
        if not entry.strip():
            continue
            
        class_name = None
        class_type = None
        room = ""
        
        # Try pattern with room: "ClassName (P/L): (Room)"
        class_match = re.search(r'(.+?)\s+\(([PL])\)\s*:\s*\(([^)]+)\)', entry)
        if class_match:
            class_name = class_match.group(1).strip()
            class_type = class_match.group(2)
            room = class_match.group(3).strip()
        else:
            # Try without room parentheses
            class_match = re.search(r'(.+?)\s+\(([PL])\)\s*:', entry)
            if class_match:
                class_name = class_match.group(1).strip()
                class_type = class_match.group(2)
                # Try to find room after the colon
                after_colon = entry[class_match.end():]
                room_match = re.search(r'\(([^)]+)\)', after_colon[:100])
                room = room_match.group(1) if room_match else ""
        
        if class_name:
            classes.append({
                'name': class_name,
                'type': class_type,
                'room': room
            })
    
    return classes

def format_classes_for_display(classes: List[Dict[str, str]]) -> str:
    """Format multiple classes for display in a cell"""
    if not classes:
        return ""
    
    if len(classes) == 1:
        # Single class - format simply
        cls = classes[0]
        if cls['room']:
            return f"{cls['name']} ({cls['type']})\nRoom {cls['room']}"
        else:
            return f"{cls['name']} ({cls['type']})"
    else:
        # Multiple classes - show all, separated by line breaks
        formatted = []
        for cls in classes:
            if cls['room']:
                formatted.append(f"{cls['name']} ({cls['type']})\nRoom {cls['room']}")
            else:
                formatted.append(f"{cls['name']} ({cls['type']})")
        return "\n\n".join(formatted)

def parse_cell_value(cell_value) -> str:
    """Parse and clean cell value"""
    if cell_value is None:
        return ""
    return str(cell_value).strip()

def is_class_cell(cell_value: str) -> bool:
    """Check if cell contains a class (not empty)"""
    if not cell_value:
        return False
    value = cell_value.strip()
    # Exclude common non-class values
    excluded = ['', 'free', 'available', '-', 'n/a', 'na']
    return value.lower() not in excluded and len(value) > 0

def get_class_type(cell_value: str) -> str:
    """Determine if class is Practical (P) or Lecture (L)"""
    if not cell_value:
        return ""
    value = cell_value.upper()
    if '(P)' in value or ' PRACTICAL' in value:
        return 'P'
    elif '(L)' in value or ' LECTURE' in value:
        return 'L'
    return 'L'  # Default to lecture

def extract_batch_name(ws) -> str:
    """Try to extract batch name from the worksheet"""
    # Check first few cells
    for row in range(1, min(5, ws.max_row + 1)):
        for col in range(1, min(5, ws.max_column + 1)):
            cell_value = ws.cell(row, col).value
            if cell_value:
                value_str = str(cell_value).upper()
                # Look for batch patterns like "23CSBTB35" or "BATCH 35"
                if 'BATCH' in value_str or 'CSBTB' in value_str:
                    return str(cell_value).strip()
    return "Unknown Batch"

def parse_single_file(contents: bytes) -> Dict:
    """Parse a single Excel file and return canonical JSON structure"""
    # Load workbook
    wb = openpyxl.load_workbook(io.BytesIO(contents), data_only=True)
    ws = wb.active
    
    # Expand merged cells
    expand_merged_cells(ws)
    
    # Find header row (contains day names)
    header_row = find_header_row(ws)
    if not header_row:
        raise ValueError("Could not find header row with day names")
    
    # Find day columns (days are in header row, columns 2+)
    day_columns = find_day_columns(ws, header_row)
    if not day_columns:
        raise ValueError("Could not find day columns")
    
    # Find time slot rows (time slots are in first column, rows after header)
    time_slot_rows = find_time_slot_rows(ws, header_row)
    
    if not time_slot_rows:
        raise ValueError("Could not find time slots")
    
    # Extract batch name
    batch_name = extract_batch_name(ws)
    
    # Build canonical JSON structure
    time_slots_list = [ts[1] for ts in time_slot_rows]
    days_list = sorted(day_columns.keys(), key=lambda d: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'].index(d) if d in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'] else 99)
    
    cells = {}
    
    # Process each day
    for day in days_list:
        day_col = day_columns[day]
        cells[day] = {}
        
        # Process each time slot
        for time_slot, (row_idx, _) in zip(time_slots_list, time_slot_rows):
            # Get cell value at intersection of time row and day column
            raw_value = ws.cell(row_idx, day_col).value
            cell_value = parse_cell_value(raw_value)
            
            # Extract ALL classes from the cell (dynamic - works for any courses)
            classes = extract_all_classes(cell_value) if cell_value else []
            
            # Format classes for display
            formatted_value = format_classes_for_display(classes)
            
            # Check if it's a class
            is_class = len(classes) > 0
            # Use the first class's type for CSS styling (or 'L' as default)
            class_type = classes[0]['type'] if classes else ""
            
            cells[day][time_slot] = {
                "value": formatted_value,
                "isClass": is_class,
                "type": class_type
            }
    
    return {
        "batch": batch_name,
        "timeSlots": time_slots_list,
        "days": days_list,
        "cells": cells
    }

def compare_timetables(timetable_a: Dict, timetable_b: Dict) -> Dict:
    """Compare two timetables and find common free time"""
    # Get common time slots and days
    time_slots_a = set(timetable_a["timeSlots"])
    time_slots_b = set(timetable_b["timeSlots"])
    common_time_slots = sorted(list(time_slots_a & time_slots_b))
    
    days_a = set(timetable_a["days"])
    days_b = set(timetable_b["days"])
    common_days = sorted(list(days_a & days_b), key=lambda d: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'].index(d) if d in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'] else 99)
    
    # Build comparison cells
    comparison_cells = {}
    
    for day in common_days:
        comparison_cells[day] = {}
        for time_slot in common_time_slots:
            # Check if both batches are free at this time
            batch_a_free = not timetable_a["cells"][day][time_slot]["isClass"]
            batch_b_free = not timetable_b["cells"][day][time_slot]["isClass"]
            
            # Common free time = both are free
            is_common_free = batch_a_free and batch_b_free
            
            comparison_cells[day][time_slot] = {
                "isCommonFree": is_common_free,
                "batchA": {
                    "isFree": batch_a_free,
                    "value": timetable_a["cells"][day][time_slot]["value"]
                },
                "batchB": {
                    "isFree": batch_b_free,
                    "value": timetable_b["cells"][day][time_slot]["value"]
                }
            }
    
    return {
        "batchA": timetable_a["batch"],
        "batchB": timetable_b["batch"],
        "timeSlots": common_time_slots,
        "days": common_days,
        "comparison": comparison_cells,
        "timetableA": timetable_a,
        "timetableB": timetable_b
    }

@app.post("/api/parse")
async def parse_timetable(file: UploadFile = File(...)):
    """Parse Excel timetable file and return canonical JSON"""
    try:
        # Read file content
        contents = await file.read()
        response = parse_single_file(contents)
        return JSONResponse(content=response)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error parsing file: {str(e)}")

@app.post("/api/compare")
async def compare_timetables_endpoint(
    fileA: UploadFile = File(...),
    fileB: UploadFile = File(...)
):
    """Compare two timetable files and find common free time"""
    try:
        # Read both files
        contents_a = await fileA.read()
        contents_b = await fileB.read()
        
        # Check if files are identical
        if contents_a == contents_b:
            raise HTTPException(
                status_code=400, 
                detail="Both files are identical. Please upload two different batch timetables."
            )
        
        # Parse both files
        timetable_a = parse_single_file(contents_a)
        timetable_b = parse_single_file(contents_b)
        
        # Compare timetables
        comparison_result = compare_timetables(timetable_a, timetable_b)
        
        return JSONResponse(content=comparison_result)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error comparing files: {str(e)}")

@app.get("/")
async def root():
    return {"message": "SRU Timetable Parser API", "status": "running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

