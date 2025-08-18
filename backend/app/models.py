# SQLAlchemy models (simplified)
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Campaign(Base):
    __tablename__ = 'campaigns'
    id = Column(Integer, primary_key=True, index=True)
    product_service = Column(String(255))
    description = Column(Text)
    target_industry = Column(String(255))
    ideal_job_roles = Column(Text)
    company_size = Column(String(50))
    region = Column(String(100))
    outreach_goal = Column(String(100))
    brand_voice = Column(String(255))
    triggers = Column(Text)

class Prospect(Base):
    __tablename__ = 'prospects'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    title = Column(String(255))
    company = Column(String(255))
    location = Column(String(255))
    profile_url = Column(String(255))
    summary = Column(Text)
    insights = Column(Text)
    campaign_id = Column(Integer, ForeignKey('campaigns.id'))
    campaign = relationship('Campaign')

class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True, index=True)
    prospect_id = Column(Integer, ForeignKey('prospects.id'))
    message = Column(Text)
    status = Column(String(50))
    prospect = relationship('Prospect')
