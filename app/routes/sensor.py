from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schema, crud
from app.database import SessionLocal

router = APIRouter()

# Dependency para obter sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schema.SensorOut)
def create_sensor_data(data: schema.SensorCreate, db: Session = Depends(get_db)):
    return crud.create_sensor_data(db, data)

@router.get("/latest", response_model=schema.SensorOut)
def get_latest_sensor_data(db: Session = Depends(get_db)):
    data = crud.get_latest_sensor_data(db)
    if not data:
        raise HTTPException(status_code=404, detail="Nenhum dado encontrado")
    return data

@router.get("/history", response_model=list[schema.SensorOut])
def get_sensor_history(db: Session = Depends(get_db), limit: int = 10):
    return crud.get_sensor_history(db, limit=limit)
