from fastapi import APIRouter, HTTPException, File, UploadFile
from pydantic import BaseModel
from app.services.scraper import scrape_url_content
from app.services.openai_service import summarize_text, analyze_lead_message
import logging
import fitz  # PyMuPDF
from typing import List
from app.schemas.lead import LeadMessage, LeadBatchRequest

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["Summarization", "Lead Qualification"])

class TextInput(BaseModel):
    text: str

class URLInput(BaseModel):
    url: str

class LeadMessage(BaseModel):
    name: str
    email: str
    message: str

class LeadBatchRequest(BaseModel):
    leads: List[LeadMessage]

@router.post("/summarize-text")
async def summarize_raw_text(data: TextInput):
    logger.info("Received request to summarize raw text.")
    summary = summarize_text(data.text)
    return {"summary": summary}

@router.post("/summarize-url")
async def summarize_from_url(data: URLInput):
    try:
        logger.info(f"Received request to summarize blog from URL: {data.url}")
        blog_content = await scrape_url_content(data.url)  # <== This works now
        summary = summarize_text(blog_content)
        return {"summary": summary}
    except Exception as e:
        logger.error(f"Error during summarization: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/summarize-pdf")
async def summarize_pdf(file: UploadFile = File(...)):
    try:
        logger.info(f"Received PDF for summarization: {file.filename}")

        contents = await file.read()
        with fitz.open(stream=contents, filetype="pdf") as doc:
            text = ""
            for page in doc:
                text += page.get_text()

        if not text.strip():
            raise HTTPException(status_code=400, detail="PDF is empty or unreadable.")

        summary = summarize_text(text)
        return {"summary": summary}

    except Exception as e:
        logger.error(f"Error during PDF summarization: {e}")
        raise HTTPException(status_code=500, detail="Failed to summarize the PDF.")

@router.post("/qualify-leads")
async def qualify_leads(data: LeadBatchRequest):
    try:
        results = []
        for lead in data.leads:
            result = analyze_lead_message(lead)
            results.append(result)
        return {"qualified_leads": results}
    except Exception as e:
        logger.error(f"Error during lead qualification: {e}")
        raise HTTPException(status_code=500, detail=str(e))
