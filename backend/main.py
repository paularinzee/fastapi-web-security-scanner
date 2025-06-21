from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, HttpUrl
from typing import Optional, List
from scanner import WebSecurityScanner
from io import BytesIO

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# New model for individual vulnerability
class Vulnerability(BaseModel):
    type: str
    path: str

# ScanRequest now optionally includes mock vulnerabilities
class ScanRequest(BaseModel):
    target_url: HttpUrl
    max_depth: int = 3
    delay: float = 1.0
    mock_vulns: Optional[List[Vulnerability]] = None

@app.post("/scan", response_class=StreamingResponse)
def scan_and_download(request: ScanRequest):
    scanner = WebSecurityScanner(
        target_url=request.target_url,
        max_depth=request.max_depth,
        delay=request.delay
    )
    
    # Run the scan logic (crawler etc.)
    scanner.scan()

    # Inject dummy vulnerabilities from frontend (optional)
    if request.mock_vulns:
        for vuln in request.mock_vulns:
            scanner.vulnerabilities.append({"type": vuln.type, "path": vuln.path})

    # Generate PDF into memory
    buffer = BytesIO()
    scanner.generate_pdf_report(file_obj=buffer)
    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=scan_report.pdf"},
    )

@app.get("/")
def root():
    return {"message": "Welcome to the Web Security Scanner API!"}
