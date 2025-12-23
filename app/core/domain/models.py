from datetime import datetime
from typing import Literal, Optional
from pydantic import BaseModel, Field, EmailStr

class LeadPayload(BaseModel):
    """
    The shape of the data coming from Salesforce.
    """
    lead_id: str = Field(..., description="Unique ID from Salesforce")
    email: EmailStr
    first_name: str
    last_name: str
    source: Literal["web", "referral", "partner"]
    signup_date: datetime = Field(default_factory=datetime.utcnow)
    
    # We add extra fields that we might generate internally
    is_processed: bool = False

    class Config:
        from_attributes = True  # Allows conversion from ORM objects later