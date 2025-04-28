from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import sensor, relay
from app.database import create_tables
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pathlib import Path


app = FastAPI(
    title="PlantMonitor API",
    description="API para monitoramento de plantas via IoT",
    version="1.0.0"
)

frontend_path = Path(__file__).resolve().parent.parent / "Frontend"
app.mount("/static", StaticFiles(directory=frontend_path), name="static")

# Libera acesso do frontend (HTML/JS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # pode ser restrito depois para segurança
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui rotas
app.include_router(sensor.router, prefix="/api/sensors")
app.include_router(relay.router, prefix="/api/relay")

# Inicializa banco de dados ao iniciar
@app.on_event("startup")
def startup_event():
    create_tables()


@app.get("/", response_class=HTMLResponse)
def serve_frontend():
    index_path = frontend_path / "index.html"
    return index_path.read_text(encoding="utf-8")