from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Substitua pelos seus dados reais do PostgreSQL
DB_USER = "welly"    
DB_PASSWORD = "Postgres1234!"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "plant_monitor"

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

def create_tables():
    from app import models
    Base.metadata.create_all(bind=engine)
