# app/schemas/lead.py

from pydantic import BaseModel
from typing import List

class LeadMessage(BaseModel):
    name: str
    email: str
    message: str

class LeadBatchRequest(BaseModel):
    leads: List[LeadMessage]