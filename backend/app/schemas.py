from pydantic import BaseModel
from typing import List, Optional

class CampaignCreate(BaseModel):
    product_service: str
    description: str
    target_industry: str
    ideal_job_roles: List[str]
    company_size: str
    region: str
    outreach_goal: str
    brand_voice: str
    triggers: Optional[List[str]] = None

class Prospect(BaseModel):
    name: str
    title: str
    company: str
    location: str
    profile_url: str
    summary: Optional[str]
    insights: Optional[str]

class Message(BaseModel):
    prospect: Prospect
    message: str
