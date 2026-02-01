#uvicorn app.main:app --reload

from fastapi import FastAPI, BackgroundTasks, Response
from . import models, schemas, nlp, linkedin_scraper, messaging, scheduler, database
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

@app.get("/")
def root():
    return {"message": "LinkedIn Sales Automation Tool API is running."}

@app.get("/favicon.ico")
def favicon():
    return Response(status_code=204)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/campaigns/")
def create_campaign(campaign: schemas.CampaignCreate, background_tasks: BackgroundTasks):
    db_campaign = database.create_campaign(campaign)
    prospects = linkedin_scraper.find_prospects(campaign)
    analyzed = [nlp.analyze_profile(p) for p in prospects]
    database.save_prospects(analyzed, db_campaign.id)
    messages = [messaging.generate_message(campaign, p) for p in analyzed]
    scheduler.schedule_outreach(db_campaign, analyzed, messages)
    return {"campaign": db_campaign, "prospects": analyzed, "messages": messages}
