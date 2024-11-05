
# models/call_record.py
from pydantic import BaseModel, Field, constr
from datetime import datetime
from typing import Literal

class CallStartRecord(BaseModel):
    call_id: int  
    type: Literal['start']
    timestamp: datetime
    source: str = Field(..., pattern=r'^\d{2}\d{8,9}$')  
    destination: str = Field(..., pattern=r'^\d{2}\d{8,9}$')
class CallEndRecord(BaseModel):
    call_id: int  
    type: Literal['end']
    timestamp: datetime
