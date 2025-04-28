from pydantic import BaseModel
from datetime import datetime

# --------- SENSORES ---------

class SensorCreate(BaseModel):
    temperature: float
    humidity: float
    soil_moisture: float

class SensorOut(SensorCreate):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True

# --------- RELÉ (opcional se quiser) ---------

class RelayStatusOut(BaseModel):
    id: int
    status: bool
    updated_at: datetime

    class Config:
        orm_mode = True
