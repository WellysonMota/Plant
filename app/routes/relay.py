from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import models, crud
from app.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/status")
def get_status(db: Session = Depends(get_db)):
    status = crud.get_relay_status(db)
    return {"status": status}

@router.post("/activate")
def activate_relay(db: Session = Depends(get_db)):
    crud.set_relay_status(db, True)
    return {"message": "Irrigação ativada"}

@router.post("/deactivate")
def deactivate_relay(db: Session = Depends(get_db)):
    crud.set_relay_status(db, False)
    return {"message": "Irrigação desativada"}
