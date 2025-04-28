from sqlalchemy.orm import Session
from app import models, schema
from sqlalchemy import desc

# ========== SENSOR DATA ==========

def create_sensor_data(db: Session, data: schema.SensorCreate):
    sensor_entry = models.SensorData(
        temperature=data.temperature,
        humidity=data.humidity,
        soil_moisture=data.soil_moisture
    )
    db.add(sensor_entry)
    db.commit()
    db.refresh(sensor_entry)
    return sensor_entry

def get_latest_sensor_data(db: Session):
    return db.query(models.SensorData).order_by(desc(models.SensorData.timestamp)).first()

def get_sensor_history(db: Session, limit: int = 10):
    return db.query(models.SensorData).order_by(desc(models.SensorData.timestamp)).limit(limit).all()

# ========== RELAY STATUS ==========

def get_relay_status(db: Session):
    last = db.query(models.RelayStatus).order_by(desc(models.RelayStatus.updated_at)).first()
    return last.status if last else False

def set_relay_status(db: Session, status: bool):
    relay_entry = models.RelayStatus(status=status)
    db.add(relay_entry)
    db.commit()
