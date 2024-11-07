
from pydantic import BaseModel, Field
from datetime import datetime

class PricingRecord(BaseModel):
    call_id: int = Field(..., description="Unique call identifier")
    type: str = Field("pricing", description="Record type, set to 'pricing'")
    call_duration: str = Field(..., description="Duration of the call in HH:MM:SS format")
    call_price: float = Field(..., description="Calculated price of the call")
    source: str = Field(..., description="Caller phone number")
    destination: str = Field(..., description="Recipient phone number")
    start_timestamp: datetime = Field(..., description="Timestamp of call start in ISO format")
    end_timestamp: datetime = Field(..., description="Timestamp of call end in ISO format")
