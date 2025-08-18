def save_prospects(prospects, campaign_id):
    from .models import Prospect
    db = SessionLocal()
    db_prospects = []
    for p in prospects:
        db_prospect = Prospect(
            name=p.get('name', ''),
            title=p.get('title', ''),
            company=p.get('company', ''),
            location=p.get('location', ''),
            profile_url=p.get('profile_url', ''),
            summary=p.get('summary', ''),
            insights=p.get('insights', ''),
            campaign_id=campaign_id
        )
        db.add(db_prospect)
        db_prospects.append(db_prospect)
    db.commit()
    db.close()
    return db_prospects
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base, Campaign
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:Bluelock1>@localhost:3306/linkedin_automation"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

Base.metadata.create_all(bind=engine)

def create_campaign(campaign):
    db = SessionLocal()
    data = campaign.dict()
    # Convert lists to comma-separated strings
    if isinstance(data.get('ideal_job_roles'), list):
        data['ideal_job_roles'] = ','.join([str(x).strip() for x in data['ideal_job_roles']])
    if isinstance(data.get('triggers'), list):
        data['triggers'] = ','.join([str(x).strip() for x in data['triggers']])
    db_campaign = Campaign(**data)
    db.add(db_campaign)
    db.commit()
    db.refresh(db_campaign)
    db.close()
    return db_campaign


