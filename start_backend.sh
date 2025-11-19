#!/bin/bash
cd "$(dirname "$0")/backend"
python3 -m uvicorn main:app --reload --port 8000

