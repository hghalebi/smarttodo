#!/usr/bin/env python3
"""
Startup script for Google Tasks FastAPI application.
"""

import uvicorn
import sys
import os

# Add the source directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.main import app

if __name__ == "__main__":
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
        access_log=True
    )