from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import time
import os

from app.api.routes import router as api_router
from app.rag.embeddings import get_embedding_generator
from app.utils.logger import log_info, log_error

# Initialize FastAPI application
app = FastAPI(
    title="Automation API Service",
    description="API service for dynamically retrieving and executing automation functions using LLM + RAG",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api")

# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

@app.on_event("startup")
async def startup_event():
    log_info("Starting up the application")
    
    # Ensure vector database directory exists
    os.makedirs("vector_db", exist_ok=True)
    
    # Initialize embedding generator and vector store at startup
    try:
        embedding_gen = get_embedding_generator()
        embedding_gen.initialize_vector_store()
        log_info("Vector store initialized successfully")
    except Exception as e:
        log_error(f"Error initializing vector store: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    log_info("Shutting down the application")

@app.get("/")
async def root():
    return {
        "message": "Automation API Service is running",
        "documentation": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}



