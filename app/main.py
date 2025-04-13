from fastapi import FastAPI
from app.routes import summarize

import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="AI Blog Summarizer API",
    description="Summarize raw blog text or articles from URLs using GPT-4.",
    version="1.0.0"
)

# Register routes
app.include_router(summarize.router)