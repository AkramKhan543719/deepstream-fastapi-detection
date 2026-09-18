from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine
from logger_config import logger
from api.v1.detections import router as detection_router


# =========================================================
# CREATE DATABASE TABLES
# =========================================================

Base.metadata.create_all(bind=engine)


# =========================================================
# FASTAPI APPLICATION
# =========================================================

app = FastAPI(
    title="DeepStream Detection API",
    description=(
        "FastAPI backend for receiving AI detection results "
        "from NVIDIA DeepStream and storing validated events "
        "in PostgreSQL."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]
)


# =========================================================
# API VERSION 1
# =========================================================

app.include_router(
    detection_router
)


# =========================================================
# ROOT
# =========================================================

@app.get("/")
def root():

    logger.info(
        "Root endpoint accessed"
    )

    return {
        "message": "DeepStream Detection API is running",
        "version": "1.0.0"
    }