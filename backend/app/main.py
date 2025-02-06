from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import documents, chat
from app.config import BASE_DIR
import logging

app = FastAPI(title="Document Search Bot", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (update this in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Include routers
app.include_router(documents.router)
app.include_router(chat.router)

@app.on_event("startup")
async def startup_event():
    logging.info("Application startup: Initializing services")

@app.on_event("shutdown")
async def shutdown_event():
    logging.info("Application shutdown: Cleaning up resources")