from pydantic import BaseModel, Field, constr, validator
from datetime import datetime
from typing import Literal

class CallStartRecord(BaseModel):
    id: int
    type: Literal['start'] 
    timestamp: datetime 
    call_id: int 
    source: str = Field(..., pattern=r'^\d{2}\d{8,9}$')  
    destination: str = Field(..., pattern=r'^\d{2}\d{8,9}$')


    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "type": "start",
                "timestamp": "2024-11-03T10:15:30",
                "call_id": 1001,
                "source": "12987654321",
                "destination": "12912345678"
            }
        }


class CallEndRecord(BaseModel):
    id: int
    type: Literal['end']  
    timestamp: datetime  
    call_id: int  

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "type": "end",
                "timestamp": "2024-11-03T10:20:30",
                "call_id": 1001
            }
        }
